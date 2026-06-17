#!/usr/bin/env python3
"""
Krita → Minerva 2D Rebranding Script
======================================
Systematically renames all Krita branding to Minerva 2D across the entire codebase.

Three-target rename model:
- Module/package: krita → minerva2d (lowercase code)
- Brand/CLI: Krita → Minerva 2D (title case, user-facing)
- Env/Config: KRITA → MINERVA2D (uppercase)

Usage: python rebrand_krita_to_minerva2d.py
"""

import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Directories to skip
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.pytest_cache'}

# Binary extensions to skip content scanning
BINARY_EXTS = {
    '.png', '.ico', '.icns', '.webp', '.mp4', '.pyc', '.woff2', '.ttf', '.otf',
    '.exe', '.dll', '.so', '.dylib', '.o', '.a', '.jar', '.kra', '.bundle',
    '.psd', '.xcf', '.exr', '.hdr', '.dds', '.tga', '.tif', '.jpg', '.jpeg',
    '.bmp', '.gif', '.jp2', '.j2c', '.avif', '.heif', '.jxl', '.mov', '.avi',
    '.mkv', '.ogg', '.webm', '.bin', '.dat', '.blob', '.bz2', '.gz', '.zip',
    '.7z', '.rar', '.tar', '.xz', '.sqlite', '.db', '.icc', '.icm',
    '.plist', '.entitlements', '.pbxproj', '.xcscheme', '.xib',
    '.jar', '.class', '.dex', '.apk',
    '.abr', '.gbr', '.ggr', '.gih', '.pat', '.aco', '.ase', '.act', '.pal',
    '.colors', '.profile', '.icc', '.icm',
}

# Text extensions to process
TEXT_EXTS = {
    '.py', '.cpp', '.h', '.hpp', '.c', '.cc', '.hh', '.hxx',
    '.cmake', '.cmake.in', '.txt', '.md', '.rst', '.html', '.htm',
    '.xml', '.yaml', '.yml', '.toml', '.cfg', '.ini', '.conf', '.desktop',
    '.desktop.in', '.json', '.js', '.css', '.qml', '.qrc',
    '.sh', '.bat', '.cmd', '.ps1', '.diff', '.patch', '.po', '.pot',
    '.svg', '.rc', '.def', '.in', '.inl', '.template', '.pro', '.pri',
    '.gradle', '.java', '.kt', '.swift', '.m', '.mm', '.pl', '.pm',
    '.sql', '.dot', '.gpl', '.dox', '.properties', '.action',
    '.shortcuts', '.style', '.stylesheet', '.workspace',
    '.kse', '.kpl', '.kpp', '.kwl', '.kws', '.ksn', '.sbz',
    '.predefinedimage',
    '.kra',  # Krita's file format is actually XML inside a zip
    '.sip', '.pyi',
    '.schema', '.xsd', '.dtd', '.xsl', '.xslt',
    '.tag', '.m', '.mm',
    '.nsh', '.nsi', '.lnk',
}

# ── Replacement rules (longest match first within each group) ──

REPLACEMENTS = [
    # ── CMake project name ──
    ("project(krita ", "project(minerva2d "),
    ("project(Krita ", "project(Minerva2D "),

    # ── Multi-word brand references (longest first) ──
    ("Krita Artists", "Minerva Artists"),
    ("Krita Manual", "Minerva Manual"),
    ("Krita Wiki", "Minerva Wiki"),
    ("Krita Python", "Minerva Python"),
    ("Krita Plugin", "Minerva Plugin"),
    ("Krita Plugins", "Minerva Plugins"),
    ("Krita Add-on", "Minerva Add-on"),
    ("Krita Add-ons", "Minerva Add-ons"),
    ("Krita Extension", "Minerva Extension"),
    ("Krita Extensions", "Minerva Extensions"),
    ("Krita Script", "Minerva Script"),
    ("Krita Scripts", "Minerva Scripts"),
    ("Krita Action", "Minerva Action"),
    ("Krita Actions", "Minerva Actions"),
    ("Krita Resource", "Minerva Resource"),
    ("Krita Resources", "Minerva Resources"),
    ("Krita Bundle", "Minerva Bundle"),
    ("Krita Bundles", "Minerva Bundles"),
    ("Krita Preset", "Minerva Preset"),
    ("Krita Presets", "Minerva Presets"),
    ("Krita Filter", "Minerva Filter"),
    ("Krita Filters", "Minerva Filters"),
    ("Krita Brush", "Minerva Brush"),
    ("Krita Brushes", "Minerva Brushes"),
    ("Krita Engine", "Minerva Engine"),
    ("Krita Engines", "Minerva Engines"),
    ("Krita Tool", "Minerva Tool"),
    ("Krita Tools", "Minerva Tools"),
    ("Krita Docker", "Minerva Docker"),
    ("Krita Dockers", "Minerva Dockers"),
    ("Krita Panel", "Minerva Panel"),
    ("Krita Panels", "Minerva Panels"),
    ("Krita Layer", "Minerva Layer"),
    ("Krita Layers", "Minerva Layers"),
    ("Krita Canvas", "Minerva Canvas"),
    ("Krita View", "Minerva View"),
    ("Krita Window", "Minerva Window"),
    ("Krita Menu", "Minerva Menu"),
    ("Krita Toolbar", "Minerva Toolbar"),
    ("Krita Shortcut", "Minerva Shortcut"),
    ("Krita Shortcuts", "Minerva Shortcuts"),
    ("Krita Profile", "Minerva Profile"),
    ("Krita Profiles", "Minerva Profiles"),
    ("Krita Color", "Minerva Color"),
    ("Krita Colors", "Minerva Colors"),
    ("Krita Palette", "Minerva Palette"),
    ("Krita Palettes", "Minerva Palettes"),
    ("Krita Gradient", "Minerva Gradient"),
    ("Krita Gradients", "Minerva Gradients"),
    ("Krita Pattern", "Minerva Pattern"),
    ("Krita Patterns", "Minerva Patterns"),
    ("Krita Texture", "Minerva Texture"),
    ("Krita Textures", "Minerva Textures"),
    ("Krita Stroke", "Minerva Stroke"),
    ("Krita Strokes", "Minerva Strokes"),
    ("Krita Selection", "Minerva Selection"),
    ("Krita Transform", "Minerva Transform"),
    ("Krita Animation", "Minerva Animation"),
    ("Krita Frame", "Minerva Frame"),
    ("Krita Frames", "Minerva Frames"),
    ("Krita Timeline", "Minerva Timeline"),
    ("Krita Onion", "Minerva Onion"),
    ("Krita Vector", "Minerva Vector"),
    ("Krita Shape", "Minerva Shape"),
    ("Krita Shapes", "Minerva Shapes"),
    ("Krita Text", "Minerva Text"),
    ("Krita File", "Minerva File"),
    ("Krita Project", "Minerva Project"),
    ("Krita Document", "Minerva Document"),
    ("Krita Image", "Minerva Image"),
    ("Krita Picture", "Minerva Picture"),
    ("Krita Art", "Minerva Art"),
    ("Krita Artwork", "Minerva Artwork"),
    ("Krita Drawing", "Minerva Drawing"),
    ("Krita Painting", "Minerva Painting"),
    ("Krita Sketch", "Minerva Sketch"),
    ("Krita Design", "Minerva Design"),
    ("Krita UI", "Minerva UI"),
    ("Krita UX", "Minerva UX"),
    ("Krita API", "Minerva API"),
    ("Krita SDK", "Minerva SDK"),
    ("Krita CLI", "Minerva CLI"),
    ("Krita GUI", "Minerva GUI"),
    ("Krita's", "Minerva's"),

    # Single-word brand (most common)
    ("Krita", "Minerva"),

    # ── Module/package: krita → minerva2d (code, lowercase) ──
    # Longest code references first
    ("krita-preview", "minerva2d-preview"),
    ("krita-preview_helper", "minerva2d-preview_helper"),
    ("krita-thumbnailer", "minerva2d-thumbnailer"),
    ("krita-thumbnailer_helper", "minerva2d-thumbnailer_helper"),
    ("krita-mock", "minerva2d-mock"),
    ("krita_script_starter", "minerva2d_script_starter"),
    ("kritaversion", "minerva2dversion"),
    ("kritaversion.h", "minerva2dversion.h"),
    ("kritaversion.cpp", "minerva2dversion.cpp"),
    ("kritarc", "minerva2drc"),
    ("krita5.xmlgui", "minerva2d5.xmlgui"),
    ("krita6.exe.manifest", "minerva2d6.exe.manifest"),
    ("krita.exe.manifest", "minerva2d.exe.manifest"),
    ("krita.action", "minerva2d.action"),
    ("kritamenu.action", "minerva2dmenu.action"),
    ("krita.qrc", "minerva2d.qrc"),
    ("krita.desktop", "minerva2d.desktop"),
    ("krita.appdata", "minerva2d.appdata"),
    ("krita.appdata.xml", "minerva2d.appdata.xml"),
    ("krita.pics", "minerva2d.pics"),
    ("krita.data", "minerva2d.data"),
    ("krita.input", "minerva2d.input"),
    ("krita.profiles", "minerva2d.profiles"),
    ("krita.gradients", "minerva2d.gradients"),
    ("krita.brushes", "minerva2d.brushes"),
    ("krita.patterns", "minerva2d.patterns"),
    ("krita.textures", "minerva2d.textures"),
    ("krita.palettes", "minerva2d.palettes"),
    ("krita.bundles", "minerva2d.bundles"),
    ("krita.resources", "minerva2d.resources"),
    ("krita.shortcuts", "minerva2d.shortcuts"),
    ("krita.styles", "minerva2d.styles"),
    ("krita.themes", "minerva2d.themes"),
    ("krita.icons", "minerva2d.icons"),
    ("krita.splash", "minerva2d.splash"),
    ("krita.logo", "minerva2d.logo"),
    ("krita.icon", "minerva2d.icon"),
    ("krita_logo", "minerva2d_logo"),
    ("krita_icon", "minerva2d_icon"),
    ("krita_splash", "minerva2d_splash"),
    ("krita_logo_light", "minerva2d_logo_light"),
    ("krita_logo_dark", "minerva2d_logo_dark"),
    ("krita_logo_svg", "minerva2d_logo_svg"),
    ("krita_logo_png", "minerva2d_logo_png"),
    ("krita_logo_ico", "minerva2d_logo_ico"),
    ("krita_logo_icns", "minerva2d_logo_icns"),
    ("kritadefault.profile", "minerva2ddefault.profile"),
    ("krita25_lcms", "minerva2d25_lcms"),
    ("Krita_3_Default_Resources", "Minerva_3_Default_Resources"),
    ("Krita_4_Default_Resources", "Minerva_4_Default_Resources"),
    ("Krita_Artists_SeExpr", "Minerva_Artists_SeExpr"),
    ("BG-Krita2.ggr", "BG-Minerva2.ggr"),
    ("krita_script", "minerva2d_script"),
    ("krita_runner", "minerva2d_runner"),
    ("krita_docker", "minerva2d_docker"),
    ("krita_panel", "minerva2d_panel"),
    ("krita_tool", "minerva2d_tool"),
    ("krita_brush", "minerva2d_brush"),
    ("krita_engine", "minerva2d_engine"),
    ("krita_filter", "minerva2d_filter"),
    ("krita_layer", "minerva2d_layer"),
    ("krita_selection", "minerva2d_selection"),
    ("krita_transform", "minerva2d_transform"),
    ("krita_animation", "minerva2d_animation"),
    ("krita_frame", "minerva2d_frame"),
    ("krita_timeline", "minerva2d_timeline"),
    ("krita_onion", "minerva2d_onion"),
    ("krita_vector", "minerva2d_vector"),
    ("krita_shape", "minerva2d_shape"),
    ("krita_text", "minerva2d_text"),
    ("krita_file", "minerva2d_file"),
    ("krita_project", "minerva2d_project"),
    ("krita_document", "minerva2d_document"),
    ("krita_image", "minerva2d_image"),
    ("krita_picture", "minerva2d_picture"),
    ("krita_art", "minerva2d_art"),
    ("krita_artwork", "minerva2d_artwork"),
    ("krita_drawing", "minerva2d_drawing"),
    ("krita_painting", "minerva2d_painting"),
    ("krita_sketch", "minerva2d_sketch"),
    ("krita_design", "minerva2d_design"),
    ("krita_ui", "minerva2d_ui"),
    ("krita_ux", "minerva2d_ux"),
    ("krita_api", "minerva2d_api"),
    ("krita_sdk", "minerva2d_sdk"),
    ("krita_cli", "minerva2d_cli"),
    ("krita_gui", "minerva2d_gui"),
    ("krita_org", "minerva2d_org"),
    ("krita_dot_org", "minerva2d_dot_org"),
    ("krita_dot_io", "minerva2d_dot_io"),
    ("krita_1", "minerva2d_1"),
    ("krita_2", "minerva2d_2"),
    ("krita_5", "minerva2d_5"),
    ("krita_6", "minerva2d_6"),
    ("pykrita", "pyminerva2d"),
    ("PyKrita", "PyMinerva2d"),
    ("Pykrita", "Pyminerva2d"),
    ("kritarunner", "minerva2drunner"),
    ("KritaToNativePath", "MinervaToNativePath"),
    ("KritaAddBrokenUnitTest", "MinervaAddBrokenUnitTest"),
    ("KritaTestSuite", "MinervaTestSuite"),
    ("MacroKritaAddBenchmark", "MacroMinervaAddBenchmark"),

    # Short code references (after longer ones)
    ("krita.", "minerva2d."),
    ("krita_", "minerva2d_"),
    ("krita-", "minerva2d-"),
    ("krita/", "minerva2d/"),
    (".kra", ".m2d"),
    ("/krita", "/minerva2d"),
    ("krita\\", "minerva2d\\"),

    # ── Env/Config: KRITA → MINERVA2D (uppercase) ──
    ("KRITA_VERSION_STRING", "MINERVA2D_VERSION_STRING"),
    ("KRITA_STABLE_VERSION_MAJOR", "MINERVA2D_STABLE_VERSION_MAJOR"),
    ("KRITA_STABLE_VERSION_MINOR", "MINERVA2D_STABLE_VERSION_MINOR"),
    ("KRITA_VERSION_RELEASE", "MINERVA2D_VERSION_RELEASE"),
    ("KRITA_VERSION_REVISION", "MINERVA2D_VERSION_REVISION"),
    ("KRITA_MSI_VERSION_RELEASE_TRANSITIONAL", "MINERVA2D_MSI_VERSION_RELEASE_TRANSITIONAL"),
    ("KRITA_STABLE_BRANCH", "MINERVA2D_STABLE_BRANCH"),
    ("KRITA_ALPHA", "MINERVA2D_ALPHA"),
    ("KRITA_BETA", "MINERVA2D_BETA"),
    ("KRITA_RC", "MINERVA2D_RC"),
    ("KRITA_STABLE", "MINERVA2D_STABLE"),
    ("KRITA_VERSION", "MINERVA2D_VERSION"),
    ("KRITA_", "MINERVA2D_"),
    ("KRITA-", "MINERVA2D-"),
    ("KRITA.", "MINERVA2D."),
    ("/KRITA", "/MINERVA2D"),
    ("\\KRITA", "\\MINERVA2D"),

    # ── URL/Domain references ──
    ("krita.org", "minerva2d.org"),
    ("krita-artists.org", "minerva-artists.org"),
    ("invent.kde.org/graphics/krita", "github.com/dr-shabana/Minerva-2D"),
    ("bugs.kde.org", "github.com/dr-shabana/Minerva-2D/issues"),
    ("docs.krita.org", "docs.minerva2d.org"),
    ("api.kde.org/legacy/krita", "api.minerva2d.org"),
    ("cdn.kde.org/ci-builds/graphics/krita", "github.com/dr-shabana/Minerva-2D/releases"),
    ("liberapay.com/Krita", "github.com/sponsors/dr-shabana"),

    # ── File extension references ──
    (".kra", ".m2d"),

    # ── Windows-specific ──
    ("krita.exe", "minerva2d.exe"),
    ("krita.com", "minerva2d.com"),
    ("krita.lnk", "minerva2d.lnk"),

    # ── KDE framework references (keep as-is, they're dependencies) ──
    # Do NOT rename: KDE, KF6, KF5, Qt, Qt6, Qt5, etc.
    # These are third-party dependencies and should keep their names
]

# Files/directories to skip entirely
SKIP_FILES = {
    'rebrand_krita_to_minerva2d.py',  # this script
    '.gitmodules',
}

SKIP_DIR_NAMES = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.pytest_cache'}


def is_text_file(filepath):
    """Check if a file is a text file we should process."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in BINARY_EXTS:
        return False
    if ext in TEXT_EXTS:
        return True
    # Try to read as text
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except:
        return False


def process_file_content(filepath):
    """Process a single file's content, applying all replacements."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"  READ ERROR: {filepath}: {e}")
        return False

    original = content
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  WRITE ERROR: {filepath}: {e}")
            return False
    return False


def should_process_dir(dirname):
    """Check if a directory should be processed."""
    return dirname not in SKIP_DIR_NAMES and not dirname.startswith('.git')


def main():
    print("=" * 60)
    print("Krita → Minerva 2D Rebranding Script")
    print("=" * 60)
    print(f"Repo root: {REPO_ROOT}")
    print()

    files_processed = 0
    files_modified = 0
    errors = 0

    # Walk all files
    for root, dirs, files in os.walk(REPO_ROOT):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if should_process_dir(d)]

        for fname in files:
            if fname in SKIP_FILES:
                continue

            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, REPO_ROOT)

            if not is_text_file(filepath):
                continue

            files_processed += 1
            try:
                if process_file_content(filepath):
                    files_modified += 1
                    if files_modified <= 50 or files_modified % 100 == 0:
                        print(f"  Modified: {rel_path}")
            except Exception as e:
                errors += 1
                print(f"  ERROR: {rel_path}: {e}")

    print()
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Errors: {errors}")
    print()
    print("Content rebranding complete.")


if __name__ == '__main__':
    main()
