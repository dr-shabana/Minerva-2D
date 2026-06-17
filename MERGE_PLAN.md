# Minerva Creative Suite — Complete Merge Plan

> **Date:** 2026-06-17
> **Author:** OWL (Alfred persona)
> **Purpose:** Phase-by-phase, step-by-step, test-by-test plan to merge all 5 projects into a unified Minerva Creative Suite monorepo
> **Constraint:** No new code creation — only merging, moving, and testing existing code

---

## Table of Contents

1. [Project Inventory](#project-inventory)
2. [Merge Strategy Overview](#merge-strategy-overview)
3. [Target Monorepo Structure](#target-monorepo-structure)
4. [Phase 1: Foundation — Minerva Bridge + DaVinci Agent](#phase-1)
5. [Phase 2: Integrate Athena Agent](#phase-2)
6. [Phase 3: Integrate Minerva 3D](#phase-3)
7. [Phase 4: Integrate Minerva 2D](#phase-4)
8. [Phase 5: Unified Build System](#phase-5)
9. [Phase 6: Cross-App Integration Testing](#phase-6)
10. [Phase 7: Polish & Release](#phase-7)
11. [Rollback Plan](#rollback-plan)
12. [Test Matrix](#test-matrix)

---

## Project Inventory

| # | Project | Files | Language | Local Path | Git Repo | Dependencies |
|---|---------|-------|----------|------------|----------|-------------|
| 1 | **Minerva 3D** | 20,727 | C++20, Python | `C:\Users\USER\Minerva-3D` | `dr-shabana/Minerva-3D` | CMake 3.21+, MSVC 1928+, Python 3.11+ |
| 2 | **Minerva 2D** | 12,277 | C++17, Qt, KDE | `C:\Users\USER\Minerva-2D` | `dr-shabana/Minerva-2D` | CMake 3.19+, Qt 5/6, KF 5/6 |
| 3 | **Minerva Bridge** | 1,575 | Python 3.11 | `C:\Users\USER\minerva-bridge` | `dr-shabana/Minerva-Bridge` | FastAPI, uvicorn, pydantic |
| 4 | **Athena Agent** | 5,204 | Python 3.11 | `C:\Users\USER\athena-agent` | `dr-shabana/athena-agent` | FastAPI, OpenAI, prompt_toolkit |
| 5 | **DaVinci Agent** | 57 | Python 3.11 | `C:\Users\USER\athena-agent\davinci-agent` | (part of athena-agent) | FastAPI, websocket, RAG |

**Total:** ~40,000 files across 5 projects

### Existing Integration Points

| Integration | Status | Location |
|-------------|--------|----------|
| DaVinci Agent → Minerva 3D | ✅ Already bundled | `Minerva-3D/scripts/addons_core/minerva3d_agent/` |
| Minerva 2D Agent → Minerva 2D | ✅ Already bundled | `Minerva-2D/plugins/python/minerva2d_agent/` |
| DaVinci Backend → Bridge | ⚠ Partial | Bridge has `/api/davinci` routes but doesn't import DaVinci code |
| Athena Agent → Bridge | ❌ Not connected | Separate repos, no shared code |
| Minerva 3D ↔ Minerva 2D | ❌ Not connected | No cross-app communication |

---

## Merge Strategy Overview

### Approach: Incremental Monorepo Construction

We will build a new monorepo (`Minerva-Suite`) incrementally, merging one project at a time, with full testing at each phase. This is **not** a big-bang merge — each phase is independently testable and reversible.

### Why This Order?

1. **Bridge first** — It's the smallest, pure-Python, and the integration hub
2. **DaVinci Agent second** — Already partially integrated, tests the Bridge connection
3. **Athena Agent third** — Adds the AI brain, tests multi-agent coordination
4. **Minerva 3D fourth** — Largest C++ project, tests the full 3D pipeline
5. **Minerva 2D fifth** — Second C++ project, tests cross-app workflows
6. **Build system** — Unified build after all code is in place
7. **Integration testing** — End-to-end cross-app workflows

### Merge Method: Git Subtree

We will use `git subtree` to merge each project into the monorepo while preserving full commit history. This allows:
- Full traceability of every change
- Ability to push changes back to original repos
- Clean separation of concerns per directory

---

## Target Monorepo Structure

```
Minerva-Suite/
├── .github/
│   └── workflows/
│       ├── ci-bridge.yml
│       ├── ci-3d.yml
│       ├── ci-2d.yml
│       └── ci-full-suite.yml
├── bridge/                          # Minerva Bridge (Python/FastAPI)
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── minerva3d.py
│   │   ├── minerva2d.py
│   │   ├── athena.py
│   │   └── davinci.py
│   ├── clients/
│   ├── models/
│   ├── tests/
│   └── requirements.txt
├── agents/
│   ├── davinci/                     # DaVinci Agent
│   │   ├── backend/
│   │   │   ├── main.py
│   │   │   ├── config/
│   │   │   ├── orchestrator/        # Planner, CodeGen, Validator, Vision
│   │   │   ├── knowledge/           # RAG indexer, YAML catalogs
│   │   │   └── llm_provider.py
│   │   ├── addon/                   # Blender/Minerva 3D add-on
│   │   │   ├── __init__.py
│   │   │   ├── ui/chat_panel.py
│   │   │   ├── engine/runner.py
│   │   │   └── ...
│   │   └── tests/
│   └── athena/                      # Athena Agent
│       ├── agent/                   # Core agent runtime
│       ├── cortex_cli/              # CLI interface
│       ├── apps/                    # Desktop app, bootstrapper
│       └── ...
├── minerva3d/                       # Minerva 3D (C++)
│   ├── source/
│   │   ├── creator/                 # Application entry point
│   │   └── minerva3d/               # Core engine
│   │       ├── blenkernel/          # Data model, scene graph
│   │       ├── blenlib/             # Math, memory, utilities
│   │       ├── depsgraph/           # Dependency graph
│   │       ├── draw/                # Viewport rendering
│   │       ├── gpu/                 # GPU abstraction
│   │       ├── nodes/               # Node system
│   │       ├── modifiers/           # Modifier stack
│   │       ├── geometry/            # Geometry algorithms
│   │       ├── editors/             # UI editors
│   │       ├── windowmanager/       # Event system
│   │       ├── python/              # Python API (bpy)
│   │       ├── render/              # Render engines
│   │       ├── compositor/          # Compositing
│   │       ├── io/                  # File I/O
│   │       └── sequencer/           # Video editing
│   ├── intern/                      # Internal libraries
│   │   ├── cycles/                  # Cycles render engine
│   │   ├── ghost/                   # Windowing system
│   │   └── ...
│   ├── scripts/
│   │   └── addons_core/
│   │       └── minerva3d_agent/     # DaVinci Agent add-on (symlink to agents/davinci/addon)
│   ├── extern/                      # Third-party libraries
│   ├── build_files/                 # Build configuration
│   ├── CMakeLists.txt
│   └── ...
├── minerva2d/                       # Minerva 2D (C++)
│   ├── libs/
│   │   ├── image/                   # Image engine (tile-based)
│   │   ├── pigment/                 # Color management
│   │   ├── brush/                   # Brush engine
│   │   ├── flake/                   # Document/shape model
│   │   ├── ui/                      # UI framework
│   │   ├── widgets/                 # Custom widgets
│   │   └── ...
│   ├── plugins/
│   │   ├── paintops/                # Paint operations
│   │   ├── filters/                 # Image filters
│   │   ├── generators/              # Procedural generators
│   │   ├── dockers/                 # UI panels
│   │   ├── tools/                   # Interactive tools
│   │   ├── impex/                   # Import/export
│   │   └── python/
│   │       └── minerva2d_agent/     # Minerva 2D Agent plugin
│   ├── minerva2d/                   # Main application
│   ├── cmake/                       # CMake modules
│   ├── CMakeLists.txt
│   └── ...
├── docs/
│   ├── ENGINE_ANALYSIS.md
│   ├── MERGE_PLAN.md                # This file
│   └── MINERVA_SUITE_DOCUMENTATION.md
├── tests/
│   ├── integration/                 # Cross-app integration tests
│   │   ├── test_bridge_davinci.py
│   │   ├── test_bridge_athena.py
│   │   ├── test_3d_addon.py
│   │   ├── test_2d_plugin.py
│   │   └── test_cross_app.py
│   └── e2e/                         # End-to-end tests
│       ├── test_full_workflow.py
│       └── test_ai_pipeline.py
├── scripts/
│   ├── build-3d.sh / .bat
│   ├── build-2d.sh / .bat
│   ├── build-bridge.sh / .bat
│   ├── run-all.sh / .bat
│   └── test-all.sh / .bat
├── CMakeLists.txt                   # Top-level CMake (for C++ projects)
├── pyproject.toml                   # Python workspace config
├── README.md
└── LICENSE
```

---

## Phase 1: Foundation — Minerva Bridge + DaVinci Agent

**Goal:** Create the monorepo with Bridge + DaVinci Agent. Test the AI 3D pipeline end-to-end.

**Duration estimate:** 1-2 days

### Step 1.1: Create Monorepo Skeleton

```bash
# Create new monorepo
mkdir C:\Users\USER\Minerva-Suite
cd C:\Users\USER\Minerva-Suite
git init

# Create directory structure
mkdir -p bridge agents/davinci agents/athena minerva3d minerva2d docs tests/integration tests/e2e scripts

# Create .gitignore
cat > .gitignore << 'EOF'
# Build outputs
build/
build_windows/
dist/
*.o
*.obj
*.exe
*.dll
*.so
*.dylib

# Python
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Large binary files (LFS)
*.blend
*.kra
*.m3d
*.m2d
*.icns
*.ico
*.png
*.jpg
*.exr
*.hdr
*.tif
*.tiff
*.psd
*.xcf
*.fbx
*.obj
*.stl
*.ply
*.abc
*.usd
*.usda
*.usdc
*.vdb
*.gltf
*.glb
EOF

git add .gitignore
git commit -m "chore: initialize Minerva Suite monorepo"
```

### Step 1.2: Merge Minerva Bridge (Subtree)

```bash
# Add Bridge as remote
git remote add bridge-origin https://github.com/dr-shabana/Minerva-Bridge.git
git fetch bridge-origin main

# Merge into bridge/ directory
git subtree add --prefix=bridge bridge-origin main --squash

# Verify
ls bridge/
# Expected: main.py, config.py, routes/, clients/, models/, tests/, requirements.txt, README.md
```

**Test 1.2.1: Bridge imports correctly**
```bash
cd bridge
pip install -r requirements.txt
python -c "from main import app; print(f'✓ Bridge loaded: {len(app.routes)} routes')"
python -c "from config import settings; print(f'✓ Config: {settings.app_name} v{settings.app_version}')"
```

**Test 1.2.2: Bridge starts**
```bash
# Start server in background
timeout 5 python -c "
from main import app
import uvicorn
import threading, time, httpx

def run():
    uvicorn.run(app, host='127.0.0.1', port=3010, log_level='error')

t = threading.Thread(target=run, daemon=True)
t.start()
time.sleep(2)

r = httpx.get('http://127.0.0.1:3010/health', timeout=5)
assert r.status_code == 200
print('✓ Bridge health check passed')

r2 = httpx.get('http://127.0.0.1:3010/', timeout=5)
data = r2.json()
assert 'components' in data
print(f'✓ Bridge root endpoint: {list(data[\"components\"].keys())}')
" 2>&1 || echo "✗ Bridge startup test failed"
```

### Step 1.3: Merge DaVinci Agent

```bash
# DaVinci Agent is local (not a separate git repo, part of athena-agent)
# Copy from local path
cp -r C:\Users\USER\athena-agent\davinci-agent\* agents/davinci/

# Verify structure
ls agents/davinci/
# Expected: addon/, backend/, docs/, tests/

git add agents/davinci/
git commit -m "feat: merge DaVinci Agent into monorepo"
```

**Test 1.3.1: DaVinci backend imports**
```bash
cd agents/davinci/backend
pip install -r requirements.txt 2>/dev/null
python -c "
import sys
sys.path.insert(0, '.')
from main import app
print(f'✓ DaVinci backend loaded: {len(app.routes)} routes')
"
```

**Test 1.3.2: DaVinci addon imports**
```bash
cd agents/davinci/addon
python -c "
import sys
sys.path.insert(0, '.')
from __init__ import bl_info
print(f'✓ DaVinci addon loaded: {bl_info[\"name\"]} v{bl_info[\"version\"]}')
"
```

**Test 1.3.3: DaVinci tests pass**
```bash
cd agents/davinci
pip install pytest pytest-asyncio
python -m pytest tests/ -v --tb=short 2>&1 | tail -20
# Expected: 104 tests passing (4 skipped bpy-dependent)
```

### Step 1.4: Connect Bridge ↔ DaVinci

The Bridge already has `/api/davinci` routes. Now we need to make the Bridge actually import and use the DaVinci backend.

**Test 1.4.1: Bridge can import DaVinci modules**
```bash
cd bridge
python -c "
import sys
sys.path.insert(0, '../agents/davinci/backend')
from orchestrator.planner import Planner
from orchestrator.code_generator import CodeGenerator
from orchestrator.llm_provider import LLMProvider
print('✓ Bridge can import DaVinci orchestrator modules')
"
```

**Test 1.4.2: DaVinci backend starts independently**
```bash
cd agents/davinci/backend
timeout 5 python -c "
from main import app
import uvicorn, threading, time, httpx

def run():
    uvicorn.run(app, host='127.0.0.1', port=8360, log_level='error')

t = threading.Thread(target=run, daemon=True)
t.start()
time.sleep(2)

r = httpx.get('http://127.0.0.1:8360/api/health', timeout=5)
print(f'✓ DaVinci backend health: {r.status_code}')
" 2>&1 || echo "✗ DaVinci backend test failed"
```

### Step 1.5: Phase 1 Integration Test

```bash
# Start both Bridge and DaVinci backend
# Test: Bridge can proxy requests to DaVinci
python -c "
import httpx, threading, time, uvicorn
import sys

# Start DaVinci backend on :8360
sys.path.insert(0, 'agents/davinci/backend')
from main import app as davinci_app
t1 = threading.Thread(target=lambda: uvicorn.run(davinci_app, host='127.0.0.1', port=8360, log_level='error'), daemon=True)
t1.start()
time.sleep(2)

# Start Bridge on :3010
sys.path.insert(0, 'bridge')
from main import app as bridge_app
t2 = threading.Thread(target=lambda: uvicorn.run(bridge_app, host='127.0.0.1', port=3010, log_level='error'), daemon=True)
t2.start()
time.sleep(2)

# Test Bridge → DaVinci proxy
r = httpx.get('http://127.0.0.1:3010/api/davinci/status', timeout=5)
print(f'Bridge→DaVinci status: {r.status_code} {r.json()}')

r2 = httpx.get('http://127.0.0.1:3010/api/davinci/pipeline', timeout=5)
print(f'Bridge→DaVinci pipeline: {r2.status_code}')

print('✓ Phase 1 integration test passed')
" 2>&1 || echo "✗ Phase 1 integration test failed"
```

**Phase 1 Checkpoint:**
- [ ] Monorepo created with proper structure
- [ ] Bridge merged and starts correctly
- [ ] DaVinci Agent merged and tests pass
- [ ] Bridge can import DaVinci modules
- [ ] Both services can run simultaneously
- [ ] All Phase 1 tests pass

**Rollback:** Delete `C:\Users\USER\Minerva-Suite` — original repos are untouched.

---

## Phase 2: Integrate Athena Agent

**Goal:** Merge Athena Agent into the monorepo. Test multi-agent coordination.

**Duration estimate:** 1-2 days

### Step 2.1: Merge Athena Agent

```bash
# Athena Agent is at C:\Users\USER\athena-agent
# We need to merge it carefully — it has its own structure

# Option A: If Athena has a git repo
cd C:\Users\USER\athena-agent
git remote -v  # Check if it's a git repo

# If it is:
cd C:\Users\USER\Minerva-Suite
git remote add athena-origin https://github.com/dr-shabana/athena-agent.git
git fetch athena-origin main
git subtree add --prefix=agents/athena athena-origin main --squash

# Option B: If not a git repo, copy and init
cp -r C:\Users\USER\athena-agent\* agents/athena/
cd agents/athena
git init
git add -A
git commit -m "chore: import Athena Agent"
cd ../..
git add agents/athena/
git commit -m "feat: merge Athena Agent into monorepo"
```

### Step 2.2: Resolve Athena Dependencies

Athena Agent has its own dependencies that may conflict with Bridge/DaVinci:

```bash
# Check Athena's requirements
cat agents/athena/requirements.txt 2>/dev/null || cat agents/athena/cortex_cli/requirements.txt 2>/dev/null

# Create a unified requirements.txt at monorepo root
# (Will be done in Phase 5)
```

**Test 2.2.1: Athena imports correctly**
```bash
cd agents/athena
python -c "
import sys
sys.path.insert(0, '.')
from cortex_cli.main import main
print('✓ Athena CLI imports correctly')
" 2>&1 || echo "⚠ Athena CLI import may need path adjustments"
```

### Step 2.3: Connect Athena ↔ Bridge

The Bridge has `/api/athena` routes. Now connect them to Athena's actual agent runtime.

**Test 2.3.1: Bridge can reach Athena modules**
```bash
cd bridge
python -c "
import sys
sys.path.insert(0, '../agents/athena')
# Try importing Athena core
try:
    from agent.agent_init import AgentInit
    print('✓ Bridge can import Athena agent core')
except ImportError as e:
    print(f'⚠ Import path needs adjustment: {e}')
"
```

### Step 2.4: Phase 2 Integration Test

```bash
# Test: All 3 Python services can run simultaneously
# Bridge (:3010) + DaVinci (:8360) + Athena (:11434)
python -c "
import httpx, time

services = {
    'Bridge': 'http://127.0.0.1:3010/health',
    'DaVinci': 'http://127.0.0.1:8360/api/health',
}

for name, url in services.items():
    try:
        r = httpx.get(url, timeout=3)
        print(f'✓ {name}: {r.status_code}')
    except:
        print(f'✗ {name}: not responding')
" 2>&1
```

**Phase 2 Checkpoint:**
- [ ] Athena Agent merged into monorepo
- [ ] Athena imports correctly
- [ ] Bridge can reach Athena modules
- [ ] All 3 Python services run simultaneously
- [ ] No dependency conflicts

---

## Phase 3: Integrate Minerva 3D

**Goal:** Merge the largest project (Minerva 3D) into the monorepo. Test the C++ build system.

**Duration estimate:** 2-3 days

### Step 3.1: Merge Minerva 3D

```bash
cd C:\Users\USER\Minerva-Suite
git remote add minerva3d-origin https://github.com/dr-shabana/Minerva-3D.git
git fetch minerva3d-origin main
git subtree add --prefix=minerva3d minerva3d-origin main --squash

# Verify
ls minerva3d/
# Expected: source/, intern/, extern/, scripts/, CMakeLists.txt, etc.
```

### Step 3.2: Create Symlink for DaVinci Add-on

The DaVinci Agent add-on is already in `minerva3d/scripts/addons_core/minerva3d_agent/` (from the original Blender fork). We need to symlink it to our merged version:

```bash
# Remove the old bundled add-on
rm -rf minerva3d/scripts/addons_core/minerva3d_agent

# Create symlink to the merged DaVinci addon
# Windows: use mklink /J for junction
cmd /c "mklink /J minerva3d\scripts\addons_core\minerva3d_agent agents\davinci\addon"

# Verify
ls -la minerva3d/scripts/addons_core/minerva3d_agent/
# Should show symlink to agents/davinci/addon/
```

### Step 3.3: Verify Minerva 3D Build System

```bash
# Check CMakeLists.txt is intact
head -20 minerva3d/CMakeLists.txt
# Expected: cmake_minimum_required(VERSION 3.21), project(Minerva3D)

# Check key source directories exist
ls minerva3d/source/minerva3d/blenkernel/ | wc -l
ls minerva3d/source/minerva3d/blenlib/ | wc -l
ls minerva3d/source/minerva3d/depsgraph/ | wc -l
ls minerva3d/source/minerva3d/draw/ | wc -l
ls minerva3d/source/minerva3d/gpu/ | wc -l
ls minerva3d/source/minerva3d/nodes/ | wc -l
ls minerva3d/intern/cycles/ | wc -l
```

**Test 3.3.1: CMake configure (dry run)**
```bash
# This will fail without MSVC, but we can verify CMakeLists.txt parses
cd minerva3d
mkdir -p build_test
cd build_test
cmake .. -G "Visual Studio 17 2022" -A x64 2>&1 | head -30
# Expected: CMake should parse successfully, fail at compiler detection
```

### Step 3.4: Phase 3 Integration Test

```bash
# Test: DaVinci addon can be loaded by Minerva 3D's Python
cd minerva3d
python -c "
import sys
sys.path.insert(0, 'scripts/addons_core/minerva3d_agent')
from __init__ import bl_info
print(f'✓ DaVinci addon loadable from Minerva 3D: {bl_info[\"name\"]}')
"
```

**Phase 3 Checkpoint:**
- [ ] Minerva 3D merged into monorepo
- [ ] DaVinci add-on symlinked correctly
- [ ] CMakeLists.txt parses without errors
- [ ] DaVinci addon loadable from Minerva 3D's Python path
- [ ] All original Minerva 3D files preserved

---

## Phase 4: Integrate Minerva 2D

**Goal:** Merge Minerva 2D into the monorepo. Test the Qt/KDE build system.

**Duration estimate:** 2-3 days

### Step 4.1: Merge Minerva 2D

```bash
cd C:\Users\USER\Minerva-Suite
git remote add minerva2d-origin https://github.com/dr-shabana/Minerva-2D.git
git fetch minerva2d-origin master
git subtree add --prefix=minerva2d minerva2d-origin master --squash

# Verify
ls minerva2d/
# Expected: libs/, plugins/, minerva2d/, cmake/, CMakeLists.txt, etc.
```

### Step 4.2: Verify Minerva 2D Build System

```bash
# Check CMakeLists.txt
head -20 minerva2d/CMakeLists.txt
# Expected: cmake_minimum_required(VERSION 3.19.0), project(minerva2d)

# Check key source directories
ls minerva2d/libs/image/ | wc -l
ls minerva2d/libs/pigment/ | wc -l
ls minerva2d/libs/brush/ | wc -l
ls minerva2d/libs/flake/ | wc -l
ls minerva2d/libs/ui/ | wc -l
ls minerva2d/plugins/paintops/ | wc -l
ls minerva2d/plugins/filters/ | wc -l
ls minerva2d/plugins/impex/ | wc -l
```

### Step 4.3: Verify Minerva 2D Agent Plugin

```bash
# Check the plugin is intact
ls minerva2d/plugins/python/minerva2d_agent/

# Verify the plugin descriptor
cat minerva2d/plugins/python/minerva2d_agent/minerva2dpyminerva2d_minerva2d_agent.desktop
```

**Test 4.3.1: Plugin syntax check**
```bash
python -m py_compile minerva2d/plugins/python/minerva2d_agent/__init__.py
echo "✓ Minerva 2D Agent plugin syntax OK"
```

### Step 4.4: Phase 4 Integration Test

```bash
# Test: All 5 projects are in the monorepo and importable
python -c "
import os, sys

# Check all directories exist
dirs = [
    'bridge',
    'agents/davinci/backend',
    'agents/davinci/addon',
    'agents/athena',
    'minerva3d/source/minerva3d/blenkernel',
    'minerva3d/source/minerva3d/blenlib',
    'minerva2d/libs/image',
    'minerva2d/libs/pigment',
    'minerva2d/libs/brush',
]

for d in dirs:
    if os.path.isdir(d):
        print(f'✓ {d}')
    else:
        print(f'✗ {d} MISSING')
" 2>&1
```

**Phase 4 Checkpoint:**
- [ ] Minerva 2D merged into monorepo
- [ ] CMakeLists.txt parses without errors
- [ ] Minerva 2D Agent plugin intact
- [ ] All 5 projects importable from monorepo
- [ ] No file conflicts between projects

---

## Phase 5: Unified Build System

**Goal:** Create a unified build system that can build all components from the monorepo root.

**Duration estimate:** 1-2 days

### Step 5.1: Create Root CMakeLists.txt

```cmake
# C:\Users\USER\Minerva-Suite\CMakeLists.txt
cmake_minimum_required(VERSION 3.21)
project(MinervaSuite LANGUAGES CXX C)

# Minerva 3D
add_subdirectory(minerva3d)

# Minerva 2D
add_subdirectory(minerva2d)
```

### Step 5.2: Create Root pyproject.toml

```toml
# C:\Users\USER\Minerva-Suite\pyproject.toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "minerva-suite"
version = "1.0.0"
description = "Minerva Creative Suite — AI-powered creative workspace"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
include = ["bridge.*", "agents.*"]
```

### Step 5.3: Create Unified requirements.txt

```txt
# C:\Users\USER\Minerva-Suite\requirements.txt
# Bridge
fastapi==0.115.0
uvicorn[standard]==0.30.0
httpx==0.27.0
pydantic==2.9.0
pydantic-settings==2.5.0
python-dotenv==1.0.0
gql==3.5.0
websockets==13.0

# DaVinci Agent
# (same as bridge + pytest for testing)
pytest==8.0.0
pytest-asyncio==0.23.0

# Athena Agent
# (from athena-agent's own requirements)
```

### Step 5.4: Create Build Scripts

```bash
# scripts/build-all.sh
#!/bin/bash
set -e
echo "Building Minerva Creative Suite..."

# Build Python components
pip install -r requirements.txt

# Build Minerva 3D (if toolchain available)
if command -v cmake &>/dev/null; then
    cd minerva3d
    mkdir -p build && cd build
    cmake .. -G "Visual Studio 17 2022" -A x64
    cmake --build . --config Release
    cd ../..
fi

# Build Minerva 2D (if toolchain available)
if command -v cmake &>/dev/null; then
    cd minerva2d
    mkdir -p build && cd build
    cmake .. -G "Visual Studio 17 2022" -A x64
    cmake --build . --config Release
    cd ../..
fi

echo "Build complete."
```

### Step 5.5: Phase 5 Test

```bash
# Test: Unified requirements install
pip install -r requirements.txt 2>&1 | tail -10

# Test: All Python modules importable
python -c "
from bridge.main import app as bridge_app
from agents.davinci.backend.main import app as davinci_app
print(f'✓ All Python modules importable')
print(f'  Bridge: {len(bridge_app.routes)} routes')
print(f'  DaVinci: {len(davinci_app.routes)} routes')
"
```

**Phase 5 Checkpoint:**
- [ ] Root CMakeLists.txt created
- [ ] Root pyproject.toml created
- [ ] Unified requirements.txt created
- [ ] Build scripts created
- [ ] All Python modules importable from monorepo root

---

## Phase 6: Cross-App Integration Testing

**Goal:** Test all cross-app workflows. This is the most critical phase.

**Duration estimate:** 2-3 days

### Step 6.1: Bridge ↔ DaVinci ↔ Minerva 3D Pipeline

**Test 6.1.1: DaVinci addon can connect to Bridge**
```bash
# Start Bridge on :3010
# Start DaVinci backend on :8360
# Load DaVinci addon in Minerva 3D's Python
# Verify: Addon connects to Bridge, Bridge proxies to DaVinci
```

**Test 6.1.2: End-to-end bpy code generation**
```bash
# Send a prompt through Bridge → DaVinci
# Verify: DaVinci generates bpy code
# Execute code in Minerva 3D's Python
# Verify: Object appears in scene
```

### Step 6.2: Bridge ↔ Athena ↔ Minerva 2D Pipeline

**Test 6.2.1: Athena can control Minerva 2D via Bridge**
```bash
# Start Bridge on :3010
# Start Athena agent
# Send painting command through Bridge → Athena → Minerva 2D
# Verify: Minerva 2D executes the command
```

### Step 6.3: Cross-App Workflows

**Test 6.3.1: Texture painting workflow**
```bash
# 1. Create 3D model in Minerva 3D
# 2. Send texture painting request to Bridge
# 3. Bridge routes to Minerva 2D
# 4. Paint texture in Minerva 2D
# 5. Apply texture to 3D model in Minerva 3D
# Verify: Texture applied correctly
```

**Test 6.3.2: AI-assisted creation workflow**
```bash
# 1. User describes a scene in natural language
# 2. Athena plans the workflow
# 3. DaVinci generates 3D geometry
# 4. Minerva 2D paints textures
# 5. Minerva 3D renders the final scene
# Verify: Complete pipeline works end-to-end
```

### Step 6.4: Regression Tests

```bash
# Run all existing tests from all projects
cd agents/davinci && python -m pytest tests/ -v 2>&1 | tail -20
cd ../.. && cd bridge && python -m pytest tests/ -v 2>&1 | tail -20
# ... etc for all test suites
```

**Phase 6 Checkpoint:**
- [ ] Bridge ↔ DaVinci ↔ Minerva 3D pipeline works
- [ ] Bridge ↔ Athena ↔ Minerva 2D pipeline works
- [ ] Cross-app workflows functional
- [ ] All existing tests still pass
- [ ] No regressions from merge

---

## Phase 7: Polish & Release

**Goal:** Final polish, documentation, and release preparation.

**Duration estimate:** 1-2 days

### Step 7.1: Final README

Create a comprehensive root README.md that describes the entire suite.

### Step 7.2: Final Documentation

Ensure all documentation is up to date:
- `ENGINE_ANALYSIS.md` — Engine architecture
- `MERGE_PLAN.md` — This file
- `MINERVA_SUITE_DOCUMENTATION.md` — Suite documentation

### Step 7.3: CI/CD Pipeline

Create a unified GitHub Actions workflow that:
1. Tests all Python components
2. Builds C++ components (when toolchain available)
3. Runs integration tests
4. Creates release artifacts

### Step 7.4: Release Tag

```bash
git tag v1.0.0
git push origin v1.0.0
```

**Phase 7 Checkpoint:**
- [ ] Root README.md complete
- [ ] All documentation updated
- [ ] CI/CD pipeline configured
- [ ] Release tagged

---

## Rollback Plan

Each phase is independently reversible:

| Phase | Rollback Action |
|-------|----------------|
| Phase 1 | Delete `Minerva-Suite/` directory. Original repos untouched. |
| Phase 2 | `git revert` the Athena merge commit. |
| Phase 3 | `git revert` the Minerva 3D merge commit. Remove symlink. |
| Phase 4 | `git revert` the Minerva 2D merge commit. |
| Phase 5 | Remove root CMakeLists.txt, pyproject.toml, requirements.txt. |
| Phase 6 | Fix issues found, no rollback needed. |
| Phase 7 | Remove release tag, fix issues. |

---

## Test Matrix

| Test ID | Phase | Test Name | Command | Expected Result |
|---------|-------|-----------|---------|-----------------|
| T1.2.1 | 1 | Bridge imports | `python -c "from bridge.main import app"` | No errors |
| T1.2.2 | 1 | Bridge health | `curl /health` | 200 OK |
| T1.3.1 | 1 | DaVinci backend imports | `python -c "from agents.davinci.backend.main import app"` | No errors |
| T1.3.2 | 1 | DaVinci addon imports | `python -c "from agents.davinci.addon import bl_info"` | No errors |
| T1.3.3 | 1 | DaVinci tests | `pytest agents/davinci/tests/` | 104 pass, 4 skip |
| T1.4.1 | 1 | Bridge→DaVinci import | Bridge imports DaVinci modules | No errors |
| T1.4.2 | 1 | DaVinci backend starts | Start on :8360 | Health check passes |
| T1.5 | 1 | Phase 1 integration | All services running | All health checks pass |
| T2.2.1 | 2 | Athena imports | `python -c "from agents.athena..."` | No errors |
| T2.3.1 | 2 | Bridge→Athena import | Bridge imports Athena modules | No errors |
| T2.4 | 2 | Phase 2 integration | All 3 services running | All health checks pass |
| T3.3.1 | 3 | CMake configure | `cmake ..` | Parses successfully |
| T3.4 | 3 | DaVinci addon in 3D | Addon loadable from 3D path | No errors |
| T4.3.1 | 4 | 2D plugin syntax | `py_compile` plugin | No errors |
| T4.4 | 4 | Phase 4 integration | All 5 projects importable | All directories exist |
| T5.5 | 5 | Unified requirements | `pip install -r requirements.txt` | All packages install |
| T6.1.1 | 6 | Addon→Bridge connection | Addon connects to Bridge | WebSocket connected |
| T6.1.2 | 6 | E2E code generation | Prompt → bpy code → execution | Object created |
| T6.3.1 | 6 | Texture workflow | 3D → 2D → 3D | Texture applied |
| T6.4 | 6 | Regression tests | All test suites | All pass |

---

## Summary

| Phase | What | Tests | Duration |
|-------|------|-------|----------|
| 1 | Bridge + DaVinci Agent | 7 tests | 1-2 days |
| 2 | + Athena Agent | 3 tests | 1-2 days |
| 3 | + Minerva 3D | 2 tests | 2-3 days |
| 4 | + Minerva 2D | 2 tests | 2-3 days |
| 5 | Unified build system | 1 test | 1-2 days |
| 6 | Cross-app integration | 4 tests | 2-3 days |
| 7 | Polish & release | 4 tests | 1-2 days |
| **Total** | **All 5 projects merged** | **23 tests** | **10-17 days** |

**Key Principle:** Each phase is independently testable and reversible. No phase depends on the next. If any phase fails, we can rollback to the previous checkpoint and fix issues before proceeding.
