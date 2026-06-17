#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from krita import Minerva, DockWidgetFactory
from .selectionsbagdocker import SelectionsBagDocker

Minerva.instance().addDockWidgetFactory(
    DockWidgetFactory("SelectionsBagDocker",
                      DockWidgetFactory.DockPosition.DockRight,
                      SelectionsBagDocker))
