### github.com/ScudLee/anime-lists ###

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import os          # os.path(.basename, .splitext, .foldername, .dirname, .exists, .join, .realpath)
import common      # 
from   common import GetXml, SaveDict, Dict

### Variables ###

### Functions ###

###
def MergeMaps(AniDBTVDBMap, AniDBTVDBMap_fix):
  dict_nodes = {}
  count      = 0
  for node in AniDBTVDBMap_fix:  dict_nodes[node.get('anidbid')] = node         # save mod list and nodes
  Log.Info("MergeMaps() - AniDBids concerned: " + str(dict_nodes.keys()))       #
  for node in AniDBTVDBMap if AniDBTVDBMap_fix else []:                         # LOOP IN EVERY ANIME IN MAPPING FILE
    if node.get('anidbid') in dict_nodes:  AniDBTVDBMap.remove(node); count+=1  #   if a correction exists: remove old mapping from AniDBTVDBMap
    if count == len(dict_nodes):           break                                #   if deleted all exit loop
  for key in dict_nodes:  AniDBTVDBMap.append( dict_nodes[key] )                # add all new anidb mapping

### anidb to tvdb imdb tmdb mapping file - Loading AniDBTVDBMap from MAPPING url with MAPPING_FIX corrections ###
def GetAniDBTVDBMap():  
  MAPPING          = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list-master.xml'                 # ScudLee mapping file url
  MAPPING_FIX      = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/anime-list-corrections.xml' # ScudLee mapping file url online override
  AniDBTVDBMap     = common.LoadFile(filename=os.path.basename(MAPPING    ), relativeDirectory="AnimeLists", url=MAPPING,     cache= CACHE_1WEEK)  # AniDB title database loaded once every 2 weeks
  AniDBTVDBMap_fix = common.LoadFile(filename=os.path.basename(MAPPING_FIX), relativeDirectory="AnimeLists", url=MAPPING_FIX, cache= CACHE_1WEEK)  # AniDB title database loaded once every 2 weeks
  MergeMaps(AniDBTVDBMap, AniDBTVDBMap_fix)
  if not AniDBTVDBMap:  Log.Critical("Failed to load core file '{file}'".format(url=os.path.splitext(os.path.basename(MAPPING)))); AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>")  #; raise Exception("HAMA Fatal Error Hit")
  return AniDBTVDBMap
AniDBTVDBMap     = GetAniDBTVDBMap()

### Anidb Movie collection ###
def GetAniDBMovieSets():  
  ANIME_MOVIESET = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-movieset-list.xml'
  AniDBMovieSets = common.LoadFile(filename=os.path.basename(ANIME_MOVIESET), relativeDirectory="AnimeLists", url=ANIME_MOVIESET, cache= CACHE_1WEEK)
  if not AniDBMovieSets:  Log.Error ("Failed to load core file '%s'" % os.path.basename(MOVIE_COLLECTION));  AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>") 
  return AniDBMovieSets
  
### Get the tvdbId from the AnimeId or the other way around ###
def GetMetadata(media, movie, error_log, id, AniDBMovieSets):  #, AniDBTVDBMap
  MAPPING_FEEDBACK = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'  # ScudLee mapping file git feedback url
  MAPPING_CUSTOM = 'anime-list-custom.xml'  # ScudLee mapping file url local override
  mappingList, scudlee_mapping_tree               = {}, AniDBTVDBMap 
  mappingList['poster_id_array'], AnimeLists_dict = {}, {}
  tmdbid, imdbid, folder                          = "", "", ""
  
  Log.Info("".ljust(157, '-'))
  source, id = id.split('-', 1) if '-' in id else ("",id)
  AniDB_id = id if source.startswith('anidb') else ""
  TVDB_id  = id if source.startswith( 'tvdb') else ""
  Log.Info("AnimeLists.GetMetadata() - source: {}, id: {}, AniDB_id: {}, TVDB_id: {}".format(source, id, AniDB_id, TVDB_id))
      
  ### Load custom mapping file in serie folder or root
  if movie: folder = os.path.dirname(media.items[0].parts[0].file)
  else:
    for s in media.seasons:  #get first file path
      for e in media.seasons[s].episodes:  folder = os.path.dirname( media.seasons[s].episodes[e].items[0].parts[0].file); break
      break
  files = []
  while folder and not folder.endswith("/") and not folder.endswith("\\"):
    scudlee_filename_custom = os.path.join(folder, MAPPING_CUSTOM)
    files.append(scudlee_filename_custom)
    folder = os.path.dirname(folder)
  files.append(os.path.join(common.CachePath,               'anime-list-corrections.xml'))
  files.append(os.path.join(common.CachePath, 'AnimeLists', 'anime-list-corrections.xml'))
  for file in files:
    if os.path.exists(file):
      Log.Info("AnimeLists.GetMetadata() - Loading local custom mapping - url: " + file)
      try:                    MergeMaps(scudlee_mapping_tree, XML.ElementFromString( Core.storage.load(os.path.realpath(file))))
      except Exception as e:  Log.Info("AnimeLists.GetMetadata() - Failed open scudlee_filename_custom, error: '%s'" % e); scudlee_1 = "<anime-list></anime-list>"
      break
  else: Log.Info("AnimeLists.GetMetadata() - Local custom mapping - No file detected")
  
  ### Search for match
  for anime in scudlee_mapping_tree.iter('anime') if scudlee_mapping_tree else []:
    AniDBid = anime.get("anidbid", "")
    TVDBid  = anime.get('tvdbid',  "")
    if not (AniDB_id and AniDBid == AniDB_id) and not(TVDB_id and TVDB_id == TVDBid):  continue
    if TVDBid.isdigit():
      mappingList['defaulttvdbseason'] = anime.get('defaulttvdbseason', "")
      mappingList['episodeoffset'    ] = anime.get('episodeoffset',     "0")
      SaveDict( (anime.get('defaulttvdbseason'), GetXml(anime, 'studio')), mappingList, 'poster_id_array', TVDBid, AniDBid)
      Log.Info("[!] AniDBid: {}, TVDBid: {}, mappingList['defaulttvdbseason']: {}".format(AniDBid, TVDBid, mappingList['defaulttvdbseason']))
      if not AniDB_id:  AniDB_id = AniDBid
      mappingList['name'] = anime.xpath("name")[0].text
      imdbid              = anime.get('tmdbid', "")
      tmdbid              = anime.get('imdbid', "")
      try: ### mapping list ###
        for season in anime.iter('mapping') if anime else []:
          anidbseason = season.get('anidbseason')
          tvdbseason  = season.get('tvdbseason' )
          offset      = season.get("offset", "0")
          start       = season.get('start')
          end         = season.get('end')
          Log.Info("[!] anidbseason: {}, tvdbseason: {}, start: {}, end: {}, offset: {}, text: {}".format(anidbseason, tvdbseason, start, end, offset, season.text))
          for ep in range (int(start), int(end)+1)             if start else []:  mappingList[ 's'+anidbseason+'e'+ep               ] = (tvdbseason, str(ep+int(offset)))
          for ep in filter(None, season.text.split(';')) if season.text else []:  mappingList[ 's'+anidbseason+'e'+ep.split('-')[0] ] = (tvdbseason, ep.split('-')[1] if len(ep.split('-'))>1 else '')
      except Exception as e:  Log.Error("AnimeLists.GetMetadata() - mappingList creation exception, Exception: '%s'" % e)
    
      ### Update Metadata 
      if TVDBid=="hentai":                                         SaveDict("X",                                                                   AnimeLists_dict, 'content_rating')
      if anime.xpath("supplemental-info/studio"):                  SaveDict(GetXml(anime, 'studio'                    ),                           AnimeLists_dict, 'studio'        )
      if anime.xpath("supplemental-info/director"):                SaveDict(GetXml(anime, "supplemental-info/director"),                           AnimeLists_dict, 'director'      )
      if anime.xpath("supplemental-info/credits"):                 SaveDict(GetXml(anime, "supplemental-info/credits" ),                           AnimeLists_dict, 'writer'        )
      for genre in anime.xpath('supplemental-info/genre'):         SaveDict([genre.text],                                                          AnimeLists_dict, 'genres'        )
      for art   in anime.xpath('supplemental-info/fanart/thumb'):  SaveDict({art.text:("/".join(art.text.split('/')[3:]), 1, art.get('preview'))}, AnimeLists_dict, 'art'           )
      
      for element in AniDBMovieSets.iter("anime") if AniDBMovieSets else []:
        if element.get('AniDBid')==AniDB_id or TVDBid in mappingList['poster_id_array'] and element.get('AniDBid') in mappingList['poster_id_array'][TVDBid] :
          node        = element.getparent()
          title, main = GetAniDBTitle(node.xpath('titles')[0])
          if 'collection' in AnimeLists_dict:  AnimeLists_dict ['collection'].append(title)
          else:                                AnimeLists_dict ['collection'] = [title]
          Log.Info("AnimeLists.GetMetadata() - AniDBid '%s' is part of movie collection: '%s'" % (AniDBid, title))
          break
      else:  Log.Info("AnimeLists.GetMetadata() - AniDBid is not part of any collection") 
      break
    elif TVDBid in ("", "unknown"):
        error_log['anime-list TVDBid missing'].append("AniDBid: %s | Title: '%s' | Has no matching TVDBid ('%s') in mapping file | " % (AniDB_id, "title", TVDBid) + common.WEB_LINK % (MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; TVDBid:" % (AniDB_id, "title"), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
        Log.Warn("'anidbTvdbMapping() - anime-list TVDBid missing.htm' log added as tvdb serie id missing in mapping file: '%s'" % TVDBid)
  
  else:
    Log.Error("AnimeLists.GetMetadata() - source '{}', id: '{}' not found in file".format(source, id))
    error_log['anime-list AniDBid missing'].append("AniDBid: " + common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid))
    AniDBid, TVDBid = '', ''
  
  Log.Info("AnimeLists.GetMetadata() - anidb: '%s', tvbdid: '%s', tmdbid: '%s', imbdid: '%s', defaulttvdbseason: '%s', name: '%s'" % (AniDBid, TVDBid, tmdbid, imdbid, mappingList['defaulttvdbseason'] if 'defaulttvdbseason' in mappingList else 'N/A', mappingList['name'] if 'name' in mappingList else 'N/A') )
  Log.Info("mappingList: "+str(mappingList))
  return AnimeLists_dict, AniDB_id or AniDBid, TVDB_id or TVDBid, tmdbid, imdbid, mappingList

### Translate AniDB numbering into TVDB numbering ###
def tvdb_ep(mappingList, season, episode):
  debug = False
  key   = 's'+season+'e'+episode.split('-')[0]
  if key in mappingList:
    new_season, new_episode = mappingList [ key ]  
    if debug:  Log.Info("mappingList has key: '{}', new_tvdb_season: {:<2}, new_tvdb_episode: {:<3}".format(key, new_season, new_episode)) 
    return new_season, new_episode          # Season Individual episode mapping + start-end offset
  else:
    if debug:  Log.Info("mappingList hasn't got key: '{}'".format(key)) 
    defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
    episodeoffset     = Dict(mappingList, 'episodeoffset', default="0")
    if defaulttvdbseason: # and not season=='0':
      if debug:  Log.Info("mappingList has defaulttvdbseason: '{}', episodeoffset: '{}'".format(defaulttvdbseason, episodeoffset))
      return defaulttvdbseason, str(int(episode) + int(episodeoffset))
  if debug:  Log.Info("Found no key nor defaulttvdbseason.") 
  return season or '0', episode

### Translate TVDB numbering into AniDB numbering ###
def anidb_ep(mappingList, season, episode):
  debug = False
  defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
  episodeoffset     = Dict(mappingList, 'episodeoffset', default="0")
  for key in mappingList:
    if mappingList[key]==(season, episode.split('-')[0]):  
      if debug:  Log.Info("anidb_ep 1 - defaulttvdbseason: '{}', episodeoffset: '{}', season: '{}', mappingList: '{}'".format(defaulttvdbseason, episodeoffset, season, mappingList))
      return tuple(key.lstrip('s').split('e'))
  if defaulttvdbseason == season and not season=='0':
    if debug:  Log.Info("anidb_ep 2 - defaulttvdbseason: '{}', episodeoffset: '{}', season: '{}', mappingList: '{}'".format(defaulttvdbseason, episodeoffset, season, mappingList))
    return season, str(int(episode) - int(episodeoffset))
  if debug:  Log.Info("anidb_ep 3 default - defaulttvdbseason: '{}', episodeoffset: '{}', season: '{}', mappingList: '{}'".format(defaulttvdbseason, episodeoffset, season, mappingList))
  return season or '0', episode
  