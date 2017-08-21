### FanartTV.com ###
#http://webservice.fanart.tv/v3/tv/79824?api_key=cfa9dc054d221b8d107f8411cd20b13f #Naruto Shippuden
#http://webservice.fanart.tv/v3/tv/81189?api_key=cfa9dc054d221b8d107f8411cd20b13f

### Imports ###
import common
from common import GetMeta, Dict, SaveDict, Dict

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(movie=False, TVDBid="", tmdbid="", imdbid="", season=0, num=100):  #Fetch from fanart.tv - Posters Seasons Fanarts Banner
  API_MOVIES_URL = 'http://webservice.fanart.tv/v3/movies/{id}?api_key={api_key}'
  API_TV_URL     = 'http://webservice.fanart.tv/v3/tv/{id}?api_key={api_key}'
  API_KEY        = 'cfa9dc054d221b8d107f8411cd20b13f'
  FanartTV_dict  = {}
  Log.Info("".ljust(157, '-'))
  Log.Info("FanartTv.GetMetadata() - movie:'{movie}', TVDBid: '{TVDBid}', tmdbid: '{tmdbid}', imdbid:'{imdbid}', season: '{season}', num: '{num}'".format(movie=movie, TVDBid=TVDBid, tmdbid=tmdbid, imdbid=imdbid, season=season, num=num))
  if "," in imdbid:  (GetMetadata(metadata, movie, "", "", imdbid_unique, season, num) for imdbid_unique in (tmdbid or imdbid).split(",")); return  #recusive call for each imdbid to reduce complexity
  if "," in tmdbid:  (GetMetadata(metadata, movie, "", tmdbid_unique, "", season, num) for tmdbid_unique in tmdbid.split(",")); return  #recusive call for each tmdbid to reduce complexity
  if not movie and TVDBid:            id, relativeDirectory, url = TVDBid,           "FanartTV/tv/"   +TVDBid,               API_TV_URL.format(id=TVDBid,           api_key=API_KEY)
  elif movie and (imdbid or tmdbid):  id, relativeDirectory, url = imdbid or tmdbid, "FanartTV/movie/"+imdbid or tmdbid, API_MOVIES_URL.format(id=imdbid or tmdbid, api_key=API_KEY)
  if (GetMeta('FanartTV', 'posters') or GetMeta('FanartTV', 'art') or GetMeta('FanartTV', 'banners')) and (TVDBid or tmdbid or imdbid):
    json = common.LoadFile(filename=id+".json", relativeDirectory=relativeDirectory, url=url, cache=CACHE_1WEEK)
    if json and (imdbid or tmdbid):
      if GetMeta('FanartTV', 'posters'):
        for item in Dict(json, 'movieposter'    ) or []:
          SaveDict((relativeDirectory+"{id}/movieposter/{filename}.jpg".format(    id=id, filename=item['id']), num, None), FanartTV_dict, 'posters', item['url'])
      if GetMeta('FanartTV', 'art'):
        for item in Dict(json, 'moviebackground') or []:
          SaveDict((relativeDirectory+"{id}/moviebackground/{filename}.jpg".format(id=id, filename=item['id']), num, None), FanartTV_dict, 'art',     item['url'])
    if json and TVDBid:
      if GetMeta('FanartTV', 'posters'):
        for item in Dict(json, 'tvposter'       ) or []:
          SaveDict((relativeDirectory+"{id}/tvposter/{filename}.jpg".format(       id=id, filename=item['id']), num, None), FanartTV_dict, 'posters', item['url'])
      if GetMeta('FanartTV', 'art'):
        for item in Dict(json, 'showbackground' ) or []:
          SaveDict((relativeDirectory+"{id}/showbackground/{filename}.jpg".format( id=id, filename=item['id']), num, None), FanartTV_dict, 'art',     item['url'])
      if GetMeta('FanartTV', 'banners'):
        for item in Dict(json, 'tvbanner'       ) or []:
          SaveDict((relativeDirectory+"{id}/tvbanner/{filename}.jpg".format(       id=id, filename=item['id']), num, None), FanartTV_dict, 'banners', item['url'])
      if GetMeta('FanartTV', 'seasons'):
        for item in Dict(json, 'seasonposter'   ) or []:
          SaveDict((relativeDirectory+"{id}/seasonposter/{filename}.jpg".format(   id=id, filename=item['id']), num, None), FanartTV_dict, 'seasons', item['season'], 'posters', item['url'])
  return FanartTV_dict
 