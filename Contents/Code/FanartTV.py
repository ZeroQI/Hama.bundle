### FanartTV.com ###
#http://webservice.fanart.tv/v3/tv/79824?api_key=cfa9dc054d221b8d107f8411cd20b13f #Naruto Shippuden
#http://webservice.fanart.tv/v3/tv/81189?api_key=cfa9dc054d221b8d107f8411cd20b13f

### Imports ###
import common
from common import Dict, SaveDict, Dict, Log, DictString

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(movie=False, TVDBid="", tmdbid="", imdbid="", season=0, num=100):  #Fetch from fanart.tv - Posters Seasons Fanarts Banner
  API_MOVIES_URL = 'http://webservice.fanart.tv/v3/movies/{id}?api_key={api_key}'
  API_TV_URL     = 'http://webservice.fanart.tv/v3/tv/{id}?api_key={api_key}'
  API_KEY        = 'cfa9dc054d221b8d107f8411cd20b13f'
  FanartTV_dict  = {}
  Log.Info("".ljust(157, '-'))
  Log.Info("FanartTv.GetMetadata() - movie:'{movie}', TVDBid: '{TVDBid}', tmdbid: '{tmdbid}', imdbid:'{imdbid}', season: '{season}', num: '{num}'".format(movie=movie, TVDBid=TVDBid, tmdbid=tmdbid, imdbid=imdbid, season=season, num=num))
  if "," in imdbid:  (GetMetadata(movie, "", "", imdbid_unique, season, num) for imdbid_unique in (tmdbid or imdbid).split(",")); return  #recusive call for each imdbid to reduce complexity
  if "," in tmdbid:  (GetMetadata(movie, "", tmdbid_unique, "", season, num) for tmdbid_unique in tmdbid.split(","));             return  #recusive call for each tmdbid to reduce complexity
  if not movie and TVDBid.isdigit():  id, relativeDirectory, url = TVDBid,           "FanartTV/tv/"   +TVDBid,               API_TV_URL.format(id=TVDBid,           api_key=API_KEY)
  elif movie and (imdbid or tmdbid):  id, relativeDirectory, url = imdbid or tmdbid, "FanartTV/movie/"+imdbid or tmdbid, API_MOVIES_URL.format(id=imdbid or tmdbid, api_key=API_KEY)
  else:                               return FanartTV_dict
  if TVDBid or tmdbid or imdbid:
    json = common.LoadFile(filename=id+".json", relativeDirectory=relativeDirectory, url=url, cache=CACHE_1WEEK)
    
    #Movies
    if json and (imdbid or tmdbid):
      for item in Dict(json, 'movieposter'    ) or []:  SaveDict((relativeDirectory+"{id}/movieposter/{filename}.jpg".format(    id=id, filename=item['id']), num, None), FanartTV_dict, 'posters', item['url'])
      for item in Dict(json, 'moviebackground') or []:  SaveDict((relativeDirectory+"{id}/moviebackground/{filename}.jpg".format(id=id, filename=item['id']), num, None), FanartTV_dict, 'art',     item['url'])
    
    #Series
    if json and TVDBid.isdigit():
      for item in Dict(json, 'tvposter'       ) or []:  SaveDict((relativeDirectory+"{id}/tvposter/{filename}.jpg".format(       id=id, filename=item['id']), num, None), FanartTV_dict, 'posters', item['url'])
      for item in Dict(json, 'showbackground' ) or []:  SaveDict((relativeDirectory+"{id}/showbackground/{filename}.jpg".format( id=id, filename=item['id']), num, None), FanartTV_dict, 'art',     item['url'])
      for item in Dict(json, 'tvbanner'       ) or []:  SaveDict((relativeDirectory+"{id}/tvbanner/{filename}.jpg".format(       id=id, filename=item['id']), num, None), FanartTV_dict, 'banners', item['url'])
      for item in Dict(json, 'seasonposter'   ) or []:  SaveDict((relativeDirectory+"{id}/seasonposter/{filename}.jpg".format(   id=id, filename=item['id']), num, None), FanartTV_dict, 'seasons', item['season'], 'posters', item['url'])

  Log.Info("FanartTV_dict: {}".format(DictString(FanartTV_dict, 4)))
  return FanartTV_dict
 
