### common ### #@parallelize @task
import os, re, inspect, json, unicodedata, datetime, time  # datetime.datetime.now() 
from string import maketrans

### Variables, accessible in this module (others if 'from common import xxx', or 'import common.py' calling them with 'common.Variable_name' ###
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
RESTRICTED_GENRE     = {'X': ["18 restricted", "pornography"], 'TV-MA': ["tv censoring", "borderline porn"]}
MOVIE_RATING_MAP     = {'TV-Y': 'G', 'TV-Y7': 'G', 'TV-G': 'G', 'TV-PG': 'PG', 'TV-14': 'PG-13', 'TV-MA': 'NC-17', 'X': 'X'}
#MyAnimeList_to_US_rating = {"G"    : "TV-Y7", # All Ages
#                            "PG"   : "TV-G",  # Children
#                            "PG-13": "TV-PG", # Teens 13 or older
#                            "R"    : "TV-14", # 17+ recommended (violence & profanity)
#                            "R+"   : "TV-MA", # Mild Nudity (may also contain violence & profanity)
#                            "Rx"   : "NC-17"} # Hentai (extreme sexual content/nudity)
#metadata.content_rating = options[ metadata.content_rating.split(" - ",1)[0] ]
Log.Info("1 - " + inspect.stack()[0][1])
Log.Info("2 - " + inspect.getfile(inspect.currentframe()))
  
### Get attribute from xml tag - from common import getElementText to use without 'common.' pre-pended ###
def getElementText(el, xp):
  return el.xpath(xp)[0].text if el and el.xpath(xp) and el.xpath(xp)[0].text else "" 

### Save file in Plex Media Server\Plug-in Support\Data\com.plexapp.agents.hama\DataItems creating folder(s) ###
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
    if file_time+cache < time.time():  too_old = True;  Log.Debug("LoadFile() - CacheTime: '{time}', Limit: '{limit}' Filename: '{file}' needs reloading..".format(file=filename, time=time.ctime(file_time), limit=time.ctime(time.time() - cache)))
    else:          file = Data.Load(relativeFilename);  Log.Debug("LoadFile() - CacheTime: '{time}', Limit: '{limit}' Filename: '{file}' loaded from cache".format(file=filename, time=time.ctime(file_time), limit=time.ctime(time.time() - cache)))
  else:  Log.Debug("LoadFile() - Filename: '{file}', Directory: 'path' does not exists in cache".format(file=filename, path=relativeDirectory))
  if not file:
    netLock.acquire()
    if url.startswith(ANIDB_HTTP_API_URL):
      if AniDB_WaitUntil > datetime.datetime.now():  Log("LoadFile() - AniDB AntiBan Delay, next download window: '%s'" % AniDB_WaitUntil)    
      while AniDB_WaitUntil > datetime.datetime.now():  time.sleep(1)
      AniDB_WaitUntil = datetime.datetime.now() + datetime.timedelta(seconds=3)
    try:                    file = str(HTTP.Request(url, headers={'Accept-Encoding':'gzip', 'content-type':'charset=utf8'}, timeout=20, cacheTime=cache))                                     # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find'
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
    try:     file, converted = json.loads(file), True
    except:  pass
  return file

#########################################################################################################################################################
def metadata_download (metatype, url, num=99, filename="", url_thumbnail=None):
  if url in metatype:  Log.Info("url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))
  else:
    file, status = None, ""
    if filename and Data.Exists(filename):  file = Data.Load(filename); status += ", Found locally"
    else:
      try:                    file = HTTP.Request(url_thumbnail if url_thumbnail else url, cacheTime=None).content
      except Exception as e:  Log.Error("error downloading, Exception: '%s'" % e); return
      if file:                status += ", Downloaded";  SaveFile(filename, file);  status += "Saved locally"
    if file:
      try:                    metatype[ url ] = Proxy.Preview(file, sort_order=num) if url_thumbnail else Proxy.Media(file, sort_order=num) # or metatype[ url ] != proxy_item # proxy_item = 
      except Exception as e:  Log.Error("issue adding picture to plex - url downloaded: '%s', filename: '%s', Exception: '%s'" % (url_thumbnail if url_thumbnail else url, filename, e)) #metatype.validate_keys( url_thumbnail if url_thumbnail else url ) # remove many posters, to avoid
      else:                   Log.Info( "url: '%s', num: '%d', filename: '%s'%s" % (url, num, filename, status))
  
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
  #                [translate(text(),"ABCDEFGHJIKLMNOPQRSTUVWXYZ 0123456789 .` :;", "abcdefghjiklmnopqrstuvwxyz 0123456789 .' ")="%s"
  #               or contains(translate(text(),"ABCDEFGHJIKLMNOPQRSTUVWXYZ 0123456789 .` :;", "abcdefghjiklmnopqrstuvwxyz 0123456789 .' "),"%s")]""" % (Name.lower().replace("'", "\'"), Name.lower().replace("'", "\'")))
def CleanTitle(title):
  DeleteChars  = ""
  ReplaceChars = maketrans("`:;-~.,/*?", "'         ")
  return " ".join(str(unicodedata.normalize('NFC', unicode(title.lower()))).translate(ReplaceChars, DeleteChars).split())  # str needed for translate

def write_logs(media, movie, error_log, metadata_id_source_core, metadata_id_number, anidbid, tvdbid):
  """
  ### HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems ###
  """
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
    Log.Debug("Locked '%s' %s" % (log, error_log_locked[log]))
    
    error_log_array, log_prefix = {}, ""
    if Data.Exists(log+".htm"):
      for line in Data.Load(log+".htm").split(log_line_separator):
        if "|" in line: error_log_array[line.split("|", 1)[0].strip()] = line.split("|", 1)[1].strip()
    Log.Debug("error_log_array: '%s'" % str(error_log_array))
    if log == 'TVDB posters missing': log_prefix = WEB_LINK % ("http://thetvdb.com/wiki/index.php/Posters",              "Restrictions") + log_line_separator
    if log == 'Plex themes missing':  log_prefix = WEB_LINK % ("https://plexapp.zendesk.com/hc/en-us/articles/201572843","Restrictions") + log_line_separator
    for entry in error_log[log]:  error_log_array[entry.split("|", 1)[0].strip()] = entry.split("|", 1)[1].strip()
    #import AniDB, tvdb
    if error_log[log] == []:
      if not log in ["Missing Episodes", "Missing Specials"]:                              keys = ["anidbid: %s" % (WEB_LINK % (ANIDB_SERIE_URL % anidbid, anidbid)), "anidbid: %s" % anidbid, "tvdbid: %s" % (WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid ) ), "tvdbid: %s" % tvdbid]
      elif not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1):  keys = ["tvdbid: %s"  % (WEB_LINK % (TVDB_SERIE_URL  % tvdbid,  tvdbid) )]
      else:                                                                                keys = ["%sid: %s" % (metadata_id_source_core, WEB_LINK % (ANIDB_SERIE_URL % metadata_id_number if metadata_id_source_core == "anidb" else TVDB_SERIE_URL % metadata_id_number, metadata_id_number) )]
      for key in keys: 
        if key in error_log_array.keys():  del(error_log_array[key])
    Data.Save(log+".htm", log_prefix + log_line_separator.join(sorted([str(key)+" | "+str(error_log_array[key]) for key in error_log_array.keys()], key = lambda x: x.split("|",1)[1] if x.split("|",1)[1].strip().startswith("Title:") and not x.split("|",1)[1].strip().startswith("Title: ''") else int(re.sub("<[^<>]*>", "", x.split("|",1)[0]).strip().split()[1].strip("'")) )))
    error_log_locked[log] = [False, 0]
    Log.Debug("Unlocked '%s' %s" % (log, error_log_locked[log]))

### [tvdb4.posters.xml] Attempt to get the ASS's image data ###############################################################################################################
def getImagesFromASS(metadata, media, tvdbid, movie, num=0):
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
  entry = postersXml.xpath("/tvdb4entries/posters[@tvdbid='%s']" % tvdbid)
  if not entry: Log.Error("tvdbid '%s' is not found in xml file" % tvdbid); return
  for line in filter(None, entry[0].text.strip().replace("\r","\n").split("\n")):
    num += 1; seasonposternum += 1
    season, posterURL = line.strip().split("|",1); season = str(int(season)) #str(int(x)) remove leading 0 from number string
    posterPath = "seasons/%s-%s-%s" % (tvdbid, season, os.path.basename(posterURL))
    if movie or season not in media.seasons:  continue
    common.metadata_download (metadata.seasons[season].posters, posterURL, num, "TVDB/"+posterPath)
  return posternum, seasonposternum
 
