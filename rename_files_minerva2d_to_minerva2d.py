#!/usr/bin/env python3
"""
Krita → Minerva 2D: File and Directory Renaming Script
=======================================================
Renames files and directories that contain 'krita' in their names.
Must be run AFTER rebrand_krita_to_minerva2d.py (content rename).

Usage: python rename_files_krita_to_minerva2d.py
"""

import os
import shutil

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}

# Directory renames: old_name -> new_name (relative to repo root)
DIR_RENAMES = [
    ("krita", "minerva2d"),
    ("dev-tools/python/krita-mock", "dev-tools/python/minerva2d-mock"),
    ("dev-tools/python/krita-mock/src/krita", "dev-tools/python/minerva2d-mock/src/minerva2d"),
    ("krita/integration/krita-preview", "minerva2d/integration/minerva2d-preview"),
    ("krita/integration/krita-preview_helper", "minerva2d/integration/minerva2d-preview_helper"),
    ("krita/integration/krita-thumbnailer", "minerva2d/integration/minerva2d-thumbnailer"),
    ("krita/integration/krita-thumbnailer_helper", "minerva2d/integration/minerva2d-thumbnailer_helper"),
    ("krita/pics/branding/Beta/krita.icon", "minerva2d/pics/branding/Beta/minerva2d.icon"),
    ("krita/pics/branding/default/krita.icon", "minerva2d/pics/branding/default/minerva2d.icon"),
    ("krita/pics/branding/Next/krita.icon", "minerva2d/pics/branding/Next/minerva2d.icon"),
    ("krita/pics/branding/Plus/krita.icon", "minerva2d/pics/branding/Plus/minerva2d.icon"),
    ("packaging/android/apk/src/org/krita", "packaging/android/apk/src/org/minerva2d"),
    ("packaging/linux/appimage/krita-apprun", "packaging/linux/appimage/minerva2d-apprun"),
    ("plugins/extensions/pykrita", "plugins/extensions/pyminerva2d"),
    ("plugins/extensions/pykrita/kritarunner", "plugins/extensions/pyminerva2d/minerva2drunner"),
    ("plugins/extensions/pykrita/plugin/krita", "plugins/extensions/pyminerva2d/plugin/minerva2d"),
    ("plugins/extensions/pykrita/sip/krita", "plugins/extensions/pyminerva2d/sip/minerva2d"),
    ("plugins/python/krita_script_starter", "plugins/python/minerva2d_script_starter"),
]

# File renames: old_name -> new_name (relative to repo root)
FILE_RENAMES = [
    ("cmake/kde_macro/KritaToNativePath.cmake", "cmake/kde_macro/MinervaToNativePath.cmake"),
    ("cmake/modules/KritaAddBrokenUnitTest.cmake", "cmake/modules/MinervaAddBrokenUnitTest.cmake"),
    ("cmake/modules/KritaTestSuite.cmake", "cmake/modules/MinervaTestSuite.cmake"),
    ("cmake/modules/MacroKritaAddBenchmark.cmake", "cmake/modules/MacroMinervaAddBenchmark.cmake"),
    ("krita/krita.action", "minerva2d/minerva2d.action"),
    ("krita/krita.exe.manifest.in", "minerva2d/minerva2d.exe.manifest.in"),
    ("krita/krita.qrc", "minerva2d/minerva2d.qrc"),
    ("krita/krita5.xmlgui", "minerva2d/minerva2d5.xmlgui"),
    ("krita/krita6.exe.manifest.in", "minerva2d/minerva2d6.exe.manifest.in"),
    ("krita/kritamenu.action", "minerva2d/minerva2dmenu.action"),
    ("krita/kritaversion.cpp", "minerva2d/minerva2dversion.cpp"),
    ("krita/org.kde.krita.appdata.xml", "minerva2d/org.minerva.minerva2d.appdata.xml"),
    ("krita/org.kde.krita.desktop", "minerva2d/org.minerva.minerva2d.desktop"),
    ("krita/data/kritarc", "minerva2d/data/minerva2drc"),
]


def rename_dirs():
    """Rename directories."""
    print("Renaming directories...")
    for old_rel, new_rel in DIR_RENAMES:
        old_path = os.path.join(REPO_ROOT, old_rel)
        new_path = os.path.join(REPO_ROOT, new_rel)
        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
                print(f"  Dir: {old_rel} -> {new_rel}")
            except Exception as e:
                print(f"  DIR ERROR: {old_rel}: {e}")
        else:
            print(f"  SKIP (not found): {old_rel}")


def rename_files():
    """Rename files."""
    print("\nRenaming files...")
    for old_rel, new_rel in FILE_RENAMES:
        old_path = os.path.join(REPO_ROOT, old_rel)
        new_path = os.path.join(REPO_ROOT, new_rel)
        if os.path.exists(old_path):
            try:
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.rename(old_path, new_path)
                print(f"  File: {old_rel} -> {new_rel}")
            except Exception as e:
                print(f"  FILE ERROR: {old_rel}: {e}")
        else:
            print(f"  SKIP (not found): {old_rel}")


def walk_and_rename():
    """Walk the entire tree and rename any remaining files/dirs with 'krita' in name."""
    print("\nWalking tree for remaining 'krita' references in filenames...")

    renames = []
    for root, dirs, files in os.walk(REPO_ROOT, topdown=False):
        for f in files:
            if 'krita' in f.lower():
                old_path = os.path.join(root, f)
                new_name = f.replace('krita', 'minerva2d').replace('Krita', 'Minerva2d').replace('KRITA', 'MINERVA2D')
                new_path = os.path.join(root, new_name)
                renames.append((old_path, new_path, os.path.relpath(old_path, REPO_ROOT)))

    for old_path, new_path, rel_path in renames:
        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
                print(f"  File: {rel_path}")
            except Exception as e:
                print(f"  ERROR: {rel_path}: {e}")


def main():
    print("=" * 60)
    print("Krita → Minerva 2D: File/Directory Renaming")
    print("=" * 60)

    rename_dirs()
    rename_files()
    walk_and_rename()

    print("\nFile/directory renaming complete.")


if __name__ == '__main__':
    main()
