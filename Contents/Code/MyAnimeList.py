### MyAnimeList.net ###
# Source agent:     https://github.com/Fribb/MyAnimeList.bundle/blob/master/Contents/Code/__init__.py
# API xml exemple:  http://fribbtastic-api.net/fribbtastic-api/services/anime?id=33487

### Imports ###
import common
from common import GetMeta, GetXml, SaveDict
import os

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(movie, MALid):
  Log.Info("".ljust(157, '-'))
  Log.Info("MyAnimeList.GetMetadata() - MALid: '%s'" % MALid)
  if not MALid.isdigit():  return {}
  
  MAL_HTTP_API_URL = "http://fribbtastic-api.net/fribbtastic-api/services/anime?id="
  MAL_PREFIX       = "https://myanimelist.cdn-dena.com"  # Some links in the XML will come from TheTVDB, not adding those....
  MyAnimeList_dict = {}
  xml              = common.LoadFile(filename=MALid+".xml", relativeDirectory=os.path.join('MyAnimeList', 'xml'), url=MAL_HTTP_API_URL + MALid, cache=CACHE_1DAY * 7)
  if xml:
    SaveDict( GetXml(xml, 'title'     ), MyAnimeList_dict, 'title'                  )
    SaveDict( GetXml(xml, 'synopsis'  ), MyAnimeList_dict, 'summary'                )
    SaveDict( GetXml(xml, 'rating'    ), MyAnimeList_dict, 'content_rating'         )
    SaveDict( GetXml(xml, 'firstAired'), MyAnimeList_dict, 'originally_available_at')
      
    #for item in xml.xpath('//anime/genres/genre' or []):  SaveDict([item.text], MyAnimeList_dict, 'genres')
    if GetXml(xml, '//anime/genres/genre'):          SaveDict( [item.text for item in xml.xpath('//anime/genres/genre')], MyAnimeList_dict, 'genres') 
    if GetXml(xml, 'status') == 'Currently Airing':  SaveDict( "Continuing", MyAnimeList_dict, 'genres')
    if GetXml(xml, 'status') == 'Finished Airing':   SaveDict( "Ended"     , MyAnimeList_dict, 'genres')
    if GetXml(xml, 'type'  ) == 'TV':                SaveDict( "Serie"     , MyAnimeList_dict, 'genres')
    if GetXml(xml, 'type'  ) == 'Movie':             SaveDict( "Movie"     , MyAnimeList_dict, 'genres')
    if GetXml(xml, 'type'  ) == 'Special':           SaveDict( "Special"   , MyAnimeList_dict, 'genres')

    for item in xml.xpath('//anime/episodes/episode') or []:
      episode = GetXml(item, 'episodeNumber')
      SaveDict( GetXml(xml, 'engTitle'), MyAnimeList_dict, 'seasons', "1", 'episodes', episode, 'title'                  )
      SaveDict( GetXml(xml, 'aired'   ), MyAnimeList_dict, 'seasons', "1", 'episodes', episode, 'originally_available_at')
      
    for item in xml.xpath('//anime/covers/cover'          ) if GetMeta('MyAnimeList', 'posters') else []:
      SaveDict(("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None) if item.text.startswith(MAL_PREFIX) else "", MyAnimeList_dict, 'posters', item.text)
    for item in xml.xpath('//anime/backgrounds/background') if GetMeta('MyAnimeList', 'art'    ) else []:
      SaveDict(("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None) if item.text.startswith(MAL_PREFIX) else "", MyAnimeList_dict, 'art',     item.text)
    for item in xml.xpath('//anime/banners/banner'        ) if GetMeta('MyAnimeList', 'banners') else []:
      SaveDict(("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None) if item.text.startswith(MAL_PREFIX) else "", MyAnimeList_dict, 'banners', item.text)

  return MyAnimeList_dict
