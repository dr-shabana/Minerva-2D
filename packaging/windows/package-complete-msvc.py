#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 L. E. Segovia <amy@amyspark.me>
# SPDX-License-Identifier: GPL-2.0-or-later

# This Python script is meant to prepare a Minerva package folder to be zipped or
# to be a base for the installer.

import argparse
import glob
import itertools
import os
import re
import pathlib
import shutil
import subprocess
import sys
import warnings


# Subroutines

def choice(prompt="Is this ok?"):
    c = input(f"{prompt} [y/n] ")
    if c == "y":
        return True
    else:
        return False


def find_on_path(variable, executable):
    os.environ[variable] = shutil.which(executable)


def prompt_for_dir(prompt):
    user_input = input(f"{prompt} ")
    if not len(user_input):
        return None
    result = os.path.exists(user_input)
    if result is None:
        print("Input does not point to valid dir!")
        return prompt_for_dir(prompt)
    else:
        return os.path.realpath(user_input)


print("Minerva Windows packaging script (MSVC version)")


# command-line args parsing
parser = argparse.ArgumentParser()

basic_options = parser.add_argument_group("Basic options")
basic_options.add_argument("--no-interactive", action='store_true',
                           help="Run without interactive prompts. When not specified, the script will prompt for some of the parameters.")
basic_options.add_argument(
    "--package-name", action='store', help="Specify the package name", required=True)

path_options = parser.add_argument_group("Path options")
path_options.add_argument("--src-dir", action='store',
                          help="Specify Minerva source dir. If unspecified, this will be determined from the script location")
path_options.add_argument("--deps-install-dir", action='store',
                          help="Specify deps install dir")
path_options.add_argument("--minerva2d-install-dir", action='store',
                          help="Specify Minerva install dir")

special_options = parser.add_argument_group("Special options")
special_options.add_argument("--pre-zip-hook", action='store',
                             help="Specify a script to be called before packaging the zip archive, can be used to sign the binaries")

args = parser.parse_args()

# Check environment config

if os.environ.get("SEVENZIP_EXE") is None:
    find_on_path("SEVENZIP_EXE", "7z.exe")
if os.environ.get("SEVENZIP_EXE") is None:
    find_on_path("SEVENZIP_EXE", "7za.exe")
if os.environ.get("SEVENZIP_EXE") is None:
    os.environ["SEVENZIP_EXE"] = f"{os.environ['ProgramFiles']}\\7-Zip\\7-Z.exe"
    if not os.path.isfile(os.environ["SEVENZIP_EXE"]):
        os.environ["SEVENZIP_EXE"] = "{}\\7-Zip\\7-Z.exe".format(
            os.environ["ProgramFiles(x86)"])
    if not os.path.isfile(os.environ["SEVENZIP_EXE"]):
        warnings.warn("7-Zip not found!")
        exit(102)
print(f"7-Zip: {os.environ['SEVENZIP_EXE']}")

# Windows SDK is needed for windeployqt to get d3dcompiler_xx.dll
# If we don't define this variable, windeployqt will fetch the library
# from  %WINDIR%\system32, which is not supposed to be redistributable
if os.environ.get("WindowsSdkDir") is None and os.environ.get("ProgramFiles(x86)") is not None:
    os.environ["WindowsSdkDir"] = "{}\\Windows Kits\\10".format(
        os.environ["ProgramFiles(x86)"])

MINERVA2D_SRC_DIR = None

if args.src_dir is not None:
    MINERVA2D_SRC_DIR = args.src_dir

if MINERVA2D_SRC_DIR is None:
    _temp = sys.argv[0]
    if os.path.dirname(_temp).endswith("\\packaging\\windows"):
        _base = pathlib.PurePath(_temp)
        if os.path.isfile(f"{_base.parents[2]}\\CMakeLists.txt"):
            if os.path.isfile(f"{_base.parents[2]}\\libs\\version\\minerva2dversion.h.cmake"):
                MINERVA2D_SRC_DIR = os.path.realpath(_base.parents[2])
                print("Script is running inside Minerva source dir")

if MINERVA2D_SRC_DIR is None:
    if args.no_interactive:
        MINERVA2D_SRC_DIR = prompt_for_dir("Provide path of Minerva src dir")
    if MINERVA2D_SRC_DIR is None:
        warnings.warn("ERROR: Minerva src dir not found!")
        exit(102)
print(f"Minerva src: {MINERVA2D_SRC_DIR}")

DEPS_INSTALL_DIR = None

if args.deps_install_dir is not None:
    DEPS_INSTALL_DIR = args.deps_install_dir
if DEPS_INSTALL_DIR is None:
    DEPS_INSTALL_DIR = f"{os.getcwd()}\\i_deps"
    print(f"Using default deps install dir: {DEPS_INSTALL_DIR}")
    if not args.no_interactive:
        status = choice()
        if not status:
            DEPS_INSTALL_DIR = prompt_for_dir(
                "Provide path of deps install dir")
    if DEPS_INSTALL_DIR is None:
        warnings.warn("ERROR: Deps install dir not set!")
        exit(102)
print(f"Deps install dir: {DEPS_INSTALL_DIR}")

MINERVA2D_INSTALL_DIR = None

if args.minerva2d_install_dir is not None:
    MINERVA2D_INSTALL_DIR = args.minerva2d_install_dir
if MINERVA2D_INSTALL_DIR is None:
    MINERVA2D_INSTALL_DIR = f"{os.getcwd()}\\i"
    print(f"Using default Minerva install dir: {MINERVA2D_INSTALL_DIR}")
    if not args.no_interactive:
        status = choice()
        if not status:
            MINERVA2D_INSTALL_DIR = prompt_for_dir(
                "Provide path of Minerva install dir")
    if MINERVA2D_INSTALL_DIR is None:
        warnings.warn("ERROR: Minerva install dir not set!")
        exit(102)
print(f"Minerva install dir: {MINERVA2D_INSTALL_DIR}")

# Simple checking
if not os.path.isdir(DEPS_INSTALL_DIR):
    warnings.warn("ERROR: Cannot find the deps install folder!")
    exit(1)
if not os.path.isdir(MINERVA2D_INSTALL_DIR):
    warnings.warn("ERROR: Cannot find the krita install folder!")
    exit(1)
# Amyspark: paths with spaces are automagically handled by Python!

pkg_name = args.package_name
print(f"Package name is {pkg_name}")

pkg_root = f"{os.getcwd()}\\{pkg_name}"
print(f"Packaging dir is {pkg_root}\n")
if os.path.isdir(pkg_root):
    warnings.warn(
        "ERROR: Packaging dir already exists! Please remove or rename it first.")
    exit(1)
if os.path.isfile(f"{pkg_root}.zip"):
    warnings.warn(
        "ERROR: Packaging zip already exists! Please remove or rename it first.")
    exit(1)
if os.path.isfile(f"{pkg_root}-dbg.zip"):
    warnings.warn(
        "ERROR: Packaging debug zip already exists! Please remove or rename it first.")
    exit(1)

if not args.no_interactive:
    status = choice()
    if not status:
        exit(255)
    print("")

# Initialize PATH
os.environ["PATH"] = f"{DEPS_INSTALL_DIR}\\bin;{os.environ['PATH']}"

print("\nThis is the packaging script for MSVC.\n")

print("\nCreating base directories...")

try:
    os.makedirs(f"{pkg_root}", exist_ok=True)
    os.makedirs(f"{pkg_root}\\bin", exist_ok=True)
    os.makedirs(f"{pkg_root}\\etc", exist_ok=True)
    os.makedirs(f"{pkg_root}\\lib", exist_ok=True)
    os.makedirs(f"{pkg_root}\\share", exist_ok=True)
except:
    warnings.warn("ERROR: Cannot create packaging dir tree!")
    exit(1)

print("\nCopying files...")
# minerva2d.exe
shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2d.exe", f"{pkg_root}\\bin\\")
shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2d.com", f"{pkg_root}\\bin\\")
if os.path.isfile(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2d.pdb"):
    shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2d.pdb", f"{pkg_root}\\bin\\")
# minerva2drunner.exe
shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2drunner.exe", f"{pkg_root}\\bin\\")
if os.path.isfile(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2drunner.pdb"):
    shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2drunner.pdb",
                f"{pkg_root}\\bin\\")
shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\minerva2drunner_com.com",
            f"{pkg_root}\\bin\\")

if os.path.isfile(f"{MINERVA2D_INSTALL_DIR}\\bin\\FreehandStrokeBenchmark.exe"):
    shutil.copy(f"{MINERVA2D_INSTALL_DIR}\\bin\\FreehandStrokeBenchmark.exe", f"{pkg_root}\\bin\\")
    subprocess.run(["xcopy", "/S", "/Y", "/I",
                   f"{DEPS_INSTALL_DIR}\\bin\\data\\", f"{pkg_root}\\bin\\data\\"])

# DLLs from bin/
print("INFO: Copying all DLLs except Qt5 * from bin/")
files = glob.glob(f"{MINERVA2D_INSTALL_DIR}\\bin\\*.dll")
pdbs = glob.glob(f"{MINERVA2D_INSTALL_DIR}\\bin\\*.pdb")
for f in itertools.chain(files, pdbs):
    if not os.path.basename(f).startswith("Qt5"):
        shutil.copy(f, f"{pkg_root}\\bin")
files = glob.glob(f"{DEPS_INSTALL_DIR}\\bin\\*.dll")
for f in files:
    pdb = f"{os.path.dirname(f)}\\{os.path.splitext(os.path.basename(f))[0]}.pdb"
    if not os.path.basename(f).startswith("Qt5"):
        shutil.copy(f, f"{pkg_root}\\bin")
        if os.path.isfile(pdb):
            shutil.copy(pdb, f"{pkg_root}\\bin")
# symsrv.yes for Dr. Mingw
shutil.copy(f"{DEPS_INSTALL_DIR}\\bin\\symsrv.yes", f"{pkg_root}\\bin")
# KF5 plugins may be placed at different locations depending on how Qt is built
subprocess.run(["xcopy", "/S", "/Y", "/I",
               f"{DEPS_INSTALL_DIR}\\lib\\plugins\\imageformats\\", f"{pkg_root}\\bin\\imageformats\\"])
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\plugins\\imageformats\\".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\bin\\imageformats\\"])
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\plugins\\kf5\\".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\bin\\kf5\\"])

# Copy the sql drivers explicitly
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\plugins\\sqldrivers\\".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\bin\\sqldrivers"], check=True)

# Qt Translations
# it seems that windeployqt does these, but only * some * of these???
os.makedirs(f"{pkg_root}\\bin\\translations", exist_ok=True)
files = glob.glob(f"{DEPS_INSTALL_DIR}\\translations\\qt_*.qm")
for f in files:
    # Exclude qt_help_*.qm
    if not os.path.basename(f).startswith("qt_help"):
        shutil.copy(f, f"{pkg_root}\\bin\\translations")

# Minerva plugins
subprocess.run(["xcopy", "/Y", "{}\\lib\\kritaplugins\\*.dll".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\lib\\kritaplugins\\"], check=True)
subprocess.run(["xcopy", "/Y", "{}\\lib\\kritaplugins\\*.pdb".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\lib\\kritaplugins\\"], check=True)
if os.path.isdir(f"{DEPS_INSTALL_DIR}\\lib\\minerva2d-python-libs"):
    subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\lib\\minerva2d-python-libs".format(DEPS_INSTALL_DIR), f"{pkg_root}\\lib\\minerva2d-python-libs"], check=True)
if os.path.isdir(f"{MINERVA2D_INSTALL_DIR}\\lib\\minerva2d-python-libs"):
    subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\lib\\minerva2d-python-libs".format(
        MINERVA2D_INSTALL_DIR), f"{pkg_root}\\lib\\minerva2d-python-libs"], check=True)
if os.path.isdir(f"{DEPS_INSTALL_DIR}\\lib\\site-packages"):
    subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\lib\\site-packages".format(
        DEPS_INSTALL_DIR), f"{pkg_root}\\lib\\site-packages"], check=True)

# MLT plugins and their data
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\lib\\mlt".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\lib\\mlt"], check=True)
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\mlt".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\share\\mlt"], check=True)

# Fontconfig
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\etc\\fonts".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\etc\\fonts"], check=True)

# Share
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\color".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\share\\color"], check=True)
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\color-schemes".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\share\\color-schemes"], check=True)
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\icons".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\share\\icons"], check=True)
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\krita".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\share\\krita"])
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\kritaplugins".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\share\\kritaplugins"], check=True)
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\kf5".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\share\\kf5"], check=True)
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\mime".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\share\\mime"], check=True)
# Python libs are copied by share\krita above
# Copy locale to bin
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\locale".format(
    MINERVA2D_INSTALL_DIR), f"{pkg_root}\\bin\\locale"])
subprocess.run(["xcopy", "/S", "/Y", "/I", "{}\\share\\locale".format(
    DEPS_INSTALL_DIR), f"{pkg_root}\\bin\\locale"], check=True)

# Copy shortcut link from source (can't create it dynamically)
shutil.copy(f"{MINERVA2D_SRC_DIR}\\packaging\\windows\\minerva2d.lnk", pkg_root)
shutil.copy(
    f"{MINERVA2D_SRC_DIR}\\packaging\\windows\\minerva2d-minimal.lnk", pkg_root)
shutil.copy(
    f"{MINERVA2D_SRC_DIR}\\packaging\\windows\\minerva2d-animation.lnk", pkg_root)

QMLDIR_ARGS = ["--qmldir", f"{DEPS_INSTALL_DIR}\\qml"]
if os.path.isdir(f"{MINERVA2D_INSTALL_DIR}\\lib\\qml"):
    subprocess.run(["xcopy", "/S", "/Y", "/I",
                   f"{MINERVA2D_INSTALL_DIR}\\lib\\qml", f"{pkg_root}\\bin\\"], check=True)
    # This doesn't really seem to do anything
    QMLDIR_ARGS.extend(["--qmldir", f"{MINERVA2D_INSTALL_DIR}\\lib\\qml"])

# windeployqt
subprocess.run(["windeployqt.exe", *QMLDIR_ARGS, "--release", "-gui", "-core", "-concurrent", "-network", "-printsupport", "-svg",
               "-xml", "-sql", "-qml", "-quick", "-quickwidgets", f"{pkg_root}\\bin\\minerva2d.exe", f"{pkg_root}\\bin\\minerva2d.dll"], check=True)

# ffmpeg
if os.path.exists(f"{DEPS_INSTALL_DIR}\\bin\\ffmpeg.exe"):
    shutil.copy(f"{DEPS_INSTALL_DIR}\\bin\\ffmpeg.exe", f"{pkg_root}\\bin")
    shutil.copy(f"{DEPS_INSTALL_DIR}\\bin\\ffprobe.exe", f"{pkg_root}\\bin")
    shutil.copy(f"{DEPS_INSTALL_DIR}\\bin\\ffmpeg_LICENSE.txt",
                f"{pkg_root}\\bin")
    shutil.copy(f"{DEPS_INSTALL_DIR}\\bin\\ffmpeg_README.txt",
                f"{pkg_root}\\bin")

# Copy embedded Python
subprocess.run(["xcopy", "/S", "/Y", "/I",
               f"{DEPS_INSTALL_DIR}\\python", f"{pkg_root}\\python"], check=True)
if os.path.exists(f"{pkg_root}\\python\\python.exe"):
    os.remove(f"{pkg_root}\\python\\python.exe")
if os.path.exists(f"{pkg_root}\\python\\pythonw.exe"):
    os.remove(f"{pkg_root}\\python\\pythonw.exe")

# Remove Python cache files
for d in os.walk(pkg_root):
    pycache = f"{d[0]}\\__pycache__"
    if os.path.isdir(pycache):
        print(f"Deleting Python cache {pycache}")
        shutil.rmtree(pycache)

if os.path.exists(f"{pkg_root}\\lib\\site-packages"):
    print(f"Deleting unnecessary Python packages")
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\packaging*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\pip*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\ply*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\pyparsing*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\PyQt_builder*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\setuptools.pth"):
        os.remove(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\setuptools*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\sip*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\toml*"):
        shutil.rmtree(f)
    for f in glob.glob(f"{pkg_root}\\lib\\site-packages\\easy-install.pth"):
        os.remove(f)

if args.pre_zip_hook:
    print("Running pre-zip hook...")
    subprocess.run(["cmd", "/c", args.pre_zip_hook,
                   f"{pkg_root}\\"], check=True)

print("\nPackaging stripped binaries...")
subprocess.run([os.environ["SEVENZIP_EXE"], "a", "-tzip",
               f"{pkg_name}.zip", f"{pkg_root}\\", "-xr!**\*.pdb"], check=True)
print("--------\n")
print("Packaging debug info...")
# (note that the top-level package dir is not included)
subprocess.run([os.environ["SEVENZIP_EXE"], "a", "-tzip",
               f"{pkg_name}-dbg.zip", "-r", f"{pkg_root}\\**\\*.pdb"], check=True)
print("--------\n")

print("\n")
print(f"Minerva packaged as {pkg_name}.zip")
if os.path.isfile(f"{pkg_name}-dbg.zip"):
    print(f"Debug info packaged as {pkg_name}-dbg.zip")
print(f"Packaging dir is {pkg_root}")
print("NOTE: Do not create installer with packaging dir. Extract from")
print(f"      {pkg_name}.zip instead")
print("and do _not_ run krita inside the extracted directory because it will")
print("       create extra unnecessary files.\n")
print("Please remember to actually test the package before releasing it.\n")
