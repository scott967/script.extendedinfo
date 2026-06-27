# Copyright (C) 2022 - Scott Smart <scott967@kodi.tv>
# This program is Free Software see LICENSE file for details
"""Uses Musicbrainz API  to query data from  Musicbrainz.

The get_* functions are called to query Musicbrainz API.

"""

import re

from resources.kutil131 import ItemList, utils

BASE_URL = 'https://musicbrainz.org/ws/2/'
HEADERS = {'Content-Type': 'application/json',
           'User-Agent': 'Kodi script.extendedinfo/6.1 ( https://github.com/xbmc/script.extendedinfo )'}


def _handle_albums(results: list[dict]) -> ItemList:
    """Converts MB query results to kutil131 ItemList

    Args:
        results (dict): MB albums for an artist

    Returns:
        ItemList: a kutil131 ItemList od dicts
    """
    albums = ItemList(content_type="albums")
    if not results:
        return albums
    if 'topalbums' in results and "album" in results['topalbums']:
        for album in results['topalbums']['album']:
            albums.append({'artist': album['artist']['name'],
                           'mbid': album.get('mbid', ""),
                           'mediatype': "album",
                           'thumb': album['image'][-1]['#text'],
                           'label': f"{album['artist']['name']} - {album['name']}",
                           'title': album['name']})
            albums.append(album)
    return albums


def _handle_artists(results) -> ItemList:
    """Converts MB artist query to kutil131 ItemList

    Args:
        results (_type_): _description_

    Returns:
        ItemList: a kutil131 ItemList of artist info as dicts
    """
    artists = ItemList(content_type="artists")
    if not results:
        return artists
    for artist in results['artist']:
        if 'name' not in artist:
            continue
        artist = {'title': artist['name'],
                  'label': artist['name'],
                  'mediatype': "artist",
                  'mbid': artist.get('mbid'),
                  'thumb': artist['image'][-1]['#text'],
                  'Listeners': format(int(artist.get('listeners', 0)), ",d")}
        artists.append(artist)
    return artists


def get_artist_albums(artist_mbid: str) -> ItemList:
    """Queries MB api artist.getTopAlbums method for an artist

    Gets 50 albums with title, mbid, and cover image

    Args:
        artist_mbid (str): The musicbrainz id for the artist

    Returns:
        ItemList: a kutil131object that wraps a list of albums
        info dicts
    """
    if not artist_mbid:
        return ItemList(content_type="albums")
    results = get_data(method="artist.getTopAlbums",
                       params={"mbid": artist_mbid})
    return _handle_albums(results)


def get_similar_artists(artist_mbid: str) -> ItemList:
    """Queries MB api artist.getsimilar for artists

   Gets name, mbid, and thumb image of similar artists

    Args:
        artist_mbid (str): The musicbrainz id for the artist

    Returns:
        ItemList: a kutil131 object that wraps a list of artists info dicts
    """
    if not artist_mbid:
        return ItemList(content_type="artists")
    params = {"mbid": artist_mbid,
              "limit": "400"}
    results = get_data(method="artist.getSimilar",
                       params=params)
    if results and "similarartists" in results:
        return _handle_artists(results['similarartists'])


def get_track_info(artist_name="", track="") -> dict:
    """ Queries MB api

    Args:
        artist_name (str, optional): The artist name. Defaults to "".
        track (str, optional): The track name. Defaults to "".

    Returns:
        dict: MB info including scrobles of a song.
    """
    if not artist_name or not track:
        return {}
    params = {"artist": artist_name,
              "track": track}
    results: list[dict] = get_data(method="track.getInfo",
                                       params=params)
    if not results:
        return {}
    summary = results['track']['wiki']['summary'] if "wiki" in results['track'] else ""
    return {'playcount': str(results['track']['playcount']),
            'thumb': str(results['track']['playcount']),
            'summary': clean_text(summary)}


def get_artist_info(artist_name="", artist_mbid="") -> dict:
    """ Queries MB api for artist info

    Args:
        artist_name (str, optional): The artist name. Defaults to "".
        artist_mbid (str, optional): The musicbrainz id for the artist. Defaults to "".

    Returns:
        dict: The artist info.
    """
    if not artist_name and not artist_mbid:
        return {}
    params = {}
    if not artist_mbid:
        #params["artist"] = artist_name
        #results = get_data(method="artist_search", params=params)
        artist_mbid = utils.fetch_musicbrainz_id(artist_name, headers=HEADERS)
    if artist_mbid:
        params["mbid"] = artist_mbid
    else:
        return {}
    results = get_data(method="artist.getInfo", params=params)
    if not results[0] or "artist" not in results:
        return {}
    artist_data = results[0]["artist"]
    return {
        "name": artist_data.get("name", ""),
        "mbid": artist_data.get("id", ""),
        "bio": clean_text(artist_data.get("bio", {}).get("summary", "")),
        "image": artist_data.get("image", [{}])[0].get("url", "") if artist_data.get("image") else ""
    }


def get_data(method: str, params=None, cache_days=10) -> list[dict]:
    """helper function runs query including using local cache

    Args:
        method (str): MB api method
        params (dict, optional): MB method parameters.  Defaults to None.
        cache_days (float, optional): Days to use cache/query. Defaults to 10.

    Returns:
        dict:  The json.loads results from the query
    """
    if params is None:
        params = {}
    if method == "artist.getInfo" and "mbid" in params:
        url = f"{BASE_URL}artist/?{params['mbid']}&fmt=json"
        return utils.get_JSON_response(url=url,
                                       cache_days=cache_days,
                                       folder="MusicBrainz",
                                       headers=HEADERS)
    elif method == "artist.getTopAlbums" and "mbid" in params:
        url = f"{BASE_URL}artist/{params['mbid']}/release-groups?fmt=json&limit=50&type=album"
        return utils.get_JSON_response(url=url,
                                       cache_days=cache_days,
                                       folder="MusicBrainz",
                                       headers=HEADERS)
    return []


def clean_text(text) -> str:
    """Helper function to unescape chars

    Args:
        text (str): text string to unescape

    Returns:
        str: text string
    """
    if not text:
        return ""
    text = re.sub(
        '(From Wikipedia, the free encyclopedia)|(Description above from the Wikipedia.*?Wikipedia)', '', text)
    text = re.sub('<(.|\n|\r)*?>', '', text)
    text = text.replace('<br />', '[CR]')
    text = text.replace('<em>', '[I]').replace('</em>', '[/I]')
    text = text.replace('&amp;', '&')
    text = text.replace('&gt;', '>').replace('&lt;', '<')
    text = text.replace('&#39;', "'").replace('&quot;', '"')
    text = re.sub("\n\\.$", "", text)
    text = text.replace(
        'User-contributed text is available under the Creative Commons By-SA License and may also be available under the GNU FDL.', '')
    removals = {'\u200b', " ", "\n"}
    while text:
        s = text[0]
        e = text[-1]
        if s in removals:
            text = text[1:]
        elif e in removals:
            text = text[:-1]
        elif s.startswith(".") and not s.startswith(".."):
            text = text[1:]
        else:
            break
    return text.strip()
