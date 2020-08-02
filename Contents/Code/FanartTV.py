### FanartTV.com ###
# https://webservice.fanart.tv/v3/tv/79824?api_key=cfa9dc054d221b8d107f8411cd20b13f #Naruto Shippuden
# https://webservice.fanart.tv/v3/tv/81189?api_key=cfa9dc054d221b8d107f8411cd20b13f

### Imports ###
# Python Modules #
import os
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###
FTV_API_KEY        = 'cfa9dc054d221b8d107f8411cd20b13f'
FTV_API_MOVIES_URL = 'https://webservice.fanart.tv/v3/movies/{id}?api_key=%s' % FTV_API_KEY
FTV_API_TV_URL     = 'https://webservice.fanart.tv/v3/tv/{id}?api_key=%s' % FTV_API_KEY

### Functions ###
def GetMetadata(movie=False, TVDBid="", tmdbid="", imdbid="", season=0):  #Fetch from fanart.tv - Posters Seasons Fanarts Banner
  Log.Info("=== FanartTv.GetMetadata() ===".ljust(157, '='))
  FanartTV_dict = {}

  Log.Info("movie:'{movie}', TVDBid: '{TVDBid}', tmdbid: '{tmdbid}', imdbid:'{imdbid}', season: '{season}'".format(movie=movie, TVDBid=TVDBid, tmdbid=tmdbid, imdbid=imdbid, season=season))
  if "," in imdbid:  (GetMetadata(movie, "", "", imdbid_unique, season) for imdbid_unique in (tmdbid or imdbid).split(",")); return  #recusive call for each imdbid to reduce complexity
  if "," in tmdbid:  (GetMetadata(movie, "", tmdbid_unique, "", season) for tmdbid_unique in tmdbid.split(","));             return  #recusive call for each tmdbid to reduce complexity
  if not movie and TVDBid.isdigit():  id, relativeDirectory, url = TVDBid,           os.path.join("FanartTV", "tv",    TVDBid),           FTV_API_TV_URL.format(id=TVDBid)
  elif movie and (imdbid or tmdbid):  id, relativeDirectory, url = imdbid or tmdbid, os.path.join("FanartTV", "movie", imdbid or tmdbid), FTV_API_MOVIES_URL.format(id=imdbid or tmdbid)
  else:                               return FanartTV_dict
  if TVDBid or tmdbid or imdbid:
    Log.Info(("--- %s.images ---" % id).ljust(157, '-'))
    json = common.LoadFile(filename=id+".json", relativeDirectory=relativeDirectory, url=url)
    
    #Movies
    if json and (imdbid or tmdbid):
      for item in Dict(json, 'movieposter'    , default=[]):  Log.Info("[ ] poster: {}".format(SaveDict((os.path.join(relativeDirectory, id, "movieposter",     "{filename}.jpg".format(filename=Dict(item, 'id'))), common.poster_rank('FanartTV', 'posters'), None), FanartTV_dict, 'posters', Dict(item, 'url'))))
      for item in Dict(json, 'moviebackground', default=[]):  Log.Info("[ ] art: {}"   .format(SaveDict((os.path.join(relativeDirectory, id, "moviebackground", "{filename}.jpg".format(filename=Dict(item, 'id'))), common.poster_rank('FanartTV', 'art'    ), None), FanartTV_dict, 'art',     Dict(item, 'url'))))
    
    #Series
    if json and TVDBid.isdigit():
      for item in Dict(json, 'tvposter'       , default=[]):  Log.Info("[ ] poster: {}"       .format(SaveDict((os.path.join(relativeDirectory, id, "tvposter",       "{filename}.jpg".format(filename=Dict(item, 'id'))), common.poster_rank('FanartTV', 'posters'), None), FanartTV_dict, 'posters', Dict(item, 'url'))))
      for item in Dict(json, 'showbackground' , default=[]):  Log.Info("[ ] art: {}"          .format(SaveDict((os.path.join(relativeDirectory, id, "showbackground", "{filename}.jpg".format(filename=Dict(item, 'id'))), common.poster_rank('FanartTV', 'art'    ), None), FanartTV_dict, 'art',     Dict(item, 'url'))))
      for item in Dict(json, 'tvbanner'       , default=[]):  Log.Info("[ ] banner: {}"       .format(SaveDict((os.path.join(relativeDirectory, id, "tvbanner",       "{filename}.jpg".format(filename=Dict(item, 'id'))), common.poster_rank('FanartTV', 'banners'), None), FanartTV_dict, 'banners', Dict(item, 'url'))))
      for item in Dict(json, 'seasonposter'   , default=[]):  Log.Info("[ ] season poster: {}".format(SaveDict((os.path.join(relativeDirectory, id, "seasonposter",   "{filename}.jpg".format(filename=Dict(item, 'id'))), common.poster_rank('FanartTV', 'posters'), None), FanartTV_dict, 'seasons', Dict(item, 'season'), 'posters', Dict(item, 'url'))))

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("FanartTV_dict: {}".format(DictString(FanartTV_dict, 4)))
  return FanartTV_dict
