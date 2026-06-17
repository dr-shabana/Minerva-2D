#! /bin/sh
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

source kundo2_aware_xgettext.sh

$EXTRACTRC `find . -name \*.ui | grep -v '/tests/'` >> rc.cpp
RCFILES=`find . -name \*.xmlgui                                               \
	| grep -v minerva2d/sketch/MinervaSketchWin.xmlgui                          \
	| grep -v minerva2d/gemini/MinervaGeminiWin.xmlgui
         `
$EXTRACTRC $RCFILES >> rc.cpp

ACTIONFILES=`find . -name \*.action | grep -v '/tests/'`
./action_i18n.pl --context=action $ACTIONFILES >> rc.cpp

# extracti18n.pl extracts additional data from brushes, palettes etc.
perl extracti18n.pl >> rc.cpp

# Ignore sdk/templates which contains templates for writing future plugins.
# Also ignore crashreporter, it has it's own catalog
# None of the placeholder strings inside will be seen by users.
kundo2_aware_xgettext minerva2d.pot rc.cpp \
                  `find . -name \*.cc -o -name \*.h  -o -name \*.cpp -o -name \*.qml | \
                  grep -v '/tests/' | grep -v './sdk/templates' | grep -v './minerva2d/crashreporter/'`

# Extract the messages in Python plugins.
$XGETTEXT -L Python `find . -name \*.py` -j -o $podir/minerva2d.pot

# Clean up
rm -f rc.cpp
