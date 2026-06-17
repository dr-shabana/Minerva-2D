#!/usr/bin/env python3
"""
Rebrand .po translation files: Krita → Minerva 2D
Updates Project-Id-Version, Language-Team URLs, and msgstr strings containing old brand names.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def find_po_files(root):
    po_files = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]
        for f in files:
            if f.endswith('.po'):
                po_files.append(os.path.join(dirpath, f))
    return po_files


def process_po_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except:
        return False

    original = content

    # Update Project-Id-Version
    content = re.sub(
        r'Project-Id-Version: Krita[^\n]*',
        'Project-Id-Version: Minerva 2D',
        content
    )
    content = re.sub(
        r'Project-Id-Version: krita VERSION',
        'Project-Id-Version: Minerva 2D',
        content
    )
    content = re.sub(
        r'Project-Id-Version: PACKAGE VERSION',
        'Project-Id-Version: Minerva 2D',
        content
    )

    # Update Language-Team URLs
    content = content.replace('translate.krita.org', 'translate.minerva2d.org')
    content = content.replace('bugs.kde.org', 'github.com/dr-shabana/Minerva-2D/issues')
    content = content.replace('invent.kde.org/graphics/krita', 'github.com/dr-shabana/Minerva-2D')

    # Update Report-Msgid-Bugs-To
    content = re.sub(
        r'Report-Msgid-Bugs-To:[^\n]*krita[^\n]*',
        'Report-Msgid-Bugs-To: https://github.com/dr-shabana/Minerva-2D/issues',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'Report-Msgid-Bugs-To: https://github\.com/dr-shabana/Minerva-2D/issues',
        'Report-Msgid-Bugs-To: https://github.com/dr-shabana/Minerva-2D/issues',
        content
    )

    # Update msgstr strings (not msgid)
    lines = content.split('\n')
    in_msgstr = False
    for i, line in enumerate(lines):
        if line.startswith('msgstr '):
            in_msgstr = True
            lines[i] = lines[i].replace('"Krita"', '"Minerva"')
            lines[i] = lines[i].replace('"krita"', '"minerva"')
        elif line.startswith('msgid '):
            in_msgstr = False
        elif in_msgstr and line.startswith('"') and line.endswith('"'):
            lines[i] = lines[i].replace('Krita', 'Minerva')
            lines[i] = lines[i].replace('krita', 'minerva')

    content = '\n'.join(lines)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    po_files = find_po_files(REPO_ROOT)
    print(f"Found {len(po_files)} .po files")

    modified = 0
    for fp in po_files:
        rel = os.path.relpath(fp, REPO_ROOT)
        if process_po_file(fp):
            modified += 1
            if modified <= 20:
                print(f"  Modified: {rel}")

    print(f"\nDone. {modified}/{len(po_files)} files modified.")


if __name__ == '__main__':
    main()
