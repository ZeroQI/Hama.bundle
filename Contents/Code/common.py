### common ###
#@parallelize @task
AniDB_title_tree          = None
AniDB_collection_tree     = None
AniDB_TVDB_mapping_tree   = None
error_log_locked          = {}
error_log_lock_sleep      = 10

#ASS_MAPPING_URL = 'http://rawgit.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.mapping.xml'                        #
ASS_POSTERS_URL  = 'http://rawgit.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.posters.xml'                        #
SPLIT_CHARS      = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations

#
RESTRICTED_GENRE          = {'X': ["18 restricted", "pornography"], 'TV-MA': ["tv censoring", "borderline porn"]}
MOVIE_RATING_MAP          = {'TV-Y': 'G', 'TV-Y7': 'G', 'TV-G': 'G', 'TV-PG': 'PG', 'TV-14': 'PG-13', 'TV-MA': 'NC-17', 'X': 'X'}
FILTER_CHARS              = "\\/:*?<>|~-; "
WEB_LINK                  = "<a href='%s' target='_blank'>%s</a>"
FILTER_SEARCH_WORDS = [ ### These are words which cause extra noise due to being uninteresting for doing searches on, Lowercase only #############################################################
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime', 'ni', 'sekai',                                             # Jp
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', 'me',  'princess', 'theater',  # En Continued
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses',                                                                                                               # Fr
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi']                                                              # Roman digits

import logging
hama_logger, formatter = logging.getLogger('com.plexapp.agents.hama'), logging.Formatter('%(asctime)-15s - %(name)s (%(thread)x) : %(levelname)s (%(module)s/%(funcName)s:%(lineno)d) - %(message)s')
#Log("Loggers: %s" % logging.Logger.manager.loggerDict)  #Log("Logger->Handlers: 'com.plexapp.agents.hama': %s" % hama_logger.handlers)
for handler in hama_logger.handlers:  handler.setFormatter(formatter)

### 
GetElementText = lambda el, xp: el.xpath(xp)[0].text if el and el.xpath(xp) and el.xpath(xp)[0].text else ""  # helper for getting text from XML element
    
### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs(): #     a = sum(getattr(t, name, 0) for name in "xyz")
  Log.Info( "ValidatePrefs()")
  DefaultPrefs = ("GetTvdbFanart", "GetTvdbPosters", "GetTvdbBanners", "GetAnidbPoster", "GetTmdbFanart", "GetTmdbPoster", "GetOmdbPoster", "GetFanartTVBackground", "GetFanartTVPoster", "GetFanartTVBanner", "GetASSPosters", "localart", "adult", 
                  "GetPlexThemes", "MinimumWeight", "SerieLanguage1", "SerieLanguage2", "SerieLanguage3", "EpisodeLanguage1", "EpisodeLanguage2")
  try:  
    for key in DefaultPrefs: Log.Info("Prefs[{key:<{width}}] = {value}".format(key=key, width=max(map(len, DefaultPrefs)), value=Prefs[key]))
    if [Prefs[key] == None for key in DefaultPrefs].count(True) > 0: Log.Error("Some Pref values do not exist. Edit and save your preferences.")
  except:  Log.Error("DefaultPrefs.json invalid, Value '%s' missing, update it and save." % key);  return MessageContainer ('Error', "Value '%s' missing from 'DefaultPrefs.json'" % key)
  else:    Log.Info( "DefaultPrefs.json is valid, Provided preference values are ok");             return MessageContainer ('Success', "DefaultPrefs.json valid")

### [tvdb4.posters.xml] Attempt to get the ASS's image data ###############################################################################################################
def getImagesFromASS(metadata, media, tvdbid, movie, num=0):
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
  try:                    postersXml = XML.ElementFromURL( ASS_POSTERS_URL, cacheTime=CACHE_1HOUR * 24)
  except Exception as e:  Log.Error("Loading poster XML failed: '%s', Exception: '%s'"% (ASS_POSTERS_URL, e)); return
  else:                   Log.Info( "Loaded poster XML: '%s'" % ASS_POSTERS_URL)
  entry = postersXml.xpath("/tvdb4entries/posters[@tvdbid='%s']" % tvdbid)
  if not entry: Log.Error("tvdbid '%s' is not found in xml file" % tvdbid); return
  for line in filter(None, entry[0].text.strip().replace("\r","\n").split("\n")):
    num += 1; seasonposternum += 1
    season, posterURL = line.strip().split("|",1); season = str(int(season)) #str(int(x)) remove leading 0 from number string
    posterPath = "seasons/%s-%s-%s" % (tvdbid, season, os.path.basename(posterURL))
    if movie or season not in media.seasons:  continue
    common.metadata_download (metadata.seasons[season].posters, posterURL, num, "TVDB/"+posterPath)
  return posternum, seasonposternum

#########################################################################################################################################################
def metadata_download (metatype, url, num=99, filename="", url_thumbnail=None):  #if url in metatype:#  Log.Debug("url: '%s', num: '%s', filename: '%s'*" % (url, str(num), filename)) # Log.Debug(str(metatype))   #  return
  if isinstance(url, str):  Log.Info( "before %s" % url);             return MessageContainer ('Success', "DefaultPrefs.json valid")
  else: Log.Info( "before %d" % url)
  if url not in metatype:
    Log.Info( "after");             return MessageContainer ('Success', "DefaultPrefs.json valid")
    file = None
    if filename and Data.Exists(filename):  ### if stored locally load it
      try:                    file = Data.Load(filename)
      except Exception as e:  Log.Warn("could not load file '%s' present in cache, Exception: '%s'" % (filename, e))
    if file == None: ### if not loaded locally download it
      try:                    file = HTTP.Request(url_thumbnail if url_thumbnail else url, cacheTime=None).content
      except Exception as e:  Log.Error("error downloading, Exception: '%s'" % e); return
      else:  ### if downloaded, try saving in cache but folders need to exist
        if filename and not filename.endswith("/"):
          try:                    Data.Save(filename, file)
          except Exception as e:  Log.Error("could not write filename '%s' in Plugin Data Folder, Exception: '%s'" % (filename, e)); return
    if file:
      try:                    metatype[ url ] = Proxy.Preview(file, sort_order=num) if url_thumbnail else Proxy.Media(file, sort_order=num) # or metatype[ url ] != proxy_item # proxy_item = 
      except Exception as e:  Log.Error("issue adding picture to plex - url downloaded: '%s', filename: '%s', Exception: '%s'" % (url_thumbnail if url_thumbnail else url, filename, e)) #metatype.validate_keys( url_thumbnail if url_thumbnail else url ) # remove many posters, to avoid
      else:                   Log.Info( "url: '%s', num: '%d', filename: '%s'" % (url, num, filename))
  else:  Log.Info("url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))

### get_json file, TMDB API supports only JSON now ######################################################################################################
def get_json(url, cache_time=CACHE_1MONTH):
  try:                    return JSON.ObjectFromURL(url, sleep=2.0, cacheTime=cache_time)
  except Exception as e:  Log.Error("Error fetching JSON url: '%s', Exception: '%s'" % (url, e))

### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
def cleanse_title(title):
  cleansed_title = title.replace("`", "'").lower()
  try:    cleansed_title=cleansed_title.encode('utf-8')
  except: pass
  for i in SPLIT_CHARS:
    if i in cleansed_title:  cleansed_title = cleansed_title.replace(i, " ")
  return  " ".join(cleansed_title.split()) # None in the translate call was giving an error of 'TypeError: expected a character buffer object'. So, we construct a blank translation table instead.

### Pull down the XML from web and cache it or from local cache for a given anime ID ####################################################################
def xmlElementFromFile(url, filename="", delay=True, cache=None):
  Log.Info("url: '%s', filename: '%s'" % (url, filename))
  if delay:  time.sleep(4) #2s between anidb requests but 2 threads #### Ban after 160 series if too short, ban also if same serie xml downloaded repetitively, delay for AniDB only for now  #try:    a = urllib.urlopen(url)#if a is not None and a.getcode()==200:
  try:                    result = str(HTTP.Request(url, headers={'Accept-Encoding':'gzip', 'content-type':'charset=utf8'}, timeout=20, cacheTime=cache))                                     # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find'
  except Exception as e:  result = None; Log.Warn("XML issue loading url: '%s', filename: '%s', Exception: '%s'" % (url, filename, e))                                                           # issue loading, but not AniDB banned as it returns "<error>Banned</error>"

  if result and len(result)>1024 and filename:  # if loaded OK save else load from last saved file
    try:                    Data.Save(filename, result)
    except Exception as e:  Log.Warn("url: '%s', filename: '%s' saving failed, probably missing folder, Exception: '%s'" % (url, filename, e))
  elif filename and Data.Exists(filename):  # Loading locally if backup exists
    Log.Info("Loading locally since banned or empty file (result page <1024 bytes)")
    try:                    result = Data.Load(filename)
    except Exception as e:  Log.Error("Loading locally failed but data present - url: '%s', filename: '%s', Exception: '%s'" % (url, filename, e)); return
  if result:
    element = XML.ElementFromString(result)
    if str(element).startswith("<Element error at "):  Log.Error("Not an XML file, AniDB banned possibly, result: '%s'" % result)
    else:                                              return element

### HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems ###
def write_logs(media, movie, error_log, metadata_id_source_core, metadata_id_number, anidbid, tvdbid):
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
    if log == 'TVDB posters missing': log_prefix = WEB_LINK % ("http://thetvdb.com/wiki/index.php/Posters",              "Restrictions") + log_line_separator
    if log == 'Plex themes missing':  log_prefix = WEB_LINK % ("https://plexapp.zendesk.com/hc/en-us/articles/201572843","Restrictions") + log_line_separator
    for entry in error_log[log]:  error_log_array[entry.split("|", 1)[0].strip()] = entry.split("|", 1)[1].strip()
    import AniDB, tvdb
    if error_log[log] == []:
      if not log in ["Missing Episodes", "Missing Specials"]:                              keys = ["anidbid: %s" % (WEB_LINK % (AniDB.ANIDB_SERIE_URL % anidbid, anidbid)), "anidbid: %s" % anidbid, "tvdbid: %s" % (WEB_LINK % (tvdb.TVDB_SERIE_URL   % tvdbid,  tvdbid ) ), "tvdbid: %s" % tvdbid]
      elif not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1):  keys = ["tvdbid: %s"  % (WEB_LINK % (tvdb.TVDB_SERIE_URL  % tvdbid,  tvdbid) )]
      else:                                                                                keys = ["%sid: %s" % (metadata_id_source_core, WEB_LINK % (AniDB.ANIDB_SERIE_URL % metadata_id_number if metadata_id_source_core == "anidb" else tvdb.TVDB_SERIE_URL % metadata_id_number, metadata_id_number) )]
      for key in keys: 
        if key in error_log_array.keys():  del(error_log_array[key])
    Data.Save(log+".htm", log_prefix + log_line_separator.join(sorted([str(key)+" | "+str(error_log_array[key]) for key in error_log_array.keys()], key = lambda x: x.split("|",1)[1] if x.split("|",1)[1].strip().startswith("Title:") and not x.split("|",1)[1].strip().startswith("Title: ''") else int(re.sub("<[^<>]*>", "", x.split("|",1)[0]).strip().split()[1]) )))
    error_log_locked[log] = [False, 0]
    Log.Debug("Unlocked '%s' %s" % (log, error_log_locked[log]))
    
