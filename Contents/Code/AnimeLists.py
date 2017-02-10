### github.com/ScudLee/anime-lists ###

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import os        # 
import common    # 

### Variables ###
MAPPING_FEEDBACK = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'  # ScudLee mapping file git feedback url

### Functions ###
def MergeAniDBTVDBMaps(AniDBTVDBMap, AniDBTVDBMap_fix):
  if not len(AniDBTVDBMap_fix): return
  correction_nodes = {}
  count            = 0
  for node in AniDBTVDBMap_fix:  correction_nodes[node.get('anidbid')] = node                        # save mod list and nodes
  Log.Info("MergeAniDBTVDBMaps() - Adding/Modifying AniDBids: '%s'" % str(correction_nodes.keys()))  #
  for node in AniDBTVDBMap:                                                                          # LOOP IN EVERY ANIME IN MAPPING FILE
    if node.get('anidbid') in correction_nodes:  AniDBTVDBMap.remove(node); count+=1                 #   if a correction exists: remove old mapping from AniDBTVDBMap
    if count == len(correction_nodes):  break                                                        #   if deleted all exit loop
  for key in correction_nodes:  AniDBTVDBMap.append( correction_nodes[key] )                         # add all new anidb mapping

def GetAniDBTVDBMap():  # anidb to tvdb imdb tmdb mapping file - Loading AniDBTVDBMap from MAPPING url with MAPPING_FIX corrections ###
  MAPPING          = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list-master.xml'                 # ScudLee mapping file url
  MAPPING_FIX      = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/anime-list-corrections.xml' # ScudLee mapping file url online override
  
  AniDBTVDBMap     = common.LoadFile(filename=os.path.basename(MAPPING    ), relativeDirectory="", url=MAPPING,     cache= CACHE_1DAY * 14)  # AniDB title database loaded once every 2 weeks
  AniDBTVDBMap_fix = common.LoadFile(filename=os.path.basename(MAPPING_FIX), relativeDirectory="", url=MAPPING_FIX, cache= CACHE_1DAY *  2)  # AniDB title database loaded once every 2 weeks
  MergeAniDBTVDBMaps(AniDBTVDBMap, AniDBTVDBMap_fix)
  if not AniDBTVDBMap:  Log.Critical("Failed to load core file '{file}'".format(url=os.path.splitext(os.path.basename(MAPPING)))); AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>")  #; raise Exception("HAMA Fatal Error Hit")
  return AniDBTVDBMap

def GetAniDBMovieSets():  # Anidb Movie collection
  ANIME_MOVIESET = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-movieset-list.xml'
  
  AniDBMovieSets = common.LoadFile(filename=os.path.basename(ANIME_MOVIESET), relativeDirectory="", url=ANIME_MOVIESET, cache= CACHE_1WEEK * 2)
  if not AniDBMovieSets:  Log.Error ("Failed to load core file '%s'" % os.path.basename(MOVIE_COLLECTION));  AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>") 
  return AniDBMovieSets
  
def anidbTvdbMapping(metadata, media, movie, anidb_id, error_log, AniDBTVDBMap):  # Get the tvdbId from the AnimeId
  MAPPING_CUSTOM = 'anime-list-custom.xml'  # ScudLee mapping file url local  override
  
  mappingList, dir, scudlee_mapping_tree = {}, "", AniDBTVDBMap 
  mappingList['poster_id_array']={}
  #Log.Info("anidbTvdbMapping() - Finding media path")
  if movie: dir = os.path.dirname(media.items[0].parts[0].file)
  else:     #seasons[-1].episodes[-1].items[0].parts[0].file) #TypeError: unhashable type #if hasattr(media, 'seasons'):
    for s in media.seasons:  #get first file path
      for e in media.seasons[s].episodes:  dir = os.path.dirname( media.seasons[s].episodes[e].items[0].parts[0].file); break
      break
  #Log.Info("anidbTvdbMapping() - dir: '%s'" % dir)
  while dir and not dir.endswith("/") and not dir.endswith("\\"):
    scudlee_filename_custom = os.path.join(dir, MAPPING_CUSTOM)
    if os.path.exists(scudlee_filename_custom):
      Log.Info("anidbTvdbMapping() - Loading local custom mapping - url: '%s'" % scudlee_filename_custom)
      try:
        scudlee_local_fix = XML.ElementFromString( Core.storage.load(os.path.realpath(scudlee_filename_custom)) )  #no caching since local
        MergeAniDBTVDBMaps(scudlee_mapping_tree, scudlee_local_fix)
      except Exception as e:  Log.Info("anidbTvdbMapping() - Failed open scudlee_filename_custom, error: '%s'" % e); scudlee_1 = "<anime-list></anime-list>"
      break
    #else: Log.Info("anidbTvdbMapping() - No local custom mapping in dir: '%s'" % dir)
    dir = os.path.dirname(dir)
  else: Log.Info("anidbTvdbMapping() - Local custom mapping - No file detected")
  for anime in scudlee_mapping_tree.iter('anime') if scudlee_mapping_tree else []:
    AniDBid                          = anime.get("anidbid",           "")
    TVDBid                           = anime.get('tvdbid',            "")
    mappingList['defaulttvdbseason'] = anime.get('defaulttvdbseason', "")
    mappingList['episodeoffset'    ] = anime.get('episodeoffset',     "")
    if TVDBid.isdigit():
      if TVDBid in mappingList['poster_id_array']:  mappingList['poster_id_array'][TVDBid].append(AniDBid)
      else:                                         mappingList['poster_id_array'][TVDBid] = [AniDBid]
    if AniDBid == anidb_id: #manage all formats latter
      mappingList['name'] = anime.xpath("name")[0].text
      if TVDBid.isdigit():
        imdbid = anime.get('tmdbid',            "")
        tmdbid = anime.get('imdbid',            "")
        try: ### mapping list ###
          for season in anime.iter('mapping') if anime else []:
            if anime.get("offset"):  mappingList[ 's'+season.get("tvdbseason")] = [anime.get("start"), anime.get("end"), anime.get("offset")]
            for string2 in filter(None, season.text.split(';')):  mappingList [ 's' + season.get("anidbseason") + 'e' + string2.split('-')[0] ] = 's' + season.get("tvdbseason") + 'e' + string2.split('-')[1]
        except Exception as e:  Log.Error("anidbTvdbMapping() - mappingList creation exception, Exception: '%s'" % e)
      elif TVDBid in ("", "unknown"):  error_log ['anime-list TVDBid missing'].append("AniDBid: %s | Title: '%s' | Has no matching TVDBid ('%s') in mapping file | " % (anidb_id, mappingList['name'], TVDBid) + common.WEB_LINK % (MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; TVDBid:" % (anidb_id, mappingList['name']), string.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
      try:    mappingList['mapping_studio'] = anime.xpath("supplemental-info/studio")[0].text
      except: mappingList['mapping_studio'] = ""
      Log.Info("anidbTvdbMapping() - anidb: '%s', tvbdid: '%s', tmdbid: '%s', imbdid: '%s', studio: '%s', defaulttvdbseason: '%s', name: '%s'" % (AniDBid, TVDBid, tmdbid, imdbid, mappingList['mapping_studio'], mappingList['defaulttvdbseason'], mappingList['name']) )
      if not TVDBid.isdigit():
        Log.Warn("'anidbTvdbMapping() - anime-list TVDBid missing.htm' log added as tvdb serie id missing in mapping file: '%s'" % TVDBid)
        error_log['anidbTvdbMapping() - anime-list TVDBid missing'].append("AniDBid: '%s' | TVDBid: '%s' | Serie not in thetvdb" % (common.WEB_LINK % (common.ANIDB_SERIE_URL % AniDBid, AniDBid), TVDBid))
      return TVDBid, tmdbid, imdbid, mappingList
  else:
    Log.Error("anidbTvdbMapping() - AniDBid '%s' not found in file" % anidb_id)
    error_log['anime-list AniDBid missing'].append("AniDBid: %s | Title: 'UNKNOWN'" % common.WEB_LINK % (common.ANIDB_SERIE_URL % AniDBid, AniDBid))
    return "", "", "", {}
