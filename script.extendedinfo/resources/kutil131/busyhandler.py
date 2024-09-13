# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details
"""_summary_Creates a Busyhandler instance as busyhandler

Returns:
    Busyhandler: manage display of "busy" dialog
    Note that kutil131 __init__ imports busyhandler as "busy"
"""

import traceback
from functools import wraps

import xbmc
import xbmcgui

from resources.kutil131 import utils


class BusyHandler:
    """
    Class to deal with busydialog handling
    """
    def __init__(self, *args, **kwargs):
        """Initializes the handler with no dialog and enabled
        self.busy is the nember of active busy requests
        """
        self.busy = 0
        self.enabled = True

    def enable(self):
        """
        Enables busydialog handling
        """
        self.enabled = True

    def disable(self):
        """
        Disables busydialog handling
        """
        self.enabled = False

    def show_busy(self):
        """
        Increase busycounter and open busydialog if needed
        """
        if not self.enabled:
            return None
        if self.busy == 0:
            xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        self.busy += 1

    def set_progress(self, percent):
        """Not implemented

        Args:
            percent (int): 0-99 completion
        """
        pass

    def hide_busy(self):
        """
        Decrease busycounter and close busydialog if needed
        """
        if not self.enabled:
            return None
        self.busy = max(0, self.busy - 1)
        if self.busy == 0:
            #  utils.log('Closing busydialognoancel')
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

    def set_busy(self, func):
        """
        Decorator to show busy dialog while function is running
        """
        @wraps(func)
        def decorator(cls, *args, **kwargs):
            self.show_busy()
            result = None
            try:
                result = func(cls, *args, **kwargs)
            except Exception:
                utils.log(traceback.format_exc())
                utils.notify("Busy Error", "please contact add-on author")
            finally:
                self.hide_busy()
                return result

        return decorator


busyhandler = BusyHandler()
