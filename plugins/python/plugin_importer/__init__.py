#
# SPDX-FileCopyrightText: 2019 Rebecca Breu <rebecca@rbreu.de>
#
# This file is part of Minerva.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import krita

from .plugin_importer_extension import PluginImporterExtension


minerva2d_instance = minerva2d.Minerva.instance()
minerva2d_instance.addExtension(PluginImporterExtension(minerva2d_instance))
