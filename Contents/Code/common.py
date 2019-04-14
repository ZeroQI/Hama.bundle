### common ###
# https://www.python.org/dev/peps/pep-0008/
# Usage: "common.GetPosters" = "from common import GetPosters"

### Imports ###               ### Functions used ###
import os                     # path.abspath, join, dirname
import inspect                # getfile, currentframe
import time                   # datetime.datetime.now() 
import re                     # sub
import logging                #
import datetime               # datetime.now
import ssl, urllib2           # urlopen
import unicodedata            #
import logging                #
from io     import open       # open
from string import maketrans  # maketrans
from lxml   import etree      # fromstring
#try:                 from urllib.request import urlopen # urlopen Python 3.0 and later
#except ImportError:  from urllib2        import urlopen # urlopen Python 2.x
import threading              #local,
tlocal = threading.local()
#Log.Info('tlocal: {}'.format(dir(tlocal)))

### Variables, accessible in this module (others if 'from common import xxx', or 'import common.py' calling them with 'common.Variable_name' ###
strptime          = datetime.datetime.strptime #avoid init crash on first use in threaded environment  #dt.strptime(data, "%Y-%m-%d").date()
PlexRoot          = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "..", "..", "..", ".."))
CachePath         = os.path.join(PlexRoot, "Plug-in Support", "Data", "com.plexapp.agents.hama", "DataItems")
downloaded        = {'posters':0, 'art':0, 'seasons':0, 'banners':0, 'themes':0, 'thumbs': 0} 
netLock           = Thread.Lock()
netLocked         = {}
WEB_LINK          = "<a href='%s' target='_blank'>%s</a>"
TVDB_SERIE_URL    = 'http://thetvdb.com/?tab=series&id='
ANIDB_SERIE_URL   = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid='
TVDB4_MAPPING_URL = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.mapping.xml'
TVDB4_POSTERS_URL = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.posters.xml'
DefaultPrefs      = ("SerieLanguagePriority", "EpisodeLanguagePriority", "PosterLanguagePriority", "MinimumWeight", "adult", "OMDbApiKey") #"Simkl", 
FieldListMovies   = ('original_title', 'title', 'title_sort', 'roles', 'studio', 'year', 'originally_available_at', 'tagline', 'summary', 'content_rating', 'content_rating_age',
                     'producers', 'directors', 'writers', 'countries', 'posters', 'art', 'themes', 'rating', 'quotes', 'trivia')
FieldListSeries   = ('title', 'title_sort', 'originally_available_at', 'duration','rating',  'reviews', 'collections', 'genres', 'tags' , 'summary', 'extras', 'countries', 'rating_count',
                     'content_rating', 'studio', 'countries', 'posters', 'banners', 'art', 'themes', 'roles', 'original_title', 
                     'rating_image', 'audience_rating', 'audience_rating_image')  # Not in Framework guide 2.1.1, in https://github.com/plexinc-agents/TheMovieDb.bundle/blob/master/Contents/Code/__init__.py
FieldListSeasons  = ('summary','posters', 'art')  #'summary', 
FieldListEpisodes = ('title', 'summary', 'originally_available_at', 'writers', 'directors', 'producers', 'guest_stars', 'rating', 'thumbs', 'duration', 'content_rating', 'content_rating_age', 'absolute_index') #'titleSort
SourceList        = ('AniDB', 'MyAnimeList', 'FanartTV', 'OMDb', 'TheTVDB', 'TheMovieDb', 'Plex', 'AnimeLists', 'tvdb4', 'TVTunes', 'Local') #"Simkl", 
Movie_to_Serie_US_rating = {"G"    : "TV-Y7", "PG"   : "TV-G", "PG-13": "TV-PG", "R"    : "TV-14", "R+"   : "TV-MA", "Rx"   : "NC-17"}
HEADERS           = {'User-agent': 'Plex/Nine', 'Content-type': 'application/json'}

### Plex Library XML ###
PLEX_LIBRARY, PLEX_LIBRARY_URL = {}, "http://127.0.0.1:32400/library/sections/"    # Allow to get the library name to get a log per library https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token
try:
  library_xml = XML.ElementFromURL(PLEX_LIBRARY_URL, timeout=float(30))
  Log.Info('Libraries: ')
  for directory in library_xml.iterchildren('Directory'):
    for location in directory:
      Log.Info('[{}] id: {:>2}, type: {:>6}, library: {:<24}, path: {}'.format(' ', directory.get("key"), directory.get('type'), directory.get('title'), location.get("path")))
      PLEX_LIBRARY[location.get("path")] = directory.get("title")
      #library_key, library_path, library_name = directory.get("key"), location.get("path"), directory.get('title')
except Exception as e:  Log.Info("PLEX_LIBRARY_URL - Exception: '{}'".format(e));  library_key, library_path, library_name = '', '', ''

### Get media directory ###
def GetMediaDir (media, movie, file=False):
  if movie:  return os.path.dirname(media.items[0].parts[0].file)
  else:
    for s in media.seasons if media else []: # TV_Show:
      for e in media.seasons[s].episodes:
        return media.seasons[s].episodes[e].items[0].parts[0].file if file else os.path.dirname(media.seasons[s].episodes[e].items[0].parts[0].file)

### Get media root folder ###
def GetLibraryRootPath(dir):
  library, root, path = '', '', ''
  for root in [os.sep.join(dir.split(os.sep)[0:x+2]) for x in range(0, dir.count(os.sep))]:
    if root in PLEX_LIBRARY:
      library = PLEX_LIBRARY[root]
      path    = os.path.relpath(dir, root)
      break
  else:  #401 no right to list libraries (windows)
    Log.Info('[!] Library access denied')
    filename = os.path.join(CachePath, '_Logs', '_root_.scanner.log')
    if os.path.isfile(filename):
      Log.Info('[!] ASS root scanner file present: "{}"'.format(filename))
      try:
        with open(filename, 'r', -1, 'utf-8') as file:  line=file.read()
      except Exception as e:  line='';  Log.Info('Exception: "{}"'.format(e))
      
      for root in [os.sep.join(dir.split(os.sep)[0:x+2]) for x in range(dir.count(os.sep)-1, -1, -1)]:
        if "root: '{}'".format(root) in line:
          path = os.path.relpath(dir, root).rstrip('.')
          break
        Log.Info('[!] root not found: "{}"'.format(root))
      else: path, root = '_unknown_folder', ''
    else:  Log.Info('[!] ASS root scanner file missing: "{}"'.format(filename))
  return library, root, path

### Check config files on boot up then create library variables ###    #platform = xxx if callable(getattr(sys,'platform')) else "" 
if not os.path.isdir(PlexRoot):
  path_location = { 'Windows': '%LOCALAPPDATA%\\Plex Media Server',
                    'MacOSX':  '$HOME/Library/Application Support/Plex Media Server',
                    'Linux':   '$PLEX_HOME/Library/Application Support/Plex Media Server' }
  PlexRoot = os.path.expandvars(path_location[Platform.OS.lower()] if Platform.OS.lower() in path_location else '~')  # Platform.OS:  Windows, MacOSX, or Linux

class PlexLog(object):
  ''' Logging class to join scanner and agent logging per serie
      Usage Scanner: (not used currently in scanner as independant from Hama)
       - from "../../Plug-ins/Hama.bundle/Contents/code/common" import PlexLog
       - log = PlexLog(file='root/folder/[anidb2-xxxx].log', isAgent=False)
      Usage Agent:
       - log = common.PlexLog(file='mytest.log', isAgent=True )
       - log.debug('some debug message: %s', 'test123')
  '''
  def Logger   (self):
    logger = logging.getLogger(hex(threading.currentThread().ident))
    return logger if logger.handlers else logging.getLogger('com.plexapp.agents.hama')
  def Root     (self, msg, *args, **kwargs):  logging.getLogger('com.plexapp.agents.hama').debug(msg, *args, **kwargs)
  def Debug    (self, msg, *args, **kwargs):  self.Logger().debug   (msg,                     *args, **kwargs)
  def Info     (self, msg, *args, **kwargs):  self.Logger().info    (msg,                     *args, **kwargs)
  def Warning  (self, msg, *args, **kwargs):  self.Logger().warning (msg,                     *args, **kwargs)
  def Error    (self, msg, *args, **kwargs):  self.Logger().error   ("ERROR: {}".format(msg), *args, **kwargs)
  def Critical (self, msg, *args, **kwargs):  self.Logger().critical(msg,                     *args, **kwargs)
  def Open     (self, media=None, movie=False, search=False, isAgent=True, log_format='%(message)s', file="", mode='w', maxBytes=4*1024*1024, backupCount=5, encoding=None, delay=False, enable_debug=True):
    if not file:  
      library, root, path = GetLibraryRootPath(GetMediaDir(media, movie))#Get movie or serie episode folder location      
      mode                = 'a' if path in ('_unknown_folder', '_root_') else 'w'
      
      #Logs folder
      for char in list("\\/:*?<>|~;"):                             # remove leftover parenthesis (work with code a bit above)
        if char in library:  library = library.replace(char, '-')  # translate anidb apostrophes into normal ones
      LOGS_PATH = os.path.join(CachePath, '_Logs', library)
      if not os.path.exists(LOGS_PATH):  os.makedirs(LOGS_PATH);  self.Debug("[!] folder: '{}'created".format(LOGS_PATH))
      
      if path=='' and root:  path='_root_'
      filename = path.split(os.sep, 1)[0]+'.agent-search.log' if search else path.split(os.sep, 1)[0]+'.agent-update.log'
      file = os.path.join(LOGS_PATH, filename)
    try:
      log = logging.getLogger(hex(threading.currentThread().ident))  # update thread's logging handler
      for handler in log.handlers:  log.removeHandler(handler)  # remove all old handlers
      handler_new = logging.FileHandler(file, mode=mode or 'w', encoding=encoding, delay=delay)
      handler_new.setFormatter(logging.Formatter(log_format))  # Set log format
      log.addHandler(handler_new)
      log.setLevel(logging.DEBUG if enable_debug else logging.INFO)  # update level

      log = logging.getLogger('com.plexapp.agents.hama')  # update hama root's logging handler
      library_log = os.path.join(LOGS_PATH, '_root_.agent.log')
      if library_log not in [handler.baseFilename for handler in log.handlers if hasattr(handler, 'baseFilename')]:
        for handler in log.handlers:
          if hasattr(handler, 'baseFilename') and os.path.join(CachePath, '_Logs') in handler.baseFilename:  log.removeHandler(handler)
        handler_new = logging.handlers.RotatingFileHandler(library_log, mode='a', maxBytes=4*1024*1024, backupCount=1, encoding=encoding, delay=delay)
        #handler_new = logging.FileHandler(library_log, mode='w', encoding=encoding, delay=delay)
        handler_new.setFormatter(logging.Formatter('%(asctime)-15s - %(thread)x - %(message)s'))  # Set log format
        log.addHandler(handler_new)
      log.info('==== common.PlexLog(file="{}")'.format(file))

    except IOError as e:  self.isAgent = isAgent;  logging.getLogger('com.plexapp.agents.hama').info('updateLoggingConfig: failed to set logfile: {}'.format(e))
    self.Info("".ljust(157, '='))
    self.Info('common.PlexLog(file="{}", movie={})'.format(file, movie))
    self.Info('[!] file:       "{}"'.format(GetMediaDir(media, movie, True)))
    self.Info('[ ] library:    "{}"'.format(library))
    self.Info('[ ] root:       "{}"'.format(root))
    self.Info('[ ] path:       "{}"'.format(path))
    self.Info('[ ] Plex root:  "{}"'.format(PlexRoot))
    self.Info('[ ] Log folder: "{}"'.format(os.path.relpath(LOGS_PATH, PlexRoot)))
    self.Info('[ ] Log file:   "{}"'.format(filename))
    self.Info('[ ] Logger:     "{}"'.format(hex(threading.currentThread().ident)))
    self.Info('[ ] mode:       "{}"'.format(mode))
    self.isAgent = isAgent
  def Close    (self):  
    log = logging.getLogger(hex(threading.currentThread().ident))  # update root logging's handler
    for handler in log.handlers:  log.removeHandler(handler)
    
Log = PlexLog()

### Code reduction one-liners that get imported specifically ###
#def GetMeta         (source="", field=""            ):  return (downloaded[field]<=1) and (not source or source in Prefs['posters' if field=='seasons' else field]) and not Prefs['posters' if field=='seasons' else field]=="None"
def GetXml          (xml,      field                ):  return xml.xpath(field)[0].text if xml.xpath(field) and xml.xpath(field)[0].text not in (None, '', 'N/A', 'null') else ''  #allow isdigit() checks
def urlFilename     (url                            ):  return "/".join(url.split('/')[3:])
def urlDomain       (url                            ):  return "/".join(url.split('/')[:3])
def LevenshteinRatio(first, second                  ):  return 100 - int(100 * LevenshteinDistance(first, second) / float(max(len(first), len(second)))) if len(first)*len(second) else 0
def natural_sort_key(s                              ):  return [int(text) if text.isdigit() else text for text in re.split(r'([0-9]+)', str(s).lower())]  # list.sort(key=natural_sort_key) #sorted(list, key=natural_sort_key) - Turn a string into string list of chunks "z23a" -> ["z", 23, "a"]
def replaceList     (string, a, b, *args):
  for index in a:  string.replace(a[index], b[index], *args)
  return string

### Library in Hama.bundle/Contents/Libraries/Shared) and "import requests"
def ssl_open(url, headers=None, timeout=20):
  ''' SSLV3_ALERT_HANDSHAKE_FAILURE
      1. Do not verify certificates. A bit like how older Python versions worked
         Import ssl and urllib2
         Use urllib2 with a default ssl context (which does not verify the certificate).
      Or:
      2. Set PlexPluginCodePolicy to Elevated in Info.plist
         Add external Python libraries to your project bundle
         Import certifi and requests into your Python code
         Use requests
  '''
  if not headers:  headers = { 'User-Agent': 'ABC/5.0.14(iPad4,4; cpu iOS 10_2_1 like mac os x; en_nl) CFNetwork/758.5.3 Darwin/15.6.0', 'appversion': '5.0.14'}
  if url.startswith('https://'):  return urllib2.urlopen(urllib2.Request(url, headers=headers), context=ssl.SSLContext(ssl.PROTOCOL_TLSv1), timeout=timeout).read()
  else:                           return urllib2.urlopen(url, timeout=timeout).read()
  
def IsIndex(var, index):  #Avoid TypeError: argument of type 'NoneType' is not iterable
  """ Return the length of the array or index no errors
  """
  try:     return var[index]
  except:  return '' 
  
def Dict(var, *arg, **kwarg):
  """ Return the value of an (imbricated) dictionnary, if all fields exist else return "" unless "default=new_value" specified as end argument
      Avoid TypeError: argument of type 'NoneType' is not iterable
      Ex: Dict(variable_dict, 'field1', 'field2', default = 0)
  """
  for key in arg:
    if isinstance(var, dict) and key and key in var:  var = var[key]
    else:  return kwarg['default'] if kwarg and 'default' in kwarg else ""   # Allow Dict(var, tvdbid).isdigit() for example
  return kwarg['default'] if var in (None, '', 'N/A', 'null') and kwarg and 'default' in kwarg else "" if var in (None, '', 'N/A', 'null') else var

def SaveDict(value, var, *arg):
  """ Save non empty value to a (nested) Dictionary fields unless value is a list or dict for which it will extend it instead
      # ex: SaveDict(GetXml(ep, 'Rating'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating')
      # ex: SaveDict(Dict(TheTVDB_dict, 'title'), TheTVDB_dict, 'title_sort')
      # ex: SaveDict(genre1,                      TheTVDB_dict, genre) to add    to current list
      # ex: SaveDict([genre1, genre2],            TheTVDB_dict, genre) to extend to current list
  """
  if not value and value!=0:  return ""  # update dict only as string would revert to pre call value being immutable
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

### import var 2 dict into var and returns it
def UpdateDict(var, var2):  var.update(var2);  return var

### return dict of fields containing their max length ###
def DisplayDictLen(items={}, fields=[]):  
  len_fields = {}
  for item in items or []:
    for field in fields:  len_fields[field] = max(len(Dict(item, field)), Dict(len_fields, field, default = 0))
  return len_fields
  
### Display alligned dict entries ###
def DisplayDict(items={}, fields=[]):
  len_fields = DisplayDictLen(items, fields)
  for item in items or {}:  Log.Info(''.join([('{}: {:<'+str(Dict(len_fields, field, default='20'))+'}, ').format(field, item[field]) for field in fields]))

def DictString(input_value, max_depth, initial_indent=0, depth=0):
  """ Expand a dict down to 'max_depth' and sort the keys.
      To print it on a single line with this function use (max_depth=0).
      EX: (max_depth=1)
        mappingList: {
          'season_map': {'13493': {'max': '3', 'min': '3'}}}
      EX: (max_depth=2)
        mappingList: {
          'season_map': {
            '9306': {'max': '2', 'min': '1'},
            '11665': {'max': '3', 'min': '3'}}}
  """
  output = ""
  indent = "\n" + " " * initial_indent + "  " * (depth+1)
  if depth >= max_depth or not isinstance(input_value, dict):
    if isinstance(input_value, list) and depth<max_depth:  output += "[" + indent + indent.join([("'{}'," if isinstance(x, str) else "{},").format(x) for x in input_value])[:-1] + "]"
    else:                                                  output += "{}".format(input_value)
  else:
    for i, key in enumerate(sorted(input_value, key=natural_sort_key)):
      value = input_value[key] if isinstance(input_value[key], basestring) else DictString(input_value[key], max_depth, initial_indent, depth+1)
      output += (
        indent + 
        "{}: ".format("'{}'".format(key.replace("'", "\\'")) if isinstance(key, basestring) else key) + 
        "{}".format("'{}'".format(value.replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")) if isinstance(input_value[key], basestring) else value) + 
        ("," if i!=len(input_value)-1 else ""))  # remove last ','
    output = "{" + output + "}"
  return output
  # Other options passed on as can't define expansion depth
  #import pprint; pprint.pprint(input_value)
  #import json; return json.dumps(input_value, indent=2, sort_keys=True)

def GetStatusCode(url):
    """ This function retreives the status code of a website by requesting HEAD data only from the host.
        This means that it only requests the headers. If the host cannot be reached or something else goes wrong, it returns None instead.
        urllib.parse.quote(string, safe='/', encoding=None, errors=None)
        - string:   string your trying to encode
        - safe:     string contain characters to ignore. Defualt is '/'
        - encoding: type of encoding url is in. Default is utf-8
        - errors:   specifies how errors are handled. Default is 'strict' which throws a UnicodeEncodeError, I think.
        #host = "/".join(url.split('/', 3)[:-1])  #path = url.replace(" ", "%20").split('/', 3)[3]  #Log.Info("host: '%s', path: '%s'" % (host, path))
    """ 
    try:
      request            = urllib2.Request(url) #urllib.quote #urllib2.quote(url,':/')
      request.get_method = lambda: 'HEAD'
      return urllib2.urlopen(request).getcode() # if "Content-Type: audio/mpeg" in response.info(): Log.Info("Content-Type: audio/mpeg")
    except Exception as e:  return str(e)
  
def SaveFile(filename="", file="", relativeDirectory=""):
  ''' Save file to cache, Thanks Dingmatt for folder creation ability
  '''
  relativeFilename            = os.path.join (relativeDirectory, filename) 
  relativeDirectory, filename = os.path.split(relativeFilename) #if os.sep in filename:
  fullpathDirectory           = os.path.abspath(os.path.join(CachePath, relativeDirectory))
  try:
    if not os.path.exists(fullpathDirectory):  os.makedirs(fullpathDirectory)
    Data.Save(relativeFilename, file)
  except Exception as e:  Log.Debug("common.SaveFile() - Exception: {exception}, relativeFilename: '{relativeFilename}', file: '{file}'".format(exception=e, relativeFilename=relativeFilename, file=file))
  else:                   Log.Info ("common.SaveFile() - CachePath: '{path}', file: '{file}'".format(path=CachePath, file=relativeFilename))
   
def LoadFile(filename="", relativeDirectory="", url="", cache=CACHE_1DAY*6, headers={}):  #, data=None):  #By Dingmatt, heavily moded
  ''' Load file in Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems if cache time not passed
      Usage (TheTVDBv2): 
      2018-05-31 05:32:31,046 (2384) :  INFO (logkit:16) - -------------------------------------------------------------------------------------------------------------------------------------------------------------
      2018-05-31 05:32:31,046 (2384) :  INFO (logkit:16) - TheTVDB.GetMetadata() - TVDBid: '280330', IMDbid: '', language_series : ['en'], language_episodes: ['en']
      2018-05-31 05:32:31,048 (2384) :  DEBUG (networking:166) - Requesting 'https://api.thetvdb.com/login'
      2018-05-31 05:32:33,694 (2384) :  ERROR (networking:219) - Error opening URL 'https://api.thetvdb.com/login'
      2018-05-31 05:32:33,694 (2384) :  INFO (logkit:16) - Error: HTTP Error 503: Service Unavailable
      2018-05-31 05:32:33,710 (2384) :  DEBUG (networking:166) - Requesting 'https://api.thetvdb.com/series/280330'
      2018-05-31 05:32:35,138 (2384) :  ERROR (networking:219) - Error opening URL 'https://api.thetvdb.com/series/280330'
      2018-05-31 05:32:35,138 (2384) :  WARNING (logkit:19) - common.LoadFile() - issue loading url: 'https://api.thetvdb.com/series/280330', filename: 'series.json', Exception: 'HTTP Error 503: Service Unavailable'
      2018-05-31 05:32:35,140 (2384) :  INFO (logkit:16) - LoadFile() - returning string
      2018-05-31 05:32:35,141 (2384) :  INFO (logkit:16) - -------------------------------------------------------------------------------------------------------------------------------------------------------------
  '''
  relativeFilename                   = os.path.join(relativeDirectory, filename) 
  fullpathFilename                   = os.path.abspath(os.path.join(CachePath, relativeDirectory, filename))
  file_valid, converted, Saved, file = False, False, False, None
  if filename.endswith(".xml.gz"):  filename = filename[:-3] #anidb title database
  
  # Load from cache if recent
  if Data.Exists(relativeFilename):
    file_time  = os.stat(fullpathFilename).st_mtime
    file_valid = file_time+cache > time.time()
    if file_valid:
      try:     file = Data.Load(relativeFilename)
      except:  file = None
      Log.Debug(   "common.LoadFile() - file cached - CacheTime: '{time}', Limit: '{limit}', url: '{url}', Filename: '{file}' file_valid: '{file_valid}'".format(file=relativeFilename, url=url, time=time.ctime(file_time), limit=time.ctime(time.time() + cache), file_valid=file_valid))
  
  if not file:
    netLock.acquire()
    
    # TheTVDB
    if url.startswith('https://api.thetvdb.com'):
      if 'Authorization' in HEADERS:
        try:     file = HTTP.Request(url, headers=UpdateDict(headers, HEADERS), timeout=60, cacheTime=0).content  # Normal loading, already Authentified
        except:  file = None
        Log.Root("Completed '{}'".format(url))
      if not file:
        try:                      HEADERS['Authorization'] = 'Bearer ' + JSON.ObjectFromString(HTTP.Request('https://api.thetvdb.com/login', data=JSON.StringFromObject( {'apikey':'A27AD9BE0DA63333'} ), headers={'Content-type': 'application/json'}).content)['token']
        except Exception as e:    Log.Info('Error: {}'.format(e))
        else:                     Log.Info('not authorised, headers: {}, HEADERS: {}'.format(headers, HEADERS))
    
    # AniDB
    if url.startswith('http://api.anidb.net:9001'):
      while 'anidb' in netLocked and netLocked['anidb'][0]:  Log.Root("Waiting for lock: 'anidb'"); time.sleep(1)
      netLocked['anidb'] = (True, int(time.time()))
      Log.Root("Lock acquired: 'anidb'")

    # File download
    if not file:
      try:                    file = HTTP.Request(url, headers=UpdateDict(headers, HEADERS if url.startswith('https://api.thetvdb.com') else {}), timeout=60, cacheTime=cache).content             #'Accept-Encoding':'gzip'                        # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find', None if 'thetvdb' in url else 
      except Exception as e:  file = None;  Log.Warning("common.LoadFile() - issue loading url: '{}', filename: '{}', Headers: {}, Exception: '{}'".format(url, filename, HEADERS, e))                                                           # issue loading, but not AniDB banned as it returns "<error>Banned</error>"
      Log.Root("Completed '{}'".format(url))
    
    # AniDB
    if url.startswith('http://api.anidb.net:9001'):
      time.sleep(6)  #Sleeping after call completion to prevent ban
      if file and '>banned<' in file:  Log.Root("Banned from 'anidb': {}".format(file))
      netLocked['anidb'] = (False, 0)
      Log.Root("Lock released: 'anidb'")

    netLock.release()
    
    # File checks and saving as cache
    if file:
      if len(file)>64 or '{' in file:
        Saved = True
        SaveFile(filename, file, relativeDirectory)
      else:
        Log.Info('[!] File received too small (<64 bytes), file: "{}"'.format(file))
        file=None  #if str(file).startswith("<Element error at ") or file in ('<error>Banned</error>', '<error>aid Missing or Invalid</error>'): 
        if Data.Exists(relativeFilename):  file = Data.Load(relativeFilename) #present, cache expired but online version incorrect or not available
        else:                              Log.Root("No preexisting file '{}' to load".format(relativeFilename))

  if isinstance(file, basestring):
    if file.startswith('<?xml '):
      try:     return XML.ElementFromString(file)
      except:  #if type(file).__name__ == '_Element' or isinstance(file, basestring) and file.startswith('<?xml '):
        try:   return XML.ElementFromString(file.decode('utf-8','ignore').replace('\b', '').encode("utf-8"))
        except:
          Log.Info("still corrupted xml after normalization")
          if Saved:  Data.Remove(relativeFilename); file=''  #DELETE CACHE AS CORRUPTED
          if Data.Exists(relativeFilename):  return Data.Load(relativeFilename) 
    else:  #Json
      try:     return JSON.ObjectFromString(file, encoding=None)
      except:  pass
  Log.Info('LoadFile() - not xml nor json: {0:80}'.format(file))
  return file
      
### Download images and themes for Plex ###############################################################################################################################
def metadata_download(metadata, metatype, url, filename="", num=99, url_thumbnail=None):
  if   metatype==metadata.posters:             string = "posters"
  elif metatype==metadata.art:                 string = "art"
  elif metatype==metadata.banners:             string = "banners"
  elif metatype==metadata.themes:              string = "themes"
  elif filename.startswith("TVDB/episodes/"):  string = "thumbs"
  else:                                        string = "seasons"
  
  if url in metatype:  Log.Info("url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))
  else:
    file, status = None, ""
    try:
      if filename and Data.Exists(filename):  status += ", Found locally"; file = Data.Load(filename)
      else:
        file = (ssl_open((url_thumbnail or url).replace('thetvdb.com', 'thetvdb.plexapp.com')) if 'thetvdb.com' in url else False) or ssl_open(url_thumbnail or url)
        if file:  status += ", Downloaded and Saved locally";  SaveFile(filename, file)
      if file:  metatype[ url ] = Proxy.Preview(file, sort_order=num) if url_thumbnail else Proxy.Media(file, sort_order=num) # or metatype[ url ] != proxy_item # proxy_item = 
    except Exception as e:  Log.Info("common.SaveFile() - Exception: {}, url: '{}', filename: '{}'".format(e, url, filename));  return
  downloaded[string] = downloaded[string] + 1
  
def cleanse_title(string):
  """ Cleanse title and translate anidb '`'
  """
  DeleteChars  = ""
  ReplaceChars = maketrans("`:~/*?-.,;", "          ") #.;_
  if len(string)<=len(String.StripDiacritics(string))+2:  string = String.StripDiacritics(string)  #else there is jap characters scrubebd outs
  try:       string2 = string.encode('ascii', 'replace')       # Encode into Ascii, prevent: UnicodeDecodeError: 'utf8' codec can't decode bytes in position 13-14: invalid continuation byte
  except:    pass
  else:      
    if not string2.count('?'): string=string2
  while re.search(r'\([^\(\)]*?\)', string):  string = re.sub(r'\([^\(\)]*?\)', ' ', string)  
  while re.search(r'\[[^\[\]]*?\]', string):  string = re.sub(r'\[[^\[\]]*?\]', ' ', string)  # string = "qwerty [asdf] zxcv [vbnm] ghjk [tyui]" > 'qwerty   zxcv   ghjk  ', string = "qwerty [asdf zxcv [vbnm] ghjk tyui]"   > 'qwerty  '
  return " ".join(str(unicodedata.normalize('NFC', unicode(string.lower()))).translate(ReplaceChars, DeleteChars).split())  # str needed for translate
  
def write_logs(media, movie, error_log, source, AniDBid, TVDBid):
  """ HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems
  """
  Log.Info("=== common.write_logs() ===".ljust(157, '='))
  if  source == 'anidb':  source = 'AniDBid'
  elif source == 'tvdb':  source = 'TVDBid'
  
  ### File lock ###
  sleep_time_max = 10
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
    Log.Info("{log:<{width}}: {content}".format(log=log, width=max(map(len, error_log)), content=str(error_log[log])))
    error_log_array    = {}
    log_line_separator = "<br />\r\n"
    error_log_file     = os.path.join('_Logs', log+'.htm')
    if Data.Exists(error_log_file):
      for line in Data.Load(error_log_file).split(log_line_separator):
        if "|" in line:  error_log_array[line.split("|", 1)[0].strip()] = line.split("|", 1)[1].strip()

    ### Remove this serie entry ###
    if not log in ["Missing Episodes", "Missing Specials"]:                              keys = ["AniDBid: "+AniDBid, "AniDBid: "+WEB_LINK % (ANIDB_SERIE_URL + AniDBid, AniDBid), "TVDBid: "+ TVDBid, "TVDBid: "+WEB_LINK % (TVDB_SERIE_URL + TVDBid, TVDBid)]
    elif not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1):  keys = ["TVDBid: %s"  % (WEB_LINK % (TVDB_SERIE_URL + TVDBid,  TVDBid) )]
    else:                                                                                keys = ["%s: %s" % (source, WEB_LINK % (ANIDB_SERIE_URL + AniDBid if source == "AniDBid" else TVDB_SERIE_URL + TVDBid, AniDBid if source == "AniDBid" else TVDBid) )]
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
    try:     Data.Save(error_log_file, log_prefix + log_line_separator.join(sorted([str(key)+" | "+str(error_log_array[key]) for key in error_log_array], key = lambda x: x.split("|",1)[1] if x.split("|",1)[1].strip().startswith("Title:") and not x.split("|",1)[1].strip().startswith("Title: ''") else int(re.sub(r"<[^<>]*>", "", x.split("|",1)[0]).strip().split()[1].strip("'")) )))
    except Exception as e:  Log.Error("Exception: '%s'" % e)
    
    netLocked[log] = (False, 0)

def Other_Tags(media, movie, status):  # Other_Tags(media, Dict(AniDB_dict, 'status') or Dict(TheTVDB_dict, 'status'))
  """ Add genre tags: Status, Extension, Dubbed/Subbed
  """
  tags = []
  if movie:  file = media.items[0].parts[0].file  
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
  
def GetMetadata(media, movie, source, TVDBid, mappingList, num=0):
  """ [tvdb4.posters.xml] Attempt to get the ASS's image data
  """
  Log.Info('=== common.GetMetadata() ==='.ljust(157, '='))
  TVDB4_dict, TVDB4_mapping, TVDB4_xml = {}, None, None

  if movie or not source == "tvdb4":  Log.Info("not tvdb4 mode");  return TVDB4_dict
  Log.Info("tvdb4 mode")

  Log.Info("--- tvdb4.mapping.xml ---".ljust(157, '-'))
  try:
    s      = media.seasons.keys()[0]
    e      = media.seasons[s].episodes.keys()[0]
    folder = os.path.dirname( media.seasons[ s ].episodes[ e ].items[0].parts[0].file)  #folder = os.path.dirname(media.seasons.itervalues().next().episodes.itervalues().next().items[0].parts[0].file)
    while folder and not folder.endswith("/") and not folder.endswith("\\"):
      filename = os.path.join(folder, os.path.basename(TVDB4_MAPPING_URL))
      if os.path.exists(filename):  TVDB4_mapping = Core.storage.load(os.path.realpath(filename));  break
      folder = os.path.dirname(folder)
    else: Log.Info("No 'tvdb4.mapping.xml' file detected locally")
  except Exception as e:  Log.Error("Issues in finding setup info as directories have most likely changed post scan into Plex, Exception: '%s'" % e)
  
  if TVDB4_mapping: Log.Debug("'tvdb4.mapping.xml' file detected locally")
  else:             TVDB4_mapping = TVDB4_mapping or LoadFile(filename=os.path.basename(TVDB4_MAPPING_URL), relativeDirectory="", url=TVDB4_MAPPING_URL, cache= CACHE_1DAY * 6)  # AniDB title database loaded once every 2 weeks
  entry = ""
  if isinstance(TVDB4_mapping, str):  entry = TVDB4_mapping
  else:
    entry = GetXml(TVDB4_mapping, "/tvdb4entries/anime[@tvdbid='%s']" % TVDBid)
    if not entry:  Log.Error("TVDBid '%s' is not found in mapping file" % TVDBid)
  if entry:
    for line in filter(None, entry.strip().splitlines()):
      season = line.strip().split("|")
      for absolute_episode in range(int(season[1]), int(season[2])+1):  SaveDict((str(int(season[0])), str(absolute_episode)), mappingList, 'absolute_map', str(absolute_episode))

  Log.Info("--- tvdb4.posters.xml ---".ljust(157, '-'))
  try:
    s      = media.seasons.keys()[0]
    e      = media.seasons[s].episodes.keys()[0]
    folder = os.path.dirname( media.seasons[ s ].episodes[ e ].items[0].parts[0].file)  #folder = os.path.dirname(media.seasons.itervalues().next().episodes.itervalues().next().items[0].parts[0].file)
    while folder and not folder.endswith("/") and not folder.endswith("\\"):
      filename = os.path.join(folder, os.path.basename(TVDB4_POSTERS_URL))
      if os.path.exists(filename):  TVDB4_xml = XML.ElementFromString( Core.storage.load(os.path.realpath(filename)) );  break
      folder = os.path.dirname(folder)
    else: Log.Info("No 'tvdb4.posters.xml' file detected locally")
  except Exception as e:  Log.Error("Issues in finding setup info as directories have most likely changed post scan into Plex, Exception: '%s'" % e)
  
  if TVDB4_xml: Log.Debug("'tvdb4.posters.xml' file detected locally")
  else:         TVDB4_xml  = TVDB4_xml or LoadFile(filename=os.path.basename(TVDB4_POSTERS_URL), relativeDirectory="", url=TVDB4_POSTERS_URL, cache= CACHE_1DAY * 6)  # AniDB title database loaded once every 2 weeks
  if TVDB4_xml:
    seasonposternum = 0
    entry = GetXml(TVDB4_xml, "/tvdb4entries/posters[@tvdbid='%s']" % TVDBid)
    if not entry:  Log.Error("TVDBid '%s' is not found in posters file" % TVDBid) 
    for line in filter(None, entry.strip().splitlines()):
      season, url       = line.strip().split("|",1)
      season            = season.lstrip("0") if season.lstrip("0") else "0"
      seasonposternum  += 1
      SaveDict(("TheTVDB/seasons/%s-%s-%s" % (TVDBid, season, os.path.basename(url)), 1, None), TVDB4_dict, 'seasons', season, 'posters', url)

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("absolute_map: {}".format(DictString(Dict(mappingList, 'absolute_map', default={}), 0)))
  Log.Info("TVDB4_dict: {}".format(DictString(TVDB4_dict, 4)))
  return TVDB4_dict

### Update meta field ###
def UpdateMetaField(metadata_root, metadata, meta_root, fieldList, field, source, movie, source_list):
  if field not in meta_root:  Log.Info('[!] field: "{}" not in meta_root, source: "{}"'.format(field, source));  return
  if type(metadata).__name__=="tuple":  
    ep_string      = ' new season: {:<2}, new_episode: {:<3}'.format(metadata[3], metadata[4])
    metadata       = metadata[0].seasons[metadata[1]].episodes[metadata[2]]
    is_episode     = True
  else:  ep_string, is_episode = "", False
  
  meta_old       = getattr(metadata, field) # getattr( metadata, field, None)
  meta_new       = meta_root[field]
  meta_new_short = (meta_new[:80]).replace("\n", "\\n").replace("\r", "\\r")+'..' if isinstance(meta_new, basestring) and len(meta_new)> 80 else meta_new
  MetaFieldList  = ('directors', 'writers', 'producers', 'guest_stars', 'collections', 'genres', 'tags', 'countries')
  MetaRoleList   = ('directors', 'writers', 'producers', 'guest_stars', 'roles')
  MetaIntList    = ('year', 'absolute_number', 'duration')
  
  ### Prepare data for comparison ###
  try:
    if isinstance(meta_new, int):
      if field == 'rating':                                          meta_new = float(meta_new)
    if isinstance(meta_new, basestring) or isinstance(meta_new, str):
      if field == 'rating':                                          meta_new = float(meta_new)
      if field == 'title_sort':                                      meta_new = SortTitle(meta_new)
      if field == 'originally_available_at':                         meta_new = Datetime.ParseDate(meta_new).date()
      if field in MetaIntList:                                       meta_new = int(meta_new) if meta_new.isdigit() else None
      if field in MetaFieldList:
        meta_new = re.sub(r'\([^)]*\)', '', meta_new)
        meta_new = meta_new.split(',' if ',' in meta_new else '|')
    if isinstance(meta_new, list) and field in MetaRoleList:
      meta_new = [{'role': Dict(obj, 'role'), 'name': Dict(obj, 'name'), 'photo': Dict(obj,'photo')} if isinstance(obj, dict) else \
                  {'role': None,              'name': obj,               'photo': None} for obj in meta_new]
  except Exception as e:  Log.Info("[!] 1{field:<23}  Sources: {sources:<60}  Value: {value}  Exception: {error}".format(field=field, sources=sources, value=meta_new_short, error=e))
      
  try:
    if not isinstance(meta_new, list):  meta_old_value = meta_old
    elif field in MetaRoleList:         meta_old_value = [ {'role': role_obj.role, 'name': role_obj.name, 'photo': role_obj.photo} for role_obj in meta_old] #if role_obj.role]
    else:                               meta_old_value = [x for x in meta_old]  #meta_old_value = [ {'role': role_obj.role, 'name': role_obj.name, 'photo': role_obj.photo} for role_obj in meta_old]
  except Exception as e:  Log.Info("[!] 2{field:<23}  Sources: {sources:<11}  Value: {value}  Exception: {error}".format(field=field, sources=sources, value=meta_new_short, error=e))
      
  ### Update ONLY IF REQUIRED ###
  if '|' in Prefs[field]:
    if metadata_root==metadata:  sources = '|'.join([Prefs[field].split('|')[is_episode].replace(source, '('+source+')'), Prefs[field].split('|')[1]])
    else:                        sources = '|'.join([Prefs[field].split('|')[is_episode], Prefs[field].split('|')[1].replace(source, '('+source+')')])                   
  else:  sources = Prefs[field].replace(source, '('+source+')')
  
  if isinstance(meta_new, dict) and field=='posters':  Log.Info('[?] meta_new: {}\n    meta_old: {}'.format(DictString(meta_new, 1, 4), DictString(sorted(meta_old.keys(), key=natural_sort_key), 1, 4))) # Can't print meta_old values as plex custom class without a string print call
  if meta_new == meta_old_value or field not in MetaRoleList and (isinstance(meta_new, dict) and set(meta_new.keys()).issubset(meta_old.keys()) or isinstance(meta_new, list) and set(meta_new)== set(meta_old)):
    Log.Info("[=] {field:<23}  {len:>4}  Sources: {sources:<60}  Inside: '{source_list}'  Value: '{value}'".format(field=field, len="({:>2})".format(len(meta_root[field])) if isinstance(meta_root[field], (list, dict)) else "", sources=sources, value=meta_new_short, source_list=source_list))
  else: 
    Log.Info("[x] {field:<23}  {len:>4}  Sources: {sources:<60}  Inside: '{source_list}'  Value: '{value}'".format(field=field, len="({:>2})".format(len(meta_root[field])) if isinstance(meta_root[field], (list, dict)) else "", sources=sources, value=meta_new_short, source_list=source_list))
    if isinstance(meta_new, dict) and field in ['posters', 'banners', 'art', 'themes', 'thumbs']:
      for url in meta_new:
        if not url in meta_old and isinstance(meta_new[url], tuple):  metadata_download(metadata_root, meta_old, url, meta_new[url][0], meta_new[url][1], meta_new[url][2])
    
    elif isinstance(meta_new, list) and field in MetaRoleList:
      try:
        meta_old.clear()
        for item in meta_new:
          meta_role = meta_old.new()
          if not isinstance(item, dict):  setattr(meta_role, 'name', item) #list of names instead of list of people, but should already be list of people
          else:
            for field in item:
              if item[field]:  setattr(meta_role, field, item[field]) 
      except Exception as e:  Log.Info("[!] {field:<29}  Sources: {sources:<60}  Value: {value}  Exception: {error}".format(field=field, sources=sources, value=meta_new_short, error=e))
    else:  
      try:                    setattr(metadata, field, meta_new)  #Type: {format:<20}  #format=type(meta_old).__name__+"/"+type(meta_new).__name__, 
      except Exception as e:  Log.Info("[!] {field:<29}  Sources: {sources:<60}  Value: {value}  Exception: {error}".format(field=field, sources=sources, value=meta_new_short, error=e))
  
def UpdateMeta(metadata, media, movie, MetaSources, mappingList):
  """ Update all metadata from a list of Dict according to set priorities 
  """
  Log.Info("=== common.UpdateMeta() ===".ljust(157, '='))
  # Display source field table
  Log.Info("Fields in Metadata Sources per movie/serie, season, episodes")
  for source in MetaSources:
    if MetaSources[source]:                               Log.Info("- {source:<11}      : {fields}".format(source=source, fields=' | '.join('{}{:<23} ({:>3})'.format('\n                     ' if i%5==0 and i>0 else '', field, len(MetaSources[source][field]) if isinstance(MetaSources[source][field], (list, dict)) else 1) for i, field in enumerate(MetaSources[source]))))
    if type(MetaSources[source]).__name__ == 'NoneType':  Log.Info("[!] source: '%s', type: '%s', bad return in function, should return an empty dict" % (source, type(MetaSources[source]).__name__))
    if 'seasons' in (MetaSources[source] if MetaSources[source] else {}) :
      season_fields, episode_fields, ep_nb, ep_invalid = {}, {}, 0, 0
      for season in sorted(MetaSources[source]['seasons'], key=natural_sort_key):
        for field in MetaSources[source]['seasons'][season]:
          if field in FieldListSeasons:                        season_fields[field] = (season_fields[field] + 1) if field in season_fields else 1
          elif not field=="episodes" and not field.isdigit():  Log.Info("Season Field Unrecognised: '{}' in source: '{}'".format(field, source))
        for episode in sorted(MetaSources[source]['seasons'][season]['episodes'], key=natural_sort_key) if 'episodes' in MetaSources[source]['seasons'][season] else []:
          for field in MetaSources[source]['seasons'][season]['episodes'][episode]:
            if field in FieldListEpisodes:      episode_fields[field] = episode_fields[field] + 1 if field in episode_fields else 1
            elif field is not 'language_rank':  Log.Info("                     {:<23} Season {:>3}, Episode: {:>3} is not a valid metadata field, value: '{!s}'".format(field, season, episode, MetaSources[source]['seasons'][season]['episodes'][episode][field])); ep_invalid+=1
          ep_nb+=1
      if len(season_fields ):  Log.Info("  - Seasons   ({nb:>3}): {fields}".format(nb=len(MetaSources[source]['seasons']), fields=' | '.join('{}{:<23} ({:>3})'.format('\n                     ' if i%5==0 and i>0 else '',field,  season_fields[field]) for i, field in  enumerate(season_fields))))
      if len(episode_fields):  Log.Info("  - Episodes  ({nb:>3}): {fields}".format(nb=ep_nb-ep_invalid                   , fields=' | '.join('{}{:<23} ({:>3})'.format('\n                     ' if i%5==0 and i>0 else '',field, episode_fields[field]) for i, field in enumerate(episode_fields))))
  Log.Info("".ljust(157, '-'))
  #if AniDB_dict['originally_available_at']:  AniDB_dict['year'] = AniDB_dict['originally_available_at'].year

  ### Metadata review display. Legend for the '[ ]' display:
  # [=] already at the right value for that source
  # [x] Xst/nd/th source had the field
  # [#] no source for that field
  # [!] Error assigning
  
  #Update engine
  Log.Info("Metadata Fields (items #), type, source provider, value")
  count     = {'posters':0, 'art':0, 'thumbs':0, 'banners':0, 'themes':0}
  languages = Prefs['EpisodeLanguagePriority'].replace(' ', '').split(',')
  #posters=[]
  
  #fields = metadata.attrs.keys()
  #if 'seasons' in fields:  fields.remove('seasons')
  
  for field in FieldListMovies if movie else FieldListSeries:
    meta_old    = getattr(metadata, field)
    source_list = [ source_ for source_ in MetaSources if Dict(MetaSources, source_, field) ]
    language_rank, language_source = len(languages)+1, None
    for source in [source.strip() for source in (Prefs[field].split('|')[0] if '|' in Prefs[field] else Prefs[field]).split(',') if Prefs[field]]:
      if source in MetaSources:
        #For AniDB assigned series will favor AniDB summary even if TheTVDB is before in the source order for summary fields IF the anidb series is not mapped to TheTVDB season 1.
        if Dict(MetaSources, source, field):
          if field=='genres'and ('|' in MetaSources[source]['genres'] or ',' in MetaSources[source]['genres']):
            MetaSources[source]['genres'] = MetaSources[source]['genres'].split('|' if '|' in MetaSources[source]['genres'] else ',')
            MetaSources[source]['genres'].extend( Other_Tags(media, movie, Dict(MetaSources, 'AniDB', 'status')) )
          if field=='title':
            title, rank = Dict(MetaSources, source, 'title'), Dict(MetaSources, source, 'language_rank')
            if rank in (None, ''):  rank = len(languages)
            if rank<language_rank:  MetaSources[source]['title_sort'], language_rank, language_source = SortTitle(title, IsIndex(languages, rank)), rank, source
          else:  UpdateMetaField(metadata, metadata, MetaSources[source], FieldListMovies if movie else FieldListSeries, field, source, movie, source_list)
          if field in count:  count[field] = count[field] + 1
          if field!='title' and (field not in ['posters', 'art', 'banners', 'themes', 'thumbs', 'title']):  break
      elif not source=="None":  Log.Info("[!] '{}' source not in MetaSources dict, please Check case and spelling".format(source))
    else:
      if field=='title':                                                     UpdateMetaField(metadata, metadata, Dict(MetaSources, language_source, default={}), FieldListMovies if movie else FieldListSeries, 'title', language_source, movie, source_list)  #titles have multiple assignments, adding only once otherwise duplicated field outputs in logs
      elif not Dict(count, field) and Prefs[field]!="None" and source_list:  Log.Info("[#] {field:<29}  Sources: {sources:<60}  Inside: {source_list}  Values: {values}".format(field=field, sources='' if field=='season' else Prefs[field], source_list=source_list, values=Dict(MetaSources, source, field)))
    
    #if field=='posters':  metadata.thumbs.validate_keys(meta_new.keys())
    
  if not movie:
    ### AniDB poster as season poster backup ###
    #if (metadata.id.startswith("tvdb") or max(map(int, media.seasons.keys())) >1) and Dict(mappingList, 'defaulttvdbseason'): # defaulttvdb season isdigit and assigned to 1 tvdb season (even if it is season 0)
    #  if Dict(MetaSources, 'AniDB', 'posters'):  SaveDict(MetaSources['AniDB']['posters'], MetaSources, 'AniDB', 'seasons', Dict(mappingList, 'defaulttvdbseason') if Dict(mappingList, 'defaulttvdbseason').isdigit() else '1', 'posters')
    #  if Dict(MetaSources, 'AniDB', 'summary'):  SaveDict(MetaSources['AniDB']['summary'], MetaSources, 'AniDB', 'seasons', Dict(mappingList, 'defaulttvdbseason') if Dict(mappingList, 'defaulttvdbseason').isdigit() else '1', 'summary')
      
    ### Seasons ###
    #languages      = Prefs['SerieLanguagePriority'].replace(' ', '').split(',')
    #count          = {'posters':0, 'art':0}
    count          = {'posters':0, 'art':0, 'thumbs':0, 'banners':0, 'themes':0}  #@task  #def UpdateEpisodes(metadata=metadata, MetaSources=MetaSources, count=count, season=season, episode=episode, cached_logs=cached_logs):
    cached_logs    = {}
    #@parallelize
    #def addMeta():
    season_posters_list = []
    for season in sorted(media.seasons, key=natural_sort_key):  # For each season, media, then use metadata['season'][season]...
      Log.Info("metadata.seasons[{:>2}]".ljust(157, '-').format(season))
      source_list = [ source_ for source_ in MetaSources if Dict(MetaSources, source_, 'seasons', season, field) ]
      new_season  = season
      for field in FieldListSeasons:  #metadata.seasons[season].attrs.keys()
        meta_old = getattr(metadata.seasons[season], field)
        for source in [source.strip() for source in Prefs[field].split(',') if Prefs[field]]:
          if source in MetaSources:
            if Dict(MetaSources, source, 'seasons', season, field) or metadata.id.startswith('tvdb4'):
              if field=='posters':  season_posters_list.extend(Dict(MetaSources, source, 'seasons', season, 'posters', default={}).keys())
              UpdateMetaField(metadata, metadata.seasons[season], Dict(MetaSources, source, 'seasons', season), FieldListSeasons, field, source, movie, source_list)
              if field in count:  count[field] = count[field] + 1
              if field not in ['posters', 'art']:  break 
          elif not source=="None": Log.Info("[!] {} Sources: '{}' not in MetaSources".format(field, source))
        else:
          if not Dict(count, field) and Dict(Prefs, field)!="None" and source_list:  Log.Info("[#] {field:<29}  Sources: {sources:<60}  Inside: {source_list}".format(field=field, sources='' if field=='seasons' else Prefs[field], source_list=source_list))
      
      ### Episodes ###
      languages = Prefs['EpisodeLanguagePriority'].replace(' ', '').split(',')
      for episode in sorted(media.seasons[season].episodes, key=natural_sort_key):
        Log.Info("metadata.seasons[{:>2}].episodes[{:>3}]".format(season, episode))
        new_season, new_episode = season, episode
        source_title, title, rank = '', '', len(languages)+1
        for field in FieldListEpisodes:  # metadata.seasons[season].episodes[episode].attrs.keys()
          meta_old     = getattr(metadata.seasons[season].episodes[episode], field)
          source_list  = [ source_ for source_ in MetaSources if Dict(MetaSources, source_, 'seasons', new_season, 'episodes', new_episode, field) ]
          for source in [source_.strip() for source_ in (Prefs[field].split('|')[1] if '|' in Prefs[field] else Prefs[field]).split(',')]:  #if shared by title and eps take later priority
            if source in MetaSources:
              if Dict(MetaSources, source, 'seasons', new_season, 'episodes', new_episode, field):
                if not field=='title':  UpdateMetaField(metadata, (metadata, season, episode, new_season, new_episode), Dict(MetaSources, source, 'seasons', new_season, 'episodes', new_episode), FieldListEpisodes, field, source, movie, source_list)
                else:
                  language_rank = Dict(MetaSources, source,  'seasons', new_season, 'episodes', new_episode, 'language_rank')
                  if language_rank not in ('', None) and language_rank < rank or len(languages)< rank:  #Manage title language for AniDB and TheTVDB by recording the rank
                    source_title = source
                    title        = Dict(MetaSources, source,  'seasons', new_season, 'episodes', new_episode, 'title'        )
                    rank         = Dict(MetaSources, source,  'seasons', new_season, 'episodes', new_episode, 'language_rank')
                    Log.Info('[?] rank: {:>1}, source_title: {:>7}, title: "{}"'.format(rank, source_title, title))
                if field in count:  count[field] = count[field] + 1
                if field!='title' and (field not in ['posters', 'art', 'banners', 'themes', 'thumbs', 'title']):  break
            elif not source=="None":  Log.Info("[!] '{}' source not in MetaSources dict, please Check case and spelling".format(source))
          else:
            if field=='title' and source_title:                                    UpdateMetaField(metadata, (metadata, season, episode, new_season, new_episode), Dict(MetaSources, source_title, 'seasons', new_season, 'episodes', new_episode), FieldListEpisodes, field, source_title, movie, source_list)
            elif not Dict(count, field) and field!='seasons' and Prefs[field]!="None" and source_list:  Log.Info("[#] {field:<29}  Sources: {sources:<60}  Inside: {source_list}".format(field=field, sources='' if field=='seasons' else Prefs[field], source_list=source_list))
        if field=='thumbs':    metadata.seasons[season].episodes[episode].thumbs.validate_keys(meta_new.keys())
        # End Of for field
      # End Of for episode
    else:  metadata.seasons[season].posters.validate_keys(season_posters_list)
    # End of for season
    Log.Info("".ljust(157, '-'))
  global downloaded; downloaded = {'posters':0, 'art':0, 'seasons':0, 'banners':0, 'themes':0, 'thumbs': 0} 
  
def LevenshteinDistance(first, second):
  """ Compute Levenshtein distance
  """
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

def SortTitle(title, language="en"):
  """ SortTitle
  """
  dict_sort = { 'en': ["The", "A", "An"],
                'fr': ["Le", "La", "Les", "L", "Un", "Une ", "Des "],
                'sp': ["El", "La", "Las", "Lo", "Los", "Uno ", "Una "]
              }
  title  = title.replace("'", " ")
  prefix = title.split  (" ", 1)[0]  #Log.Info("SortTitle - title:{}, language:{}, prefix:{}".format(title, language, prefix))
  return title.replace(prefix+" ", "", 1) if language in dict_sort and prefix in dict_sort[language] else title 

def AdjustMapping(source, mappingList, dict_AniDB, dict_TheTVDB):
  """ EX:
  season_map: {'max_season': 2, '12560': {'max': 1, 'min': 1}, '13950': {'max': 0, 'min': 0}}
  relations_map: {'12560': {'Sequel': ['13950']}, '13950': {'Prequel': ['12560']}}
  TVDB Before: {'s1': {'12560': '0'}, 's0': {'13950': '0'}, '13950': (0, '')}
    's0e5': ('1', '4', '9453')
    's1': {'12560': '0'}
    '13950': (0, '')
  """
  Log.Info("=== common.AdjustMapping() ===".ljust(157, '=')) 
  is_modified   = False
  adjustments   = {}
  tvdb6_seasons = {1: 1}
  is_banned     = Dict(dict_AniDB,  'Banned',        default=False)
  TVDB          = Dict(mappingList, 'TVDB',          default={})
  season_map    = Dict(mappingList, 'season_map',    default={})
  relations_map = Dict(mappingList, 'relations_map', default={})
  
  if source not in ['tvdb', 'tvdb6']:  Log.Info("source is neither 'tvdb' nor 'tvdb6'");  return is_modified
  Log.Info("adjusting mapping for 'anidb3/tvdb' & 'anidb4/tvdb6' usage") 

  #Log.Info("dict_TheTVDB: {}".format(dict_TheTVDB))
  Log.Info("season_map: {}".format(DictString(season_map, 0)))
  Log.Info("relations_map: {}".format(DictString(relations_map, 1)))

  try:
    Log.Info("--- tvdb mapping adjustments ---".ljust(157, '-'))
    Log.Info("TVDB Before: {}".format(DictString(TVDB, 0)))
    for id in sorted(season_map, key=natural_sort_key):
      new_season, new_episode = '', ''
      if id == 'max_season':  continue
      #### Note: Below must match scanner (variable names are different but logic matches) ####
      Log.Info("Checking AniDBid: %s" % id)
      def get_prequel_info(prequel_id):
        Log.Info("-- get_prequel_info(prequel_id): %s, season min: %s, season max: %s" % (prequel_id, season_map[prequel_id]['min'], season_map[prequel_id]['max']))
        if source=="tvdb":
          if season_map[prequel_id]['min'] == 0 and 'Prequel' in relations_map[prequel_id] and relations_map[prequel_id]['Prequel'][0] in season_map:
            a, b = get_prequel_info(relations_map[prequel_id]['Prequel'][0])             # Recurively go down the tree following prequels
            if not str(a).isdigit():  return ('', '')
            return (a, b+100) if a < season_map['max_season'] else (a+1, 0)  # If the prequel is < max season, add 100 to the episode number offset: Else, add it into the next new season at episode 0
          if season_map[prequel_id]['min'] == 0:                          return ('', '')                              # Root prequel is a special so leave mapping alone as special
          elif season_map[prequel_id]['max'] < season_map['max_season']:  return (season_map[prequel_id]['max'], 100)  # Root prequel season is < max season so add to the end of the Prequel season
          else:                                                           return (season_map['max_season']+1, 0)       # Root prequel season is >= max season so add to the season after max
        if source=="tvdb6":
          if season_map[prequel_id]['min'] != 1 and 'Prequel' in relations_map[prequel_id] and relations_map[prequel_id]['Prequel'][0] in season_map:
            a, b = get_prequel_info(relations_map[prequel_id]['Prequel'][0])             # Recurively go down the tree following prequels
            #Log.Info("%s+%s+%s-%s" % (a,1,season_map[prequel_id]['max'],season_map[prequel_id]['min']))
            return (a+1+season_map[prequel_id]['max']-season_map[prequel_id]['min'], 0) if str(a).isdigit() else ('', '') # Add 1 to the season number and start at episode 0
          return (2, 0) if season_map[prequel_id]['min'] == 1 else ('', '')              # Root prequel is season 1 so start counting up. Else was a sequel of specials only so leave mapping alone
      if source=="tvdb":
        if season_map[id]['min'] == 0 and 'Prequel' in relations_map[id] and relations_map[id]['Prequel'][0] in season_map:
          new_season, new_episode = get_prequel_info(relations_map[id]['Prequel'][0])    # Recurively go down the tree following prequels to a TVDB season non-0 AniDB prequel 
      if source=="tvdb6":
        if 'Prequel' in relations_map[id] and relations_map[id]['Prequel'][0] in season_map:
          new_season, new_episode = get_prequel_info(relations_map[id]['Prequel'][0])    # Recurively go down the tree following prequels to the TVDB season 1 AniDB prequel 

      if str(new_season).isdigit():  # A new season & eppisode offset has been assigned # As anidb4/tvdb6 does full season adjustments, we need to remove and existing season mapping
        is_modified = True
        removed = {}
        for key in TVDB.keys():
          if isinstance(TVDB[key], dict)  and id in TVDB[key]:
            Log.Info("-- Deleted: %s: {'%s': '%s'}" % (key, id, TVDB[key][id]))
            removed[key] = {id: TVDB[key][id]}
            del TVDB[key][id]  # Delete season entries for its old anidb non-s0 season entries | 's4': {'11350': '0'}
          if isinstance(TVDB[key], tuple) and TVDB[key][0] == '1' and TVDB[key][2] == id:
            Log.Info("-- Deleted: {}: {}".format(key, TVDB[key]))
            removed[key] = TVDB[key]
            del TVDB[key]      # Delete episode entries for its old anidb s1 entries           | 's0e5': ('1', '4', '9453')
        SaveDict(str(new_episode), TVDB, 's'+str(new_season), id)
        Log.Info("-- Added  : {}: {}".format('s'+str(new_season), {id: str(new_episode)}))
        
        adjustments['s'+str(new_season)+'e'+str(new_episode)] = {'deleted': removed, 'added': [str(new_season), str(new_episode)]}
        tvdb6_seasons[new_season] = season_map[id]['min']  # tvdb6_seasons[New season] = [Old season]

    Log.Info("TVDB After : {}".format(DictString(Dict(mappingList, 'TVDB'), 0)))
    
    # Push back the 'dict_TheTVDB' season munbers if tvdb6 for the new inserted season
    if source=="tvdb6":
      Log.Info("--- tvdb meta season adjustments ---".ljust(157, '-'))
      top_season, season, adjustment, new_seasons = max(map(int, dict_TheTVDB['seasons'].keys())), 1, 0, {}
      Log.Info("dict_TheTVDB Seasons Before : {}".format(sorted(dict_TheTVDB['seasons'].keys(), key=int)))
      Log.Info("tvdb6_seasons : {}".format(tvdb6_seasons))
      if "0" in dict_TheTVDB['seasons']:  new_seasons["0"] = dict_TheTVDB['seasons'].pop("0")
      while season <= top_season:
        if Dict(tvdb6_seasons, season + adjustment) == 0:
          Log.Info("-- New TVDB season  '{}'".format(season + adjustment))
          adjustment += 1
        else:
          Log.Info("-- Adjusting season '{}' -> '{}'".format(season, season + adjustment))
          if str(season) in dict_TheTVDB['seasons']:  new_seasons[str(season + adjustment)] = dict_TheTVDB['seasons'].pop(str(season))
          season += 1
      SaveDict(new_seasons, dict_TheTVDB, 'seasons')
      Log.Info("dict_TheTVDB Seasons After  : {}".format(sorted(dict_TheTVDB['seasons'].keys(), key=int)))

    # Copy in the 'dict_TheTVDB' deleted episode meta into its new added location
    Log.Info("--- tvdb meta episode adjustments ---".ljust(157, '-'))
    Log.Info("adjustments: {}".format(DictString(adjustments, 2)))
    for entry in sorted(adjustments, key=natural_sort_key):
      # EX: {'s6e0': {'added': ['6', '0'], 'deleted': {'s0e16': ('1', '1', '12909'), 's-1': {'12909': '0'}}}}
      added_season, added_offset = adjustments[entry]['added']  # 'added': ['6', '0']
      Log.Info("added_season: '{}', added_offset: '{}'".format(added_season, added_offset))
      for deleted in sorted(adjustments[entry]['deleted'], key=natural_sort_key):
        Log.Info("-- deleted: '{}': {}".format(deleted, adjustments[entry]['deleted'][deleted]))
        if isinstance(adjustments[entry]['deleted'][deleted], dict):
          deleted_season = deleted[1:]                                         # {-->'s0'<--: {'6463': '0'}}
          deleted_offset = adjustments[entry]['deleted'][deleted].values()[0]  # {'s0': {'6463': -->'0'<--}}
          if deleted=='s-1':
            Log.Info("---- {:<9}: Dead season".format("'%s'" % deleted))
            continue  # EX: {'s-1': {'12909': '0'}}
          if deleted!='s0' and added_offset=='0' and deleted_offset=='0':
            Log.Info("---- {:<9}: Whole season (s1+) was adjusted in previous section".format("'%s'" % deleted))
            continue  # EX: {'s3e0': 'added': ['3', '0'], 'deleted': {'s2': {'7680': '0'}}} == Adjusting season '2' -> '3'
          # EX: {'s2e0': 'added': ['2', '0' ], 'deleted': {'s0': {'6463': '0'}}}
          # EX: {'s1e100': 'added': ['1', '100'], 'deleted': {'s0': {'982': '1'}}}
          interation = 1
          Log.Info("---- deleted_season: '{}', deleted_offset: '{}'".format(deleted_season, deleted_offset))
          while Dict(dict_TheTVDB, 'seasons', deleted_season, 'episodes', str(int(deleted_offset) + interation)):
            a, b, x = deleted_season, str(int(deleted_offset) + interation), str(int(added_offset) + interation)
            SaveDict(Dict(dict_TheTVDB, 'seasons', a, 'episodes', b), dict_TheTVDB, 'seasons', added_season, 'episodes', x)
            Log.Info("---- {:<9}: dict_TheTVDB['seasons']['{}']['episodes']['{}'] => dict_TheTVDB['seasons']['{}']['episodes']['{}']".format("'%s'" % deleted, a, b, added_season, x))
            interation += 1
        if isinstance(adjustments[entry]['deleted'][deleted], tuple):
          a, b = list(filter(None, re.split(r"[se]", deleted)))                        # 's0e16' --> ['0', '16']
          x = str(int(adjustments[entry]['deleted'][deleted][1]) + int(added_offset))  # ('1', -->'1'<--, '12909')
          Log.Info("---- {:<9}: dict_TheTVDB['seasons']['{}']['episodes']['{}'] => dict_TheTVDB['seasons']['{}']['episodes']['{}']".format("'%s'" % deleted, a, b, added_season, x))
          SaveDict(Dict(dict_TheTVDB, 'seasons', a, 'episodes', b), dict_TheTVDB, 'seasons', added_season, 'episodes', x)

  except Exception as e:
    if is_banned:  Log.Info("Expected exception hit, as you were banned from AniDB so you have incomplete data to proceed")
    else:          Log.Error("Unexpected exception hit")
    Log.Info('Exception: "{}"'.format(e))
    Log.Info("Removing AniDB & TVDB data from memory to prevent incorrect data from being loaded")
    dict_AniDB.clear(); dict_TheTVDB.clear()
    is_modified = False

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("is_modified: {}".format(is_modified))
  return is_modified
