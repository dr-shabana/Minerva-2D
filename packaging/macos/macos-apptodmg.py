#!/usr/bin/env python3

import pathlib
import os
import shutil
import subprocess
import argparse

# TODO: port all shutil move to Path.move after python 3.14

class DmgFile:
    def __init__(self, src_location: pathlib.Path, dst_path: [str|pathlib.Path],dst_name: str=None):
        self.src_path = src_location
        self.dst_path = pathlib.Path(dst_path)
        self.dst_name = src_location.name if not dst_name else dst_name

    def install(self, dmg_root: pathlib.Path):
        final_dst = dmg_root.joinpath(self.dst_path)
        if not final_dst.exists():
            final_dst.mkdir()

        shutil.copy2(self.src_path, final_dst.joinpath(self.dst_name))



def main():
    parser = argparse.ArgumentParser(prog='macos_apptodmg',
                                     description='Utility to generate a dmg from a minerva2d.app',
                                     epilog="This code does not sign the resulting dmg or bundle")
    parser.add_argument('minerva2d_app', metavar='minerva2d.app', help="minerva2d.app path location")
    parser.add_argument('--buildroot', help="Directory where krita src and _install are located",
                        default=os.getenv("BUILDROOT", False))
    parser.add_argument('--media-path', dest="media_path", metavar='<path>', help="path location of background, icons, and ToS")

    parser.add_argument('--style', help="Style defined from dmgstyle.sh's output",metavar='<file>')
    parser.add_argument('--bg', help="Set a background image for dmg window",metavar='<file>')
    parser.add_argument('-n','--dmg_name', help="Set DMG output dmg_name",metavar='<string>')
    parser.add_argument('--suffix', dest="suffix", help="Set DMG output name suffix", metavar='<string>')
    args = parser.parse_args()

    minerva2d_app = pathlib.Path(args.minerva2d_app).resolve()
    print(f'Creating dmg from: {minerva2d_app}')

    # --- Style options DMG
    if args.buildroot:
        print(f"root {args.buildroot}")
        if args.media_path:
            print("WARNING: --media-path ignored as --buildroot or env BUILDROOT is present")
        minerva2d_root: pathlib.Path = pathlib.Path(args.buildroot).resolve()
        minerva2d_source_dir = pathlib.Path(os.path.join(minerva2d_root, "krita"))
        minerva2d_media_path = minerva2d_source_dir.joinpath('packaging','macos')

    else:
        if not args.media_path:
            print("ERROR: if --builroot or env BUILDROOT is missing --media-path must be present")
            exit(1)
        minerva2d_media_path = pathlib.Path(args.media_path).resolve()


    minerva2d_dmg_background = minerva2d_media_path.joinpath('minerva2d_dmgBG.png') if not args.bg or not os.path.exists(args.bg) else pathlib.Path(args.bg)
    dmg_files: list[DmgFile] = [
        DmgFile(
            minerva2d_dmg_background
            , ".background"
        ),
        DmgFile(
            minerva2d_media_path.joinpath('Terms_of_use.rtf')
            , 'Terms of Use'
            , 'Terms_of_use.rtf'
        ),
        DmgFile(
            minerva2d_media_path.joinpath('MinervaIcon.icns')
            , "."
            , '.VolumeIcon.icns'
        )
    ]

    # preparing style to parsed string.
    minerva2d_dmg_style = minerva2d_media_path.joinpath('default.style') if not args.style or not os.path.exists(args.style) else pathlib.Path(args.style)
    # we still don't know the mounting point, so we pass through the first substitution
    kritadmg_style_formatted = minerva2d_dmg_style.read_text() % ("%s", minerva2d_dmg_background.name)


    # --- Minerva version adjustments
    kisenv = os.environ.copy()
    kisenv['PATH'] = f"{os.path.join(minerva2d_app,'Contents','MacOS')}:{kisenv['PATH']}"

    kis_version_full = subprocess.run(['minerva2d_version', '-v'],
                                      capture_output=True, text=True, env=kisenv).stdout
    kis_version = kis_version_full.replace("-", " ").split()
    # os.environ['KRITACI_RELEASE_PACKAGE_NAMING'] = "ON"
    if 'KRITACI_RELEASE_PACKAGE_NAMING' in os.environ:
        kis_version_str = kis_version[0]
    else:
        kis_version_str = "-".join(kis_version)

    kis_name = "minerva2d-" + kis_version_str
    if args.dmg_name:
        kis_name = args.dmg_name
    if args.suffix:
        kis_name += args.suffix

    minerva2d_dmg = kritaCreateDMG(minerva2d_app, dmg_files, kis_name, kritadmg_style_formatted)


    if args.buildroot:
        minerva2d_packaging = minerva2d_root.joinpath("_packaging")
    else:
        minerva2d_packaging = pathlib.Path("_packaging").resolve()

    minerva2d_packaging.mkdir(exist_ok=True)
    shutil.move(minerva2d_dmg, minerva2d_packaging)

    print(f'minerva2d.app to dmg finished!')
    print(f'output file {minerva2d_dmg} saved to {minerva2d_packaging}')



def kritaCreateDMG(minerva2d_app: pathlib.Path, minerva2d_dmg_media: list[DmgFile], dmg_name: str,
                   kritadmg_style: str
                   ) -> pathlib.Path:

    # Create dmg_root location must only contain minerva2d.app
    minerva2d_dmg_root = pathlib.Path('_dmg_wd').resolve()
    minerva2d_dmg_root.mkdir()

    # since qt6, codesign embbed Plugins/permissions/obj-Release/* special attributes for a valid signature
    # we use rsync to ensure a real clone with Extended attributes
    print(f'Cloning source minerva2d.app to working dir {minerva2d_dmg_root}')
    cmd = ['rsync', '-aE', minerva2d_app, minerva2d_dmg_root]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as err:
        print(f"## ERROR: Cloning minerva2d.app failed!\n{err.stderr}")
        exit(1);

    kritadmg_title = dmg_name + '.dmg'
    kritadmg_output = pathlib.Path(kritadmg_title).resolve()

    # hardcoded size to 2.0G
    dmg_size = 2000

    minerva2d_dmgtmp = pathlib.Path("minerva2d.temp.dmg")

    cmd = f'hdiutil create -srcfolder {minerva2d_dmg_root} -volname {dmg_name} \
            -fs APFS -format UDIF -verbose -size {dmg_size}m'.split()
    cmd.append(str(minerva2d_dmgtmp))
    print(f'## RUNNING: {cmd}')
    subprocess.run(cmd)

    kritadmg_mountpoint = pathlib.Path("_kritadmg")
    cmd = f"hdiutil attach -mountpoint {kritadmg_mountpoint}".split()
    cmd.append('-readwrite')
    cmd.append('-noverify')
    cmd.append('-noautoopen')
    cmd.append(f'{minerva2d_dmgtmp}')
    print(f'## RUNNING: {" ".join(cmd)}')
    subprocess.run(cmd)


    kritadmg_applink = pathlib.Path(kritadmg_mountpoint,'Applications')
    kritadmg_applink.symlink_to(pathlib.Path('/','Applications'))

    # copy media files for style to dmg
    for entry in minerva2d_dmg_media:
        entry.install(kritadmg_mountpoint)

    # set icon and style for dmg
    cmd = f'SetFile -a C {kritadmg_mountpoint}'.split()
    subprocess.run(cmd)
    print("## RUNNING: osascript")
    subprocess.run('osascript', input=kritadmg_style % kritadmg_mountpoint, text=True)

    cmd = f'chmod -Rf go-w {kritadmg_mountpoint}'.split()
    subprocess.run(cmd)

    # Make sure all writting operations to dmg are finished
    subprocess.run(['sync'])

    cmd = f'hdiutil detach {kritadmg_mountpoint}'.split()
    subprocess.run(cmd)

    cmd = f'hdiutil convert {minerva2d_dmgtmp} -format UDZO -imagekey -zlib-level=9 \
        -o {kritadmg_title}'.split()
    print(f'## RUNNING: {" ".join(cmd)}')
    subprocess.run(cmd)

    minerva2d_dmgtmp.unlink()

    return kritadmg_output



if __name__ == '__main__':
    main()
