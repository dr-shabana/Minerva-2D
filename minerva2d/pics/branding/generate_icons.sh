#!/usr/bin/env bash
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

set -x

for dir in $(find ./ -maxdepth 1 -mindepth 1 -type d); do
  rm ${dir}/*.png ${dir}/*.ico

  for i in $(echo "16 22 32 48 64 128 256 512 1024"); do
    inkscape -z -e ${dir}/${i}-apps-minerva2d.png -w ${i} -h ${i} ${dir}/sc-apps-minerva2d.svgz
	#convert ${dir}/sc-apps-minerva2d.svgz -resize "${i}x" ${dir}/${i}-apps-minerva2d.png
  done

  convert ${dir}/sc-apps-minerva2d.svgz -alpha off -resize 256x256 \
           -define icon:auto-resize="256,128,96,64,48,32,16" \
           ${dir}/minerva2d.ico
done
