# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# Modifications copyright (C) 2022 - Scott Smart <scott967@kodi.tv>
# This program is Free Software see LICENSE file for details

import traceback

import xbmc
import xbmcgui
from resources.kutil131 import (ActionHandler, addon, kodijson, selectdialog, slideshow,
                    windows)

from resources.kutil131 import VideoItem, utils, youtube
from resources.lib import themoviedb as tmdb
from resources.lib.windowmanager import wm

ch = ActionHandler()

ID_LIST_YOUTUBE = 350
ID_LIST_IMAGES = 1250
ID_BUTTON_BOUNCEUP = 20000
ID_BUTTON_BOUNCEDOWN = 20001

ACTION_LIST = ['ACTION_NONE = 0',
'ACTION_MOVE_LEFT = 1',
'ACTION_MOVE_RIGHT = 2',
'ACTION_MOVE_UP = 3',
'ACTION_MOVE_DOWN = 4',
'ACTION_PAGE_UP = 5',
'ACTION_PAGE_DOWN = 6',
'ACTION_SELECT_ITEM = 7',
'ACTION_HIGHLIGHT_ITEM = 8',
'ACTION_PARENT_DIR = 9',
'ACTION_PREVIOUS_MENU = 10',
'ACTION_SHOW_INFO = 11',
'ACTION_PAUSE = 12',
'ACTION_STOP = 13',
'ACTION_NEXT_ITEM = 14',
'ACTION_PREV_ITEM = 15',
'ACTION_FORWARD = 16',
'ACTION_REWIND = 17',
'ACTION_SHOW_GUI = 18',
'ACTION_ASPECT_RATIO = 19',
'ACTION_STEP_FORWARD = 20',
'ACTION_STEP_BACK = 21',
'ACTION_BIG_STEP_FORWARD = 22',
'ACTION_BIG_STEP_BACK = 23',
'ACTION_SHOW_OSD = 24',
'ACTION_SHOW_SUBTITLES = 25',
'ACTION_NEXT_SUBTITLE = 26',
'ACTION_PLAYER_DEBUG = 27',
'ACTION_NEXT_PICTURE = 28',
'ACTION_PREV_PICTURE = 29',
'ACTION_ZOOM_OUT = 30',
'ACTION_ZOOM_IN = 31',
'ACTION_TOGGLE_SOURCE_DEST = 32',
'ACTION_SHOW_PLAYLIST = 33',
'ACTION_QUEUE_ITEM = 34',
'ACTION_REMOVE_ITEM = 35',
'ACTION_SHOW_FULLSCREEN = 36',
'ACTION_ZOOM_LEVEL_NORMAL = 37',
'ACTION_ZOOM_LEVEL_1 = 38',
'ACTION_ZOOM_LEVEL_2 = 39',
'ACTION_ZOOM_LEVEL_3 = 40',
'ACTION_ZOOM_LEVEL_4 = 41',
'ACTION_ZOOM_LEVEL_5 = 42',
'ACTION_ZOOM_LEVEL_6 = 43',
'ACTION_ZOOM_LEVEL_7 = 44',
'ACTION_ZOOM_LEVEL_8 = 45',
'ACTION_ZOOM_LEVEL_9 = 46',
'ACTION_CALIBRATE_SWAP_ARROWS = 47',
'ACTION_CALIBRATE_RESET = 48',
'ACTION_ANALOG_MOVE = 49',
'ACTION_ROTATE_PICTURE_CW = 50',
'ACTION_ROTATE_PICTURE_CCW = 51',
'ACTION_SUBTITLE_DELAY_MIN = 52',
'ACTION_SUBTITLE_DELAY_PLUS = 53',
'ACTION_AUDIO_DELAY_MIN = 54',
'ACTION_AUDIO_DELAY_PLUS = 55',
'ACTION_AUDIO_NEXT_LANGUAGE = 56',
'ACTION_CHANGE_RESOLUTION = 57',
'none58',
'none59',
'none60',
'none61',
'none62',
'none63',
'none64',
'none65',
'none66',
'none67',
'none68',
'ACTION_PLAYER_PROCESS_INFO = 69',
'ACTION_PLAYER_PROGRAM_SELECT = 70',
'ACTION_PLAYER_RESOLUTION_SELECT = 71',
'none72',
'none73',
'none74',
'none75',
'ACTION_SMALL_STEP_BACK = 76',
'ACTION_PLAYER_FORWARD = 77',
'ACTION_PLAYER_REWIND = 78',
'ACTION_PLAYER_PLAY = 79',
'ACTION_DELETE_ITEM = 80',
'ACTION_COPY_ITEM = 81',
'ACTION_MOVE_ITEM = 82',
'none83',
'none84',
'ACTION_TAKE_SCREENSHOT = 85',
'none86',
'ACTION_RENAME_ITEM = 87',
'ACTION_VOLUME_UP = 88',
'ACTION_VOLUME_DOWN = 89',
'ACTION_VOLAMP = 90',
'ACTION_MUTE = 91',
'ACTION_NAV_BACK = 92',
'ACTION_VOLAMP_UP = 93',
'ACTION_VOLAMP_DOWN = 94',
'ACTION_CREATE_EPISODE_BOOKMARK = 95',
'ACTION_CREATE_BOOKMARK = 96',
'ACTION_CHAPTER_OR_BIG_STEP_FORWARD = 97',
'ACTION_CHAPTER_OR_BIG_STEP_BACK = 98',
'ACTION_CYCLE_SUBTITLE = 99',
'ACTION_MOUSE_LEFT_CLICK = 100',
'ACTION_MOUSE_RIGHT_CLICK = 101',
'ACTION_MOUSE_MIDDLE_CLICK = 102',
'ACTION_MOUSE_DOUBLE_CLICK = 103',
'ACTION_MOUSE_WHEEL_UP = 104',
'ACTION_MOUSE_WHEEL_DOWN = 105',
'ACTION_MOUSE_DRAG = 106',
'ACTION_MOUSE_MOVE = 107',
'ACTION_MOUSE_LONG_CLICK = 108',
'ACTION_MOUSE_END = 109',
'ACTION_BACKSPACE = 110',
'ACTION_SCROLL_UP = 111',
'ACTION_SCROLL_DOWN = 112',
'ACTION_ANALOG_FORWARD = 113',
'ACTION_ANALOG_REWIND = 114',
'ACTION_MOVE_ITEM_UP = 115',
'ACTION_MOVE_ITEM_DOWN = 116',
'ACTION_CONTEXT_MENU = 117',
'ACTION_SHIFT = 118',
'ACTION_SYMBOLS = 119',
'ACTION_CURSOR_LEFT = 120',
'ACTION_CURSOR_RIGHT = 121',
'ACTION_BUILT_IN_FUNCTION = 122',
'ACTION_SHOW_OSD_TIME = 123',
'ACTION_ANALOG_SEEK_FORWARD = 124',
'ACTION_ANALOG_SEEK_BACK = 125',
'ACTION_VIS_PRESET_SHOW = 126',
'none127',
'ACTION_VIS_PRESET_NEXT = 128',
'ACTION_VIS_PRESET_PREV = 129',
'ACTION_VIS_PRESET_LOCK = 130',
'ACTION_VIS_PRESET_RANDOM = 131',
'ACTION_VIS_RATE_PRESET_PLUS = 132',
'ACTION_VIS_RATE_PRESET_MINUS = 133',
'ACTION_SHOW_VIDEOMENU = 134',
'ACTION_ENTER = 135',
'ACTION_INCREASE_RATING = 136',
'ACTION_DECREASE_RATING = 137',
'ACTION_NEXT_SCENE = 138',
'ACTION_PREV_SCENE = 139',
'ACTION_NEXT_LETTER = 140',
'ACTION_PREV_LETTER = 141',
'ACTION_JUMP_SMS2 = 142',
'ACTION_JUMP_SMS3 = 143',
'ACTION_JUMP_SMS4 = 144',
'ACTION_JUMP_SMS5 = 145',
'ACTION_JUMP_SMS6 = 146',
'ACTION_JUMP_SMS7 = 147',
'ACTION_JUMP_SMS8 = 148',
'ACTION_JUMP_SMS9 = 149',
'ACTION_FILTER_CLEAR = 150',
'ACTION_FILTER_SMS2 = 151',
'ACTION_FILTER_SMS3 = 152',
'ACTION_FILTER_SMS4 = 153',
'ACTION_FILTER_SMS5 = 154',
'ACTION_FILTER_SMS6 = 155',
'ACTION_FILTER_SMS7 = 156',
'ACTION_FILTER_SMS8 = 157',
'ACTION_FILTER_SMS9 = 158',
'ACTION_FIRST_PAGE = 159',
'ACTION_LAST_PAGE = 160',
'ACTION_AUDIO_DELAY = 161',
'ACTION_SUBTITLE_DELAY = 162',
'ACTION_MENU = 163',
'ACTION_SET_RATING = 164',
'ACTION_PREV_SUBTITLE = 165',
'none166',
'none167',
'none168',
'none169',
'ACTION_RECORD = 170',
]

XML_ITEM_DICT = {20000: "Bnone",
20001: "Bnone",
4000: "grouplist",
140: "group",
132: "Bnone",
800: "Tagline plot",
50000: "group",
5000: "Grouplist",
8: "RB Play",
120: "RB Open",
99: "group",
9: "B percent played",
30000: "group",
6001: "RB Your rating",
6003: "RB FavButton_Label",
6005: "RB Add to list",
6002: "RB Show lists",
6006: "RB Already rated",
100: "RB Extras",
445: "RB Manage",
11000: "grouuplist lang flags",
12000: "grouplist sub flags",
50111: "group",
1000: "panel actors",
54111:  "group",
750:  "panel crew",
50112: "group",
150: "panel similar",
50113: "group",
250:  "panel sets",
1150:  "panel unk",
350: "panel youtube video",
550:  "panel studios",
1450:  "panel unk",
650:  "panel certs",
850:  "panel genres",
1050:  "panel reviews",
950:  "panel keywords",
1250:  "panel images",
1350:  "panel backdrops",
50215:  "group related movie lists",
450:  "panel lists",
2000:  "panel unk",
33000:  "group unk"}

class DialogBaseInfo(windows.DialogXML):
    """Class constructs a basic dialog xml window.   Subclasses augment for different
    dialog types (eg actor info or movie info)

    Args:
        windows.DialogXML (DialogXML): a kutil131 class derived from xbmcgui.WindowXMLDialog
        and kutil131 WindowMixin classes

    Returns:
        DialogBaseInfo: class instance
    """
    ACTION_PREVIOUS_MENU = [92, 9]
    ACTION_EXIT_SCRIPT = [13, 10]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #utils.log('DialogBaseInfo check login status')
        self.logged_in: bool = tmdb.tmdb_login.check_login()
        #utils.log(f'DialogBaseInfo tmdb logged in? {self.logged_in}')
        self.bouncing = False
        self.last_focus = None
        self.lists = None
        self.states = False
        self.yt_listitems = []
        self.info = VideoItem() # kutil131 listitem
        self.last_control = None
        self.last_position = None

    def onInit(self, *args, **kwargs):
        utils.log('onInit callback to DialogBaseInfo')
        super().onInit()
        # self.set_buttons()
        self.info.to_windowprops(window_id=self.window_id)  #kutil131 sets dialog window
        #properties from the info VideoItem(listitem)
        for container_id, key in self.LISTS:
            try:
                self.getControl(container_id).reset()
                items = [i.get_listitem() for i in self.lists[key]] # lists is a dict of ItemList get_listitem gets xbmc listitem from VideoItem
                self.getControl(container_id).addItems(items)
            except (IndexError, KeyError) as err:
                utils.log(f'Notice: No container with id {container_id} key {key} available due to {err}')
            except Exception as err:
                utils.log(f'Notice: No container with id {container_id} key {key} available due to {err}')
                utils.log(f'traceback for this exception\n{traceback.format_exc()}')
        if self.last_control:
            self.setFocusId(self.last_control)
        if self.last_control and self.last_position:
            try:
                self.getControl(self.last_control).selectItem(
                    self.last_position)
            except Exception:
                pass
        addon.set_global("ImageColor", self.info.get_property('ImageColor'))
        addon.set_global("ImageFilter", self.info.get_property('ImageFilter'))
        addon.set_global("infobackground", self.info.get_art('fanart_small'))
        self.setProperty("type", self.TYPE)
        self.setProperty("tmdb_logged_in", "true" if self.logged_in else "")
        utils.log('DialogBaseInfo onInit done')

    def onAction(self, action):
        utils.log(f'DialogBaseInfo got onAction for {ACTION_LIST[action.getId()]} from {self.getFocusId()} {XML_ITEM_DICT.get(self.getFocusId(), "unknown")}')
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id: int):
        super().onClick(control_id)
        ch.serve(control_id, self)

    def onFocus(self, control_id):
        if control_id == ID_BUTTON_BOUNCEUP:
            if not self.bouncing:
                self.bounce("up")
            self.setFocusId(self.last_focus)
        elif control_id == ID_BUTTON_BOUNCEDOWN:
            if not self.bouncing:
                self.bounce("down")
            self.setFocusId(self.last_focus)
        self.last_focus = control_id

    def close(self):
        utils.log('DialogBaseInfo.close')
        try:
            self.last_position = self.getFocus().getSelectedPosition()
        except Exception:
            self.last_position = None
        addon.set_global("infobackground", "")
        self.last_control = self.getFocusId()
        utils.log('dialogbaseinfo.DialogBaseInfo call DialogXML.close()')  #debug
        super().close()
        utils.log('dialogbaseinfo.close returned ')  #debug

    @utils.run_async
    def bounce(self, identifier):
        self.bouncing = True
        self.setProperty("Bounce.%s" % identifier, "true")
        xbmc.sleep(200)
        self.clearProperty("Bounce.%s" % identifier)
        self.bouncing = False

    #@ch.click_by_type("music") not working
    @ch.click_by_type("song")
    # hack: use "song" was "music" until "pictures" got added to core
    def open_image(self, control_id):
        key = [key for container_id,
               key in self.LISTS if container_id == control_id][0]
        pos = slideshow.open(listitems=self.lists[key],
                             index=self.getControl(control_id).getSelectedPosition())
        self.getControl(control_id).selectItem(pos)

    @ch.click_by_type("video")
    def play_youtube_video(self, control_id):
        utils.log('DialogBaseInfo.click_by_type(video) call wm.play_youtube_video')
        wm.play_youtube_video(youtube_id=self.FocusedItem(control_id).getProperty("youtube_id"),
                              listitem=self.FocusedItem(control_id))

    @ch.click_by_type("artist")
    def open_actor_info(self, control_id):
        wm.open_actor_info(actor_id=self.FocusedItem(control_id).getProperty("id"),
                            name=self.FocusedItem(control_id).getLabel())

    @ch.click_by_type("movie")
    def open_movie_info(self, control_id):
        wm.open_movie_info(movie_id=self.FocusedItem(control_id).getProperty("id"),
                           dbid=self.FocusedItem(control_id).getVideoInfoTag().getDbId())

    @ch.click_by_type("tvshow")
    def open_tvshow_info(self, control_id):
        wm.open_tvshow_info(tmdb_id=self.FocusedItem(control_id).getProperty("id"),
                            dbid=self.FocusedItem(control_id).getVideoInfoTag().getDbId())

    @ch.click_by_type("episode")
    def open_episode_info(self, control_id):
        info = self.FocusedItem(control_id).getVideoInfoTag()
        wm.open_episode_info(tvshow=self.info.get_info("tvshowtitle"),
                             tvshow_id=self.tvshow_id,
                             season=info.getSeason(),
                             episode=info.getEpisode())

    #@ch.context("music")  not working testing "song" as hack
    @ch.context("song")
    def thumbnail_options(self, control_id:int) -> None:
        """sets a Kodi library item poster or fanart from tmdb art

        Args:
            control_id (int): the dialog window control id that has focus (image)

        Returns:
            None
        """
        #utils.log(f'DialogBaseInfo thumbnail_options called for contextmenu song with control id {control_id}')
        listitem:xbmcgui.ListItem = self.FocusedItem(control_id)
        art_type = listitem.getProperty("type")
        options = []
        if self.info.get_info("dbid") and art_type == "poster":
            options.append(("db_art", addon.LANG(32006)))
        if self.info.get_info("dbid") and art_type == "fanart":
            options.append(("db_art", addon.LANG(32007)))
        movie_id = listitem.getProperty("movie_id")
        #utils.log(f'DialogBaseInfo.thumbnail_options options are : {options} and movie_id {movie_id if movie_id else "None"}')
        if movie_id:
            options.append(("movie_info", addon.LANG(10524)))
        if not options:
            return None
        action = utils.contextmenu(options=options)
        if action == "db_art":
            #utils.log('DialogBaseInfo.thumbnail_options setting db_art on item')
            art_result = kodijson.set_art(media_type=self.getProperty("type"),
                             art={art_type: listitem.getArt("original")},
                             dbid=self.info.get_info("dbid"))
            #utils.log(f'DialogBaseInfo.thumbnail_options seting json results {art_result}')
            if art_result and art_result.get('result') == 'OK':
                utils.notify(addon.NAME, f'{addon.LANG(32119)} / {xbmc.getLocalizedString(24138)}')
        elif action == "movie_info":
            wm.open_movie_info(movie_id=listitem.getProperty("movie_id"),
                               dbid=listitem.getVideoInfoTag().getDbId())

    @ch.context("video")
    def video_context_menu(self, control_id):
        index = xbmcgui.Dialog().contextmenu(list=[addon.LANG(33003)])
        if index == 0:
            #utils.download_video(self.FocusedItem(
            #    control_id).getProperty("youtube_id"))
            pass
        utils.notify(addon.NAME, xbmc.getLocalizedString(10005))

    @ch.context("movie")
    def movie_context_menu(self, control_id):
        movie_id = self.FocusedItem(control_id).getProperty("id")
        dbid = self.FocusedItem(control_id).getVideoInfoTag().getDbId()
        options = [addon.LANG(32113)]
        if self.logged_in:
            options.append(addon.LANG(32083))
        index = xbmcgui.Dialog().contextmenu(list=options)
        if index == 0:
            rating = utils.input_userrating()
            if rating == -1:
                return None
            tmdb.set_rating(media_type="movie",
                            media_id=movie_id,
                            rating=rating,
                            dbid=dbid)
            xbmc.sleep(2000)
            tmdb.get_movie(movie_id=movie_id,
                           cache_days=0)
        elif index == 1:
            account_lists = tmdb.get_account_lists()
            if not account_lists:
                return False
            listitems = ["%s (%i)" % (i["name"], i["item_count"])
                         for i in account_lists]
            i = xbmcgui.Dialog().select(addon.LANG(32136), listitems)
            if i > -1:
                tmdb.change_list_status(list_id=account_lists[i]["id"],
                                        movie_id=movie_id,
                                        status=True)

    @ch.context("artist")
    def person_context_menu(self, control_id):
        listitem = self.FocusedItem(control_id)
        options = [addon.LANG(32009), addon.LANG(32070)]
        credit_id = listitem.getProperty("credit_id")
        if credit_id and self.TYPE == "TVShow":
            options.append(addon.LANG(32147))
        index = xbmcgui.Dialog().contextmenu(list=options)
        if index == 0:
            wm.open_actor_info(actor_id=listitem.getProperty("id"))
        if index == 1:
            filters = [{"id": listitem.getProperty("id"),
                        "type": "with_people",
                        "label": listitem.getLabel()}]
            wm.open_video_list(filters=filters)
        if index == 2:
            self.open_credit_dialog(credit_id)

    @ch.context("tvshow")
    def tvshow_context_menu(self, control_id):
        tvshow_id = self.FocusedItem(control_id).getProperty("id")
        dbid = self.FocusedItem(control_id).getVideoInfoTag().getDbId()
        credit_id = self.FocusedItem(control_id).getProperty("credit_id")
        options = [addon.LANG(32169)]
        if credit_id:
            options.append(addon.LANG(32147))
        index = xbmcgui.Dialog().contextmenu(list=options)
        if index == 0:
            rating = utils.input_userrating()
            if rating == -1:
                return None
            tmdb.set_rating(media_type="tvshow",
                            media_id=tvshow_id,
                            rating=rating,
                            dbid=dbid)
            xbmc.sleep(2000)
            tmdb.get_tvshow(tvshow_id=tvshow_id,
                            cache_days=0)
        if index == 1:
            self.open_credit_dialog(credit_id=credit_id)

    @ch.action("parentdir", "*")
    @ch.action("parentfolder", "*")
    def previous_menu(self, control_id):
        onback = self.getProperty("%i_onback" % control_id)
        utils.log(f'DialogBaseInfo.previous_menu onback {onback} control_id {control_id}')
        if onback:
            xbmc.executebuiltin(onback)
        else:
            utils.log('DialogBaseInfo.previous_menu close dialog')
            self.close()

    @ch.action("previousmenu", "*")
    def exit_script(self, *args):
        utils.log('dialogbaseinfo.exit_script call exit')
        self.exit()

    # @utils.run_async
    def get_youtube_vids(self, search_str):
        try:
            youtube_list = self.getControl(ID_LIST_YOUTUBE)
        except Exception as err:
            utils.log(f'DialogBaseInfo.get_youtube_vids getControl for ID_LIST_YOUTUBE threw exception {err}')
            return None
        if not self.yt_listitems:
            user_key = addon.setting("Youtube API Key")
            search_str = search_str.replace('-', '')
            self.yt_listitems = youtube.search(
                search_str, limit=15, api_key=user_key)
        if not self.yt_listitems:
            return None
        vid_ids = [item.get_property(
            "key") for item in self.lists["videos"]] if "videos" in self.lists else []
        youtube_list.reset()
        youtube_list.addItems(
            [i.get_listitem() for i in self.yt_listitems if i.get_property("youtube_id") not in vid_ids])

    def open_credit_dialog(self, credit_id):
        info = tmdb.get_credit_info(credit_id)
        listitems = []
        if "seasons" in info["media"]:
            listitems += tmdb.handle_seasons(info["media"]["seasons"])
        if "episodes" in info["media"]:
            listitems += tmdb.handle_episodes(info["media"]["episodes"])
        if not listitems:
            listitems += [{"label": addon.LANG(19055)}]
        index = selectdialog.open(header=addon.LANG(32151),
                                  listitems=listitems)
        if index == -1:
            return None
        listitem = listitems[index]
        if listitem["mediatype"] == "episode":
            wm.open_episode_info(season=int(listitem["season"]),
                                 episode=listitem["episode"],
                                 tvshow_id=info["media"]["id"])
        elif listitem["mediatype"] == "season":
            wm.open_season_info(season=int(listitem["season"]),
                                tvshow_id=info["media"]["id"])

    def update_states(self):
        if not self.states:
            return None
        #utils.log(f'DialogBaseInfo.update_states updating window props from self.states {self.states} {id(self.states)}')
        #utils.log(f'DialogBaseInfo.update_states updating window props from tmdb.get_account_props(self.states) {tmdb.get_account_props(self.states)}')
        utils.dict_to_windowprops(data=tmdb.get_account_props(self.states),
                                  window_id=self.window_id)
