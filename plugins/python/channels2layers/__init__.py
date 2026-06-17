#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from .channels2layers import ChannelsToLayers

# And add the extension to Minerva's list of extensions:
app = Minerva.instance()
# Instantiate your class:
extension = ChannelsToLayers(parent=app)
app.addExtension(extension)
