# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# Modifications copyright (C) 2022 - Scott Smart <scott967@kodi.tv>
# This program is Free Software see LICENSE file for details
"""Module called by Runscript() as executable in Kodi
"""

from __future__ import annotations

from resources.kutil131 import utils
from resources.lib.scriptmain import Main


if (__name__ == "__main__"):
    #utils.log(f'syspath is {sys.path}') #debug
    Main()
utils.log('finished')
