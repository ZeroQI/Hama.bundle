### common ### #@parallelize @task
# https://www.python.org/dev/peps/pep-0008/
# https://github.com/plexinc-agents/PlexMovie.bundle/blob/master/Contents/Code/__init__.py
#  audience rating line 940

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import os              #path.abspath, join, dirname
import inspect         # getfile, currentframe
import time            # datetime.datetime.now() 
import re
import logging
import datetime        # datetime.now
from io     import open
from string import maketrans
from lxml   import etree                                  # fromstring
try:                 from urllib.request import urlopen # urlopen Python 3.0 and later
except ImportError:  from urllib2        import urlopen # urlopen Python 2.x #import urllib2 # urlopen

### Variables, accessible in this module (others if 'from common import xxx', or 'import common.py' calling them with 'common.Variable_name' ###
strptime          = datetime.datetime.strptime #avoid init crash on first use in threaded environment  #dt.strptime(data, "%Y-%m-%d").date()
PlexRoot          = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "..", "..", "..", ".."))
CachePath         = os.path.join(PlexRoot, "Plug-in Support", "Data", "com.plexapp.agents.hama", "DataItems")
downloaded        = {'posters':0, 'art':0, 'seasons':0, 'banners':0, 'themes':0, 'thumbs': 0} 
AniDB_WaitUntil   = datetime.datetime.now() 
netLock           = Thread.Lock()
netLocked         = {}
WEB_LINK          = "<a href='%s' target='_blank'>%s</a>"
TVDB_SERIE_URL    = 'http://thetvdb.com/?tab=series&id='
ANIDB_SERIE_URL   = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid='
DefaultPrefs      = ("SerieLanguagePriority", "EpisodeLanguagePriority", "MinimumWeight", "localart", "adult", "GetSingleOne", 'OMDbApiKey') #"Simkl", 
FieldListMovies   = ('original_title', 'title', 'roles', 'year', 'originally_available_at', 'studio', 'tagline', 'summary', 'content_rating', 'content_rating_age',
                     'producers', 'directors', 'writers', 'countries', 'posters', 'art', 'themes', 'rating', 'quotes', 'trivia')
FieldListSeries   = ('genres', 'tags' , 'collections', 'duration', 'rating', 'title', 'summary', 'originally_available_at', 'reviews', 'extras', 'countries', 'rating_count',
                     'content_rating', 'studio', 'countries', 'posters', 'banners', 'art', 'themes', 'roles', 'original_title', 'title_sort',
                     'rating_image', 'audience_rating', 'audience_rating_image')  # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDb.bundle/blob/master/Contents/Code/__init__.py
FieldListSeasons  = ('summary', 'posters', 'art')
FieldListEpisodes = ('title', 'summary', 'originally_available_at', 'writers', 'directors', 'producers', 'guest_stars', 'rating', 'thumbs', 'duration', 'content_rating', 'content_rating_age', 'absolute_index') #'titleSort
SourceList        = ('AniDB', 'MyAnimeList', 'FanartTV', 'OMDb', 'TheTVDB', 'TheMovieDb', 'Plex', 'AnimeLists', 'tvdb4', 'TVTunes', 'Local') #"Simkl", 
Movie_to_Serie_US_rating = {"G"    : "TV-Y7", "PG"   : "TV-G", "PG-13": "TV-PG", "R"    : "TV-14", "R+"   : "TV-MA", "Rx"   : "NC-17"}

### Plex Library XML ###
PLEX_LIBRARY, PLEX_LIBRARY_URL = {}, "http://127.0.0.1:32400/library/sections/"    # Allow to get the library name to get a log per library https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token
Log.Info("test library: "+PlexRoot)  #Log.Info(file)
if os.path.isfile(os.path.join(PlexRoot, "X-Plex-Token.id")):
  Log.Info("'X-Plex-Token.id' file present")
  token_file=Data.Load(os.path.join(PlexRoot, "X-Plex-Token.id"))
  if token_file:
    PLEX_LIBRARY_URL += "?X-Plex-Token=" + token_file.strip()
    #Log.Info(PLEX_LIBRARY_URL) ##security risk if posting logs with token displayed
try:
  library_xml = etree.fromstring(urlopen(PLEX_LIBRARY_URL).read())
  for library in library_xml.iterchildren('Directory'):
    for path in library.iterchildren('Location'):
      PLEX_LIBRARY[path.get("path")] = library.get("title")
      Log.Info( path.get("path") + " = " + library.get("title") )
except Exception as e:  Log.Info("Place correct Plex token in X-Plex-Token.id file in logs folder or in PLEX_LIBRARY_URL variable to have a log per library - https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token" + str(e))
 
### Get media directory ###
def GetMediaDir (media, movie):
  if movie:  return os.path.dirname(media.items[0].parts[0].file)
  else:
    for s in media.seasons if media else []: # TV_Show:
      for e in media.seasons[s].episodes:
        return os.path.dirname(media.seasons[s].episodes[e].items[0].parts[0].file)

### Get media root folder ###
def GetLibraryRootPath(dir):
  library, root, path = '', '', ''
  for root in [os.sep.join(dir.split(os.sep)[0:x+2]) for x in range(0, dir.count(os.sep))]:
    if root in PLEX_LIBRARY:  library, path = PLEX_LIBRARY[root], os.path.relpath(dir, root); break
  else:  #401 no right to list libraries (windows)
    filename = os.path.join(CachePath, '_Logs', '_root_.scanner.log')
    if os.path.isfile(filename):
      with open(filename, 'r') as file:  line=file.read()
      for root in [os.sep.join(dir.split(os.sep)[0:x+2]) for x in range(dir.count(os.sep)-1, -1, -1)]:
        if "root: '{}'".format(root) in line:   library, path = '', os.path.relpath(dir, root).rstrip('.'); break
      else:  library, path, root = '', '_unknown_folder', '';  Log.Debug("root not found")
    Log.Debug("GetLibraryRootPath() - library: '{}', path: '{}', root: '{}', dir:'{}', PLEX_LIBRARY: '{}'".format(library, path, root, dir, str(PLEX_LIBRARY)))
  return library, root, path

### Check config files on boot up then create library variables ###    #platform = xxx if callable(getattr(sys,'platform')) else "" 
if not os.path.isdir(PlexRoot):
  path_location = { 'Windows': '%LOCALAPPDATA%\\Plex Media Server',
                    'MacOSX':  '$HOME/Library/Application Support/Plex Media Server',
                    'Linux':   '$PLEX_HOME/Library/Application Support/Plex Media Server' }
  PlexRoot = os.path.expandvars(path_location[Platform.OS.lower()] if Platform.OS.lower() in path_location else '~')  # Platform.OS:  Windows, MacOSX, or Linux

### Logging class to join scanner and agent logging per serie
# 
# Scanner:
#  - from "../../Plug-ins/Hama.bundle/Contents/code/common" import PlexLog
#  - log = PlexLog(file='root/folder/[anidb2-xxxx].log', isAgent=False)
# Agent:    log = common.PlexLog(file='mytest.log', isAgent=True )
# Useage:   log.debug('some debug message: %s', 'test123')
class PlexLog(object):
  Log.Info(str(dir(logging)))  # %(asctime)-15s (%(thread)+9x/%(module)-15s/%(funcName)-18s/%(lineno)4d) %(levelname)-8s 
  def __init__ (self, media=None, movie=False, search=False, isAgent = True, log_format='%(message)s', file="", mode='w', maxBytes=4*1024*1024, backupCount=5, encoding=None, delay=False, enable_debug=True):
  
    if not file:
      dir                 = GetMediaDir(media, movie)
      library, root, path = GetLibraryRootPath(dir)#Get movie or serie episode folder location      
      extension           = '.agent-search.log' if search else '.agent-update.log'
      LOGS_PATH, file, mode = os.path.join(CachePath, '_Logs', library), path.split(os.sep, 1)[0]+extension, 'a' if path=='_unknown_folder' else 'w'
      if not os.path.exists(LOGS_PATH):  os.makedirs(LOGS_PATH);  Log.Debug("common.PlexLog() - folder: '{}', directory absent".format(LOGS_PATH))
      file = os.path.join(LOGS_PATH, file)
      Log.Debug("Log file: " + file)
    try:
      log = logging.getLogger()                                      # update root logging's handler
      for handler in log.handlers:  log.removeHandler(handler)       # remove all old handlers
      new_handler = logging.handlers.RotatingFileHandler(file, mode=mode or 'w', maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)
      new_handler.setFormatter(logging.Formatter(log_format))        # Set log format
      log.addHandler(new_handler)                                    # set the new handler
      log.setLevel(logging.DEBUG if enable_debug else logging.INFO)  # update level
    except IOError, e:  self.error('updateLoggingConfig: failed to set logfile: %s', str(e))
    self.isAgent = isAgent
  def debug    (self, msg, *args, **kwargs):  (Log.Debug    if self.isAgent else logging.debug   ) (msg, *args, **kwargs)  #def debug    (self, msg, *args, **kwargs):  LOG[DEBUG   ][self.isAgent](msg, *args, **kwargs)
  def info     (self, msg, *args, **kwargs):  (Log.Info     if self.isAgent else logging.info    ) (msg, *args, **kwargs)
  def warning  (self, msg, *args, **kwargs):  (Log.Warning  if self.isAgent else logging.warning ) (msg, *args, **kwargs)
  def error    (self, msg, *args, **kwargs):  (Log.Error    if self.isAgent else logging.error   ) (msg, *args, **kwargs)
  def critical (self, msg, *args, **kwargs):  (Log.Critical if self.isAgent else logging.critical) (msg, *args, **kwargs)
  def stop     (self                      ):
    log = logging.getLogger()                                      # update root logging's handler
    for handler in log.handlers:  log.removeHandler(handler)

### Code reduction one-liners that get imported specifically ###
def GetMeta         (source="", field=""            ):  return (not Prefs['GetSingleOne'] or downloaded[field]<=1) and (not source or source in Prefs['posters' if field=='seasons' else field]) and not Prefs['posters' if field=='seasons' else field]=="None"  #not Prefs['GetSingleOne'] or downloaded[field    ]>0 fails randomly due to downloaded emptied  #Log.Info("test - downloaded[field]: {}, downloaded: {}".format(downloaded[field]<=1, downloaded))
def GetXml          (xml,      field                ):  return xml.xpath(field)[0].text if xml.xpath(field) and xml.xpath(field)[0].text not in (None, '', 'N/A', 'null') else ''  #allow isdigit() checks
def natural_sort_key(s):  return [int(text) if text.isdigit() else text for text in re.split(re.compile('([0-9]+)'), str(s).lower())]  # list.sort(key=natural_sort_key) #sorted(list, key=natural_sort_key) - Turn a string into string list of chunks "z23a" -> ["z", 23, "a"]
def urlFilename     (url):                              return "/".join(url.split('/')[3:])
def urlDomain       (url):                              return "/".join(url.split('/')[:3])
def replaceList     (string, a,b, *args):
  for index in a:  string.replace(a[index], b[index], *args)
  return string

### Return dict value if all fields exists "" otherwise (to allow .isdigit()), avoid key errors
def Dict(var, *arg, **kwarg):  #Avoid TypeError: argument of type 'NoneType' is not iterable
  """ Return the value of an (imbricated) dictionnary, return "" if doesn't exist unless "default=new_value" specified as end argument
      Ex: Dict(variable_dict, 'field1', 'field2', default = 0)
  """
  for key in arg:
    if isinstance(var, dict) and key and key in var:  var = var[key]
    else:  return kwarg['default'] if kwarg and 'default' in kwarg else ""   # Allow Dict(var, tvdbid).isdigit() for example
  return kwarg['default'] if var in (None, '', 'N/A', 'null') and kwarg and 'default' in kwarg else "" if var in (None, '', 'N/A', 'null') else var

### Save non null value in imbricated dict without error if not created yet, add if destination exist and is a list
def SaveDict(value, var, *arg):
  """ Save value to a Dictionary field (can be imbricated) and if value is a list, it exten the lsit instead
      # ex: SaveDict(GetXml(ep, 'Rating'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating')
      # ex: SaveDict(Dict(TheTVDB_dict, 'title'), TheTVDB_dict, 'title_sort')
      # ex: SaveDict(genre1,                      TheTVDB_dict, genre) to add    to current list
      # ex: SaveDict([genre1, genre2],            TheTVDB_dict, genre) to extend to current list
  """
  if not value:  return ""  # update dict only as string would revert to pre call value being immutable
  if not arg and (isinstance(var, list) or isinstance(var, dict)):
    if not (isinstance(var, list) or isinstance(var, dict)):  var = value
    elif isinstance(value, list) or isinstance(value, dict):  var.extend (value)
    else:                                                     var.append (value)
    return value
    
  for key in arg[:-1]:
    if not isinstance(var, dict):  return ""
    if not key in var:  var[key] = {}
    var = var[key]
  if not arg[-1] in var or not isinstance(var[arg[-1]], list):  var[arg[-1]] = value
  elif isinstance(value, list) or isinstance(value, dict):      var[arg[-1]].extend (value)
  else:                                                         var[arg[-1]].append (value)
  return value
  
### Gives HTTP status code using header info only ##########################################################################################################################
def GetStatusCode(url):
    """ This function retreives the status code of a website by requesting HEAD data from the host.
        This means that it only requests the headers. If the host cannot be reached or something else goes wrong, it returns None instead.
        urllib.parse.quote(string, safe='/', encoding=None, errors=None)
        - string:   string your trying to encode
        - safe:     string contain characters to ignore. Defualt is '/'
        - encoding: type of encoding url is in. Default is utf-8
        - errors:   specifies how errors are handled. Default is 'strict' which throws a UnicodeEncodeError, I think.
        #host = "/".join(url.split('/', 3)[:-1])  #path = url.replace(" ", "%20").split('/', 3)[3]  #Log.Info("host: '%s', path: '%s'" % (host, path))
    """ 
    try:
      import urllib2
      request            = urllib2.Request(url) #urllib.quote #urllib2.quote(url,':/')
      request.get_method = lambda: 'HEAD'
      return urllib2.urlopen(request).getcode() # if "Content-Type: audio/mpeg" in response.info(): Log.Info("Content-Type: audio/mpeg")
    except Exception as e:  return str(e)
  
### Save file to cache
def SaveFile(filename="", file="", relativeDirectory=""):  #Thanks Dingmatt for folder creation ability
  #Log.Debug("common.SaveFile() - file: "+filename)
  relativeFilename            = os.path.join (relativeDirectory, filename) 
  relativeDirectory, filename = os.path.split(relativeFilename) #if os.sep in filename:
  fullpathDirectory           = os.path.abspath(os.path.join(CachePath, relativeDirectory))
  if os.path.exists(fullpathDirectory):  Log.Debug("common.SaveFile() - CachePath: '{path}', file: '{file}', directory present".format(path=CachePath, file=relativeFilename))
  else:
    try:                    os.makedirs(fullpathDirectory)
    except Exception as e:  Log.Debug("common.SaveFile() - CachePath: '{path}', file: '{file}', directory absent, exception: {exception}".format(path=CachePath, file=relativeFilename, exception=e))
    else:                   Log.Debug("common.SaveFile() - CachePath: '{path}', file: '{file}', directory absent.".format(path=CachePath, file=relativeFilename))
  try:                    Data.Save(relativeFilename, file)
  except Exception as e:  Log.Info("common.SaveFile() - Exception: {exception}, relativeFilename: '{relativeFilename}'".format(exception=e, relativeFilename=relativeFilename))
  
  #if os.path.exists(fullpathDirectory): Log.Debug("common.SaveFile() - path exist")
  #else:                                 Log.Debug("common.SaveFile() - path does not exist: " + fullpathDirectory)

### Load file in Plex Media Server\Plug-in Support\Data\com.plexapp.agents.hama\DataItems if cache time not passed ###
def LoadFile(filename="", relativeDirectory="", url="", cache=CACHE_1DAY*6):  #By Dingmatt, heavily moded
  ANIDB_HTTP_API_URL = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='  # this prevent CONSTANTS.py module loaded on every module, only common.py loaded on modules and all modules on __init__.py
  relativeFilename   = os.path.join(relativeDirectory, filename) 
  fullpathFilename   = os.path.abspath(os.path.join(CachePath, relativeDirectory, filename))
  too_old, converted = False, False
  file               = None
  global AniDB_WaitUntil
  if filename.endswith(".xml.gz"):  filename = filename[:-3] #anidb title database
  # missing_meta = False  # data in agent dict
  #  if missing_meta and its info is not in cache file and
  #    ( prev 7 days=< date - ep release date<= 14 days or #everyday refresh within 7 days of new release
  #      date - cache_file_date >= 7 days and serie in progress or   # every 7 days afterwards if in progress
  #      serie not in progress and date - cache_file_date >= 90 days )  #every 3 months if terminated
  if relativeFilename and Data.Exists(relativeFilename) and os.path.isfile(fullpathFilename):       
    file_time = os.stat(fullpathFilename).st_mtime
    if file_time+cache < time.time():  too_old = True;  Log.Debug("common.LoadFile() - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' needs reloading..".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() + cache)))
    else:          file = Data.Load(relativeFilename);  Log.Debug("common.LoadFile() - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' loaded from cache".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() + cache)))
  else:  Log.Debug("common.LoadFile() - Filename: '{file}', Directory: '{path}', url: '{url}' does not exists in cache".format(file=filename, path=relativeDirectory, url=url))
  if not file:
    netLock.acquire()
    if url.startswith(ANIDB_HTTP_API_URL):
      if AniDB_WaitUntil > datetime.datetime.now():  Log("common.LoadFile() - AniDB AntiBan Delay, next download window: '%s'" % AniDB_WaitUntil)    
      while AniDB_WaitUntil > datetime.datetime.now():  time.sleep(1)
      AniDB_WaitUntil = datetime.datetime.now() + datetime.timedelta(seconds=4)
    try:                    file = str(HTTP.Request(url, headers={'Accept-Encoding':'gzip'}, timeout=20, cacheTime=cache))                                     # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find'
    except Exception as e:  file = None;       Log.Warn("common.LoadFile() - issue loading url: '%s', filename: '%s', Exception: '%s'" % (url, filename, e))                                                           # issue loading, but not AniDB banned as it returns "<error>Banned</error>"
    #else:                   Log.Info("common.LoadFile() - url loaded: '%s'" %url)
    finally:                netLock.release()
    if file:
      Log.Debug("LoadFile() - url: '{url}' loaded".format(url=url))
      if len(file)>1024:  SaveFile(filename, file, relativeDirectory)
      elif str(file).startswith("<Element error at "):  Log.Error("common.LoadFile() - Not an XML file, AniDB banned possibly, result: '%s'" % result); return None
      elif too_old:                                     file = Data.Load(relativeFilename) #present, cache expired but online version incorrect or not available
  try:     return XML.ElementFromString(file)
  except:  
    if type(file).__name__ == '_Element' or isinstance(file, basestring) and file.startswith('<?xml '):
      Log.Info("corrupted xml")
      import unicodedata
      try:     return XML.ElementFromString(file.decode('utf-8','ignore').replace('\b', '').encode("utf-8"))
      except:
        Log.Info("still corrupted xml after normalization")
        Data.Remove(relativeFilename)  #DELETE CACHE AS CORRUPTED
    else:
      try:     return JSON.ObjectFromString(file, encoding=None)
      except:  pass
  return file

### Download images and themes for Plex ###############################################################################################################################
def metadata_download(metadata, metatype, url, filename="", num=99, url_thumbnail=None):
  def GetMetadata(metatype): 
    if metatype==metadata.posters:             return "posters", GetMeta('', 'posters')
    if metatype==metadata.art:                 return "art",     GetMeta('', 'art')
    if metatype==metadata.banners:             return "banners", GetMeta('', 'banners')
    if metatype==metadata.themes:              return "themes",  Prefs['themes']
    if filename.startswith("TVDB/episodes/"):  return "thumbs",  Prefs['thumbs']
    return "seasons", True  #GetMeta('', 'posters') #Only one left, no need to get season number then for testing: metadata.seasons[season].posters
  
  string, test = GetMetadata(metatype)
  global downloaded
  if url in metatype:  Log.Info("url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))
  elif not test:       Log.Info("url: '%s', num: '%d', filename: '%s' Not in Plex but threshold exceded or thumbs/themes agent setting not selected" % (url, num, filename))
  else:
    file, status = None, ""
    if filename and Data.Exists(filename):  file = Data.Load(filename); status += ", Found locally"
    else:
      try:                    file = HTTP.Request(url_thumbnail if url_thumbnail else url, cacheTime=None).content                                  
      except Exception as e:  Log.Info("common.SaveFile() - Exception: {exception!s}, url: '{url}'".format(exception=e, url=url)); return
      if file:                status += ", Downloaded";  SaveFile(filename, file);  status += "Saved locally"
      elif 'thetvdb.com' in url:
        Log.Info("TheTVDB.com times out, using Plex server")
        try:                    file = HTTP.Request((url_thumbnail if url_thumbnail else url).replace('thetvdb.com', 'thetvdb.plexapp.com'), cacheTime=0).content
        except Exception as e:  Log.Info("common.SaveFile() - Exception: {exception!s}, url: '{url}'".format(exception=e, url=url)); return
    if file:
      try:                    metatype[ url ] = Proxy.Preview(file, sort_order=num) if url_thumbnail else Proxy.Media(file, sort_order=num) # or metatype[ url ] != proxy_item # proxy_item = 
      except Exception as e:  Log.Error("issue adding File to plex - url downloaded: '{}', filename: '{}', Exception: '{!s}'".format(url_thumbnail if url_thumbnail else url, filename, e)); return #metatype.validate_keys( url_thumbnail if url_thumbnail else url ) # remove many posters, to avoid
      #!#else:                   Log.Info( "url: '%s', num: '%d', filename: '%s' %s" % (url, num, filename, status))
  downloaded[string] = downloaded[string] + 1
  
### Cleanse title and translate anidb '`' ############################################################################################################
def cleanse_title(string):#def CleanTitle(title):
  import unicodedata
  DeleteChars  = ""
  ReplaceChars = maketrans("`:~/*?-.,", "         ") #.;_
  if len(string)<=len(String.StripDiacritics(string))+2:  string = String.StripDiacritics(string)  #else there is jap characters scrubebd outs
  try:       string2 = string.encode('ascii', 'replace')       # Encode into Ascii, prevent: UnicodeDecodeError: 'utf8' codec can't decode bytes in position 13-14: invalid continuation byte
  except:    pass
  else:      
    if not string2.count('?'): string=string2
  while re.match(".*\([^\(\)]*?\).*", string):  string = re.sub(r'\([^\(\)]*?\)', ' ', string)  
  return " ".join(str(unicodedata.normalize('NFC', unicode(string.lower()))).translate(ReplaceChars, DeleteChars).split())  # str needed for translate

  
### HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems ###
def write_logs(media, movie, error_log, metadata_id_source_core, metadata_id_number, AniDBid, TVDBid):
  Log.Info("".ljust(157, '-'))
  
  ### File lock ###
  global netLocked
  sleep_time_max = 10
  Log.Info("error_log: {}".format(error_log))
  for log in error_log:
    sleep_time = 0
    while log in netLocked and netLocked[log][0]:
      time.sleep(1)
      sleep_time += 1
      if sleep_time > sleep_time_max:
        Log.Error("Could not obtain the lock in {}sec & lock age is {}sec. Skipping log update.".format(sleep_time_max, int(time.time())-netLocked[1] if 1 in netLocked else "never"))
        continue #break #netLock.acquire()
    netLocked[log] = (True, int(time.time()))
  
    ### Load previous entries ###
    Log.Debug("common.write_logs() - {log:<{width}}: {content}".format(log=log, width=max(map(len, error_log)), content=str(error_log[log])))
    error_log_array    = {}
    log_line_separator = "<br />\r\n"
    if Data.Exists(os.path.join('_Logs', log+'.htm')):
      for line in Data.Load(os.path.join('_Logs', log+'.htm')).split(log_line_separator):
        if "|" in line:  error_log_array[line.split("|", 1)[0].strip()] = line.split("|", 1)[1].strip()
    
    ### Remove this serie entry ###
    keys    = ["AniDBid: "+AniDBid, "AniDBid: "+WEB_LINK % (ANIDB_SERIE_URL + AniDBid, AniDBid), "TVDBid: "+ TVDBid, "TVDBid: "+WEB_LINK % (TVDB_SERIE_URL + TVDBid, TVDBid)]
    deleted = []
    for key in keys:
      if key in error_log_array:
        deleted.append(error_log_array[key]) 
        del(error_log_array[key]) # remove entry, needs updating or removal...
    if not deleted and not error_log[log]:  netLocked[log] = (False, 0);  continue  # didn't delete anything, no entry to add, the only case when we skip
    
    ### Generate prefix, append to error_log_array and Save error_log_array ###
    log_prefix = ''
    if log == 'TVDB posters missing': log_prefix = WEB_LINK % ("http://thetvdb.com/wiki/index.php/Posters",              "Restrictions") + log_line_separator
    if log == 'Plex themes missing':  log_prefix = WEB_LINK % ("https://plexapp.zendesk.com/hc/en-us/articles/201572843","Restrictions") + log_line_separator
    for entry in error_log[log]:  error_log_array[entry.split("|", 1)[0].strip()] = entry.split("|", 1)[1].strip() if len(entry.split("|", 1))>=2 else ""
    import re
    Log.Info("error_log_array: {}".format(error_log_array))
    try:     Data.Save(os.path.join('_Logs', log+'.htm'), log_prefix + log_line_separator.join(sorted([str(key)+" | "+str(error_log_array[key]) for key in error_log_array], key = lambda x: x.split("|",1)[1] if x.split("|",1)[1].strip().startswith("Title:") and not x.split("|",1)[1].strip().startswith("Title: ''") else int(re.sub("<[^<>]*>", "", x.split("|",1)[0]).strip().split()[1].strip("'")) )))
    except Exception as e:  Log.Error("Exception: '%s'" % e)
    
    netLocked[log] = (False, 0)

### Add genre tags: Status, Extension, Dubbed/Subbed ###
def Other_Tags(media, movie, status):  # Other_Tags(media, Dict(AniDB_dict, 'status') or Dict(TheTVDB_dict, 'status'))
  tags = []
  if movie:  file = media.items[0].parts[0]    
  else:
    s = media.seasons.keys()[0] if media.seasons.keys()[0]!='0' else media.seasons.keys()[1] if len(media.seasons.keys()) >1 else None
    if s:
      e    = media.seasons[s].episodes.keys()[0]
      file = media.seasons[s].episodes[e].items[0].parts[0] 
    else: file = ''
    
    ### Status tag: #"Ended" or "Continuing", "" from:AniDB, TVDB ###
    if status in ('Ended', 'Continuing'):  tags.append(status)
   
  if file:
    
    ### Extension tag ###
    tags.append(str(os.path.splitext(file.file)[1].lstrip('.')))  # avoid u'ext'
  
    ### Tag Dubbed/Subbed ###yyy
    streams = {1:[], 2:[], 3:[]}  #StreamTypes = {1: 'video', 2: 'audio', 3: 'subtitle'}
    for stream in file.streams:
      if stream.type in streams:  streams[stream.type].append(stream.language if hasattr(stream, 'language') else "")
    for audio in streams[2]:
      if not streams[3]:  tags.extend([audio + " Dubbed" for audio in streams[2]])
      else:  tags.extend([audio + " Subbed " + subtitle for audio in streams[2] for subtitle in streams[3]])
        
  return tags
  
### [tvdb4.posters.xml] Attempt to get the ASS's image data ###############################################################################################################
def GetMetadata(media, movie, source, TVDBid, num=0):
  TVDB4_POSTERS_URL = 'http://rawgit.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.posters.xml'
  TVDB4_xml         = None
  if movie or not source == "tvdb4": return {}
  Log.Info("".ljust(157, '-'))
  Log.Info("common.GetMetadata() - tvdb4 mode")
  try:
    s      = media.seasons.keys()[0]
    e      = media.seasons[s].episodes.keys()[0]
    folder = os.path.dirname( media.seasons[ s ].episodes[ e ].items[0].parts[0].file)  #folder = os.path.dirname(media.seasons.itervalues().next().episodes.itervalues().next().items[0].parts[0].file)
    while folder and not folder.endswith("/") and not folder.endswith("\\"):
      filename = os.path.join(folder, os.path.basename(TVDB4_POSTERS_URL))
      if os.path.exists(filename):  TVDB4_xml = XML.ElementFromString( Core.storage.load(os.path.realpath(filename)) );  break
      folder = os.path.dirname(folder)
    else: Log.Info("common.GetMetadata() - No 'tvdb4.posters.xml' file detected locally")
  except Exception as e:  Log.Error("common.GetMetadata() - Issues in finding setup info as directories have most likely changed post scan into Plex, Exception: '%s'" % e)
  
  TVDB4_dict = {}
  if TVDB4_xml: Log.Debug("common.GetMetadata() - 'tvdb4.posters.xml' file detected locally")
  else:         TVDB4_xml  = TVDB4_xml or LoadFile(filename=os.path.basename(TVDB4_POSTERS_URL), relativeDirectory="", url=TVDB4_POSTERS_URL, cache= CACHE_1DAY * 6)  # AniDB title database loaded once every 2 weeks
  if TVDB4_xml:
    seasonposternum = 0
    entry = GetXml(TVDB4_xml, "/tvdb4entries/posters[@tvdbid='%s']" % TVDBid)
    if not entry:  Log.Error("common.GetMetadata() - TVDBid '%s' is not found in xml file" % TVDBid) 
    for line in filter(None, entry.strip().replace("\r","\n").split("\n")):
      season, url       = line.strip().split("|",1)
      season            = season.lstrip("0") if season.lstrip("0") else "0"
      seasonposternum  += 1
      SaveDict(("TheTVDB/seasons/%s-%s-%s" % (TVDBid, season, os.path.basename(url)), 1, None), TVDB4_dict, 'seasons', season, 'posters', url)
  return TVDB4_dict

### Update meta field ###
def UpdateMetaField(metadata_root, metadata, meta_root, fieldList, field, source, movie):
  if field not in meta_root:  Log.Info("meta field: '%s' not in meta_root" % field);  return
  if type(metadata).__name__=="tuple":  
    ep_string      = ' new season: {:<2}, new_episode: {:<3}'.format(metadata[3], metadata[4])
    metadata       = metadata[0].seasons[metadata[1]].episodes[metadata[2]]
  else:  ep_string = ""
  
  meta_old       = getattr(metadata, field) # getattr( metadata, field, None)
  meta_new       = meta_root[field]
  meta_new_short = (meta_new[:80]).replace("\n", " ")+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
  MetaFieldList  = ('directors', 'writers', 'producers', 'guest_stars', 'collections', 'genres', 'tags', 'countries')
  MetaRoleList   = ('directors', 'writers', 'producers', 'guest_stars', 'roles')
  MetaIntList    = ('year', 'absolute_number', 'duration')
  
  ### Prepare data for comparison ###
  try:
    if isinstance(meta_new, basestring):
      if field == 'title_sort':                                      meta_new = SortTitle(meta_new)
      if field == 'originally_available_at':                         meta_new = Datetime.ParseDate(meta_new).date()
      if field == 'rating':                                          meta_new = float(meta_new) if "." in meta_new    else None
      if field in ('year', 'absolute_number', 'duration'):           meta_new = int  (meta_new) if meta_new.isdigit() else None
      if field in  MetaFieldList:                           
        meta_new = re.sub(r'\([^)]*\)', '', meta_new)
        meta_new = meta_new.split(',' if ',' in meta_new else '|')
    if isinstance(meta_new, list) and field in MetaRoleList:
      #meta_new = [{key:Dict(obj, key) for key in ('role', 'name', 'photo')} if isinstance(obj, dict) else {'role':None, 'name':obj, 'photo':None} for obj in meta_new if obj]
      meta_new = [{'role': Dict(obj, 'role'), 'name': Dict(obj, 'name'), 'photo': Dict(obj,'photo')} if isinstance(obj, dict) else \
                  {'role': None,              'name': obj,               'photo': None} for obj in meta_new]
  except Exception as e:  Log.Info("[!] 1{field:<23}  Sources: {sources:<60}  Type: {format:<20}  Value: {value}  Exception: {error}".format(field=field, sources=sources, format=type(meta_old).__name__+"/"+type(meta_new).__name__, value=meta_new_short, error=e))
      
  try:
    if not isinstance(meta_new, list):  meta_old_value = meta_old
    elif field in MetaRoleList:         meta_old_value = [ {'role': role_obj.role, 'name': role_obj.name, 'photo': role_obj.photo} for role_obj in meta_old] #if role_obj.role]
    else:                               meta_old_value = [x for x in meta_old]  #meta_old_value = [ {'role': role_obj.role, 'name': role_obj.name, 'photo': role_obj.photo} for role_obj in meta_old]
  except Exception as e:  Log.Info("[!] 2{field:<23}  Sources: {sources:<11}  Type: {format:<20}  Value: {value}  Exception: {error}".format(field=field, sources=sources, format=type(meta_old).__name__+"/"+type(meta_new).__name__, value=meta_new_short, error=e))
      
  ### Update ONLY IF REQUIRED ###
  if '|' in Prefs[field]:
    if metadata_root==metadata:  sources = '|'.join([Prefs[field].split('|')[0].replace(source, '('+source+')'), Prefs[field].split('|')[1]])
    else:                        sources = '|'.join([Prefs[field].split('|')[0], Prefs[field].split('|')[1].replace(source, '('+source+')')])                   
  else:  sources = Prefs[field].replace(source, '('+source+')')
  
  if meta_new == meta_old_value or \
     isinstance(meta_new, dict) and field not in MetaRoleList and set(meta_new.keys()).issubset(meta_old.keys()) or \
     isinstance(meta_new, list) and field not in MetaRoleList and set(meta_new)== set(meta_old):
    Log.Info("[=] {field:<23}  {len:>4}  Sources: {sources:<60}  Type: {format:<20}  Value: '{value}'{ep}".format(field=field, len="({:>2})".format(len(meta_root[field])) if isinstance(meta_root[field], (list, dict)) else "", sources=sources, format=type(meta_new).__name__, value=meta_new_short, ep=ep_string))
  else:
    temp = [MetaSource.strip() for MetaSource in (Prefs[field].split('|')[0] if '|' in Prefs[field] else Prefs[field]).split(',') if MetaSource and MetaSource.strip()]
    Log.Info("[{rank}] {field:<23}  {len:>4}  Sources: {sources:<60}  Type: {format:<20}  Value: '{value}'{ep}".format(field=field, len="({:>2})".format(len(meta_root[field])) if isinstance(meta_root[field], (list, dict)) else "", source=source, sources=sources, rank=temp.index(source)+1 if source in Prefs[field] else "x", format=type(meta_new).__name__, value=meta_new_short, ep=ep_string))
    
    if isinstance(meta_new, dict)and field in ['posters', 'banners', 'art', 'themes', 'thumbs']:
      for url in meta_new:
        if not url in meta_old and isinstance(meta_new[url], tuple):  metadata_download(metadata_root, meta_old, url, meta_new[url][0], meta_new[url][1], meta_new[url][2])
        #metadata_download(metadata_root, meta_old, url, meta_new[url][0], meta_new[url][1], meta_new[url][2])
        
    elif isinstance(meta_new, list) and field in MetaRoleList:
      try:
        meta_old.clear()
        for item in meta_new:
          meta_role = meta_old.new()
          if not isinstance(item, dict):  setattr(meta_role, 'name', item) #list of names instead of list of people, but should already be list of people
          else:
            for field in item:
              if item[field]:  setattr(meta_role, field, item[field]) 
      except Exception as e:  Log.Info("[!] {field:<29}  Sources: {sources:<60}  Type: {format:<20}  Value: {value}  Exception: {error}".format(field=field, sources=sources, format=type(meta_old).__name__+"/"+type(meta_new).__name__, value=meta_new_short, error=e))
    else:  
      try:                    setattr(metadata, field, meta_new)
      except Exception as e:  Log.Info("[!] {field:<29}  Sources: {sources:<60}  Type: {format:<20}  Value: {value}  Exception: {error}".format(field=field, sources=sources, format=type(meta_old).__name__+"/"+type(meta_new).__name__, value=meta_new_short, error=e))
  
### Update all metadata from a list of Dict according to set priorities ##############################################################################
#if AniDB_dict['originally_available_at']:  AniDB_dict['year'] = AniDB_dict['originally_available_at'].year
def UpdateMeta(metadata, media, movie, MetaSources, mappingList):
  Log.Info("".ljust(157, '-'))
  Log.Info("common.UpdateMeta() - List of Metadata Sources and their movie/serie, season, episodes fields gathered")
  for source in MetaSources:
    if MetaSources[source]:  Log.Info("- {source:<11}      : {fields}".format(source=source, fields =' | '.join('{:<23} ({:>3})'.format(field, len(MetaSources[source][field]) if isinstance(MetaSources[source][field], (list, dict)) else 1) for field in MetaSources[source])))
    if type(MetaSources[source]).__name__ == 'NoneType': Log.Info("[!] source: '%s', type: '%s', bad return in function, should return an empty dict" % (source, type(MetaSources[source]).__name__))
    if 'seasons' in (MetaSources[source] if MetaSources[source] else {}) :
      season_fields, episode_fields, ep_nb, ep_invalid = {}, {}, 0, 0
      for season in sorted(MetaSources[source]['seasons'], key=natural_sort_key):
        for field in MetaSources[source]['seasons'][season]:
          if field in FieldListSeasons:  season_fields[field] = (season_fields[field] + 1) if field in season_fields else 1
          elif not field=="episodes" and not field.isdigit():  Log.Info("Season Field Unrecognised: '{}' in source: '{}'".format(field, source))
        for episode in sorted(MetaSources[source]['seasons'][season]['episodes'], key=natural_sort_key) if 'episodes' in MetaSources[source]['seasons'][season] else []:
          for field in MetaSources[source]['seasons'][season]['episodes'][episode]:
            if field in FieldListEpisodes:  episode_fields[field] = episode_fields[field] + 1 if field in episode_fields else 1
            elif field is not 'language_rank':  Log.Info("                     {:<23} Season {:>3}, Episode: {:>3} is not a valid metadata field, value: '{!s}'".format(field, season, episode, MetaSources[source]['seasons'][season]['episodes'][episode][field])); ep_invalid+=1
          ep_nb+=1
      if len(season_fields ):  Log.Info("  - Seasons   ({nb:>3}): {fields}".format(nb=len(MetaSources[source]['seasons']), fields =' | '.join('{:<23} ({:>3})'.format(field,  season_fields[field]) for field in  season_fields)))
      if len(episode_fields):  Log.Info("  - Episodes  ({nb:>3}): {fields}".format(nb=ep_nb-ep_invalid                   , fields =' | '.join('{:<23} ({:>3})'.format(field, episode_fields[field]) for field in episode_fields)))
  Log.Info("".ljust(157, '-'))
  
  ### Metadata review display. Legend for the '[ ]' display:
  # [=] already at the right value for that source
  # [x] Xst/nd/th source had the field
  # [#] no source for that field
  # [!] Error assigning
  Log.Info("Plex.UpdateMeta() - Metadata Fields (items #), type, source provider, value, ")
  count    = {'posters':0, 'art':0, 'thumbs':0, 'banners':0, 'themes':0}
  languages = Prefs['EpisodeLanguagePriority'].replace(' ', '').split(',')
  for field in FieldListMovies if movie else FieldListSeries:
    meta_old = getattr(metadata, field)
    if field=='title':  rank, found = len(languages), False
    for source in (source.strip() for source in (Prefs[field].split('|')[0] if '|' in Prefs[field] else Prefs[field]).split(',') if Prefs[field]):
      if source in MetaSources:
        if Dict(MetaSources, source, field):
          if field=='genres':
            if '|' in MetaSources[source]['genres'] or ',' in MetaSources[source]['genres']:
              MetaSources[source]['genres'] = MetaSources[source]['genres'].split('|' if '|' in MetaSources[source]['genres'] else ',')
              MetaSources[source]['genres'].extend( Other_Tags(media, movie, Dict(MetaSources, 'AniDB', 'status')) )
          if field=='title':
            language_rank = Dict(MetaSources, source, 'language_rank')
            title         = Dict(MetaSources, source, 'title'        )
            #Log.Info("[!] language source: {}, rank: {}, found: {}, language_rank: '{}'".format(source, rank, found, language_rank))
            if title and (language_rank not in (None, '') and (language_rank<rank or not found and language_rank==rank) or not found and rank==len(languages)):  found, rank = True, language_rank
            else:                                                                                                                                                continue  #Lower index (or same index at higher index metadata source) title exists
          UpdateMetaField(metadata, metadata, MetaSources[source], FieldListMovies if movie else FieldListSeries, field, source, movie)
          if field in count:  count[field] = count[field] + 1
          if field in ['posters', 'art', 'banners', 'themes', 'thumbs'] and not Prefs['GetSingleOne'] or field=="title" and language_rank==0:  continue
          else:                                                                                                                                break
      elif not source=="None":  Log.Info("[!] '{}' source not in MetaSources dict, please Check case and spelling".format(source))
    else:
      if not Dict(count, field):
        source_list = [ source for source in MetaSources if source not in Prefs[field] and Dict(MetaSources, source, field) ]
        Log.Info("[#] {field:<29}  Sources: {sources:<60}  Type: {format:<20}  Field present in this sources: '{other}'".format(field=field, format=type(meta_old).__name__, sources=Prefs[field], other=source_list))
        
  if not movie:
    import AnimeLists
              
    ### AniDB poster as season poster backup ###
    #if (metadata.id.startswith("tvdb") or max(map(int, media.seasons.keys())) >1) and Dict(mappingList, 'defaulttvdbseason'): # defaulttvdb season isdigit and assigned to 1 tvdb season (even if it is season 0)
    #  if Dict(MetaSources, 'AniDB', 'posters'):  SaveDict(MetaSources['AniDB']['posters'], MetaSources, 'AniDB', 'seasons', Dict(mappingList, 'defaulttvdbseason') if Dict(mappingList, 'defaulttvdbseason').isdigit() else '1', 'posters')
    #  if Dict(MetaSources, 'AniDB', 'summary'):  SaveDict(MetaSources['AniDB']['summary'], MetaSources, 'AniDB', 'seasons', Dict(mappingList, 'defaulttvdbseason') if Dict(mappingList, 'defaulttvdbseason').isdigit() else '1', 'summary')
      
    ### Seasons ###
    AniDB_numbered = not(metadata.id.startswith("tvdb") or max(map(int, media.seasons.keys()))>=1)
    for season in sorted(media.seasons, key=natural_sort_key):  # For each season, media, then use metadata['season'][season]...
      Log.Info("metadata.seasons[{:>2}]".ljust(157, '-').format(season))
      count = {'posters':0, 'art':0, 'thumbs':0, 'banners':0, 'themes':0}
      for field in FieldListSeasons:
        meta_old = getattr(metadata.seasons[season], field)
        for source in (source.strip() for source in Prefs[field].split(',') if Prefs[field]):
          new_season = season
          if source in MetaSources:
            if source=='AniDB'   and (metadata.id.startswith("tvdb" ) or max(map(int, media.seasons.keys()))>1):  new_season = Dict(mappingList, 'defaulttvdbseason') if Dict(mappingList, 'defaulttvdbseason') and Dict(mappingList, 'defaulttvdbseason') !='a' else '1'
            if source=='TheTVDB' and  AniDB_numbered:  new_season = (Dict(mappingList, 'defaulttvdbseason') or season) if season!='0' else season
            if Dict(MetaSources, source, 'seasons', new_season, field) and (season in metadata.seasons or metadata.id.startswith('tvdb4')):
              UpdateMetaField(metadata, metadata.seasons[season], MetaSources[source]['seasons'][new_season], FieldListSeasons, field, source, movie)
              if field in count:  count[field] = count[field] + 1
              if field=="title" and 'language_rank' in source and Dict(MetaSources, source, 'language_rank'):  continue  #try other meta source if index not 0 which is the first selected language
              if field not in ['posters', 'art', 'banners', 'themes', 'thumbs'] or Prefs['GetSingleOne']:  break 
          elif not source=="None": Log.Info("[!] '{}' source not in MetaSources".format(source))
        else:  #nothing found
          if not Dict(count, field):    
            source_list = [ source for source in MetaSources if source not in Prefs[field] and Dict(MetaSources, source, 'season', new_season, field) ]
            Log.Info("[#] {field:<29}  Sources: {sources:<60}  Type: {format:<20}  Inside: {other}".format(field=field, format=type(meta_old).__name__, sources=Prefs[field], other=source_list))
      
      ### Episodes ###
      for episode in sorted(media.seasons[season].episodes, key=natural_sort_key):
        Log.Info("metadata.seasons[{:>2}].episodes[{:>3}]".format(season, episode))
        count={'posters':0, 'art':0, 'thumbs':0}
        for field in FieldListEpisodes:  # Get a field
          try:                    meta_old = getattr(metadata.seasons[season].episodes[episode], field)
          except Exception as e:  Log.Info("[!] "+str(e)); meta_old=""
          if field=='title':  rank, found = len(languages), False
          for source in [source.strip() for source in (Prefs[field].split('|')[1] if '|' in Prefs[field] else Prefs[field]).split(',')]:  #if shared by title and eps take later priority
            if source in MetaSources:
              new_season, new_episode = '1' if metadata.id.startswith('tvdb4') and not season=='0' else season, episode
              if Dict(MetaSources, source, 'seasons', new_season, 'episodes', new_episode, field):
                if field=='title':
                  language_rank = Dict(MetaSources, source,  'seasons', new_season, 'episodes', new_episode, 'language_rank')
                  title         = Dict(MetaSources, source,  'seasons', new_season, 'episodes', new_episode, 'title')
                  #Log.Info("[!] language source: {}, rank: {}, found: {}, language_rank: '{}'".format(source, rank, found, language_rank))
                  if title and (language_rank not in (None, '') and (language_rank<rank or not found and language_rank==rank) or not found and rank==len(languages)):  found, rank = True, language_rank
                  else:                                                                                                                                                continue  #Lower index (or same index at higher index metadata source) title exists
                UpdateMetaField(metadata, (metadata, season, episode, new_season, new_episode), MetaSources[source]['seasons'][new_season]['episodes'][new_episode], FieldListEpisodes, field, source, movie)
                count[field] = count[field] + 1 if field in count else 1
                if field in ['posters', 'art', 'banners', 'themes', 'thumbs'] and not Prefs['GetSingleOne'] or field=="title" and language_rank==0:  continue
                else:                                                                                                                                break
            elif not source=="None": Log.Info("[!] '{}' source not in MetaSources".format(str(source)))
          if not Dict(count, field):
            source_list = [ source for source in MetaSources if Dict(MetaSources, source, 'seasons', new_season, 'episodes', new_episode, field) ]
            Log.Info("[!] {field:<29}  Sources: {sources:<60}  Type: {format:<20}  Inside : {other}".format(field=field, format=type(meta_old).__name__, sources=Prefs[field], other=source_list))
      # End Of for episode
    # End of for season
    Log.Info("".ljust(157, '-'))
  global downloaded
  downloaded = {'posters':0, 'art':0, 'seasons':0, 'banners':0, 'themes':0, 'thumbs': 0} 
  
### Compute Levenshtein distance.
def LevenshteinDistance(first, second):
  if len(first) > len(second):  first, second = second, first
  if len(second) == 0: return len(first)
  first_length    = len(first ) + 1
  second_length   = len(second) + 1
  distance_matrix = [[0] * second_length for x in range(first_length)]
  for i in range(first_length):   distance_matrix[i][0] = i
  for j in range(second_length):  distance_matrix[0][j] = j
  for i in xrange(1, first_length):
    for j in range(1, second_length):
      distance_matrix[i][j] = min(distance_matrix[i][j-1]+1, distance_matrix[i-1][j]+1, distance_matrix[i-1][j-1] + (1 if first[i-1] != second[j-1] else 0))
  return distance_matrix[first_length-1][second_length-1]

### Levenshtein ratio.
def LevenshteinRatio(first, second):
  return 100 - int(100 * LevenshteinDistance(first, second) / float(max(len(first), len(second)))) if len(first)*len(second) else 0

### SortTitle ###
def SortTitle(title, language="en"):
  dict_sort = { 'en': ["The", "A", "An"],
                'fr': ["Le", "La", "Les", "L", "Un", "Une ", "Des "],
                'sp': ["El", "La", "Las", "Lo", "Los", "Uno ", "Una "]
              }
  title  = title.replace("'", " ")
  prefix = title.split  (" ", 1)[0]  #Log.Info("SortTitle - title:{}, language:{}, prefix:{}".format(title, language, prefix))
  return title.replace(prefix+" ", "", 1) if language in dict_sort and prefix in dict_sort[language] else title 

### Collections
# metadata.collections.clear()
# metadata.collections.add(collection)
#
#
  