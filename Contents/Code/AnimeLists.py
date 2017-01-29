### ScudLee Anime-List ###
import common

MOVIE_COLLECTION = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-movieset-list.xml'               # ScudLee Movie collection mapping file
MAPPING          = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list-master.xml'                 # ScudLee mapping file url
MAPPING_FIX      = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/anime-list-corrections.xml' # ScudLee mapping file url online override
MAPPING_CUSTOM   = 'anime-list-custom.xml'                                                                              # ScudLee mapping file url local  override
MAPPING_FEEDBACK = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'                                  # ScudLee mapping file git feedback url

AniDB_TVDB_mapping_tree  = common.LoadFile(filename=os.path.basename(MAPPING    ), relativeDirectory="", url=MAPPING,     cache= CACHE_1HOUR * 24 * 14)  # AniDB title database loaded once every 2 weeks
AniDB_TVDB_corrections   = common.LoadFile(filename=os.path.basename(MAPPING_FIX), relativeDirectory="", url=MAPPING_FIX, cache= CACHE_1HOUR * 24 *  2)  # AniDB title database loaded once every 2 weeks
correction_list_nodes    = {}
for node in AniDB_TVDB_corrections:  correction_list_nodes[node.get('anidbid')] = node #save mod list and nodes
Log.Info("AniDB_TVDB_corrections, correcting mapping for anidbid: '%s'" % str(correction_list_nodes.keys()))
for node in AniDB_TVDB_mapping_tree:
  if node.get('anidbid') in correction_list_nodes:                                              # if a correction exists
    AniDB_TVDB_mapping_tree.remove(node);                                                       # remove old mapping
    AniDB_TVDB_mapping_tree.append( correction_list_nodes[node.get('anidbid')] )                # add new mapping
    del correction_list_nodes[node.get('anidbid')]                                              # remove it from the dict
  if not len(correction_list_nodes):  break                                                     # if dict empty we stop
for key in correction_list_nodes:  AniDB_TVDB_mapping_tree.append( correction_list_nodes[key] ) # if some things weren't added, it's add all new anidb mapping
if not AniDB_TVDB_mapping_tree:
  Log.Critical("Failed to load core file '{file}'".format(url=os.path.splitext(os.path.basename(MAPPING))))
  raise Exception("HAMA Fatal Error Hit")
      
AniDB_collection_tree = common.LoadFile(filename=os.path.basename(MOVIE_COLLECTION), relativeDirectory="", url=MOVIE_COLLECTION, cache= CACHE_1HOUR * 24 * 14)  # AniDB title database loaded once every 2 weeks
if not AniDB_collection_tree:   Log.Error   ("Failed to load core file '%s'" % os.path.basename(MOVIE_COLLECTION  )); AniDB_collection_tree  = XML.ElementFromString("<anime-set-list></anime-set-list>"); 

### Get the tvdbId from the AnimeId #######################################################################################################################
def anidbTvdbMapping(metadata, media, movie, anidb_id, error_log):
  mappingList, dir, scudlee_mapping_tree,  = {}, "", AniDB_TVDB_mapping_tree 
  mappingList['poster_id_array']={}
  Log.Info("Finding media path")
  
  if movie: dir = os.path.dirname(media.items[0].parts[0].file)
  else:      #dir = os.path.dirname(media.seasons[:1].episodes[:1].items[0].parts[0].file) #TypeError: unhashable type #if hasattr(media, 'seasons'):
    for s in media.seasons:  #get first file path
      for e in media.seasons[s].episodes:
        dir = os.path.dirname( media.seasons[s].episodes[e].items[0].parts[0].file); break
      break
  Log.Info("dir: '%s'" % dir)
  while dir and not dir.endswith("/") and not dir.endswith("\\"):
    scudlee_filename_custom = os.path.join(dir, MAPPING_CUSTOM)
    if os.path.exists(scudlee_filename_custom):
      Log.Info("Loading local custom mapping - url: '%s'" % scudlee_filename_custom)
      try:
        with io.open(os.path.realpath(scudlee_filename_custom), "r") as file:  scudlee_1 = file.read()
        scudlee_2            = etree.tostring( AniDB_TVDB_mapping_tree, encoding="UTF-8", method="xml")
        scudlee_mapping_tree = etree.fromstring( scudlee_1[:scudlee_1.rfind("</anime-list>")-1] + scudlee_2[scudlee_2.find("<anime-list>")+len("<anime-list>")+1:] )  #cut both fiels together removing ending and starting tags to do so
      except Exception as e:  Log.Info("Failed open scudlee_filename_custom, error: '%s'" % e); scudlee_1 = "<anime-list></anime-list>"
      break
    else: Log.Info("No local custom mapping in dir: '%s'" % dir)
    dir = os.path.dirname(dir)
  else: Log.Info("Local custom mapping - No file detected")
  for anime in scudlee_mapping_tree.iter('anime') if scudlee_mapping_tree else []:
    anidbid, tvdbid, tmdbid, imdbid, mappingList['defaulttvdbseason'], mappingList['episodeoffset'] = anime.get("anidbid"), anime.get('tvdbid'), anime.get('tmdbid'), anime.get('imdbid'), anime.get('defaulttvdbseason'), anime.get('episodeoffset')
    if tvdbid.isdigit():  mappingList['poster_id_array'][tvdbid] = mappingList['poster_id_array'][tvdbid] + 1 if tvdbid in mappingList['poster_id_array'] else 0  # Count posters to have a unique poster per anidbid
    if anidbid == anidb_id: #manage all formats latter
      name = anime.xpath("name")[0].text 
      if tvdbid.isdigit():
        try: ### mapping list ###
          for season in anime.iter('mapping') if anime else []:
            if anime.get("offset"):  mappingList[ 's'+season.get("tvdbseason")] = [anime.get("start"), anime.get("end"), anime.get("offset")]
            for string2 in filter(None, season.text.split(';')):  mappingList [ 's' + season.get("anidbseason") + 'e' + string2.split('-')[0] ] = 's' + season.get("tvdbseason") + 'e' + string2.split('-')[1]
        except Exception as e:  Log.Error("mappingList creation exception, Exception: '%s'" % e)
      elif tvdbid in ("", "unknown"):  error_log ['anime-list tvdbid missing'].append("anidbid: %s | Title: '%s' | Has no matching tvdbid ('%s') in mapping file | " % (anidb_id, name, tvdbid) + common.WEB_LINK % (MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; tvdbid:" % (anidb_id, name), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
      try:    mappingList['mapping_studio'] = anime.xpath("supplemental-info/studio")[0].text
      except: mappingList['mapping_studio'] = ""
      Log.Info("anidb: '%s', tvbdid: '%s', tmdbid: '%s', imbdid: '%s', studio: '%s', defaulttvdbseason: '%s', name: '%s'" % (anidbid, tvdbid, tmdbid, imdbid, mappingList['mapping_studio'], mappingList['defaulttvdbseason'], name) )
      if not tvdbid.isdigit():
        Log.Warn("'anime-list tvdbid missing.htm' log added as tvdb serie id missing in mapping file: '%s'" % tvdbid)
        error_log['anime-list tvdbid missing'].append("anidbid: '%s' | tvdbid: '%s' | Serie not in thetvdb" % (common.WEB_LINK % (common.ANIDB_SERIE_URL % anidbid, anidbid), tvdbid))
      return tvdbid, tmdbid, imdbid, mappingList
  else:
    Log.Error("anidbid '%s' not found in file" % anidb_id)
    error_log['anime-list anidbid missing'].append("anidbid: %s | Title: 'UNKNOWN'" % common.WEB_LINK % (ANIDB_SERIE_URL % anidbid, anidbid))
    return "", "", "", {}
