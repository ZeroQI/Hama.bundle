### FanartTV.com ###

### Imports ###
import common
from common import GetPosters, GetSeasons, GetFanarts, GetBanners, GetElementText

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(metadata, TVDBid="", tmdbid="", imdbid="", movie=False, season=0, num=100):  #Fetch from fanart.tv - Posters Seasons Fanarts Banner
  API_MOVIES_URL = 'http://webservice.fanart.tv/v3/movies/{id}?api_key={api_key}'
  API_TV_URL     = 'http://webservice.fanart.tv/v3/tv/{id}?api_key={api_key}'
  API_KEY        = 'cfa9dc054d221b8d107f8411cd20b13f'
  FanartTV_dict  = {}
  Log.Info("".ljust(157, '-'))
  Log.Info("FanartTv.GetMetadata() - movie:'{movie}', TVDBid: '{TVDBid}', imdbid:'{imdbid}', tmdbid: '{tmdbid}', season: '{season}', num: '{num}'".format(movie=movie, TVDBid=TVDBid, imdbid=imdbid, tmdbid=tmdbid, season=season, num=num))
  if Prefs['FanartTV'] and ( GetPosters() or GetFanarts() or GetBanners()):  # No need to re-check "Prefs['FanartTV']" afterwards
    if movie and (imdbid or tmdbid):  ### Movies ###
      if "," in imdbid:  (GetImages(metadata, movie, imdbid_unique, None, season, num) for imdbid_unique in imdbid.split(",")); return  #recusive call for each imdbid to reduce complexity
      if "," in tmdbid:  (GetImages(metadata, movie, tmdbid_unique, None, season, num) for tmdbid_unique in tmdbid.split(",")); return  #recusive call for each tmdbid to reduce complexity
      id = imdbid if imdbid else tmdbid
      json = common.LoadFile(filename=id+".json", relativeDirectory="FanartTV/movie/"+id, url=API_MOVIES_URL.format(id=id, api_key=API_KEY), cache=CACHE_1WEEK)
      if json:
        for item in json['moviebackground'] if 'moviebackground' in json and GetFanarts() else ():  FanartTV_dict[ item['url'] ] = ("FanartTV/movie/id/movieposter/{filename}.jpg".format(    filename=item['id'], id=id), num, None)
        for item in json['movieposter'    ] if 'movieposter'     in json and GetPosters() else ():  FanartTV_dict[ item['url'] ] = ("FanartTV/movie/id/moviebackground/{filename}.jpg".format(filename=item['id'], id=id), num, None)
    
    if TVDBid:  ### Series ###
      json = common.LoadFile(filename="%s.json" % TVDBid, relativeDirectory="FanartTV/tv/"+TVDBid, url=API_TV_URL.format(id=TVDBid, api_key=API_KEY), cache=CACHE_1WEEK)  # AniDB title database loaded once every 2 week
      if json:
        for item in json['showbackground' ] if 'showbackground'  in json and GetFanarts() else ():  FanartTV_dict[ item['url'] ] = ("FanartTV/tv/{id}/showbackground/{filename}.jpg".format(filename=item['id'], id=TVDBid), num, None)
        for item in json['tvposter'       ] if 'tvposter'        in json and GetPosters() else ():  FanartTV_dict[ item['url'] ] = ("FanartTV/tv/{id}/tvposter/{filename}.jpg".format(      filename=item['id'], id=TVDBid), num, None)
        for item in json['tvbanner'       ] if 'tvbanner'        in json and GetBanners() else ():  FanartTV_dict[ item['url'] ] = ("FanartTV/tv/{id}/tvbanner/{filename}.jpg".format(      filename=item['id'], id=TVDBid), num, None)
        for item in json['seasonposter'   ] if 'seasonposter'    in json and GetSeasons() else ():  FanartTV_dict[ item['url'] ] = ("FanartTV/tv/{id}/seasonposter/{filename}.jpg".format(  filename=item['id'], id=TVDBid), num, None)
  return FanartTV_dict
  
###Template ###
#import code-reducing one-liners
#def xxx
#  if need to to anything:
#    if right id present
#      reload for multiple ids in meta id;return
#      load json/xml and label as such
#      if need to dl: dl meta if single link no loop
#      loop if needed using item variable: dl meta (include thumbnail url for fanart when present)
#      loop if needed using item variable: (dl meta if myanimelist didn't shamelessly stole anidb link)

#http://webservice.fanart.tv/v3/tv/79824?api_key=cfa9dc054d221b8d107f8411cd20b13f #Naruto Shippuden
#http://webservice.fanart.tv/v3/tv/81189?api_key=cfa9dc054d221b8d107f8411cd20b13f
