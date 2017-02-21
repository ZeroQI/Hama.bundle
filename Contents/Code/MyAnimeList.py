### MyAnimeList.net ###
# Source agent:     https://github.com/Fribb/MyAnimeList.bundle/blob/master/Contents/Code/__init__.py
# API xml exemple:  http://fribbtastic-api.net/fribbtastic-api/services/anime?id=33487

### Imports ###
import common
from common import GetPosters, GetSeasons, GetFanarts, GetBanners, GetElementText

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(metadata, movie, MALid):
  MAL_HTTP_API_URL = "http://fribbtastic-api.net/fribbtastic-api/services/anime?id="
  MAL_PREFIX       = "https://myanimelist.cdn-dena.com"  # Some links in the XML will come from TheTVDB, not adding those....
  Log.Info("".ljust(157, '-'))
  Log.Info("MyAnimeList.GetMetadata() - MALid: '%s'" % MALid)
  MyAnimeList_dict = {}
  if MALid.isdigit():
    xml = common.LoadFile(filename=MALid+".xml", relativeDirectory="MAL", url=MAL_HTTP_API_URL + MALid, cache=CACHE_1DAY * 7)
    if xml:
      if GetPosters('MyAnimeList') or GetFanarts('MyAnimeList') or GetBanners('MyAnimeList'):  # No need to re-check "Prefs['MyAnimeList']" afterwards
        for item in xml.xpath('//anime/covers/cover'          ) if GetPosters('MyAnimeList') else():
          if item.text.startswith(MAL_PREFIX):
            if 'posters' not in MyAnimeList_dict:  MyAnimeList_dict['posters'] = {}
            MyAnimeList_dict['posters'][item.text] = ("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None)
        for item in xml.xpath('//anime/backgrounds/background') if GetFanarts('MyAnimeList') else():
          if item.text.startswith(MAL_PREFIX):
            if 'art' not in MyAnimeList_dict:  MyAnimeList_dict['art'] = {}
            MyAnimeList_dict['art'][item.text] = ("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None)
        for item in xml.xpath('//anime/banners/banner'        ) if GetBanners('MyAnimeList') else():
          if item.text.startswith(MAL_PREFIX):
            if 'banners' not in MyAnimeList_dict:  MyAnimeList_dict['banners'] = {}
            MyAnimeList_dict['banners'][item.text] = ("MyAnimeList/" + "/".join(item.text.split('/')[3:]), 50, None)
      if xml.xpath('firstAired')[0].text:  MyAnimeList_dict['originally_available_at'] = xml.xpath('firstAired')[0].text
      if xml.xpath('title')[0].text:       MyAnimeList_dict['title'                  ] = xml.xpath('title'     )[0].text
      MyAnimeList_dict['content_rating'] = xml.xpath('rating'  )[0].text  # <rating>PG-13 - Teens 13 or older</rating>
      MyAnimeList_dict['rating'        ] = xml.xpath('score'   )[0].text  # <rating>PG-13 - Teens 13 or older</rating>
      MyAnimeList_dict['summary'       ] = xml.xpath('synopsis')[0].text  # <rating>PG-13 - Teens 13 or older</rating>
      MyAnimeList_dict['genres'        ] = [item.text for item in xml.xpath('//anime/genres/genre')]
      #xml.xpath('status')[0].text  # <status>Currently Airing</status>
      #xml.xpath('type')[0].text    # <type>TV</type>

      for item in xml.xpath('//anime/episodes/episode'):
        season  = "1"
        episode = item.xpath('episodeNumber')[0].text
        if not 'seasons'  in MyAnimeList_dict:                                 MyAnimeList_dict['seasons']                              = {}
        if not  season    in MyAnimeList_dict['seasons']:                      MyAnimeList_dict['seasons'][season]                      = {}
        if not 'episodes' in MyAnimeList_dict['seasons'][season]:              MyAnimeList_dict['seasons'][season]['episodes']          = {}
        if not  episode   in MyAnimeList_dict['seasons'][season]['episodes']:  MyAnimeList_dict['seasons'][season]['episodes'][episode] = {}
        MyAnimeList_dict['seasons'][season]['episodes'][episode]['originally_available_at'] = item.xpath('aired'   )[0].text
        MyAnimeList_dict['seasons'][season]['episodes'][episode]['title'                  ] = item.xpath('engTitle')[0].text  #japTitle
        
  return MyAnimeList_dict
  
