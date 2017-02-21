### common ### #@parallelize @task
# https://www.python.org/dev/peps/pep-0008/

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import os              #path.abspath, join, dirname
import inspect
import datetime
import time           # datetime.datetime.now() 
import re
import urllib
from string import maketrans

### Variables, accessible in this module (others if 'from common import xxx', or 'import common.py' calling them with 'common.Variable_name' ###
metadata_count       = {'posters':0, 'fanarts':0, 'seasons':0, 'banners':0, 'themes':0, 'thumbs': 0} 
CachePath            = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "..", "..", "..", "..", "Plug-in Support", "Data", "com.plexapp.agents.hama", "DataItems"))
AniDB_WaitUntil      = datetime.datetime.now() 
netLock              = Thread.Lock()
error_log_locked     = {}
error_log_lock_sleep = 10
TVDB_SERIE_URL       = 'http://thetvdb.com/?tab=series&id=%s'
ANIDB_SERIE_URL      = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s' # AniDB link to the anime
FILTER_CHARS         = "\\/:*?<>|~-; "
SPLIT_CHARS          = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations
WEB_LINK             = "<a href='%s' target='_blank'>%s</a>"
FILTER_SEARCH_WORDS = [ ### These are words which cause extra noise due to being uninteresting for doing searches on, Lowercase only #############################################################
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime', 'ni', 'sekai',                                             # Jp
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', 'me',  'princess', 'theater',  # En Continued
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses',                                                                                                               # Fr
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi']                                                              # Roman digits
MOVIE_RATING_MAP     = {'TV-Y': 'G', 'TV-Y7': 'G', 'TV-G': 'G', 'TV-PG': 'PG', 'TV-14': 'PG-13', 'TV-MA': 'NC-17', 'X': 'X'}
Movie_to_Serie_US_rating = {"G"    : "TV-Y7", # All Ages
                            "PG"   : "TV-G",  # Children
                            "PG-13": "TV-PG", # Teens 13 or older
                            "R"    : "TV-14", # 17+ recommended (violence & profanity)
                            "R+"   : "TV-MA", # Mild Nudity (may also contain violence & profanity)
                            "Rx"   : "NC-17" # Hentai (extreme sexual content/nudity) #metadata.content_rating = options[ metadata.content_rating.split(" - ",1)[0] ]
                           }

MoviePriority   = { 'genres'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'tags'                    : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'collections'             : ('AnimeLists', 'AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'duration'                : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),  # milliseconds
                    'rating'                  : ('AniDB', 'TheTVDB'),  #float 0-10
                    'rating_image'            : (),   # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDB.bundle/blob/master/Contents/Code/__init__.py
                    'audience_rating'         : (),   # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDB.bundle/blob/master/Contents/Code/__init__.py
                    'audience_rating_image'   : (),   # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDB.bundle/blob/master/Contents/Code/__init__.py
                    'original_title'          : ('AniDB', 'TheTVDB'),
                    'title'                   : ('AniDB', 'TheTVDB'),
                    #'title_sort'                   : ('AniDB', 'TheTVDB'),
                    'year'                    : ('AniDB', 'TheTVDB'),
                    'originally_available_at' : ('AniDB', 'TheTVDB'),
                    'studio'                  : ('AnimeLists', 'AniDB', 'TheMovieDB'),
                    'tagline'                 : ('TheMovieDB',),
                    'summary'                 : ('AniDB', 'TheTVDB'),
                    'trivia'                  : (),
                    'quotes'                  : (),
                    'content_rating'          : ('AniDB', 'TheTVDB'),
                    'content_rating_age'      : (),
                    'producers'               : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'directors'               : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'writers'                 : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'countries'               : (),
                    'posters'                 : ('TheTVDB', 'FanartTV', 'TheMovieDB', 'OMDb', 'AniDB'),
                    'art'                     : ('TheTVDB', 'FanartTV', 'TheMovieDB'),
                    'themes'                  : ()
                    } #16
SeriePriority   = { 'genres'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'tags'                    : (),
                    'collections'             : ('AnimeLists', 'AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'duration'                : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'rating'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'rating_image'            : (),   # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDB.bundle/blob/master/Contents/Code/__init__.py
                    'audience_rating'         : (),   # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDB.bundle/blob/master/Contents/Code/__init__.py
                    'audience_rating_image'   : (),   # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDB.bundle/blob/master/Contents/Code/__init__.py
                    'title'                   : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'), 
                    'summary'                 : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'originally_available_at' : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'content_rating'          : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'studio'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'countries'               : (),
                    'posters'                 : ('TheTVDB', 'FanartTV', 'MyAnimeList', 'TheMovieDB', 'OMDb', 'AniDB'),
                    'banners'                 : ('TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV'),
                    'art'                     : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV'),
                    'themes'                  : ('Plex',  'TVTunes'),
                    'tagline'                 : (),                                                                    # in gui, not in Framework guide 2.1.1
                    'roles'                   : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),  # Not in Framework guide 2.1.1
                    'original_title'          : ('AniDB', ),                                                           # in gui, not in Framework guide 2.1.1
                  }
SeasonPriority  = { 'summary'                 : ('TheTVDB',),
                    'posters'                 : ('TheTVDB',),
                    'banners'                 : ('TheTVDB',),
                    'art'                     : (),        # in gui, not in Framework guide 2.1.1
                    #'thumb'                   : (),
                  }
EpisodePriority = { 'title'                   : ('AniDB', 'TheTVDB'),
                    'summary'                 : ('TheTVDB',),
                    'originally_available_at' : ('TheTVDB',),
                    'rating'                  : ('TheTVDB',),
                    'writers'                 : ('TheTVDB', 'AniDB'),
                    'directors'               : ('TheTVDB', 'AniDB'),
                    'producers'               : ('TheTVDB', 'AniDB'),
                    'guest_stars'             : (),
                    'rating'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'), #
                    #'absolute_number'         : ('TheTVDB',), #
                    'thumbs'                  : ('TheTVDB',),
                    'duration'                : ('TheTVDB',)
                  }

Log.Info("1 - " + inspect.stack()[0][1])
Log.Info("2 - " + inspect.getfile(inspect.currentframe()))
  
### Code reduction one-liners that get imported specifically ###
def GetElementText  (el, xp                         ):  return el.xpath(xp)[0].text if el and el.xpath(xp) and el.xpath(xp)[0].text else ""   ### Get attribute from xml tag - from common import GetElementText to use without 'common.' pre-pended ###
def GetPosters      (source=""                      ):  return Prefs['Posters'] and not (Prefs['GetSingleOne'] and metadata_count['posters']) and (source=="" or source and Prefs[source])
def GetSeasons      (source=""                      ):  return Prefs['Seasons'] and not (Prefs['GetSingleOne'] and metadata_count['seasons']) and (source=="" or source and Prefs[source])
def GetFanarts      (source=""                      ):  return Prefs['Fanarts'] and not (Prefs['GetSingleOne'] and metadata_count['fanarts']) and (source=="" or source and Prefs[source])
def GetBanners      (source=""                      ):  return Prefs['Banners'] and not (Prefs['GetSingleOne'] and metadata_count['banners']) and (source=="" or source and Prefs[source])
def natural_sort_key(s, ns_re=re.compile('([0-9]+)')):  return [int(text) if text.isdigit() else text.lower() for text in re.split(ns_re, s)] ### Turn a string into a list of string and number chunks  "z23a" -> ["z", 23, "a"] - files.sort(key=natural_sort_key) ###############################
#def GetKey     (obj, key ):  return obj[key] if key in obj else None   ### Get attribute from xml tag - from common import GetElementText to use without 'common.' pre-pended ###
def GetServerCode   (url                            ):  return urllib.urlopen(url).getcode()

#def dict_field_count(d                              ):  return (0 if not isinstance(d, dict) else len(d) + sum(dict_field_count(v) for v in d.itervalues()) )
def len_dict_fields(d):
  n = 0
  for e in d:  n = n + (len_dict_fields(d[e]) if type(d[e]) is dict  else 1)
  return n

### Save file in Plex Media Server\Plug-in Support\Data\com.plexapp.agents.hama\DataItems creating folder(s) ###
def Logging():
  import logging
  for handler in logging.getLogger('com.plexapp.agents.hama').handlers:  handler.setFormatter(logging.Formatter('%(asctime)-15s (%(thread)x/%(module)-15s/%(funcName)-18s/%(lineno)4d) %(levelname)-8s %(message)s'))
  
def SaveFile(filename="", file="", relativeDirectory=""):  #By Dingmatt, slight changes, used by metadata_download
  if os.sep in filename and not relativeDirectory:  relativeDirectory, filename = os.path.split(filename)  #make it Data.Save() friendly
  fullpathDirectory = os.path.abspath(os.path.join(CachePath, relativeDirectory))
  relativeFilename  = os.path.join(relativeDirectory, filename) 
  if os.path.exists(fullpathDirectory):  Log.Debug("SaveFile() - CachePath: '{path}', file: '{file}', directory(ies) were present".format(path=CachePath, file=relativeFilename))
  else:                                  Log.Debug("SaveFile() - CachePath: '{path}', file: '{file}', directory(ies) were absent.".format(path=CachePath, file=relativeFilename)); os.makedirs(fullpathDirectory)
  Data.Save(relativeFilename, file)

### Load file in Plex Media Server\Plug-in Support\Data\com.plexapp.agents.hama\DataItems if cache time not passed ###
def LoadFile(filename="", relativeDirectory="", url="", cache= CACHE_1HOUR * 24 *2):  #By Dingmatt, hevilly moded
  ANIDB_HTTP_API_URL = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='  # this prevent CONSTANTS.py module loaded on every module, only common.py loaded on modules and all modules on __init__.py
  relativeFilename   = os.path.join(relativeDirectory, filename) 
  fullpathFilename   = os.path.abspath(os.path.join(CachePath, relativeDirectory, filename))
  too_old, converted = False, False
  file               = None
  global AniDB_WaitUntil
  if filename.endswith(".xml.gz"):  filename = filename[:-3] #anidb title database
  if relativeFilename and Data.Exists(relativeFilename) and os.path.isfile(fullpathFilename):       
    file_time = os.stat(fullpathFilename).st_mtime
    if file_time+cache < time.time():  too_old = True;  Log.Debug("common.LoadFile() - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' needs reloading..".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() - cache)))
    else:          file = Data.Load(relativeFilename);  Log.Debug("common.LoadFile() - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' loaded from cache".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() - cache)))
  else:  Log.Debug("common.LoadFile() - Filename: '{file}', Directory: '{path}' does not exists in cache".format(file=filename, path=relativeDirectory))
  if not file:
    netLock.acquire()
    if url.startswith(ANIDB_HTTP_API_URL):
      if AniDB_WaitUntil > datetime.datetime.now():  Log("common.LoadFile() - AniDB AntiBan Delay, next download window: '%s'" % AniDB_WaitUntil)    
      while AniDB_WaitUntil > datetime.datetime.now():  time.sleep(1)
      AniDB_WaitUntil = datetime.datetime.now() + datetime.timedelta(seconds=3)
    try:                    file = str(HTTP.Request(url, headers={'Accept-Encoding':'gzip'}, timeout=20, cacheTime=cache))                                     # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find'
    except Exception as e:  file = None; Log.Warn("common.LoadFile() - issue loading url: '%s', filename: '%s', Exception: '%s'" % (url, filename, e))                                                           # issue loading, but not AniDB banned as it returns "<error>Banned</error>"
    finally:                netLock.release()
    if file:
      Log.Debug("LoadFile() - url: '{url} loaded".format(url=url))
      if len(file)>1024:  SaveFile(filename, file, relativeDirectory)
      elif str(file).startswith("<Element error at "):  Log.Error("common.LoadFile() - Not an XML file, AniDB banned possibly, result: '%s'" % result); return None
      elif too_old:                                     file = Data.Load(relativeFilename) #present, cache expired but online version incorrect or not available
  try:     file, converted = XML.ElementFromString(file), True
  except:  pass
  if not converted:
    try:
      import json
      file, converted = json.loads(file), True
    except:  pass
  return file

#########################################################################################################################################################
def metadata_download(metadata, metatype, url, filename="", num=99, url_thumbnail=None):
  def GetMetadata(metatype): 
    if metatype==metadata.posters:             return "posters", GetPosters()
    if metatype==metadata.art:                 return "fanarts", GetFanarts()
    if metatype==metadata.banners:             return "banners", GetBanners()
    if metatype==metadata.themes:              return "themes",  Prefs['Plex']
    if filename.startswith("TVDB/episodes/"):  return "thumbs",  Prefs['Thumbs']
    return "seasons", GetSeasons() #Only one left, no need to get season number then for testing: metadata.seasons[season].posters
  string, test = GetMetadata(metatype)
  global metadata_count
  Log.Info("".ljust(157, '-'))
  if url in metatype:  Log.Info("url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))
  elif not test:       Log.Info("url: '%s', num: '%d', filename: '%s' Not in Plex but threshold exceded or thumbs/themes agent setting not selected" % (url, num, filename))
  else:
    file, status = None, ""
    if filename and Data.Exists(filename):  file = Data.Load(filename); status += ", Found locally"
    else:
      try:                    file = HTTP.Request(url_thumbnail if url_thumbnail else url, cacheTime=None).content
      except Exception as e:  Log.Error("error downloading, Exception: '%s'" % e); return
      if file:                status += ", Downloaded";  SaveFile(filename, file);  status += "Saved locally"
    if file:
      try:                    metatype[ url ] = Proxy.Preview(file, sort_order=num) if url_thumbnail else Proxy.Media(file, sort_order=num) # or metatype[ url ] != proxy_item # proxy_item = 
      except Exception as e:  Log.Error("issue adding File to plex - url downloaded: '%s', filename: '%s', Exception: '%s'" % (url_thumbnail if url_thumbnail else url, filename, e)); return #metatype.validate_keys( url_thumbnail if url_thumbnail else url ) # remove many posters, to avoid
      else:                   Log.Info( "url: '%s', num: '%d', filename: '%s'%s" % (url, num, filename, status))
  metadata_count[string] = metadata_count[string] + 1
  
### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
def cleanse_title(title):
  new_func_title = CleanTitle(title)
  cleansed_title = title.replace("`", "'").lower()
  try:    cleansed_title=cleansed_title.encode('ascii')
  except: pass
  for i in SPLIT_CHARS:
    if i in cleansed_title:  cleansed_title = cleansed_title.replace(i, " ")
  cleansed_title = str(" ".join(cleansed_title.split()))
  if not cleansed_title == new_func_title:
    Log.Info("cleanse_title: '%s' %s, new_func_title: '%s' %s, title: '%s' %s" % (cleansed_title, type(cleansed_title), new_func_title, type(new_func_title), title, type(title)))
  return cleansed_title
  # None in the translate call was giving an error of 'TypeError: expected a character buffer object'. So, we construct a blank translation table instead.
  # [translate(text(),"ABCDEFGHJIKLMNOPQRSTUVWXYZ 0123456789 .` :;", "abcdefghjiklmnopqrstuvwxyz 0123456789 .' ")="%s"
  #  or contains(translate(text(),"ABCDEFGHJIKLMNOPQRSTUVWXYZ 0123456789 .` :;", "abcdefghjiklmnopqrstuvwxyz 0123456789 .' "),"%s")]""" % (Name.lower().replace("'", "\'"), Name.lower().replace("'", "\'")))
def CleanTitle(title):
  DeleteChars  = ""
  ReplaceChars = maketrans("`:;-~.,/*?", "'         ")
  import unicodedata
  return " ".join(str(unicodedata.normalize('NFC', unicode(title.lower()))).translate(ReplaceChars, DeleteChars).split())  # str needed for translate

### HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems ###
def write_logs(media, movie, error_log, metadata_id_source_core, metadata_id_number, AniDBid, TVDBid):
  #Log.Debug("error_log: '%s'" % str(error_log))
  Log.Info("".ljust(157, '-'))
  global error_log_locked, error_log_lock_sleep
  log_line_separator = "<br />\r\n"
  for key in error_log.keys():
    if key not in error_log_locked.keys(): error_log_locked[key] = [False, 0]
  for log in error_log:
    num_of_sleep_sec = 0
    while error_log_locked[log][0]:
      Log.Warn("common.write_logs() - '%s' lock exists. Sleeping 1sec for lock to disappear." % log)
      num_of_sleep_sec += 1
      if num_of_sleep_sec > error_log_lock_sleep: break
      time.sleep(1)
    if int(time.time())-error_log_locked[log][1] < error_log_lock_sleep * 2 and num_of_sleep_sec > error_log_lock_sleep:   Log.Error("Could not obtain the lock in %ssec & lock age is < %ssec. Skipping log update." % (error_log_lock_sleep, error_log_lock_sleep * 2)); continue
    error_log_locked[log] = [True, int(time.time())]
    #Log.Debug("Locked '%s' %s" % (log, error_log_locked[log]))
    error_log_array, log_prefix = {}, ""
    if Data.Exists(log+".htm"):
      for line in Data.Load(log+".htm").split(log_line_separator):
        if "|" in line: error_log_array[line.split("|", 1)[0].strip()] = line.split("|", 1)[1].strip()
    if error_log[log]:  Log.Debug("common.write_logs() - '{log:<{width}}': {content}".format(log=log, width=max(map(len, error_log.keys())), content=str(error_log[log])))
    if log == 'TVDB posters missing': log_prefix = WEB_LINK % ("http://thetvdb.com/wiki/index.php/Posters",              "Restrictions") + log_line_separator
    if log == 'Plex themes missing':  log_prefix = WEB_LINK % ("https://plexapp.zendesk.com/hc/en-us/articles/201572843","Restrictions") + log_line_separator
    for entry in error_log[log]:  error_log_array[entry.split("|", 1)[0].strip()] = entry.split("|", 1)[1].strip()
    #import AniDB, tvdb
    if error_log[log] == []:
      if not log in ["Missing Episodes", "Missing Specials"]:                              keys = ["AniDBid: %s" % (WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid)), "AniDBid: %s" % AniDBid, "TVDBid: %s" % (WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid ) ), "TVDBid: %s" % TVDBid]
      elif not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1):  keys = ["TVDBid: %s"  % (WEB_LINK % (TVDB_SERIE_URL  % TVDBid,  TVDBid) )]
      else:                                                                                keys = ["%sid: %s" % (metadata_id_source_core, WEB_LINK % (ANIDB_SERIE_URL % metadata_id_number if metadata_id_source_core == "anidb" else TVDB_SERIE_URL % metadata_id_number, metadata_id_number) )]
      for key in keys: 
        if key in error_log_array.keys():  del(error_log_array[key])
    import re
    Data.Save(log+".htm", log_prefix + log_line_separator.join(sorted([str(key)+" | "+str(error_log_array[key]) for key in error_log_array.keys()], key = lambda x: x.split("|",1)[1] if x.split("|",1)[1].strip().startswith("Title:") and not x.split("|",1)[1].strip().startswith("Title: ''") else int(re.sub("<[^<>]*>", "", x.split("|",1)[0]).strip().split()[1].strip("'")) )))
    error_log_locked[log] = [False, 0]
    #Log.Debug("Unlocked '%s' %s" % (log, error_log_locked[log]))

### [tvdb4.posters.xml] Attempt to get the ASS's image data ###############################################################################################################
def GetMetadata(metadata, media, TVDBid, movie, num=0):
  TVDB4_POSTERS_URL          = 'http://rawgit.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.posters.xml'
  if movie or not metadata.id.startswith("tvdb4"): return {}
  try:
    dir_path = os.path.dirname(media.seasons.itervalues().next().episodes.itervalues().next().items[0].parts[0].file)  #s        = media.seasons.keys()[0] # e        = media.seasons[s].episodes.keys()[0] # dir_path = os.path.dirname(media.seasons[s].episodes[e].items[0].parts[0].file)
    dir_name = os.path.basename(dir_path)
    if    "[tvdb4-" not in dir_name and "tvdb4.id" not in os.listdir(dir_path): Log.Debug("Files are in a season folder (option 1)"); return
    elif  "tvdb4.mapping" in os.listdir(dir_path):                              Log.Debug("Files are in the series folder and has a mapping file (option 2)"); return
    else:                                                                       Log.Debug("Files are in the series folder and has no mapping file (option 3)")
  except Exception as e:  Log.Error("Issues in finding setup info as directories have most likely changed post scan into Plex, Exception: '%s'" % e)
  
  TVDB4_dict = {}
  TVDB4_xml=common.LoadFile(filename=os.path.basename(MAPPING_FIX), relativeDirectory="", url=TVDB4_POSTERS_URL, cache= CACHE_1DAY * 7)  # AniDB title database loaded once every 2 weeks
  if TVDB4_xml:
    entry = postersXml.xpath("/tvdb4entries/posters[@TVDBid='%s']" % TVDBid)
    if entry: 
      seasonposternum = 0
      for line in filter(None, entry[0].text.strip().replace("\r","\n").split("\n")):
        season, posterURL = line.strip().split("|",1)
        season, seasonposternum = season.lstrip("0"), seasonposternum+1
        if season in media.seasons:  common.metadata_download(metadata, metadata.seasons[season].posters, posterURL, seasonposternum, "TVDB/seasons/%s-%s-%s" % (TVDBid, season, os.path.basename(posterURL)))
    else: Log.Error("TVDBid '%s' is not found in xml file" % TVDBid)
  return TVDB4_dict

### Update meta field ###
def UpdateMetaField(metadata_root, metadata, meta_root, Priority_dict, meta_field, meta_source, movie):
  
  if meta_field not in meta_root:  Log.Info("meta field: '%s' not in meta_root" % meta_field);  return
  meta_old       = getattr( metadata, meta_field, None)
  meta_new       = meta_root[meta_field]
  meta_new_short = (meta_new[:80]).replace("\n", " ")+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
  
  ### Prepare data for comparison ###
  meta_old_value = meta_old
  if isinstance(meta_new, list):
    if meta_field == 'roles':  meta_old_value=[ {'role': role_obj.role,     'name': role_obj.name,     'photo': role_obj.photo    } for role_obj  in meta_old if role_obj.role]
    else:                      meta_old_value = [x for x in meta_old]
  try:
    if meta_field == 'originally_available_at' and isinstance(meta_new, basestring):  meta_new = Datetime.ParseDate(meta_new).date()
    if meta_field == 'rating'                  and isinstance(meta_new, basestring):  meta_new = float(meta_new) if "." in meta_new else None
    #if meta_field == 'absolute_number'         and isinstance(meta_new, basestring):  meta_new = int(meta_new) if meta_new.isdigit() else meta_new
  except Exception as e:  Log.Info("[!] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: {value}  Exception: {error}".format(field=meta_field, source=meta_source, format=type(meta_old).__name__+"/"+type(meta_new).__name__, value=meta_new_short, error=e))
  
  ### Update ONLY IF REQUIRED ###
  if meta_new == meta_old_value or isinstance(meta_new, dict) and set(meta_new.keys()).issubset(meta_old.keys()) or isinstance(meta_new, list) and set(meta_new)== set(meta_old):
    Log.Info("[=] {field:<23}  {len:>4}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, len="({:>2})".format(len(meta_root[meta_field])) if isinstance(meta_root[meta_field], (list, dict)) else "", source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
  else:
    Log.Info("[{rank}] {field:<23}  {len:>4}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, len="({:>2})".format(len(meta_root[meta_field])) if isinstance(meta_root[meta_field], (list, dict)) else "", source=meta_source, rank=Priority_dict[meta_field].index(meta_source)+1, format=type(meta_new).__name__, value=meta_new_short))
    if isinstance(meta_new, list):  #meta_field in ('genres', 'collections', 'tags', 'roles'):
      if meta_old:          meta_old.clear()
      if meta_field == 'roles':
        for item in meta_new:
          meta_role = meta_old.new()
          for field in item:  setattr(meta_role, field, item[field])  #role, actor, name. photo
      else:
        meta_old = meta_new #meta_old.add(item)  #Lists: Tags, etc...
        Log.Info("meta_old: '%s'" % str(meta_old))
          
    elif isinstance(meta_new, dict):
      if meta_field in ['posters', 'art', 'themes', 'thumbs']:  # Can't access MapObject, so have to write these out
        for url in meta_new:
          if not url in meta_old and isinstance(meta_new[url], tuple):
            metadata_download(metadata_root, meta_old, url, meta_new[url][0], meta_new[url][1], meta_new[url][2])
    else:
      if meta_field == 'rating' and isinstance(meta_new, float):  metadata.rating=meta_new
      else:
        try:     meta_old = meta_new
        except:  Log.Info("[!] {field:<23}  {len:>4}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, len="({:>2})".format(len(meta_root[meta_field])) if isinstance(meta_root[meta_field], (list, dict)) else "", source=meta_source, format=type(meta_old).__name__+"/"+type(meta_new).__name__, value=meta_new_short))
    #Log.Info("[=] {field:<23}  {len:>4}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, len="({:>2})".format(len(meta_root[meta_field])) if isinstance(meta_root[meta_field], (list, dict)) else "", source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
    
### Update all metadata from a list of Dict according to set priorities ##############################################################################
def UpdateMeta(metadata, MetaSources, movie):
  # [=] already at the right value for that source   # [x] Xst/nd/th source had the field   # [?] Tests, unsure
  # [#] no source for that field                     # [!] Error assigning
  Log.Info("".ljust(157, '-'))
  Log.Info("Plex.UpdateMeta() - Metadata Sources with fields")
  for source in MetaSources:
    if MetaSources[source]:  Log.Info("- {source:<11}      : {fields}".format(source=source, fields =' | '.join('{:<23} ({:>3})'.format(field, len(MetaSources[source][field]) if isinstance(MetaSources[source][field], (list, dict)) else 1) for field in MetaSources[source])))
    if 'seasons' in MetaSources[source]:
      season_fields, episode_fields, ep_nb, ep_invalid = {}, {}, 0, 0
      for season in MetaSources[source]['seasons']:
        for field in MetaSources[source]['seasons'][season]:
          if field in SeasonPriority:  season_fields[field] = (season_fields[field] + 1) if field in season_fields else 1
        for episode in MetaSources[source]['seasons'][season]['episodes'] if 'episodes' in MetaSources[source]['seasons'][season] else []:
          for field in MetaSources[source]['seasons'][season]['episodes'][episode]:
            if field in EpisodePriority:  episode_fields[field] = (episode_fields[field] + 1) if field in episode_fields else 1
            else:                         Log.Info("Field Unrecognised: '%s'" % field); ep_invalid+=1
          ep_nb+=1
      if len(season_fields ):  Log.Info("  - Seasons   ({nb:>3}): {fields}".format(nb=len(MetaSources[source]['seasons']), fields =' | '.join('{:<23} ({:>3})'.format(field,  season_fields[field]) for field in  season_fields)))
      if len(episode_fields):  Log.Info("  - Episodes  ({nb:>3}): {fields}".format(nb=ep_nb-ep_invalid                   , fields =' | '.join('{:<23} ({:>3})'.format(field, episode_fields[field]) for field in episode_fields)))
  Log.Info("".ljust(157, '-'))
  
  Log.Info("Plex.UpdateMeta() - Metadata Fields")
  for meta_field in SeriePriority:
    meta_old       = getattr( metadata, meta_field, None)
    for meta_source in SeriePriority[meta_field]:  # Loop through the metadata source (ordered immutable) tuple ("AniDB", "TheTVDB", ...)
      if meta_source in MetaSources and meta_field in MetaSources[meta_source] and MetaSources[meta_source][meta_field]:
        UpdateMetaField(metadata, metadata, MetaSources[meta_source], Moviepriority if movie else SeriePriority, meta_field, meta_source, movie)
        if meta_field not in ['posters', 'art', 'banners', 'themes', 'thumbs']:  break
    
  if not movie:
    ### Seasons ###
    for season in sorted(metadata.seasons, key=natural_sort_key):  # For each season
      if not season:  continue  #empty key
      Log.Info("metadata.seasons[%2s]." % (season))
      for meta_field in SeasonPriority:                 # Get a field
        meta_old       = getattr( metadata, meta_field, None)
        for meta_source in SeasonPriority[meta_field]:  # Loop through the metadata source (ordered immutable) tuple ("AniDB", "TheTVDB", ...)
          if meta_source in MetaSources and 'seasons' in MetaSources[meta_source] and season in MetaSources[meta_source]['seasons'] and meta_field in MetaSources[meta_source]['seasons'][season] and MetaSources[meta_source]['seasons'][season][meta_field]:
            UpdateMetaField(metadata, metadata.seasons[season], MetaSources[meta_source]['seasons'][season], SeasonPriority, meta_field, meta_source, movie)
            if meta_field not in ['posters', 'art', 'banners', 'themes', 'thumbs']:  break
        #else:  Log.Info("[#] {field:<23}  Type: {format:<20}".format(field=meta_field, format=type(meta_old).__name__))
          
      ### Episodes ###
      for episode in sorted(metadata.seasons[season].episodes, key=natural_sort_key):
        Log.Info("metadata.seasons[%2s].episodes[%3s]." % (season, episode))
        for meta_field in EpisodePriority:                 # Get a field
          meta_old       = getattr( metadata, meta_field, None)
          for meta_source in EpisodePriority[meta_field]:
            if meta_source in MetaSources and 'seasons' in MetaSources[meta_source] and season in MetaSources[meta_source]['seasons'] and \
            'episodes' in MetaSources[meta_source]['seasons'][season] and episode in MetaSources[meta_source]['seasons'][season]['episodes'] and \
            meta_field in MetaSources[meta_source]['seasons'][season]['episodes'][episode] and MetaSources[meta_source]['seasons'][season]['episodes'][episode][meta_field]:
              UpdateMetaField(metadata, metadata.seasons[season].episodes[episode], MetaSources[meta_source]['seasons'][season]['episodes'][episode], EpisodePriority, meta_field, meta_source, movie)
              if meta_field not in ['posters', 'art', 'banners', 'themes', 'thumbs']:  break
          #else:  Log.Info("[#] {field:<23}  Type: {format:<20}".format(field=meta_field, format=type(meta_old).__name__))
    Log.Info("".ljust(157, '-'))
