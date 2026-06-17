# Minerva Creative Suite — Complete Documentation

> **Last Updated:** 2026-06-17
> **Phase:** 1 (Codebase Rebranding & Integration) — Complete
> **Phase:** 2 (CI/CD, Translations, Build Toolchain) — In Progress

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Repositories](#repositories)
3. [Phase 1: What Was Done](#phase-1-what-was-done)
4. [Phase 2: In Progress](#phase-2-in-progress)
5. [Rebranding Details](#rebranding-details)
6. [Build Toolchain](#build-toolchain)
7. [File Structure](#file-structure)
8. [Pending Items](#pending-items)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MINERVA CREATIVE SUITE                       │
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │   MINERVA 3D         │    │   MINERVA 2D         │            │
│  │   (Blender fork)     │    │   (Krita fork)       │            │
│  │                      │    │                      │            │
│  │  ┌────────────────┐  │    │  ┌────────────────┐  │            │
│  │  │ DaVinci Agent  │  │    │  │ Athena Agent   │  │            │
│  │  │ (bpy add-on)   │  │    │  │ (PyKrita       │  │            │
│  │  │                │  │    │  │  plugin)       │  │            │
│  │  │ - Chat panel   │  │    │  │                │  │            │
│  │  │ - Code gen     │  │    │  │ - Chat panel   │  │            │
│  │  │ - Screenshot   │  │    │  │ - Brush assist │  │            │
│  │  │ - Mesh cleanup │  │    │  │ - Layer mgmt   │  │            │
│  │  └───────┬────────┘  │    │  │ - Filter gen   │  │            │
│  │          │           │    │  └───────┬────────┘  │            │
│  └──────────┼───────────┘    └──────────┼───────────┘            │
│             │                           │                        │
│             └───────────┬───────────────┘                        │
│                         │                                        │
│              ┌──────────▼──────────┐                             │
│              │   MINERVA BRIDGE    │                             │
│              │   (FastAPI :3010)   │                             │
│              │                     │                             │
│              │  - Unified API      │                             │
│              │  - File exchange    │                             │
│              │  - Render queue     │                             │
│              │  - WebSocket :3010  │                             │
│              └─────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Repositories

| Repo | GitHub URL | Local Path | Default Branch |
|------|-----------|------------|----------------|
| **Minerva 3D** | `github.com/dr-shabana/Minerva-3D` | `C:\Users\USER\Minerva-3D` | `main` |
| **Minerva 2D** | `github.com/dr-shabana/Minerva-2D` | `C:\Users\USER\Minerva-2D` | `master` |
| **Minerva Bridge** | `github.com/dr-shabana/Minerva-Bridge` | `C:\Users\USER\minerva-bridge` | `main` |

### Upstream Remotes

Both Minerva 3D and Minerva 2D have upstream remotes configured for syncing with original projects:

```bash
# Minerva 3D
git remote add upstream https://github.com/blender/blender.git

# Minerva 2D
git remote add upstream https://github.com/kde/krita.git
```

---

## Phase 1: What Was Done

### 1.1 Repository Setup
- Forked `blender/blender` → `dr-shabana/Minerva-3D` (already existed)
- Forked `kde/krita` → `dr-shabana/Minerva-2D`
- Created `dr-shabana/Minerva-Bridge`
- Cloned all three repos locally with `--depth 1` (shallow clone)
- Used `GIT_LFS_SKIP_SMUDGE=1` to avoid LFS errors

### 1.2 Rebranding — Minerva 3D (Blender → Minerva 3D)

**Script:** `rebrand_blender_to_minerva3d.py`
**Results:** 13,611 files processed, **9,587 modified**, 0 errors

**Three-target rename model:**
| Target | Old | New | Example |
|--------|-----|-----|---------|
| Brand/CLI | `Blender` | `Minerva` | Window title, About dialog |
| Module/package | `blender` | `minerva3d` | `source/blender/` → `source/minerva3d/` |
| Env/Config | `BLENDER` | `MINERVA3D` | `WITH_BLENDER` → `WITH_MINERVA3D` |

**Key renames:**
- `source/blender/` → `source/minerva3d/`
- `scripts/addons_core/io_scene_gltf2/blender/` → `scripts/addons_core/io_scene_gltf2/minerva3d/`
- `release/darwin/Blender.app/` → `release/darwin/Minerva3D.app/`
- `build_files/buildbot/config/blender_*.cmake` → `build_files/buildbot/config/minerva3d_*.cmake`
- `CMakeLists.txt`: `project(Blender)` → `project(Minerva3D)`
- All `blender.org` URLs → `minerva3d.org`
- File extensions: `.blend` → `.m3d`, `.blender` → `.minerva3d`
- Binary names: `blender.exe` → `minerva3d.exe`, `blender.com` → `minerva3d.com`

**Preserved (NOT renamed):**
- `bpy` Python API module name (it's the Blender Python API namespace — changing it breaks all scripts)
- `.blend` format references in compatibility/io contexts
- Third-party dependency names (KDE, Qt, etc.)
- Copyright headers (added Minerva attribution, didn't remove original)

### 1.3 Rebranding — Minerva 2D (Krita → Minerva 2D)

**Script:** `rebrand_krita_to_minerva2d.py`
**Results:** 9,710 files processed, **2,410 modified**, 0 errors

**Three-target rename model:**
| Target | Old | New | Example |
|--------|-----|-----|---------|
| Brand/CLI | `Krita` | `Minerva` | Window title, About dialog |
| Module/package | `krita` | `minerva2d` | `krita/` → `minerva2d/` |
| Env/Config | `KRITA` | `MINERVA2D` | `KRITA_VERSION` → `MINERVA2D_VERSION` |

**Key renames:**
- `krita/` directory → `minerva2d/`
- `plugins/extensions/pykrita/` → `plugins/extensions/pyminerva2d/`
- `CMakeLists.txt`: `project(krita)` → `project(minerva2d)`
- `KRITA_VERSION_STRING` → `MINERVA2D_VERSION_STRING`
- All `krita.org` URLs → `minerva2d.org`
- File extensions: `.kra` → `.m2d`
- `krita.desktop` → `minerva2d.desktop`
- `org.kde.krita.appdata.xml` → `org.minerva.minerva2d.appdata.xml`

**Preserved:**
- KDE Framework references (KF6, KF5)
- Qt references (Qt6, Qt5)
- Third-party dependency names

### 1.4 DaVinci Agent Integration (Minerva 3D)

**Location:** `C:\Users\USER\Minerva-3D\scripts\addons_core\minerva3d_agent\`

The DaVinci Agent was copied from `C:\Users\USER\athena-agent\davinci-agent\addon\` and rebranded:
- 15 Python files modified
- `bl_info` updated: `"name": "Minerva 3D Agent"`
- Panel location: `View3D > Sidebar > Minerva`
- All URLs updated to `github.com/dr-shabana/Minerva-3D`

**Add-on structure:**
```
scripts/addons_core/minerva3d_agent/
├── __init__.py          # bl_info, registration
├── agent/               # Context builder, prompt templates
├── connection/          # WebSocket client, protocol
├── engine/              # Runner, sandbox, validator
├── operators/           # Cancel, execute, export, preview, rollback, send
├── panels/              # Chat panel, settings panel
├── state/               # History, scene snapshot, selection
└── ui/                  # World-class sidebar chat (850 lines)
```

### 1.5 Minerva 2D Agent Plugin (Minerva 2D)

**Location:** `C:\Users\USER\Minerva-2D\plugins\python\minerva2d_agent\`

Created as a PyKrita plugin with:
- Chat panel UI (PyQt5/PySide2)
- WebSocket connection to Minerva Bridge
- Scene context builder (document info, layers, colors)
- Role-based chat bubbles (user/assistant/system/error)
- Settings panel (backend URL, model selection, auto-screenshot)

**Plugin structure:**
```
plugins/python/minerva2d_agent/
├── __init__.py                              # Main plugin + chat panel
└── minerva2dpyminerva2d_minerva2d_agent.desktop  # Krita plugin descriptor
```

### 1.6 Minerva Bridge v0.2.0

**Location:** `C:\Users\USER\minerva-bridge\`

Updated from v0.1.0 (AFFiNE + AppFlowy integration) to v0.2.0 (unified Minerva integration).

**New routes:**
| Endpoint | Description |
|----------|-------------|
| `/` | Root — lists all components and endpoints |
| `/health` | Health check |
| `/version` | Version info |
| `/api/3d` | Minerva 3D routes (status, info) |
| `/api/2d` | Minerva 2D routes (status, info) |
| `/api/athena` | Athena Agent routes (status, models) |
| `/api/davinci` | DaVinci Agent routes (status, pipeline) |
| `/ws` | WebSocket endpoint for real-time communication |

**Config:** `MINERVA_*` env vars (prefix: `MINERVA_`)
- `MINERVA_PORT` (default: 3010)
- `MINERVA_DAVINCI_BACKEND_URL` (default: http://localhost:8360)
- `MINERVA_ATHENA_GATEWAY_URL` (default: http://localhost:11434)
- `MINERVA_OPENROUTER_API_KEY`

---

## Phase 2: In Progress

### 2.1 Translation Files (.po)

**Script:** `rebrand_po_files.py` (separate script in each repo)

**Minerva 3D:** 49 .po files found, 2 modified (Japanese, Swedish — contained brand strings in msgstr)
**Minerva 2D:** 75 .po files found, 6 modified (Afrikaans, Croatian, Portuguese, Slovenian, Swedish, Vietnamese)

**What was updated:**
- `Project-Id-Version:` header
- `Language-Team:` URLs
- `Report-Msgid-Bugs-To:` URLs
- `msgstr` strings containing old brand names (NOT `msgid` — source strings preserved)

**Note:** Most .po files didn't contain brand-specific strings in their msgstr values — they were either empty (untranslated) or contained generic UI strings.

### 2.2 GitHub Actions CI/CD

Created `.github/workflows/ci.yml` for all three repos:

**Minerva 3D CI:**
- Rebrand audit (checks for remaining "Blender" references)
- Python syntax check (compiles all .py files)
- DaVinci Agent tests
- Build info display

**Minerva 2D CI:**
- Rebrand audit (checks for remaining "Krita" references)
- Python syntax check
- Minerva 2D Agent plugin check
- Build info display

**Minerva Bridge CI:**
- Syntax & import check
- FastAPI startup test
- Health check (starts server, hits /health endpoint)

### 2.3 Build Toolchain

**Status:** Partially set up

**Available:**
- Python 3.11.15
- Git 2.53.0
- VS Code (C:\Users\USER\AppData\Local\Programs\Microsoft VS Code)
- Windows SDK 10
- Chocolatey (package manager)
- Winget (package manager)

**Missing (needed for compilation):**
- MSVC compiler (`cl.exe`) — requires Visual Studio 2022 or Build Tools
- CMake — download in progress
- Ninja — not yet installed

**Disk space:** 35 GB free (C: drive, 475 GB total, 93% used)

---

## Rebranding Details

### Scripts Created

| Script | Location | Purpose |
|--------|----------|---------|
| `rebrand_blender_to_minerva3d.py` | `Minerva-3D/` | Content rename across all files |
| `rename_files_blender_to_minerva3d.py` | `Minerva-3D/` | File/directory renames |
| `rebrand_minerva3d_agent.py` | `Minerva-3D/` | DaVinci add-on rebrand |
| `rebrand_po_files.py` | `Minerva-3D/` | Translation file rebrand |
| `rebrand_krita_to_minerva2d.py` | `Minerva-2D/` | Content rename across all files |
| `rename_files_krita_to_minerva2d.py` | `Minerva-2D/` | File/directory renames |
| `rebrand_po_files.py` | `Minerva-2D/` | Translation file rebrand |

### What NOT to Rename (Preserved)

1. **`bpy` module** — Blender Python API namespace. Changing it breaks every Blender script/add-on.
2. **`.blend` format references** — File format compatibility. Only renamed in UI strings, not in I/O code.
3. **KDE/Qt framework names** — Third-party dependencies in Minerva 2D.
4. **Copyright headers** — Added Minerva attribution, kept original.
5. **Model names** — References to actual model names (e.g., "Hermes 3") are identifiers, not branding.
6. **Protocol identifiers** — Internal field names that define wire-format compatibility.

### Rebranding Order (Critical)

The rename was executed in this specific order to avoid broken imports:

1. Constants & config files
2. Package metadata (pyproject.toml, CMakeLists.txt)
3. Core modules (top-level files)
4. Agent core
5. Tools
6. CLI
7. Gateway
8. Tests
9. Docs
10. Install/packaging
11. File/directory renames (after content renames)
12. Translation files (.po)

---

## Build Toolchain

### Minerva 3D (Blender) Build Requirements

| Requirement | Minimum Version | Status |
|-------------|----------------|--------|
| MSVC | 1928 (VS 2019 16.9+) | ❌ Not installed |
| CMake | 3.21+ | ⏳ Download in progress |
| Python | 3.11+ | ✅ 3.11.15 |
| Ninja | Latest | ❌ Not installed |
| RAM | 64 GB recommended | Unknown |
| Disk | ~100 GB for build | ⚠ 35 GB free |

**Build command (once toolchain is ready):**
```bash
cd C:\Users\USER\Minerva-3D
mkdir build_windows
cd build_windows
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release --target INSTALL
```

### Minerva 2D (Krita) Build Requirements

| Requirement | Minimum Version | Status |
|-------------|----------------|--------|
| MSVC | 1928 (VS 2019 16.9+) | ❌ Not installed |
| CMake | 3.19+ | ⏳ Download in progress |
| Qt | 6.x | ❌ Not installed |
| KDE Frameworks | 6.x | ❌ Not installed |
| Python | 3.11+ | ✅ 3.11.15 |

**Build command (once toolchain is ready):**
```bash
cd C:\Users\USER\Minerva-2D
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
```

### Minerva Bridge Build

```bash
cd C:\Users\USER\minerva-bridge
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 3010
```

**Requirements:** `fastapi==0.115.0`, `uvicorn==0.30.0`, `httpx==0.27.0`, `pydantic==2.9.0`, `pydantic-settings==2.5.0`, `python-dotenv==1.0.0`, `gql==3.5.0`, `websockets==13.0`

---

## File Structure

### Minerva 3D
```
C:\Users\USER\Minerva-3D\
├── .github\workflows\ci.yml          # GitHub Actions CI
├── source\minerva3d\                  # Main source (was blender/)
│   ├── creator\                       # Application entry point
│   └── ...                            # All Blender source modules
├── scripts\addons_core\minerva3d_agent\  # DaVinci Agent (bundled)
├── locale\po\                         # Translation files (49 languages)
├── build_files\                       # Build configuration
├── CMakeLists.txt                     # Top-level CMake (project(Minerva3D))
├── rebrand_blender_to_minerva3d.py    # Rebrand script (gitignored)
├── rename_files_blender_to_minerva3d.py
├── rebrand_minerva3d_agent.py
├── rebrand_po_files.py
└── ...
```

### Minerva 2D
```
C:\Users\USER\Minerva-2D\
├── .github\workflows\ci.yml          # GitHub Actions CI
├── minerva2d\                         # Main application (was krita/)
├── plugins\python\minerva2d_agent\    # Minerva 2D Agent plugin
│   ├── __init__.py
│   └── minerva2dpyminerva2d_minerva2d_agent.desktop
├── plugins\extensions\pyminerva2d\   # Python API (was pykrita)
├── po\                                # Translation files (75 languages)
├── libs\                              # Core libraries (pigment, image, etc.)
├── CMakeLists.txt                     # Top-level CMake (project(minerva2d))
├── rebrand_krita_to_minerva2d.py      # Rebrand script (gitignored)
├── rename_files_krita_to_minerva2d.py
├── rebrand_po_files.py
└── ...
```

### Minerva Bridge
```
C:\Users\USER\minerva-bridge\
├── .github\workflows\ci.yml          # GitHub Actions CI
├── main.py                            # FastAPI application
├── config.py                          # Settings (pydantic-settings)
├── routes\
│   ├── health.py                      # /health, /version
│   ├── minerva3d.py                   # /api/3d
│   ├── minerva2d.py                   # /api/2d
│   ├── athena.py                      # /api/athena
│   └── davinci.py                     # /api/davinci
├── clients\                           # External service clients
├── models\                            # Data models
├── tests\                             # Test files
├── requirements.txt
└── .env.example
```

---

## Pending Items

### High Priority
- [ ] **Logo/Icon integration** — Logo being designed externally. When ready, integrate into:
  - Minerva 3D: `release/windows/` (icons), `release/darwin/` (icns), `release/datafiles/` (splash)
  - Minerva 2D: `minerva2d/pics/branding/` (icons, splash)
  - Minerva Bridge: API returns logo URL
- [ ] **Visual Studio 2022 Build Tools** — Required to compile either codebase
- [ ] **CMake** — Download was in progress (44 MB downloaded to /tmp/cmake.zip)

### Medium Priority
- [ ] **GitHub Actions secrets** — Set up any needed secrets for CI/CD
- [ ] **Upstream sync** — Test merging upstream Blender/Krita changes
- [ ] **Binary asset replacement** — Splash screens, icons, installer graphics (waiting on logo)

### Low Priority
- [ ] **Translation completion** — Remaining .po files that need manual review
- [ ] **Windows installer** — NSIS installer with Minerva branding
- [ ] **macOS bundle** → `.app` bundle with Minerva branding
- [ ] **Linux AppImage** — With Minerva branding
- [ ] **Documentation site** — docs.minerva3d.org, docs.minerva2d.org
- [ ] **Weblate integration** — Translation platform setup

---

## Google Stitch Logo Prompt

A detailed prompt was created for generating the Minerva logo via Google Stitch. The prompt centers on **Minerva herself** (not her owl), drawing from Roman mythology:

> Minerva is the Roman goddess of wisdom, strategic warfare, the arts, and craftsmanship. She sprang fully formed from Jupiter's head, armored and ready. The logo should embody: wisdom + creative power + precision + mythological gravitas.

The prompt requests 4 variations: helmet-crest "M", crossed spear-and-brush, coin-profile silhouette, and loom-shuttle stylus. Color palette: deep midnight blue (#0B1D3A) + burnished gold (#C9A84C).

**Status:** Logo being designed externally. Will integrate when ready.

---

## Key Commands

```bash
# Minerva 3D
cd C:\Users\USER\Minerva-3D
git log --oneline -5
git status

# Minerva 2D
cd C:\Users\USER\Minerva-2D
git log --oneline -5
git status

# Minerva Bridge
cd C:\Users\USER\minerva-bridge
git log --oneline -5
python -m uvicorn main:app --reload --port 3010

# Run CI locally (Minerva Bridge)
cd C:\Users\USER\minerva-bridge
pip install -r requirements.txt
python -c "from main import app; print(f'Routes: {len(app.routes)}')"
python -c "from config import settings; print(f'{settings.app_name} v{settings.app_version}')"
```
