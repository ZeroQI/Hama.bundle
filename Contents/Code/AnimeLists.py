### github.com/ScudLee/anime-lists ###

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import os          # os.path(.basename, .splitext, .foldername, .dirname, .exists, .join, .realpath)
import common      # CachePath, common.WEB_LINK , common.LoadFile
from   common import GetXml, SaveDict, Dict

### Functions ###

### Merge Source ScudLee anidb to tvdb mapping list witl Online and local fix ones ###
def MergeMaps(AniDBTVDBMap, AniDBTVDBMap_fix):
  dict_nodes, count = {}, 0  #Log.Info('type1: {}, type2: {}'.format(type(AniDBTVDBMap).__name__ , type(AniDBTVDBMap_fix).__name__))
  if type(AniDBTVDBMap_fix).__name__ == '_Element':
    for node in AniDBTVDBMap_fix or []:  dict_nodes[node.get('anidbid')] = node           # save mod list and nodes
    Log.Info("MergeMaps() - AniDBids concerned: " + str(dict_nodes.keys()))                #
  for node in AniDBTVDBMap or []:                                                        # LOOP IN EVERY ANIME IN MAPPING FILE
    if node and node.get('anidbid') in dict_nodes:  AniDBTVDBMap.remove(node); count+=1  #   if a correction exists: remove old mapping from AniDBTVDBMap
    if count == len(dict_nodes):                    break                                #   if deleted all exit loop
  for key in dict_nodes or {}:  AniDBTVDBMap.append( dict_nodes[key] )                   # add all new anidb mapping
  
### anidb to tvdb imdb tmdb mapping file - Loading AniDBTVDBMap from MAPPING url with MAPPING_FIX corrections ###
def GetAniDBTVDBMap():  
  MAPPING       = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list-master.xml'                                  # ScudLee mapping file url
  MAPPING_FIX   = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/anime-list-corrections.xml'                  # ScudLee mapping file url online override
  MAPPING_LOCAL = os.path.join(common.CachePath, 'AnimeLists', 'anime-list-custom.xml')                                            # Custom mapping list(PlexRoot, "Plug-in Support", "Data", "com.plexapp.agents.hama", "DataItems", 'AnimeLists', 'anime-list-corrections.xml')
  AniDBTVDBMap  = common.LoadFile(filename=os.path.basename(MAPPING), relativeDirectory="AnimeLists", url=MAPPING, cache= CACHE_1DAY*6)  # 
  if not AniDBTVDBMap:  Log.Critical("GetAniDBTVDBMap() - Failed to load core file '{file}'".format(url=os.path.splitext(os.path.basename(MAPPING)))); AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>")  #; raise Exception("HAMA Fatal Error Hit")
  
  MergeMaps(AniDBTVDBMap, common.LoadFile(filename=os.path.basename(MAPPING_FIX), relativeDirectory="AnimeLists", url=MAPPING_FIX, cache= CACHE_1DAY*6))  #Online ScudLee anidb to tvdb mapping list
    
  if os.path.exists(MAPPING_LOCAL):  #Local  ScudLee anidb to tvdb mapping list
    Log.Info("GetAniDBTVDBMap() - Loading local custom mapping - url: " + MAPPING_LOCAL)
    try:                    MergeMaps(AniDBTVDBMap, XML.ElementFromString( Core.storage.load(MAPPING_LOCAL)))
    except Exception as e:  Log.Info("GetAniDBTVDBMap() - Failed open scudlee_filename_custom, error: '%s'" % e)
  else:                     Log.Info("GetAniDBTVDBMap() - Local custom mapping file not present: {}".format(MAPPING_LOCAL))
  return AniDBTVDBMap
  
### Anidb Movie collection ###
def GetAniDBMovieSets():  
  ANIME_MOVIESET = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-movieset-list.xml'
  AniDBMovieSets = common.LoadFile(filename=os.path.basename(ANIME_MOVIESET), relativeDirectory="AnimeLists", url=ANIME_MOVIESET, cache= CACHE_1WEEK*4)
  if not AniDBMovieSets:  Log.Error ("Failed to load core file '%s'" % os.path.basename(MOVIE_COLLECTION))  #;  AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>") 
  return AniDBMovieSets
  
### Get the tvdbId from the AnimeId or the other way around ###
def GetMetadata(media, movie, error_log, id, AniDBMovieSets):
  MAPPING_FEEDBACK               = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'  # ScudLee mapping file git feedback url
  mappingList, AnimeLists_dict   = {}, {}  #mappingList['poster_id_array'] = {}
  tmdbid, imdbid, found          = '', '', False
  source, id                     = id.split('-', 1) if '-' in id else ("",id)
  AniDB_id                       = id if source.startswith('anidb') else ""
  TVDB_id                        = id if source.startswith( 'tvdb') else ""
  
  ### Search for match ###
  Log.Info("".ljust(157, '-'))
  for anime in AniDBTVDBMap.iter('anime') if AniDBTVDBMap else []:
    AniDBid = anime.get("anidbid", "")
    TVDBid  = anime.get('tvdbid',  "")
    if (not AniDBid or AniDBid != AniDB_id) and (not TVDBid or TVDBid !=TVDB_id):  continue  #if not (AniDB_id and AniDBid == AniDB_id) and not(TVDB_id and TVDB_id == TVDBid):  continue
    found = True
    Log.Info("AnimeLists.GetMetadata() - AniDBid: {}, TVDBid: {}, defaulttvdbseason: {}, episodeoffset: {}, name: {}".format(AniDBid, TVDBid, anime.get('defaulttvdbseason'), anime.get('episodeoffset') or '0', GetXml(anime, 'name')))
    
    if AniDBid and TVDBid.isdigit()and anime.get('defaulttvdbseason')=='1' and anime.get('episodeoffset') in ('', None, '0'):
      if not TVDB_id:   TVDB_id  = TVDBid
      if not AniDB_id:  AniDB_id = AniDBid
    
    ### Anidb numbered serie ###
    if AniDB_id: # or defaulttvdbseason=='1':
      
      SaveDict(anime.get('tmdbid',        ""),              mappingList, 'tmdbid'           )
      SaveDict(anime.get('imdbid',        ""),              mappingList, 'imdbid'           )
      SaveDict(anime.get('defaulttvdbseason'),              mappingList, 'defaulttvdbseason')
      SaveDict(anime.get('episodeoffset'    ) or '0',       mappingList, 'episodeoffset'    )
      SaveDict(GetXml(anime, 'name'         ),              mappingList, 'name'             )
      SaveDict(GetXml(anime, 'studio'                    ), AnimeLists_dict, 'studio'        )
      SaveDict(GetXml(anime, "supplemental-info/director"), AnimeLists_dict, 'director'      )
      SaveDict(GetXml(anime, "supplemental-info/credits" ), AnimeLists_dict, 'writer'        )
      for genre in anime.xpath('supplemental-info/genre'):         SaveDict([genre.text],                                                          AnimeLists_dict, 'genres')
      for art   in anime.xpath('supplemental-info/fanart/thumb'):  SaveDict({art.text:('/'.join(art.text.split('/')[3:]), 1, art.get('preview'))}, AnimeLists_dict, 'art'   )
      
      if movie or max(map(int, media.seasons.keys()))<=1:  break  #AniDB guid need 1 AniDB xml only, not an TheTVDB numbered serie with anidb guid (not anidb2 since seen as TheTVDB)
      
    ### TheTVDB numbered series ###
    if TVDB_id or not movie and max(map(int, media.seasons.keys()))>1:  #In case AniDB guid but multiple seasons
      if TVDBid.isdigit():
        if anime.get('defaulttvdbseason'):  SaveDict(anime.get('episodeoffset') or '0', mappingList, 'TVDB', 's'+anime.get('defaulttvdbseason'), AniDBid)  #mappingList['TVDB'][s1][anidbid]=episodeoffset
        for season in anime.iter('mapping'):  ### mapping list: <mapping-list> <mapping anidbseason="0" tvdbseason="0">;1-12;2-14;3-16;4-18;</mapping> </mapping-list> 
          anidbseason, tvdbseason, offset, start, end = season.get('anidbseason'), season.get('tvdbseason'), season.get('offset') or '0', season.get('start'), season.get('end')
          Log.Info("AnimeLists.GetMetadata() - [!] anidbseason: {}, tvdbseason: {}, start: {}, end: {}, offset: {}, text: {}".format(anidbseason, tvdbseason, start, end, offset, season.text))
          for ep in range(int(start), int(end)+1)        if start       else []:  SaveDict((anidbseason, ep,               AniDBid), mappingList, 'TVDB', 's'+tvdbseason+'e'+str(ep+int(offset)) ) #mappingList['TVDB'][s1e1]=(AniDB_season, AniDB_episode, AniDBid) for start-end mappings
          for ep in filter(None, season.text.split(';')) if season.text else []:  SaveDict((anidbseason, ep.split('-')[0], AniDBid), mappingList, 'TVDB', 's'+tvdbseason+'e'+ep.split('-')[1])     #mappingList['TVDB'][s1e1]=(AniDB_season, AniDB_episode, AniDBid) for manual mapping like '1-12'
      
      elif TVDBid=="hentai":  SaveDict("X", AnimeLists_dict, 'content_rating')
      elif TVDBid in ("", "unknown", None):
        error_log['anime-list TVDBid missing'].append("AniDBid: %s | Title: '%s' | Has no matching TVDBid ('%s') in mapping file | " % (AniDB_id, "title", TVDBid) + common.WEB_LINK % (MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; TVDBid:" % (AniDB_id, "title"), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
        Log.Warn("anidbTvdbMapping() - 'anime-list TVDBid missing.htm' log added as tvdb serie id missing in mapping file: '%s'" % TVDBid)
  else:
    if not found:
      Log.Error("AnimeLists.GetMetadata() - source '{}', id: '{}' not found in file".format(source, id))
      error_log['anime-list AniDBid missing'].append("AniDBid: " + common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid))
    AniDBid, TVDBid = '', ''
    
  ### Update collection 
  #for element in AniDBMovieSets.iter("anime") if AniDBMovieSets else []:
  #  if element.get('AniDBid')==AniDB_id or TVDBid in mappingList['TVDB'] and element.get('AniDBid') in mappingList['TVDB']:
  #    node        = element.getparent()
  #    title, main = GetAniDBTitle(node.xpath('titles')[0])
  #    SaveDict(title, AnimeLists_dict, 'collection')
  #    Log.Info("AnimeLists.GetMetadata() - AniDBid '%s' is part of movie collection: '%s'" % (AniDBid, title))
  #    break
  #else
  TVDB_collection, title=[], ''
  for anime in AniDBTVDBMap.iter('anime') if AniDBTVDBMap else []:
    if anime.get('tvdbid',  "") == TVDB_id:
      TVDB_collection.append(anime.get("anidbid", ""))
      if anime.get('defaulttvdbseason')=='1' and anime.get('episodeoffset')=='':  title = GetXml(anime, 'name')
  if len(TVDB_collection)>1 and title:  SaveDict(title + ' Collection', AnimeLists_dict, 'collection')
  
  Log.Info("anidbTvdbMapping() - mappingList: {}".format(mappingList))
  return AnimeLists_dict, AniDB_id or AniDBid, (TVDB_id or TVDBid) if (TVDB_id or TVDBid).isdigit() else "", tmdbid, imdbid, mappingList

### Translate AniDB numbering into TVDB numbering ###
def tvdb_ep(mappingList, season, episode, source=''):
  if source.startswith('tvdb4') and season!='0':  season='1'
  
  defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
  episodeoffset     = Dict(mappingList, 'episodeoffset', default="0")
  key               = 's'+season+'e'+episode.split('-')[0]
  #if season=='0' and episode=='1':  Log.Info('defaulttvdbseason: {}, episodeoffset: {},  Dict(mappingList, key): {}, []: {}'.format(defaulttvdbseason, episodeoffset, Dict(mappingList, key), str([x for x in Dict(mappingList, 'TVDB')])))
  if key in mappingList:                                                                                                                                        mapping = mappingList [ key ] # Season Individual episode mapping + start-end offset
  elif defaulttvdbseason not in (None, '0') and (not Dict(mappingList, 'TVDB') or not [x for x in Dict(mappingList, 'TVDB') if x.startswith('s'+season+'e')]):  mapping = (defaulttvdbseason, str(int(episode) + int(episodeoffset)))
  else:                                                                                                                                                         mapping = ('0', '0')#(season or '0', episode)
  return mapping
#AnimeLists.GetMetadata() - AniDBid: 11680, TVDBid: 257516, defaulttvdbseason: 0, episodeoffset: 10, name: Accel World: Infinite Burst
#anidbTvdbMapping() - mappingList: {'defaulttvdbseason': '0', 'name': 'Accel World: Infinite Burst', 'episodeoffset': '10'}

### Translate TVDB numbering into AniDB numbering ###
def anidb_ep(mappingList, season, episode):
  ep_mapping = Dict(mappingList, 'TVDB', 's'+season+'e'+episode.split('-')[0])
  if ep_mapping:  return ep_mapping[0], ep_mapping[1], ep_mapping[2]            #Lvl 3 & 2 direct ep mapping (ep or season with start-end range)
  anidbid_list = Dict(mappingList, 'TVDB', 's'+season)                          #anidbid_list: '{'10747': '0', '12291': '8'}'
  for offset, anidbid in sorted(zip(anidbid_list.values(), anidbid_list.keys()), key=lambda x: common.natural_sort_key(x[0]), reverse=True) if anidbid_list else[]:  #reverse value&index and sort per offset
    if int(episode.split('-')[0])> int(offset):  Log.Info('defaulttvdbseason');  return '1', str(int(episode.split('-')[0])-int(offset)), anidbid   #Lvl 1 - defaulttvdbseason + offset
  defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
  episodeoffset     = Dict(mappingList, 'episodeoffset', default="0")
  if defaulttvdbseason and season==defaulttvdbseason:  return '1', str(int(episode)-int(episodeoffset)), ''
  else:                                                return '0', '0', ''

### Variables ###
AniDBTVDBMap = GetAniDBTVDBMap()
