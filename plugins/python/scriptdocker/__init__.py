#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

import krita
from .scriptdocker import ScriptDocker

Application.addDockWidgetFactory(
    minerva2d.DockWidgetFactory("scriptdocker",
                            minerva2d.DockWidgetFactoryBase.DockRight,
                            ScriptDocker)
)
