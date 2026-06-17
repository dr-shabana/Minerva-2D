# Minerva Creative Suite — Engine Deep Analysis

> **Date:** 2026-06-17
> **Purpose:** Deep architectural analysis of both Minerva 3D (Blender) and Minerva 2D (Krita) engines
> **Scope:** Read-only analysis — no code changes

---

## Table of Contents

1. [Minerva 3D (Blender) Engine Analysis](#minerva-3d-blender)
2. [Minerva 2D (Krita) Engine Analysis](#minerva-2d-krita)
3. [Comparative Analysis](#comparative-analysis)
4. [Integration Points](#integration-points)

---

## Minerva 3D (Blender)

### 1. High-Level Architecture

Minerva 3D is a **monolithic C++ application** (~7,166 source files in `source/`) built on a custom data model with Python scripting integration. The architecture follows a **data-centric design** where everything is a "datablock" in a unified scene graph.

**Build System:** CMake 3.21+, MSVC 1928+, C++20
**Total Source Files:** ~13,600 (including tests, tools, scripts)
**Core Language:** C++ (~80%), Python (~15%), C (~1.5%), GLSL (~1.2%)

### 2. Core Subsystems

#### 2.1 DNA/RNA System (Data Model)

**Location:** `source/minerva3d/makesdna/` (113 files) + `source/minerva3d/makesrna/` (133 files)

The DNA/RNA system is the **backbone of Blender's entire data model**:

- **DNA (DeoxyNucleic Acid):** Defines the binary data structures (C structs) that represent every object in the scene — meshes, materials, lights, cameras, armatures, etc. These are defined in header files like `DNA_mesh_types.h`, `DNA_material_types.h`, `DNA_object_types.h`.
  - DNA types are compiled into a "DNA struct" that can be serialized to `.blend` files
  - The `makesdna/` module generates the binary format at build time
  - Forward compatibility: old Blender can read new `.blend` files (but not vice versa)

- **RNA (Ribonucleic Acid):** The property system that wraps DNA structs with a higher-level API. RNA provides:
  - Property definitions (name, type, min/max, description)
  - Getter/setter functions
  - Property paths (e.g., `bpy.data.objects["Cube"].location.x`)
  - Automatic UI generation from property definitions
  - The bridge between C++ data and Python API

**Key files:**
- `DNA_types.h` — Master type registry
- `RNA_types.hh` — RNA type system
- `RNA_define.hh` — Property definition macros
- `RNA_access.hh` — Property access functions

#### 2.2 BLenKernel (Core Kernel)

**Location:** `source/minerva3d/blenkernel/` (571 files)

The kernel is the **brain of the application** — it manages:

- **Datablock management:** Every object (mesh, material, texture, etc.) is a datablock with a unique name, reference counting, and library linking
- **Scene graph:** Hierarchical scene organization (collections, parent-child relationships)
- **Dependency graph (depsgraph):** Tracks relationships between objects for evaluation order
- **Undo system:** Full undo/redo with memory-efficient diffing
- **Evaluation pipeline:** Updates only what changed (dirty propagation)

**Key files:**
- `BKE_main.hh` — Main database (all datablocks)
- `BKE_scene.hh` — Scene management
- `BKE_object.hh` — Object management
- `BKE_mesh.hh` — Mesh data operations
- `BKE_material.hh` — Material management
- `BKE_node.hh` — Node system base

#### 2.3 BLenLib (Core Library)

**Location:** `source/minerva3d/blenlib/` (499 files)

General-purpose utilities and data structures:

- **Math library:** Vectors, matrices, quaternions, bounding boxes, kd-trees, BVH trees
- **Memory management:** Allocators, memory pools, guarded allocation
- **String handling:** UTF-8 string operations, path manipulation
- **Collections:** Dynamic arrays, hash sets, priority queues
- **Geometry:** Mesh operations, spatial queries, intersection tests

**Key files:**
- `BLI_math.hh` — Math primitives (float3, float4x4, quaternion)
- `BLI_vector.hh` — Dynamic array (similar to std::vector but with small-buffer optimization)
- `BLI_string.hh` — String utilities
- `BLI_kdop_bvh.hh` — Bounding volume hierarchy for spatial queries

#### 2.4 Dependency Graph (Depsgraph)

**Location:** `source/minerva3d/depsgraph/` (128 files)

The dependency graph is the **evaluation engine** that determines what needs to be recalculated when something changes:

- **Node-based graph:** Each object/operation is a node; edges represent dependencies
- **Dirty propagation:** When an object changes, only dependent objects are re-evaluated
- **Parallel evaluation:** Independent nodes can be evaluated in parallel (thread pool)
- **Physics integration:** Physics simulations are nodes in the depsgraph

**Key files:**
- `DEG_depsgraph.hh` — Main depsgraph structure
- `DEG_depsgraph_build.hh` — Graph construction
- `DEG_depsgraph_query.hh` — Query interface
- `DEG_depsgraph_physics.hh` — Physics integration

#### 2.5 Drawing Engine (DRaw)

**Location:** `source/minerva3d/draw/` (698 files)

The drawing engine renders the 3D viewport:

- **GPU abstraction:** `gpu/` module (706 files) provides a unified API over OpenGL, Vulkan, and Metal
- **Draw engines:** Multiple renderers for different viewport modes:
  - `eevee/` — Real-time PBR renderer (EEVEE)
  - `workbench/` — Fast solid/wireframe renderer
  - `external/` — External render engine interface
  - `overlay/` — Selection outlines, gizmos, annotations
  - `select/` — GPU selection buffer
- **Grease Pencil:** 2D drawing in 3D space (gpencil_legacy, grease_pencil editors)

**Key files:**
- `DRW_engine.hh` — Draw engine base class
- `DRW_pbvh.hh` — PBVH (Partitioned Bounding Volume Hierarchy) for sculpting
- `GPU_batch.hh` — GPU batch rendering
- `GPU_shader.hh` — Shader management
- `GPU_material.hh` — Material GPU state

#### 2.6 Node System

**Location:** `source/minerva3d/nodes/` (703 files)

The node system is a **visual programming framework** used for:

- **Geometry Nodes:** Procedural mesh generation and manipulation (the flagship feature)
- **Shader Nodes:** Material and shader graph editing
- **Compositor Nodes:** Post-processing and compositing
- **Texture Nodes:** Procedural texture generation

**Architecture:**
- Nodes are defined in C++ with input/output sockets
- The node graph is evaluated lazily (only when output is needed)
- Geometry Nodes use a "field" system for attribute propagation
- Lazy evaluation with `LazyFunctionGraph` for performance

**Key files:**
- `NOD_geometry.hh` — Geometry node definitions
- `NOD_composite.hh` — Compositor node definitions
- `NOD_geometry_nodes_execute.hh` — Geometry nodes evaluation
- `NOD_geometry_nodes_lazy_function.hh` — Lazy evaluation system

#### 2.7 Modifiers

**Location:** `source/minerva3d/modifiers/` (109 files)

Modifiers are **non-destructive operations** applied to objects:

- **Mesh modifiers:** Subdivision, boolean, mirror, array, bevel, solidify, etc.
- **Geometry Nodes modifier:** Embeds a geometry node tree as a modifier
- **Armature modifiers:** Skeletal deformation
- **Particle modifiers:** Particle system integration

Modifiers are evaluated in the depsgraph and can be stacked.

#### 2.8 Geometry Module

**Location:** `source/minerva3d/geometry/` (117 files)

Core geometry algorithms:

- **Mesh operations:** Boolean, bevel, triangulate, merge, split
- **Curve operations:** Extrude, bevel, trim
- **Volume operations:** Mesh-to-volume, volume-to-mesh
- **Attribute system:** Generic attribute storage (position, normal, UV, color, custom)

#### 2.9 Editors

**Location:** `source/minerva3d/editors/` (1,200 files)

The editor subsystem implements all **UI panels and tools**:

- **Space types:** Each editor type (3D View, Outliner, Node Editor, etc.) is a "space"
- **Tool system:** `space_tool/` — Interactive tools (move, rotate, scale, sculpt, etc.)
- **Draw callbacks:** Custom rendering within editors
- **Operators:** Reversible operations (the "undoable" actions)

**Key editors:**
- `space_3dview/` — 3D Viewport
- `space_outliner/` — Scene hierarchy
- `space_node/` — Node Editor
- `space_image/` — Image/UV Editor
- `space_sequencer/` — Video Sequencer
- `space_nla/` — NLA Editor (animation)

#### 2.10 Window Manager

**Location:** `source/minerva3d/windowmanager/` (80 files)

The window manager is the **top-level application controller**:

- **Event system:** Keyboard, mouse, tablet, XR events
- **Message bus:** Pub/sub system for inter-module communication
- **Keymap system:** Configurable keyboard shortcuts
- **Window management:** Multi-window support
- **XR support:** VR/AR integration

**Key files:**
- `WM_types.hh` — Core types (events, operators, windows)
- `WM_event_system.hh` — Event dispatch
- `WM_keymap.hh` — Keymap management
- `WM_message.hh` — Message bus

#### 2.11 Python API (bpy)

**Location:** `source/minerva3d/python/` (207 files)

The Python API is **auto-generated from RNA definitions**:

- `bpy.types` — All Blender types (Object, Mesh, Material, etc.)
- `bpy.ops` — All operators (actions)
- `bpy.data` — All datablocks
- `bpy.context` — Current state
- `bpy.utils` — Utility functions
- `bmesh` — Low-level mesh editing
- `mathutils` — Math library (vectors, matrices, quaternions)
- `gpu` — GPU drawing API

The Python API is the **primary scripting interface** and is what DaVinci Agent uses to control Minerva 3D.

#### 2.12 Render Engines

**Location:** `source/minerva3d/render/` (44 files) + `intern/cycles/` (936 files)

- **EEVEE:** Real-time PBR renderer (OpenGL/Vulkan based)
- **Cycles:** Physically-based path tracer (CPU/GPU, supports CUDA, OptiX, HIP, Metal)
- **Workbench:** Fast solid/wireframe renderer for viewport
- **Hydra render delegate:** USD Hydra integration for external renderers

#### 2.13 I/O System

**Location:** `source/minerva3d/io/` (308 files)

File format support:
- **Native:** `.blend` (binary, DNA-based)
- **3D formats:** FBX, glTF, OBJ, STL, PLY, Alembic, USD
- **Image formats:** OpenEXR, PNG, JPEG, TIFF, WebP, HDR
- **Video:** FFmpeg integration

#### 2.14 Internal Libraries (intern/)

**Location:** `intern/` (1,562 files)

| Library | Files | Purpose |
|---------|-------|---------|
| `cycles/` | 936 | Cycles render engine |
| `ghost/` | 148 | Windowing system (GHOST = Generic Handy Operating System Toolkit) |
| `gpu/` | (in draw/) | GPU abstraction |
| `libmv/` | 179 | Motion tracking (libmv) |
| `opensubdiv/` | 41 | OpenSubdiv integration |
| `itasc/` | 85 | IK solver |
| `mantaflow/` | 10 | Fluid simulation |
| `guardedalloc/` | 16 | Memory allocation tracking |
| `clog/` | 3 | Logging system |

### 3. Application Entry Point

**File:** `source/creator/creator.cc`

The main application flow:
1. Parse command-line arguments (`creator_args.cc`)
2. Initialize subsystems (window manager, DNA/RNA, Python)
3. Load default scene or open file
4. Main event loop (process events, update depsgraph, draw)
5. Shutdown and cleanup

### 4. Key Design Patterns

- **Everything is a datablock:** All data lives in a central database (`Main`)
- **DNA/RNA separation:** Low-level data (DNA) vs. high-level API (RNA)
- **Dependency graph:** Lazy evaluation with dirty propagation
- **Operator system:** All actions are reversible operators
- **Python as first-class citizen:** Python can access everything via RNA
- **Plugin architecture:** Add-ons can register new operators, panels, nodes, modifiers

---

## Minerva 2D (Krita)

### 1. High-Level Architecture

Minerva 2D is a **Qt/KDE-based C++ application** (~5,215 files in `libs/` + ~4,390 in `plugins/`) built on a **layer-based document model** with a sophisticated brush engine.

**Build System:** CMake 3.19+, MSVC 1928+, C++17, Qt 5/6, KDE Frameworks 5/6
**Total Source Files:** ~12,269 (including tests, plugins, translations)
**Core Language:** C++ (~90%), Python (~3%), QML (~1.2%)

### 2. Core Subsystems

#### 2.1 Image Engine

**Location:** `libs/image/` (1,335 files)

The image engine is the **core of Krita's painting system**:

- **Tile-based architecture:** Images are divided into tiles (typically 64×64 pixels) for memory efficiency and parallel processing
- **Layer system:** Multiple layer types (paint, vector, group, filter, file, fill, clone, generator)
- **Mask system:** Transparency masks, filter masks, transform masks, selection masks
- **Projection system:** Layers are composited into a single projection for display
- **Undo system:** Tile-based undo with memory-efficient diffing
- **Processing pipeline:** Asynchronous image processing with progress reporting

**Key files:**
- `kis_image.hh` — Image class (collection of layers)
- `kis_layer.hh` — Base layer class
- `kis_paint_layer.hh` — Paint layer (raster)
- `kis_group_layer.hh` — Group layer (container)
- `kis_mask.hh` — Base mask class
- `kis_filter.hh` — Filter base class
- `kis_adjustment_layer.hh` — Adjustment layer
- `kis_generator_layer.hh` — Generator layer (procedural content)
- `kis_async_merger.hh` — Asynchronous layer compositing
- `kis_base_processor.hh` — Base image processor

**Tile system:**
- `kis_tile.hh` — Individual tile
- `kis_tiled_data_manager.hh` — Tile data management
- `kis_tiled_data_manager_p.h` — Private implementation

#### 2.2 Pigment Engine (Color)

**Location:** `libs/pigment/` (236 files)

The pigment engine handles **color management and conversion**:

- **Color spaces:** RGB (sRGB, Adobe RGB, ProPhoto), CMYK, Lab, XYZ, Grayscale
- **Color profiles:** ICC profile support (input, display, output)
- **Color conversions:** Fast color space conversion with caching
- **Dithering:** Ordered and error-diffusion dithering
- **Histogram:** Per-channel histogram computation
- **Color blending:** Porter-Duff compositing operations

**Key files:**
- `KoColor.h` — Color class (color space + channel values)
- `KoColorSpace.h` — Color space base class
- `KoColorConversionSystem.h` — Color conversion graph
- `KoColorProfile.h` — ICC profile wrapper
- `KoChannelInfo.h` — Channel metadata (type, size, position)
- `KoBasicHistogramProducers.h` — Histogram computation
- `KisDitherOp.h` — Dithering operations

#### 2.3 Brush Engine

**Location:** `libs/brush/` (92 files)

The brush engine is **Krita's crown jewel** — one of the most sophisticated digital painting brush engines:

- **Brush types:**
  - `kis_auto_brush` — Auto-brush (generated from parameters)
  - `kis_abr_brush` — Adobe Photoshop ABR brush import
  - `kis_gbr_brush` — GIMP GBR brush import
  - `kis_png_brush` — PNG-based brush tip
  - `kis_svg_brush` — SVG-based brush tip
  - `kis_text_brush` — Text-based brush
  - `kis_imagepipe_brush` — Image pipe brush (animated/multi-tip)
  - `kis_scaling_size_brush` — Size-responsive brush

- **Brush parameters:** Size, opacity, flow, spacing, rotation, scale, scatter, texture, color rate, pressure curves
- **Dab rendering:** Each brush stroke is composed of "dabs" (individual impressions)
- **Brush engines (paintops):** Different brush behaviors (pixel, smudge, sketch, hairy, etc.)

**Key files:**
- `kis_brush.h` — Base brush class
- `kis_brush_factory.h` — Brush factory (serialization)
- `kis_brush_registry.h` — Brush registry
- `kis_dab_shape.h` — Dab shape definition
- `kis_brushes_pipe.h` — Brush pipe (multi-tip)
- `kis_boundary.h` — Brush boundary computation

#### 2.4 Flake (Document/Shape Model)

**Location:** `libs/flake/` (851 files)

Flake is the **document object model** for shapes and canvas:

- **Shape system:** Vector shapes (rectangles, ellipses, paths, text)
- **Canvas system:** `KoCanvasBase` — Abstract canvas for rendering
- **Resource management:** Patterns, gradients, palettes
- **Clip paths and masks:** Vector clipping
- **Shape commands:** Undoable shape operations

**Key files:**
- `KoCanvasBase.h` — Abstract canvas
- `KoCanvasController.h` — Canvas controller (zoom, pan, rotation)
- `KoCanvasResourceProvider.h` — Resource management (patterns, gradients)
- `KoClipPath.h` — Clip path
- `KoClipMask.h` — Clip mask
- `KoShape.h` — Base shape class (in `libs/flake/` subdirectories)

#### 2.5 UI Framework

**Location:** `libs/ui/` (1,603 files)

The UI framework provides **Krita's user interface**:

- **Action system:** `kis_action.h` — Menu/toolbar actions
- **Action manager:** `kis_action_manager.h` — Action registration and execution
- **Canvas:** `kis_canvas2.h` — Main painting canvas
- **Input:** Tablet/stylus input handling
- **Animation:** Animation timeline and playback
- **Resource management:** Brush presets, palettes, patterns
- **Configuration:** Settings and preferences

**Key files:**
- `kis_action.h` — Action base class
- `kis_action_manager.h` — Action manager
- `kis_canvas_resource_provider.h` — Canvas resources (brush, color, pattern)
- `kis_imagepipe_brush.h` — Image pipe brush
- `kis_animation_frame_cache.h` — Animation frame cache

#### 2.6 Widgets

**Location:** `libs/widgets/` (171 files)

Custom UI widgets:

- **Color selector:** HSV wheel, color slider, palette view
- **Angle selector:** `KisAngleSelector` — Circular angle picker
- **Color button:** `kis_color_button.h` — Color swatch button
- **Palette view:** `kis_palette_view.h` — Color palette display
- **Spinbox color selector:** `kis_spinbox_color_selector.h`

#### 2.7 Paint Operations (Paintops)

**Location:** `plugins/paintops/` (1,038 files)

Paint operations are the **brush behaviors** — what happens when you paint:

| Paintop | Description |
|---------|-------------|
| `defaultpaintops/` | Basic pixel painting |
| `colorsmudge/` | Color smudging/blending |
| `curvebrush/` | Curve-based brush strokes |
| `deform/` | Deformation (push, expand, shrink) |
| `experiment/` | Experimental brushes |
| `gridbrush/` | Grid-based brush |
| `hairy/` | Hair/fur brush |
| `hatching/` | Hatching/cross-hatching |
| `mypaint` | MyPaint brush engine integration |
| `particle/` | Particle-based brush |
| `roundmarker/` | Round marker brush |
| `sketch/` | Sketching brush |
| `spray/` | Spray/airbrush |
| `tangentnormal` | Tangent normal brush |
| `filterop/` | Filter brush (paint with filters) |

Each paintop implements a specific brush behavior by overriding the `paint()` method.

#### 2.8 Filters

**Location:** `plugins/filters/` (423 files)

Image filters (non-destructive when used as filter masks):

| Category | Filters |
|----------|---------|
| Blur | Gaussian, motion, lens, box |
| Color | HSV adjustment, color balance, levels, curves, gradient map |
| Edge detection | Sobel, Laplacian, edge detect |
| Emboss | Emboss, phong bump map |
| Enhancement | Sharpen, unsharp mask, dodge/burn |
| Noise | Add noise, reduce noise |
| Distort | Oil paint, pixelize, raindrops, wave, whirl/pinch |
| Artistic | ASLCDL, fast color transfer, halftone |
| Adjustment | Posterize, threshold, normalize, index colors |

#### 2.9 Generators

**Location:** `plugins/generators/` (95 files)

Procedural content generators:

- `gradient/` — Gradient fills
- `pattern/` — Pattern fills
- `multigridpattern/` — Multi-grid patterns
- `screentone/` — Screentone patterns (manga)
- `seexpr/` — SeExpr scripting (Disney's expression language)
- `simplexnoise/` — Simplex noise generation
- `solid/` — Solid color fills

#### 2.10 Dockers

**Location:** `plugins/dockers/` (577 files)

Dockers are **floating/panels** in the UI:

| Docker | Purpose |
|--------|---------|
| `layerdocker` | Layer stack |
| `advancedcolorselector` | Advanced color selector |
| `palettedocker` | Color palette |
| `presetdocker` | Brush presets |
| `histogramdocker` | Histogram |
| `historydocker` | Undo history |
| `gamutmaskdocker` | Gamut mask |
| `animationdocker` | Animation timeline |
| `storyboarddocker` | Storyboard |
| `logdocker` | Log output |
| `recorderdocker` | Macro recorder |

#### 2.11 Tools

**Location:** `plugins/tools/` (473 files)

Interactive tools:

| Tool | Purpose |
|------|---------|
| `basictools/` | Basic tools (move, crop, gradient, measure) |
| `selectiontools/` | Selection tools (rectangle, ellipse, freehand, bezier, magnetic) |
| `tool_transform2` | Transform tool |
| `tool_crop` | Crop tool |
| `tool_lazybrush` | Lazy brush (smart selection) |
| `tool_knife` | Knife tool (cut shapes) |
| `tool_polygon` | Polygon tool |
| `tool_polyline` | Polyline tool |
| `svgtexttool` | SVG text tool |

#### 2.12 Import/Export (Impex)

**Location:** `plugins/impex/` (877 files)

File format support:

| Format | Type | Notes |
|--------|------|-------|
| `.kra` | Native | Krita's native format (ZIP with XML + images) |
| `.krz` | Native | Compressed Krita format |
| `.psd` | Import/Export | Adobe Photoshop (read/write) |
| `.ora` | Import/Export | OpenRaster |
| `.png` | Import/Export | Full alpha support |
| `.jpg` | Import/Export | JPEG |
| `.tiff` | Import/Export | TIFF with layers |
| `.exr` | Import/Export | OpenEXR (HDR) |
| `.webp` | Import/Export | WebP |
| `.svg` | Import/Export | SVG (vector) |
| `.pdf` | Export | PDF |
| `.gif` | Import/Export | GIF (animated) |
| `.xcf` | Import | GIMP XCF |
| `.csv` | Import | Color swatch CSV |
| `.brush` | Import | Brush presets |
| `.heightmap` | Import/Export | Height maps |
| `.spriter` | Export | Spriter animation |

#### 2.13 Resource System

**Location:** `libs/resources/` (185 files)

Resource management:

- **Brush presets:** `.bundle` files (ZIP with brush data)
- **Patterns:** Image patterns for fill
- **Gradients:** Gradient definitions
- **Palettes:** Color palettes (`.gpl`, `.pal`, `.aco`, `.ase`)
- **Workspaces:** UI layout presets
- **Sessions:** Named workspace configurations

#### 2.14 Global Definitions

**Location:** `libs/global/` (145 files)

- `kis_global.h` — Global macros and types
- `kis_algebra_2d.h` — 2D math (vectors, matrices, transformations)
- `kis_assert.h` — Assertion macros
- `kis_debug.h` — Debug utilities
- `kis_config_notifier.h` — Configuration change notification
- `kis_latency_tracker.h` — Performance tracking

### 3. Application Entry Point

**File:** `minerva2d/main.cc`

The main application flow:
1. Initialize Qt application
2. Initialize KDE Frameworks (KAboutData, KCmdLineArgs)
3. Create main window (`KisMainWindow`)
4. Initialize resource system (brushes, patterns, palettes)
5. Load plugins (paintops, filters, tools, dockers, impex)
6. Show main window
7. Enter Qt event loop

### 4. Key Design Patterns

- **Tile-based image processing:** Images are divided into tiles for memory efficiency and parallelism
- **Layer compositing:** Layers are composited on-the-fly using a projection system
- **Plugin architecture:** All functionality (paintops, filters, tools, dockers) is plugin-based
- **Resource system:** Brushes, patterns, palettes are resources that can be bundled and shared
- **Non-destructive editing:** Filters and adjustments can be applied as masks
- **Python scripting:** PyKrita plugin system for automation
- **KDE integration:** Uses KConfig, KIO, KXMLGUI, KAction frameworks

---

## Comparative Analysis

### Architecture Comparison

| Aspect | Minerva 3D (Blender) | Minerva 2D (Krita) |
|--------|---------------------|---------------------|
| **Core paradigm** | 3D scene graph (datablocks) | 2D layer-based document |
| **Data model** | DNA/RNA (C structs + property system) | Tile-based image + layer tree |
| **Language** | C++20, Python 3.11 | C++17, Qt, KDE Frameworks |
| **Build system** | CMake 3.21+ | CMake 3.19+ |
| **Windowing** | Custom (GHOST) | Qt/KDE |
| **Rendering** | OpenGL/Vulkan/Metal (GPU) | Qt painting + OpenGL |
| **Scripting** | Python (bpy, auto-generated from RNA) | Python (PyKrita, manual bindings) |
| **Plugin system** | Python add-ons + C++ modules | C++ plugins + Python scripts |
| **File format** | `.blend` (binary, DNA-based) | `.kra` (ZIP with XML + images) |
| **Undo system** | Datablock-level undo | Tile-level undo |
| **Evaluation** | Dependency graph (depsgraph) | Layer projection (async merger) |
| **Node system** | Geometry/Shader/Compositor/Texture nodes | Limited (filter layers) |
| **Color management** | OCIO (OpenColorIO) | ICC profiles (pigment engine) |
| **Brush engine** | Grease Pencil (2D in 3D) | Full digital painting engine |
| **Animation** | Full animation system (rigging, NLA, graph editor) | Frame-by-frame animation |
| **Physics** | Built-in (Bullet, Mantaflow) | None |
| **Video** | Video Sequencer | None |
| **XR support** | OpenXR | None |

### Codebase Size Comparison

| Metric | Minerva 3D | Minerva 2D |
|--------|-----------|-----------|
| Total files | ~20,700 | ~12,269 |
| Source files | ~7,166 | ~5,215 (libs) + ~4,390 (plugins) |
| Test files | ~7,745 | Included in plugins |
| Python files | ~853 (scripts) | ~278 (plugins/python) |
| C++ files | ~5,700+ | ~4,500+ |
| Translation files | 49 .po | 75 .po |

### Key Architectural Differences

1. **Data Model:**
   - Minerva 3D: Everything is a datablock in a central database. Objects reference each other by name/pointer.
   - Minerva 2D: Document contains a tree of layers. Each layer has its own pixel data (tiles).

2. **Evaluation Model:**
   - Minerva 3D: Dependency graph determines evaluation order. Only dirty objects are re-evaluated.
   - Minerva 2D: Layer projection composites all visible layers. Only changed tiles are re-projected.

3. **Rendering:**
   - Minerva 3D: Full 3D rendering pipeline (vertex shaders, fragment shaders, ray tracing).
   - Minerva 2D: 2D canvas rendering (Qt painting, OpenGL for canvas display).

4. **Extensibility:**
   - Minerva 3D: Python add-ons can add operators, panels, nodes, modifiers, importers.
   - Minerva 2D: C++ plugins for paintops/filters/tools, Python scripts for automation.

5. **Color Management:**
   - Minerva 3D: OCIO (OpenColorIO) — industry-standard color management.
   - Minerva 2D: Pigment engine — custom ICC-based color management.

---

## Integration Points

### How DaVinci Agent Controls Minerva 3D

1. **Python API (bpy):** DaVinci generates bpy code that is executed in Minerva's Python runtime
2. **WebSocket connection:** The add-on connects to the DaVinci backend via WebSocket
3. **Code execution:** Generated code is executed in a sandboxed environment with safety checks
4. **Viewport screenshots:** The add-on captures viewport screenshots for vision verification

### How Minerva 2D Agent Controls Minerva 2D

1. **PyKrita plugin:** The agent is a PyKrita plugin that runs inside Minerva 2D
2. **Krita API:** Uses `krita` Python module to control the application
3. **Docker UI:** The chat interface is embedded as a Krita docker (panel)
4. **WebSocket connection:** Connects to Minerva Bridge for LLM access

### Cross-Application Workflows (via Minerva Bridge)

1. **Texture painting:** Paint in Minerva 2D → Apply to 3D model in Minerva 3D
2. **Concept to model:** Sketch in Minerva 2D → Generate 3D model via DaVinci Agent
3. **Render compositing:** Render in Minerva 3D → Composite in Minerva 2D
4. **AI-assisted creation:** Natural language → Control both applications

### Shared Infrastructure

- **Minerva Bridge:** Unified API layer (FastAPI, port 3010)
- **Athena Agent:** Shared LLM provider/model management
- **File exchange:** Shared file format understanding
- **Session management:** Cross-application session state
