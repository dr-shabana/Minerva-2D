# Merge Approach Analysis: Monorepo vs. Agent-First

> **Date:** 2026-06-17
> **Purpose:** Rigorous analysis of the proposed "honest assessment" approach vs. our current monorepo merge plan
> **Verdict:** The assessment is largely correct. Our current plan needs a fundamental pivot.

---

## The Core Question

**Should we merge Blender and Krita into one binary, or keep them separate and connect them via an agent layer?**

---

## What the Assessment Gets Right

### 1. "Two independent operating systems that happen to draw pixels"

**Verdict: ✅ Correct, and we confirmed it.**

| Blender | Krita |
|---------|-------|
| Custom window manager (GHOST) | Qt/KDE windowing |
| Own GPU context (OpenGL/Vulkan via `GPU_context_create`) | Qt painting + `QOpenGLWidget` |
| DNA/RNA data model | KisImage/KisLayer tile system |
| Depsgraph evaluation engine | Async layer projection |
| `int main()` in `creator.cc` | `int main()` in `main.cc` |
| 101 Qt references (minimal) | 101 Qt references (core dependency) |

Both have their own `main()` function. Both create their own GPU context. Both have their own event loop. Merging them into one binary means resolving **two event loops, two GPU contexts, two undo systems, two file formats** — in one process.

### 2. "Frankenstein merge — 9/10 pain level"

**Verdict: ✅ Correct.** We confirmed:
- Both have `int main()` — symbol conflict at link time
- Blender's GHOST creates an OpenGL context; Krita's Qt creates another — two GPU contexts in one process
- Blender's depsgraph and Krita's async merger are fundamentally different evaluation models
- CMake would need to reconcile 2653 lines (Blender) + 1702 lines (Krita) of build configuration

### 3. "Porting Krita's brush engine — 6/10 pain, realistic path"

**Verdict: ✅ Correct, and this is the most valuable insight.**

Krita's brush engine (`libs/brush/` — 50 files, `plugins/paintops/` — 1038 files) is genuinely world-class. Blender's texture painting is functional but not competitive with Krita for serious digital painting.

### 4. "The real prize is the agent layer"

**Verdict: ✅ Correct.** Neither Blender nor Krita has native AI agent integration. This is our unique value.

---

## What the Assessment Misses

### 1. We've already done the rebranding

We've already invested significant effort into rebranding both codebacks. The assessment assumes we're starting from scratch. We're not — we have:
- Minerva 3D: 9,587 files rebranded
- Minerva 2D: 2,410 files rebranded
- Both pushed to GitHub with full history

**This investment isn't wasted** — the rebranding works regardless of whether we merge or keep separate.

### 2. The monorepo plan has value even without a binary merge

Even if we don't merge into one binary, a monorepo is still valuable:
- Single `git clone` for developers
- Shared CI/CD
- Cross-project refactoring
- Unified documentation
- Easier dependency management

### 3. The assessment underestimates the Bridge

The assessment proposes "IPC/FFI" as option 2, but we've already built the Bridge. The Bridge is the IPC layer. The question is what we connect to it.

---

## Revised Recommendation

Based on the assessment and our actual codebase analysis, here's what I recommend:

### Option A: Agent-First (Recommended)

**Keep Minerva 3D and Minerva 2D as separate applications. Connect them via the Bridge + Agents.**

```
┌─────────────────────┐    ┌─────────────────────┐
│   Minerva 3D         │    │   Minerva 2D         │
│   (standalone app)   │    │   (standalone app)   │
│                      │    │                      │
│  ┌────────────────┐  │    │  ┌────────────────┐  │
│  │ DaVinci Agent  │  │    │  │ Athena Agent   │  │
│  │ (bpy add-on)   │  │    │  │ (PyKrita       │  │
│  │                │  │    │  │  plugin)       │  │
│  └───────┬────────┘  │    │  └───────┬────────┘  │
│          │           │    │          │           │
└──────────┼───────────┘    └──────────┼───────────┘
           │                           │
           └───────────┬───────────────┘
                       │
              ┌────────▼────────┐
              │   Minerva Bridge │
              │   (FastAPI :3010)│
              │                 │
              │  - Unified API  │
              │  - File exchange│
              │  - Render queue │
              │  - WebSocket    │
              └─────────────────┘
```

**Pros:**
- Each app compiles and runs independently
- No symbol conflicts, no CMake madness
- Can test each app separately
- Agent layer is the differentiator
- Faster iteration

**Cons:**
- Two separate processes
- IPC latency for cross-app workflows
- Not "one program" feel

### Option B: Monorepo + Separate Binaries (Compromise)

**Merge all code into one monorepo, but build separate binaries.**

```
Minerva-Suite/
├── bridge/              ← Python/FastAPI (one process)
├── agents/
│   ├── davinci/         ← DaVinci Agent (Python)
│   └── athena/          ← Athena Agent (Python)
├── minerva3d/           ← Minerva 3D (C++, separate binary)
│   └── scripts/addons_core/minerva3d_agent → symlink to agents/davinci/addon
├── minerva2d/           ← Minerva 2D (C++, separate binary)
│   └── plugins/python/minerva2d_agent/ ← (already bundled)
├── docs/
├── tests/
│   ├── integration/     ← Cross-app tests
│   └── unit/            ← Per-project tests
└── scripts/
    ├── build-3d.sh
    ├── build-2d.sh
    └── run-all.sh
```

**Pros:**
- Single `git clone`
- Shared CI/CD
- Cross-project refactoring
- Each binary compiles independently
- Agent layer connects everything

**Cons:**
- Still two separate processes
- More complex build system

### Option C: Full Binary Merge (Not Recommended)

**Merge everything into one binary.**

**Verdict: ❌ Don't do this.** The assessment is right — 9/10 pain level. We confirmed the technical blockers:
- Two `main()` functions
- Two GPU contexts
- Two event loops
- Two undo systems
- CMake configuration conflict (2653 + 1702 lines)

---

## What This Means for Our Current Plan

### What to Keep
1. **Monorepo structure** — Still valuable for code organization
2. **Bridge** — This is the integration hub, keep it
3. **Agent integration** — This is the unique value, keep it
4. **Rebranding** — Already done, works regardless
5. **CI/CD** — Already configured, works regardless

### What to Change
1. **No binary merge** — Don't try to compile Blender + Krita into one executable
2. **Separate build targets** — Build `minerva3d` and `minerva2d` as separate binaries
3. **Bridge as IPC** — The Bridge becomes the IPC layer between separate processes
4. **Agent layer as the differentiator** — Focus on making the agents deeply integrated into each app

### Revised Phase Plan

| Phase | What | Approach |
|-------|------|----------|
| 1 | Monorepo skeleton + Bridge | Keep as planned |
| 2 | DaVinci Agent | Keep as planned |
| 3 | Athena Agent | Keep as planned |
| 4 | Minerva 3D | Merge code, build as **separate binary** |
| 5 | Minerva 2D | Merge code, build as **separate binary** |
| 6 | Unified build system | Build scripts for each binary + Bridge |
| 7 | Cross-app integration | Bridge connects separate processes via WebSocket/IPC |
| 8 | Polish & release | Unified installer that installs all components |

---

## The Proof of Concept

The assessment suggests spiking a proof-of-concept. I agree. Here's what that looks like:

### Week 1 Spike: Agent-in-Blender Workflow

1. Start with Minerva 3D (already rebranded)
2. Load DaVinci Agent add-on (already bundled)
3. Connect to Bridge (already built)
4. Send a natural language prompt: "Create a red cube"
5. Bridge routes to DaVinci backend
6. DaVinci generates bpy code
7. Code executes in Minerva 3D
8. Cube appears in scene

**This proves the entire agent pipeline works end-to-end.**

If this works, the full vision is worth the investment. If it doesn't, we've learned in a week what would have taken months to discover in a full merge.

---

## Final Verdict

| Aspect | Our Original Plan | Revised Plan |
|--------|------------------|--------------|
| Binary merge | Yes (all into one) | No (separate binaries) |
| Monorepo | Yes | Yes (code organization) |
| Bridge | Integration hub | IPC layer between processes |
| Agent layer | Add-on | Core differentiator |
| Build system | Unified CMake | Separate CMake per C++ project |
| Risk | High (symbol conflicts) | Low (independent builds) |
| Time to first test | Weeks | Days |

**The assessment is right. Pivot to Option B: Monorepo + Separate Binaries + Agent Layer.**

The rebranding work isn't wasted. The Bridge isn't wasted. The agent integration isn't wasted. We just need to change the merge target from "one binary" to "one suite, separate processes, connected by agents."
