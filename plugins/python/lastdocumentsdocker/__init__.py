#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

import krita
from .lastdocumentsdocker import LastDocumentsDocker


Application.addDockWidgetFactory(
    minerva2d.DockWidgetFactory("lastdocumentsdocker",
                            minerva2d.DockWidgetFactoryBase.DockPosition.DockRight,
                            LastDocumentsDocker))
