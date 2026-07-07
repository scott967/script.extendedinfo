# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details
"""Provides a VideoPlayer class to wrap xbmc.Player
"""

import xbmc
from resources.kutil131 import busy, utils
from resources.kutil131.kodimonitor import Xbmcmonitor


class VideoPlayer(xbmc.Player):
    """Helper class for xbmc.Player

    Args:
        xbmc.Player: Player class provides callbacks for status
        of player
    """

    def __init__(self, *args, **kwargs):
        """Constructor to initialize VideoPlayer instance state vars
        """
        super().__init__()
        self.stopped = False
        self.started = False

    def onPlayBackEnded(self): #Kodi Player callback
        self.stopped = True
        self.started = False

    def onPlayBackStopped(self): #Kodi Player callback
        self.stopped = True
        self.started = False

    def onPlayBackError(self): #Kodi Player callback
        self.stopped = True
        self.started = False

    def onAVStarted(self): #Kodi Player callback
        self.started = True
        self.stopped = False
        utils.log(f'kutil131.player.Videoplayer.onAVStarted {self.started} stopped {self.stopped}', adb=True) #debug

    def onPlayBackStarted(self): #Kodi Player callback
        self.started = True
        self.stopped = False
        utils.log(f'kutil131.player.Videoplayer.onPlayBackStarted callback {self.started} stopped {self.stopped}', adb=True) #debug

    @busy.set_busy
    def youtube_info_by_id(self, youtube_id) -> None:
        """function uses inop YTStreamextractor

        Args:
            youtube_id(str): youtube video id

        Returns:
            None : method retained for future use
        """
        #vid = utils.get_youtube_info(youtube_id)
        vid = {}
        if not vid:
            return None, None
        #listitem = xbmcgui.ListItem(label=vid.title)
        #listitem.setArt({'thumb': vid.thumbnail})
        #listitem.setInfo(type='video',
        #                 infoLabels={"genre": vid.sourceName,
        #                             "plot": vid.description})
        #return vid.streamURL(), listitem

    def wait_for_video_end(self):
        """Monitor loop that waits for playing video to stop
        kodi xbmc.Player callback sets self.stopped
        """
        if not self.stopped:
            monitor: Xbmcmonitor = Xbmcmonitor()
            while not monitor.waitForAbort(1.0):
                if monitor.abortRequested():
                    break
                if self.stopped:
                    break
            del monitor
        self.stopped = False

    def wait_for_video_start(self):
        """Monitor that waits for plugin.video.youtube to send a
        Notifyall JSON callback to signal start of playback or
        failure to play eg, no streams found, etc
        """
        _monitor: Xbmcmonitor = Xbmcmonitor()
        timeout = 45
        while not _monitor.waitForAbort(1.0):  #wait to see if video starts
            if _monitor.abortRequested():
                break
            if _monitor.ytplaystart:
                utils.log('kutil.player.wait_for_video_start av started', adb=True) #debug
                self.started = True
                break
            if _monitor.ytplayfail or (timeout == 0):
                utils.log('kutil.player.wait_for_video_start yt fail', adb=True) #debug
                self.stopped = True
                break
            utils.log('kutil.player.wait_for_video_start no timeout or Notifyall so sleep', adb=True)
            timeout += -1
        del _monitor

    def wait_for_kodivideo_start(self):
        """Timer called from dialogmovieinfo that checks if Kodi can play selected listitem
        Sets a 20 sec timer to attempt play local db media.  If
        timer ends videoplayer self.stopped is set
        """
        utils.log('kutil131.player.Videoplayer.wait_for_kodivideo_start start timer', adb=True)  #debug
        monitor = xbmc.Monitor()
        timeout = 20
        while not monitor.waitForAbort(1):  #wait to see if video starts
            if monitor.abortRequested():
                break
            timeout += -1
            if self.started:
                utils.log('kutil131.player.VideoPlayer av started exit wait_for_kodivideo_start', adb=True) #debug
                break
            if timeout == 0:
                self.stopped = True
                utils.log(f'kutil131.player.VideoPlayer.wait_for_kodivideo_start exit start timeout self.stopped {self.stopped}', adb=True) #debug
                break
