### ScudLee Anime-List ###
import common

MOVIE_COLLECTION = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-movieset-list.xml'               # ScudLee Movie collection mapping file
MAPPING          = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list-master.xml'                 # ScudLee mapping file url
MAPPING2         = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/anime-list-corrections.xml' # ScudLee mapping file url online override
MAPPING_CUSTOM   = 'anime-list-custom.xml'                                                                              # ScudLee mapping file url local  override
MAPPING_FEEDBACK = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'                                  # ScudLee mapping file git feedback url

AniDB_TVDB_mapping_tree = common.xmlElementFromFile(MAPPING,          os.path.basename(MAPPING         ), False, CACHE_1HOUR * 24 * 2); scudlee_2               = etree.tostring( AniDB_TVDB_mapping_tree, encoding="UTF-8", method="xml")
AniDB_TVDB_mapping_tree = common.xmlElementFromFile(MAPPING2,         os.path.basename(MAPPING2        ), False, CACHE_1HOUR * 24 * 2); scudlee_1               = etree.tostring( AniDB_TVDB_mapping_tree, encoding="UTF-8", method="xml")
AniDB_TVDB_mapping_tree = etree.fromstring( scudlee_1[:scudlee_1.rfind("</anime-list>")-1] + scudlee_2[scudlee_2.find("<anime-list>")+len("<anime-list>")+1:] )  #cut both fiels together removing ending and starting tags to do so  
if not AniDB_TVDB_mapping_tree: Log.Critical("Failed to load core file '%s'" % os.path.basename(MAPPING));            raise Exception("HAMA Fatal Error Hit") #; AniDB_TVDB_mapping_tree = XML.ElementFromString("<anime-list></anime-list>")

AniDB_collection_tree   = common.xmlElementFromFile(MOVIE_COLLECTION, os.path.basename(MOVIE_COLLECTION), False, CACHE_1HOUR * 24 * 2)
if not AniDB_collection_tree:   Log.Error   ("Failed to load core file '%s'" % os.path.basename(MOVIE_COLLECTION  )); AniDB_collection_tree  = XML.ElementFromString("<anime-set-list></anime-set-list>"); 

### Get the tvdbId from the AnimeId #######################################################################################################################
def anidbTvdbMapping(metadata, media, movie, anidb_id, error_log):
  dir, scudlee_mapping_tree, poster_id_array, mappingList = "", AniDB_TVDB_mapping_tree, {}, {}
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
      except Exception as e:  Log.Info("Failed open scudlee_filename_custom, error: '%s'" % e); scudlee_1 = "<anime-list></anime-list>"
      else:
        scudlee_2            = etree.tostring( AniDB_TVDB_mapping_tree, encoding="UTF-8", method="xml")
        scudlee_mapping_tree = etree.fromstring( scudlee_1[:scudlee_1.rfind("</anime-list>")-1] + scudlee_2[scudlee_2.find("<anime-list>")+len("<anime-list>")+1:] )  #cut both fiels together removing ending and starting tags to do so
      break
    else: Log.Info("No local custom mapping in dir: '%s'" % dir)
    dir = os.path.dirname(dir)
  else: Log.Info("Local custom mapping - No file detected")
  for anime in scudlee_mapping_tree.iter('anime') if scudlee_mapping_tree else []:
    anidbid, tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList['episodeoffset'] = anime.get("anidbid"), anime.get('tvdbid'), anime.get('tmdbid'), anime.get('imdbid'), anime.get('defaulttvdbseason'), anime.get('episodeoffset')
    if tvdbid.isdigit():  poster_id_array [tvdbid] = poster_id_array [tvdbid] + 1 if tvdbid in poster_id_array else 0  # Count posters to have a unique poster per anidbid
    if anidbid == anidb_id: #manage all formats latter
      name = anime.xpath("name")[0].text 
      if tvdbid.isdigit():
        try: ### mapping list ###
          for season in anime.iter('mapping') if anime else []:
            if anime.get("offset"):  mappingList[ 's'+season.get("tvdbseason")] = [anime.get("start"), anime.get("end"), anime.get("offset")]
            for string2 in filter(None, season.text.split(';')):  mappingList [ 's' + season.get("anidbseason") + 'e' + string2.split('-')[0] ] = 's' + season.get("tvdbseason") + 'e' + string2.split('-')[1]
        except Exception as e:  Log.Error("mappingList creation exception, Exception: '%s'" % e)
      elif tvdbid in ("", "unknown"):  error_log ['anime-list tvdbid missing'].append("anidbid: %s | Title: '%s' | Has no matching tvdbid ('%s') in mapping file | " % (anidb_id, name, tvdbid) + WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; tvdbid:" % (anidb_id, name), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
      try:    mapping_studio = anime.xpath("supplemental-info/studio")[0].text
      except: mapping_studio = ""
      Log.Info("anidb: '%s', tvbdid: '%s', tmdbid: '%s', imbdid: '%s', studio: '%s', defaulttvdbseason: '%s', name: '%s'" % (anidbid, tvdbid, tmdbid, imdbid, mapping_studio, defaulttvdbseason, name) )
      anidbid_table = []
      for anime2 in AniDB_collection_tree.iter("anime") if AniDB_collection_tree else []:
        if tvdbid == anime2.get('tvdbid'):  anidbid_table.append( anime2.get("anidbid") ) #collection gathering
      if not tvdbid.isdigit():
        Log.Warn("'anime-list tvdbid missing.htm' log added as tvdb serie deleted: '%s', modify in custom mapping file to circumvent but please submit feedback to ScumLee's mapping file using html log link" % (TVDB_SERIE_URL % (tvdbid, tvdbid)))
        error_log['anime-list tvdbid missing'].append("anidbid: %s | tvdbid: %s | " % (WEB_LINK % (ANIDB_SERIE_URL % anidbid, anidbid), WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid)) + " | Not downloadable so serie deleted from thetvdb")
      return tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio, anidbid_table, poster_id_array [tvdbid] if tvdbid in poster_id_array else {}
  else:
    Log.Error("anidbid '%s' not found in file" % anidb_id)
    error_log['anime-list anidbid missing'].append("anidbid: %s | Title: 'UNKNOWN'" % WEB_LINK % (ANIDB_SERIE_URL % anidbid, anidbid))
    return "", "", "", "", [], "", [], "0"
