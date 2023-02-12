# -*- coding: utf-8 -*-

# Copyright (C)  2023 - Scott Smart <scott967@kodi.tv>
# This program is Free Software see LICENSE file for details

"""Kodi context menu for script.extendedinfo
Available when in Video actor or director node
Select will load extendedactorinfo dialog
"""

import xbmc

def main():
    """Executes script.extendedinfo when called with runscript
    """
    if (xbmc.getCondVisibility('String.IsEqual(ListItem.DBType,actor)') or
    xbmc.getCondVisibility('String.IsEqual(ListItem.DBType,director)')):
        xbmc.executebuiltin(f'RunScript(script.extendedinfo,info=extendedactorinfo,name={xbmc.getInfoLabel("ListItem.Label")})')

if __name__ == '__main__':
    main()
