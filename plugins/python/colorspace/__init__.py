#
# SPDX-License-Identifier: CC0-1.0
#

import krita
from .colorspace import ColorSpaceExtension

Scripter.addExtension(ColorSpaceExtension(minerva2d.Minerva.instance()))
