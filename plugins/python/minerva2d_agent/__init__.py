"""
Minerva 2D Agent — AI-powered digital painting assistant for Minerva 2D.

An LLM-driven agent that understands Minerva 2D's entire tool surface and
generates brush strokes, layer operations, filters, and color operations
from natural language prompts.

Inspired by DaVinci Agent (Minerva 3D) and Athena Agent.
"""

bl_info = {
    "name": "Minerva 2D Agent",
    "author": "Dr. Shabana / Athena Agent",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),  # Not used for Krita, kept for compatibility
    "location": "View > Dockers > Minerva 2D Agent",
    "description": (
        "AI-powered digital painting assistant. Describe what you want in "
        "natural language — the agent generates brush strokes, layer operations, "
        "filters, and color operations."
    ),
    "warning": "",
    "doc_url": "https://github.com/dr-shabana/Minerva-2D",
    "tracker_url": "https://github.com/dr-shabana/Minerva-2D/issues",
    "category": "Dockers",
}

import os
import sys
import json
import threading
import time
from pathlib import Path

# Add the DaVinci backend to the path for the LLM provider
DAVINCI_BACKEND_PATH = Path(__file__).parent.parent.parent.parent / "davinci-agent" / "backend"
if DAVINCI_BACKEND_PATH.exists():
    sys.path.insert(0, str(DAVINCI_BACKEND_PATH))

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
        QLabel, QScrollArea, QFrame, QSplitter, QComboBox, QLineEdit,
        QCheckBox, QSpinBox, QTabWidget, QFileDialog, QMessageBox,
        QApplication, QSizePolicy
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread, QSize
    from PyQt5.QtGui import QFont, QColor, QTextCursor, QIcon, QPixmap
    HAS_QT = True
except ImportError:
    try:
        from PySide2.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
            QLabel, QScrollArea, QFrame, QSplitter, QComboBox, QLineEdit,
            QCheckBox, QSpinBox, QTabWidget, QFileDialog, QMessageBox,
            QApplication, QSizePolicy
        )
        from PySide2.QtCore import Qt, QTimer, Signal as pyqtSignal, QObject, QThread, QSize
        from PySide2.QtGui import QFont, QColor, QTextCursor, QIcon, QPixmap
        HAS_QT = True
    except ImportError:
        HAS_QT = False

# Try to import Krita's Python API
try:
    from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase
    HAS_KRITA = True
except ImportError:
    HAS_KRITA = False


# =============================================================================
# Signal bridge for thread-safe UI updates
# =============================================================================

class SignalBridge(QObject):
    """Thread-safe signal bridge for updating the UI from background threads."""
    message_received = pyqtSignal(str, str)  # role, content
    status_changed = pyqtSignal(str)  # status message
    connection_state_changed = pyqtSignal(bool)  # connected
    screenshot_ready = pyqtSignal(str)  # base64 image
    tool_call_received = pyqtSignal(dict)  # tool call data
    stream_token = pyqtSignal(str)  # single token


# =============================================================================
# Chat Message Data Model
# =============================================================================

class ChatMessage:
    """Represents a single chat message."""
    def __init__(self, role, content="", tool_calls=None, screenshot_b64=None):
        self.id = id(self)
        self.role = role  # "user", "assistant", "system", "error"
        self.content = content
        self.tool_calls = tool_calls or []
        self.screenshot_b64 = screenshot_b64
        self.is_streaming = False
        self.timestamp = time.time()


# =============================================================================
# Minerva 2D Connection Client
# =============================================================================

class Minerva2DConnection:
    """Connection client for the Minerva 2D Agent backend."""

    def __init__(self, backend_url="http://localhost:8360"):
        self.backend_url = backend_url
        self.ws = None
        self.connected = False
        self._thread = None
        self._message_queue = []
        self._lock = threading.Lock()

    def connect(self):
        """Connect to the backend."""
        try:
            import websocket
            self.ws = websocket.WebSocketApp(
                f"{self.backend_url.replace('http', 'ws')}/ws",
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open,
            )
            self._thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self._thread.start()
            self.connected = True
            return True
        except ImportError:
            # Fallback to HTTP polling
            self.connected = True
            return True
        except Exception as e:
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from the backend."""
        if self.ws:
            self.ws.close()
        self.connected = False

    def send_message(self, message, context=None):
        """Send a message to the backend."""
        payload = {
            "type": "user_message",
            "content": message,
            "context": context or {},
            "timestamp": time.time(),
        }
        try:
            if self.ws:
                self.ws.send(json.dumps(payload))
            else:
                # HTTP fallback
                import urllib.request
                req = urllib.request.Request(
                    f"{self.backend_url}/api/generate",
                    data=json.dumps(payload).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}

    def _on_message(self, ws, message):
        pass

    def _on_error(self, ws, error):
        self.connected = False

    def _on_close(self, ws, close_status, close_msg):
        self.connected = False

    def _on_open(self, ws):
        self.connected = True


# =============================================================================
# Chat Manager (Singleton)
# =============================================================================

class ChatManager:
    """Manages the chat state for the Minerva 2D Agent."""

    _instance = None

    def __init__(self):
        self.messages = []
        self.connection = Minerva2DConnection()
        self.signals = SignalBridge()
        self.backend_url = "http://localhost:8360"
        self.auto_screenshot = True
        self.model = "deepseek/deepseek-chat-v3-0324:free"

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_message(self, role, content="", tool_calls=None):
        msg = ChatMessage(role, content, tool_calls)
        self.messages.append(msg)
        self.signals.message_received.emit(role, content)
        return msg

    def send_user_message(self, text):
        if not text.strip():
            return
        self.add_message("user", text)
        # Build context
        context = self._build_scene_context()
        # Send to backend
        if self.connection.connected:
            self.connection.send_message(text, context)
        else:
            self.add_message("error", "Not connected to backend. Start the Minerva 2D Agent backend on port 8360.")

    def _build_scene_context(self):
        """Build the current scene context from Krita."""
        context = {}
        if HAS_KRITA:
            try:
                app = Krita.instance()
                doc = app.activeDocument()
                if doc:
                    context = {
                        "width": doc.width(),
                        "height": doc.height(),
                        "color_model": doc.colorModel(),
                        "color_depth": doc.colorDepth(),
                        "num_layers": doc.topLevelNodes() if hasattr(doc, 'topLevelNodes') else 0,
                    }
            except:
                pass
        return context

    def connect(self, url=None):
        if url:
            self.backend_url = url
            self.connection = Minerva2DConnection(url)
        return self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()


# =============================================================================
# Chat Panel UI
# =============================================================================

class ChatPanelWidget(QWidget):
    """The main chat panel widget for the Minerva 2D Agent."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_manager = ChatManager.instance()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Connection bar
        conn_bar = QHBoxLayout()
        self.status_label = QLabel("🔴 Disconnected")
        self.status_label.setFont(QFont("Segoe UI", 9))
        conn_bar.addWidget(self.status_label)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setFixedWidth(80)
        self.connect_btn.clicked.connect(self._on_connect)
        conn_bar.addWidget(self.connect_btn)

        self.url_input = QLineEdit("http://localhost:8360")
        self.url_input.setPlaceholderText("Backend URL")
        conn_bar.addWidget(self.url_input, 1)

        layout.addLayout(conn_bar)

        # Chat messages area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)
        self.messages_layout.setSpacing(4)
        self.messages_layout.setContentsMargins(4, 4, 4, 4)

        self.scroll_area.setWidget(self.messages_container)
        layout.addWidget(self.scroll_area, 1)

        # Input area
        input_bar = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Describe what you want to create or modify...")
        self.input_field.setFixedHeight(60)
        self.input_field.setFont(QFont("Segoe UI", 10))
        input_bar.addWidget(self.input_field, 1)

        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedWidth(60)
        self.send_btn.setFixedHeight(60)
        self.send_btn.clicked.connect(self._on_send)
        input_bar.addWidget(self.send_btn)

        layout.addLayout(input_bar)

        # Settings row
        settings_bar = QHBoxLayout()
        self.screenshot_checkbox = QCheckBox("Auto-screenshot")
        self.screenshot_checkbox.setChecked(True)
        settings_bar.addWidget(self.screenshot_checkbox)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "deepseek/deepseek-chat-v3-0324:free",
            "qwen/qwen3-235b-a22b:free",
            "deepseek/deepseek-r1:free",
            "meta-llama/llama-4-maverick:free",
        ])
        self.model_combo.setEditable(True)
        settings_bar.addWidget(QLabel("Model:"))
        settings_bar.addWidget(self.model_combo, 1)

        layout.addLayout(settings_bar)

    def _connect_signals(self):
        mgr = self.chat_manager
        mgr.signals.message_received.connect(self._on_message_received)
        mgr.signals.status_changed.connect(self._on_status_changed)
        mgr.signals.connection_state_changed.connect(self._on_connection_state_changed)

    def _on_connect(self):
        url = self.url_input.text().strip()
        if self.chat_manager.connect(url):
            self.status_label.setText("🟢 Connected")
            self.status_label.setStyleSheet("color: #4caf50;")
            self.chat_manager.add_message("system", f"Connected to {url}")
        else:
            self.status_label.setText("🔴 Failed")
            self.status_label.setStyleSheet("color: #f44336;")
            self.chat_manager.add_message("error", f"Failed to connect to {url}")

    def _on_send(self):
        text = self.input_field.toPlainText().strip()
        if text:
            self.chat_manager.send_user_message(text)
            self.input_field.clear()

    def _on_message_received(self, role, content):
        """Add a message bubble to the chat."""
        bubble = self._create_bubble(role, content)
        self.messages_layout.addWidget(bubble)
        # Scroll to bottom
        QTimer.singleShot(50, self._scroll_to_bottom)

    def _create_bubble(self, role, content):
        """Create a chat bubble widget."""
        bubble = QFrame()
        bubble.setFrameShape(QFrame.StyledPanel)
        bubble.setLineWidth(1)

        # Role-based styling
        colors = {
            "user": ("#1e3a5f", "#cce5ff"),
            "assistant": ("#1a3a1a", "#d4edda"),
            "system": ("#3a3a3a", "#e0e0e0"),
            "error": ("#5a1a1a", "#f8d7da"),
        }
        border_color, bg_color = colors.get(role, ("#3a3a3a", "#e0e0e0"))
        bubble.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 4px;
            }}
        """)

        layout = QVBoxLayout(bubble)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        # Role label
        role_label = QLabel(role.capitalize())
        role_label.setFont(QFont("Segoe UI", 8, QFont.Bold))
        role_label.setStyleSheet(f"color: {border_color}; border: none; background: transparent;")
        layout.addWidget(role_label)

        # Content
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setFont(QFont("Segoe UI", 10))
        content_label.setStyleSheet("border: none; background: transparent;")
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(content_label)

        return bubble

    def _scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _on_status_changed(self, status):
        self.chat_manager.add_message("system", status)

    def _on_connection_state_changed(self, connected):
        if connected:
            self.status_label.setText("🟢 Connected")
            self.status_label.setStyleSheet("color: #4caf50;")
        else:
            self.status_label.setText("🔴 Disconnected")
            self.status_label.setStyleSheet("color: #f44336;")


# =============================================================================
# Krita Docker Integration
# =============================================================================

if HAS_KRITA:
    class Minerva2DAgentDocker(DockWidget):
        """Krita Docker widget for the Minerva 2D Agent."""

        def __init__(self):
            super().__init__()
            self.setWindowTitle("Minerva 2D Agent")
            self.chat_panel = ChatPanelWidget()
            self.setWidget(self.chat_panel)

        def canvasChanged(self, canvas):
            pass

    # Register the docker
    Krita.instance().addDockWidgetFactory(
        DockWidgetFactory(
            "minerva2d_agent",
            DockWidgetFactoryBase.DockRight,
            Minerva2DAgentDocker,
        )
    )


# =============================================================================
# Plugin Registration (for Krita's Python plugin system)
# =============================================================================

class Minerva2DAgentExtension:
    """Krita extension that registers the Minerva 2D Agent."""

    def __init__(self, parent):
        self.parent = parent
        self.chat_manager = ChatManager.instance()

    def setup(self):
        """Called when the plugin is loaded."""
        pass

    def createActions(self, window):
        """Create menu actions."""
        pass


# Desktop file for the plugin
DESKTOP_FILE = """
[Desktop Entry]
Type=Service
ServiceTypes=Krita/PythonPlugin
X-KDE-Library=minerva2d_agent
X-KDE-PluginInfo-Author=Dr. Shabana
X-KDE-PluginInfo-Email=
X-KDE-PluginInfo-Name=minerva2d_agent
X-KDE-PluginInfo-Version=0.1.0
X-KDE-PluginInfo-Website=https://github.com/dr-shabana/Minerva-2D
X-KDE-PluginInfo-Category=python
X-KDE-PluginInfo-Depends=
X-KDE-PluginInfo-License=GPL-3.0
X-KDE-PluginInfo-EnabledByDefault=true
Name=Minerva 2D Agent
Comment=AI-powered digital painting assistant
"""
