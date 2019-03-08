### MyAnimeList.net ###
# Source agent:     https://github.com/Fribb/MyAnimeList.bundle/blob/master/Contents/Code/__init__.py
# API xml exemple:  http://fribbtastic-api.net/fribbtastic-api/services/anime?id=33487

### Imports ###
import common
from common import GetXml, SaveDict, Log, DictString
import os

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(movie, MALid):
  Log.Info("=== MyAnimeList.GetMetadata() ===".ljust(157, '='))
  MAL_HTTP_API_URL = "http://fribbtastic-api.net/fribbtastic-api/services/anime?id="
  MAL_PREFIX       = "https://myanimelist.cdn-dena.com"  # Some links in the XML will come from TheTVDB, not adding those....
  MyAnimeList_dict = {}

  Log.Info("MALid: '%s'" % MALid)
  if not MALid or not MALid.isdigit():  return MyAnimeList_dict

  Log.Info("--- series ---".ljust(157, '-'))
  xml = common.LoadFile(filename=MALid+".xml", relativeDirectory=os.path.join('MyAnimeList', 'xml'), url=MAL_HTTP_API_URL + MALid, cache=CACHE_1DAY * 7)
  if xml:
    Log.Info("[ ] title: {}"                  .format(SaveDict( GetXml(xml, 'title'         ), MyAnimeList_dict, 'title'                  )))
    Log.Info("[ ] summary: {}"                .format(SaveDict( GetXml(xml, 'synopsis'      ), MyAnimeList_dict, 'summary'                )))
    Log.Info("[ ] score: {}"                  .format(SaveDict( GetXml(xml, 'rating'        ), MyAnimeList_dict, 'score'                  )))
    #Log.Info("[ ] rating: {}"                 .format(SaveDict( GetXml(xml, 'content_rating').split(" ")[0], MyAnimeList_dict, 'rating'   )))
    Log.Info("[ ] originally_available_at: {}".format(SaveDict( GetXml(xml, 'firstAired'    ), MyAnimeList_dict, 'originally_available_at')))
      
    #for item in xml.xpath('//anime/genres/genre' or []):  SaveDict([item.text], MyAnimeList_dict, 'genres')
    if GetXml(xml, '//anime/genres/genre'):          Log.Info("[ ] genres: {}".format(SaveDict( sorted([item.text for item in xml.xpath('//anime/genres/genre')]), MyAnimeList_dict, 'genres')))
    if GetXml(xml, 'status') == 'Currently Airing':  Log.Info("[ ] status: {}".format(SaveDict( "Continuing", MyAnimeList_dict, 'status')))
    if GetXml(xml, 'status') == 'Finished Airing':   Log.Info("[ ] status: {}".format(SaveDict( "Ended"     , MyAnimeList_dict, 'status')))

    Log.Info("--- episodes ---".ljust(157, '-'))
    for item in xml.xpath('//anime/episodes/episode') or []:
      ep_number, ep_title, ep_air = GetXml(item, 'episodeNumber'), GetXml(xml, 'engTitle'), GetXml(xml, 'aired')
      Log.Info('[ ] s1e{:>3} air_date: {}, title: "{}"'.format(ep_number, ep_title, ep_air))
      SaveDict( ep_title, MyAnimeList_dict, 'seasons', "1", 'episodes', ep_number, 'title'                  )
      SaveDict( ep_air,   MyAnimeList_dict, 'seasons', "1", 'episodes', ep_number, 'originally_available_at')
      
    Log.Info("--- images ---".ljust(157, '-'))
    for item in xml.xpath('//anime/covers/cover'          ):
      Log.Info("[ ] poster: {}".format(SaveDict(("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None) if item.text.startswith(MAL_PREFIX) else "", MyAnimeList_dict, 'posters', item.text)))
    for item in xml.xpath('//anime/backgrounds/background'):
      Log.Info("[ ] art: {}"   .format(SaveDict(("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None) if item.text.startswith(MAL_PREFIX) else "", MyAnimeList_dict, 'art',     item.text)))
    for item in xml.xpath('//anime/banners/banner'        ):
      Log.Info("[ ] banner: {}".format(SaveDict(("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None) if item.text.startswith(MAL_PREFIX) else "", MyAnimeList_dict, 'banners', item.text)))

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("MyAnimeList_dict: {}".format(DictString(MyAnimeList_dict, 4)))
  return MyAnimeList_dict
