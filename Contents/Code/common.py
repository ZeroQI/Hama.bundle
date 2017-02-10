### common ### #@parallelize @task

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import os              #path.abspath, join, dirname
import inspect
import datetime
import time           # datetime.datetime.now() 
import re

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

MoviePriority   = { 'title'                   : ('AniDB', 'TheTVDB'),
                    'summary'                 : ('AniDB', 'TheTVDB'),
                    'original_title'          : ('AniDB', 'TheTVDB'),
                    'originally_available_at' : ('AniDB', 'TheTVDB'),
                    'rating'                  : ('AniDB', 'TheTVDB'),
                    'art'                     : ('AniDB', 'TheTVDB'),
                    'posters'                 : ('AniDB', 'TheTVDB'),
                    'themes'                  : ('AniDB', 'TheTVDB'),
                    'genres'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'tags'                    : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'collections'             : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'year'                    : ('AniDB', 'TheTVDB'),
                    'content_rating'          : ('AniDB', 'TheTVDB'),
                    'trivia'                  : ('AniDB', 'TheTVDB'),
                    'quotes'                  : ('AniDB', 'TheTVDB'),
                    'tagline'                 : ('TheMovieDB',)
                  } #16
SeriePriority   = { 'title'                   : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'), 
                    'original_title'          : ('AniDB', ),
                    'summary'                 : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'originally_available_at' : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'rating'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'studio'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'tagline'                 : (),
                    'countries'               : ('AniDB', 'TheTVDB'),
                    'duration'                : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'genres'                  : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'roles'                   : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    #'producers'               : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    #'directors'               : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    #'writers'                 : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'content_rating'          : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'collections'             : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'art'                     : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV'),
                    'posters'                 : ('AniDB', 'TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV', 'OMDb'),
                    'banners'                 : ('TheTVDB', 'MyAnimeList' 'TheMovieDB', 'FanartTV'),
                    'themes'                  : ('Plex',),
                  } #15
SeasonPriority  = { 'summary'                 : ('TheTVDB',),
                    'posters'                 : ('TheTVDB',),
                    'banners'                 : ('TheTVDB',),
                  } #5
EpisodePriority = { 'absolute_index'          : ('TheTVDB',),
                    'title'                   : ('AniDB', 'TheTVDB'),
                    'summary'                 : ('TheTVDB',),
                    'originally_available_at' : ('TheTVDB',),
                    'rating'                  : ('TheTVDB',),
                    'thumbs'                  : ('TheTVDB',),
                    'writers'                 : ('TheTVDB',),
                    'directors'               : ('TheTVDB',),
                    'producers'               : ('TheTVDB',)
                  } #9

Log.Info("1 - " + inspect.stack()[0][1])
Log.Info("2 - " + inspect.getfile(inspect.currentframe()))
  
### Code reduction one-liners that get imported specifically ###
def GetElementText(el, xp):  return el.xpath(xp)[0].text if el and el.xpath(xp) and el.xpath(xp)[0].text else ""   ### Get attribute from xml tag - from common import GetElementText to use without 'common.' pre-pended ###
def GetPosters (source=""):  return Prefs['Posters'] and not (Prefs['GetSingleOne'] and metadata_count['posters']) and (source=="" or source and Prefs[source])
def GetSeasons (source=""):  return Prefs['Seasons'] and not (Prefs['GetSingleOne'] and metadata_count['seasons']) and (source=="" or source and Prefs[source])
def GetFanarts (source=""):  return Prefs['Fanarts'] and not (Prefs['GetSingleOne'] and metadata_count['fanarts']) and (source=="" or source and Prefs[source])
def GetBanners (source=""):  return Prefs['Banners'] and not (Prefs['GetSingleOne'] and metadata_count['banners']) and (source=="" or source and Prefs[source])
#def GetKey     (obj, key ):  return obj[key] if key in obj else None   ### Get attribute from xml tag - from common import GetElementText to use without 'common.' pre-pended ###
     
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
    if file_time+cache < time.time():  too_old = True;  Log.Debug("LoadFile() - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' needs reloading..".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() - cache)))
    else:          file = Data.Load(relativeFilename);  Log.Debug("LoadFile() - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' loaded from cache".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() - cache)))
  else:  Log.Debug("LoadFile() - Filename: '{file}', Directory: 'path' does not exists in cache".format(file=filename, path=relativeDirectory))
  if not file:
    netLock.acquire()
    if url.startswith(ANIDB_HTTP_API_URL):
      if AniDB_WaitUntil > datetime.datetime.now():  Log("LoadFile() - AniDB AntiBan Delay, next download window: '%s'" % AniDB_WaitUntil)    
      while AniDB_WaitUntil > datetime.datetime.now():  time.sleep(1)
      AniDB_WaitUntil = datetime.datetime.now() + datetime.timedelta(seconds=3)
    try:                    file = str(HTTP.Request(url, headers={'Accept-Encoding':'gzip'}, timeout=20, cacheTime=cache))                                     # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find'
    except Exception as e:  file = None; Log.Warn("LoadFile() - issue loading url: '%s', filename: '%s', Exception: '%s'" % (url, filename, e))                                                           # issue loading, but not AniDB banned as it returns "<error>Banned</error>"
    finally:                netLock.release()
    if file:
      Log.Debug("LoadFile() - url: '{url} loaded".format(url=url))
      if len(file)>1024:  SaveFile(filename, file, relativeDirectory)
      elif str(file).startswith("<Element error at "):  Log.Error("Not an XML file, AniDB banned possibly, result: '%s'" % result); return None
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
def metadata_download(metadata, metatype, url, num=99, filename="", url_thumbnail=None):
  def GetMetadata(metatype): 
    if metatype==metadata.posters:             return "posters", GetPosters()
    if metatype==metadata.art:                 return "fanarts", GetFanarts()
    if metatype==metadata.banners:             return "banners", GetBanners()
    if metatype==metadata.themes:              return "themes",  Prefs['Themes']
    if filename.startswith("TVDB/episodes/"):  return "thumbs",  Prefs['Thumbs']
    return "seasons", GetSeasons() #Only one left, no need to get season number then for testing: metadata.seasons[season].posters
  string, test = GetMetadata(metatype)
  global metadata_count
  if url in metatype:  Log.Info("url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))
  elif not test:       Log.Info("url: '%s', num: '%d', filename: '%s' Not in Plex but threshold exceded" % (url, num, filename))
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
  global error_log_locked, error_log_lock_sleep
  log_line_separator = "<br />\r\n"
  for key in error_log.keys():
    if key not in error_log_locked.keys(): error_log_locked[key] = [False, 0]
  for log in error_log:
    num_of_sleep_sec = 0
    while error_log_locked[log][0]:
      Log.Warn("'%s' lock exists. Sleeping 1sec for lock to disappear." % log)
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
    if error_log[log]:  Log.Debug("write_logs() - '{log:<{width}}': {content}".format(log=log, width=max(map(len, error_log.keys())), content=str(error_log[log])))
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
def getImagesFromASS(metadata, media, TVDBid, movie, num=0):
  TVDB4_POSTERS_URL = 'http://rawgit.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.posters.xml'
  posternum, seasonposternum = 0, 0
  if movie: return
  try:
    s        = media.seasons.keys()[0]
    e        = media.seasons[s].episodes.keys()[0]
    dir_path = os.path.dirname(media.seasons[s].episodes[e].items[0].parts[0].file)
    dir_name = os.path.basename(dir_path)
    if    "[tvdb4-" not in dir_name and "tvdb4.id" not in os.listdir(dir_path): Log.Debug("Files are in a season folder (option 1)"); return
    elif  "tvdb4.mapping" in os.listdir(dir_path):                              Log.Debug("Files are in the series folder and has a mapping file (option 2)"); return
    else:                                                                       Log.Debug("Files are in the series folder and has no mapping file (option 3)")
  except Exception as e:  Log.Error("Issues in finding setup info as directories have most likely changed post scan into Plex, Exception: '%s'" % e)
  try:                    postersXml = XML.ElementFromURL( TVDB4_POSTERS_URL, cacheTime=CACHE_1HOUR * 24)
  except Exception as e:  Log.Error("Loading poster XML failed: '%s', Exception: '%s'"% (TVDB4_POSTERS_URL, e)); return
  else:                   Log.Info( "Loaded poster XML: '%s'" % TVDB4_POSTERS_URL)
  entry = postersXml.xpath("/tvdb4entries/posters[@TVDBid='%s']" % TVDBid)
  if not entry: Log.Error("TVDBid '%s' is not found in xml file" % TVDBid); return
  for line in filter(None, entry[0].text.strip().replace("\r","\n").split("\n")):
    num += 1; seasonposternum += 1
    season, posterURL = line.strip().split("|",1); season = str(int(season)) #str(int(x)) remove leading 0 from number string
    posterPath = "seasons/%s-%s-%s" % (TVDBid, season, os.path.basename(posterURL))
    if movie or season not in media.seasons:  continue
    common.metadata_download(metadata, metadata.seasons[season].posters, posterURL, num, "TVDB/"+posterPath)
  return posternum, seasonposternum

### Turn a string into a list of string and number chunks  "z23a" -> ["z", 23, "a"] - files.sort(key=natural_sort_key) ###############################
def natural_sort_key(s, ns_re=re.compile('([0-9]+)')):  return [int(text) if text.isdigit() else text.lower() for text in re.split(ns_re, s)]

def UpdateMeta_field(metadata, MetaSources, meta_source, meta_field):
  meta_new       = MetaSources[meta_source][meta_field]
  meta_old       = getattr( metadata, meta_field, None)
  meta_old_short = meta_old[:80]+'..' if isinstance(meta_old, basestring) and len(meta_old)> 80 else meta_old
  meta_new_short = meta_new[:60]+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
  if meta_new == meta_old:  
    Log.Info("[ ] {field:<{width}}  Format: {format:<22}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, width=max(map(len, SeriePriority.keys())), source=meta_source, format=type(meta_new), value=meta_new_short))
  else:
    Log.Info("[X] {field:<{width}}  Format: {format:<22}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, width=max(map(len, SeriePriority.keys())), source=meta_source, format=type(meta_new), value=meta_new_short))
    
    if isinstance(meta_new, list):  #meta_field in ('genres', 'collections', 'tags', 'roles'):
      if meta_field == 'roles':
        meta_role = meta_old.new()
        for role_dict in meta_new:
          for field in role_dict:  setattr(meta_role, field, role_dict[field])  #role, actor, name. photo
      else:  #Lists: Tags, etc...
        if  meta_old:  meta_old.clear()
        for item in meta_new:  meta_old.add(item)
    
    elif isinstance(meta_new, dict):
      if meta_field in ['posters', 'art', 'themes']:  # Can't access MapObject, so have to write these out
        for url in meta_new:
          if isinstance(meta_new[url], tuple):
            if not url in meta_old:  metadata_download(metadata, meta_old, url, meta_new[url][0], meta_new[url][1], meta_new[url][2])  #Log.Info("[X] ['posters', 'art', 'themes'] tuple: '%s'" % str(meta_new[url]))
            else: meta_old[url] = meta_new[url]
      else:  # Dict update
        for key in meta_new:  meta_old[key] = meta_new [key]  # for k,v in dict_value.iteritems()
    
    elif meta_field is 'originally_available_at':
      try:     meta_old.setcontent(Datetime.ParseDate(meta_new).date())
      except:  pass #continue
    
    elif meta_field in ('seasons', 'episodes'):
      Log.Info("meta_field is seasons/episodes: '%s', recursive load" % meta_field)
      #for item in meta_new:  UpdateMeta(meta_old[item], MetaSourceSeasons[item], MetaSourceEpisodes)
    else:  meta_old = meta_new
    
### Update all metadata from a list of Dict according to set priorities ##############################################################################
def UpdateMeta(metadata, MetaSources, movie):
  
  Log.Info("".ljust(157, '-'))
  Log.Info("Plex.UpdateMeta() - Metadata Sources with fields")
  for source in MetaSources:  Log.Info("- {source:<20} ({nb:>2}) [{fields}]".format(source=source, nb=len(MetaSources[source]), fields =' | '.join('{:<22} '.format(field) for field in MetaSources[source].keys())))
  Log.Info("".ljust(157, '-'))
  Log.Info("Plex.UpdateMeta() - Metadata Fields")
  for meta_field in SeriePriority:
    for meta_source in SeriePriority[meta_field]:  # Loop through the metadata source (ordered immutable) tuple ("AniDB", "TheTVDB", ...)
      if meta_source in MetaSources and meta_field in MetaSources[meta_source] and MetaSources[meta_source][meta_field]:
        meta_new       = MetaSources[meta_source][meta_field]
        meta_old       = getattr( metadata, meta_field, None)
        meta_old_short = meta_old[:80]+'..' if isinstance(meta_old, basestring) and len(meta_old)> 80 else meta_old
        meta_new_short = meta_new[:80]+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
        if meta_new == meta_old:  
          Log.Info("[ ] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
        else:
          Log.Info("[X] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
          
          if isinstance(meta_new, list):  #meta_field in ('genres', 'collections', 'tags', 'roles'):
            if meta_field == 'roles':
              meta_role = meta_old.new()
              for role_dict in meta_new:
                for field in role_dict:  setattr(meta_role, field, role_dict[field])  #role, actor, name. photo
            else:  #Lists: Tags, etc...
              if  meta_old:  meta_old.clear()
              for item in meta_new:  meta_old.add(item)
          
          elif isinstance(meta_new, dict):
            if meta_field in ['posters', 'art', 'themes']:  # Can't access MapObject, so have to write these out
              for url in meta_new:
                if isinstance(meta_new[url], tuple):
                  if not url in meta_old:  metadata_download(metadata, meta_old, url, meta_new[url][0], meta_new[url][1], meta_new[url][2])  #Log.Info("[X] ['posters', 'art', 'themes'] tuple: '%s'" % str(meta_new[url]))
                else: meta_old[url] = meta_new[url]
            else:  # Dict update
              for key in meta_new:  meta_old[key] = meta_new [key]  # for k,v in dict_value.iteritems()
          
          elif meta_field is 'originally_available_at':
            try:     meta_old.setcontent(Datetime.ParseDate(meta_new).date())
            except:  continue
          
          else:  meta_old = meta_new
        break
  
  if movie:  pass
  else:
  
    ### test meta ###
    if not 'seasons' in MetaSources['TheTVDB']:   MetaSources['TheTVDB']['seasons'] = {}
    if "1" in MetaSources['TheTVDB']['seasons']:  MetaSources['TheTVDB']['seasons']["1"]['summary'] = "TheTVDB s1 summary test 1"
    else:                                         MetaSources['TheTVDB']['seasons']["1"] = {'summary': "TheTVDB s1 summary test 1"}
    
    ### Seasons ###
    #Log.Info("Plex.UpdateMeta() - Metadata Season Fields")
    for season in sorted(metadata.seasons, key=natural_sort_key):  # For each season
      Log.Info("metadata.seasons[%2s]." % (season))
      for meta_field in SeasonPriority:                 # Get a field
        for meta_source in SeriePriority[meta_field]:  # Loop through the metadata source (ordered immutable) tuple ("AniDB", "TheTVDB", ...)
          if meta_source in MetaSources and 'seasons' in MetaSources[meta_source] and season in MetaSources[meta_source]['seasons'] and meta_field in MetaSources[meta_source]['seasons'][season] and MetaSources[meta_source]['seasons'][season][meta_field]:
            meta_old       = getattr( metadata.seasons[season], meta_field, None)
            meta_old_short = meta_old[:80]+'..' if isinstance(meta_old, basestring) and len(meta_old)> 80 else meta_old
            meta_new       = MetaSources[meta_source]['seasons'][season][meta_field]
            meta_new_short = meta_new[:80]+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
            if meta_new == meta_old:  
              Log.Info("[O] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
            else:
              Log.Info("[X] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
            break
        #else:
        #  Log.Info(    "[ ] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=str(SeasonPriority[meta_field]), format=type(meta_old).__name__, value=meta_old_short))
          
      ### Episodes ###
      for episode in sorted(metadata.seasons[season].episodes, key=natural_sort_key):
        Log.Info("metadata.seasons[%2s].episodes[%3s]." % (season, episode))
        for meta_field in EpisodePriority:                 # Get a field
          for meta_source in EpisodePriority[meta_field]:
            if meta_source in MetaSources and 'seasons' in MetaSources[meta_source] and season in MetaSources[meta_source]['seasons'] and episode in MetaSources[meta_source]['seasons'][season] and meta_field in MetaSources[meta_source]['seasons'][season][episode] and MetaSources[meta_source]['seasons'][season][episode][meta_field]:
              meta_old       = getattr( metadata.seasons[season].episodes[episode], meta_field, None)
              meta_old_short = meta_old[:80]+'..' if isinstance(meta_old, basestring) and len(meta_old)> 80 else meta_old
              meta_new       = MetaSources[meta_source]['seasons'][season][episode][meta_field]
              meta_new_short = meta_new[:80]+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
              if meta_new == meta_old:
                Log.Info("[O] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
              else:
                Log.Info("[X] {field:<23}  Type: {format:<20}  Source: {source:<11}  Value: '{value}'".format(field=meta_field, source=meta_source, format=type(meta_new).__name__, value=meta_new_short))
              break  
         # else:
         #   Log.Info(    "[ ] {field:<23}  Type: {format:<20}".format(field=meta_field, format=type(meta_old).__name__))
          
    ### Closing ###
    Log.Info("".ljust(157, '-'))
