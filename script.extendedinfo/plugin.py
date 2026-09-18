# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# Modifications copyright (C) 2022 - Scott Smart <scott967@kodi.tv>
# This program is Free Software see LICENSE file for details
"""Module called by Runplugin() as executable in Kodi
"""

from resources.kutil131 import utils
from resources.lib.pluginmain import Main

if (__name__ == "__main__"):
    Main()
utils.log('finished')
