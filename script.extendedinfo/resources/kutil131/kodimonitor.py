# Copyright (C) 2024 - Scott Smart <scott967@kodi.tv>
# This program is Free Software see LICENSE file for details
"""helper Xbmcmonitor class for xbmc.Monitor()
"""

import xbmc

from resources.kutil131 import utils


class Xbmcmonitor(xbmc.Monitor):
    """wraps xbmc.Monitor to handle onNotification events from Youtube """

    def __init__(self):
        super().__init__()
        self.ytplaystart = False
        self.ytplayfail = False
        #self.notify_ws = KodiWebSocket(port=9090)

    def onNotification(self, sender, method, data):
        utils.log(f'onNotification sender {sender} method {method} data {data}')
        if (sender == 'plugin.video.youtube') and (method == 'Other.playback_init'):
            utils.log('Youtube notify Xbmcmonitor video play init')
        elif (sender == 'plugin.video.youtube') and (method == 'Other.playback_started'):
            utils.log('Youtube notify Xbmcmonitor video play started')
            self.ytplaystart = True
        elif (sender == 'plugin.video.youtube') and (method == 'Other.playback_failed'):
            utils.log('Youtube notify Xbmcmonitor video play fail')
            self.ytplayfail = True
