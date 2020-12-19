### github.com/Anime-Lists/anime-lists ###

### Imports ###
# Python Modules #
import os
import copy
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict, GetXml # Direct import of heavily used functions
import AniDB

### Variables ###
SCHUDLEE_MASTER          = 'https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-list-master.xml'                                  # ScudLee mapping file url
ASS_SCHUDLEE_CORRECTIONS = 'https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/anime-list-corrections.xml'                  # ScudLee mapping file url online override
AniDBTVDBMap             = None

SCHUDLEE_MOVIESET = 'https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-movieset-list.xml'
AniDBMovieSets    = None

SCHUDLEE_CUSTOM   = 'anime-list-custom.xml'
SCHUDLEE_FEEDBACK = 'https://github.com/Anime-Lists/anime-lists/issues/new?title={title}&body={body}'  # ScudLee mapping file git feedback url

### Functions ###

### Merge Source ScudLee anidb to tvdb mapping list witl Online and local fix ones ###
def MergeMaps(AniDBTVDBMap, AniDBTVDBMap_fix):
  AniDBTVDBMap_new = copy.deepcopy(AniDBTVDBMap)
  dict_nodes, count = {}, 0  #Log.Info('type1: {}, type2: {}'.format(type(AniDBTVDBMap).__name__ , type(AniDBTVDBMap_fix).__name__))
  if type(AniDBTVDBMap_fix).__name__ == '_Element':
    for node in AniDBTVDBMap_fix or []:  dict_nodes[node.get('anidbid')] = node          # save mod list and nodes
    Log.Info("MergeMaps() - AniDBids concerned: " + str(dict_nodes.keys()))              #
  for node in AniDBTVDBMap_new or []:                                                        # LOOP IN EVERY ANIME IN SCHUDLEE_MASTER FILE
    if node and node.get('anidbid') in dict_nodes:  AniDBTVDBMap_new.remove(node); count+=1  #   if a correction exists: remove old mapping from AniDBTVDBMap
    if count == len(dict_nodes):                    break                                #   if deleted all exit loop
  for key in dict_nodes or {}:  AniDBTVDBMap_new.append( dict_nodes[key] )                   # add all new anidb mapping
  return AniDBTVDBMap_new
  
### anidb to tvdb imdb tmdb mapping file - Loading AniDBTVDBMap from SCHUDLEE_MASTER url with ASS_SCHUDLEE_CORRECTIONS corrections ###
def GetAniDBTVDBMap():  
  global AniDBTVDBMap
  AniDBTVDBMap  = common.LoadFile(filename=os.path.basename(SCHUDLEE_MASTER), relativeDirectory="AnimeLists", url=SCHUDLEE_MASTER)  # 
  if not AniDBTVDBMap:  raise Exception("GetAniDBTVDBMap() - Failed to load core file '{file}'".format(url=os.path.splitext(os.path.basename(SCHUDLEE_MASTER))))  #; AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>")  #; raise Exception("HAMA Fatal Error Hit")
  else: Log.Info("Entries loaded: {}, File: {}".format(len(AniDBTVDBMap), SCHUDLEE_MASTER))
  AniDBTVDBMap  = MergeMaps(AniDBTVDBMap, common.LoadFile(filename=os.path.basename(ASS_SCHUDLEE_CORRECTIONS), relativeDirectory="AnimeLists", url=ASS_SCHUDLEE_CORRECTIONS))  #Online ScudLee anidb to tvdb mapping list
  
def GetAniDBTVDBMapCustom(media, movie):  
  AniDBTVDBMapCustom = None
  lib, root, path = common.GetLibraryRootPath(common.GetMediaDir(media, movie))
  dir = os.path.join(root, path)
  while dir:
    scudlee_filename_custom = os.path.join(dir, SCHUDLEE_CUSTOM)
    if os.path.exists( scudlee_filename_custom ):
      try:
        AniDBTVDBMapCustom = XML.ElementFromString(Core.storage.load(scudlee_filename_custom))
        Log.Info("Local custom mapping file loaded: {}".format(scudlee_filename_custom))
      except:  Log.Error("Failed to open: '%s', error: '%s'" % (scudlee_filename_custom, e))
      else:    break
    dir = os.path.dirname(dir) if len(dir) > len(root) else ''  # Clear variable if we've just finished processing down to (and including) root
  else:  Log.Info("Local custom mapping file not present: {}".format(SCHUDLEE_CUSTOM))
  return AniDBTVDBMapCustom
  
### Anidb Movie collection ###
def GetAniDBMovieSets():  
  global AniDBMovieSets
  AniDBMovieSets = common.LoadFile(filename=os.path.basename(SCHUDLEE_MOVIESET), relativeDirectory="AnimeLists", url=SCHUDLEE_MOVIESET, cache=CACHE_1MONTH)
  if not AniDBMovieSets:  raise Exception("GetAniDBMovieSets() - Failed to load core file '%s'" % os.path.basename(SCHUDLEE_MOVIESET))  #;  AniDB_Movie_Set = XML.ElementFromString("<anime-set-list></anime-set-list>") 
  else: Log.Info("Entries loaded: {}, File: {}".format(len(AniDBMovieSets), SCHUDLEE_MOVIESET))
  
### Get the tvdbId from the AnimeId or the other way around ###
def GetMetadata(media, movie, error_log, id):
  Log.Info("=== AnimeLists.GetMetadata() ===".ljust(157, '='))
  mappingList, AnimeLists_dict   = {}, {}
  found                          = False
  source, id                     = id.split('-', 1) if '-' in id else ("",id)
  AniDB_id                       = id if source.startswith('anidb') else ""
  TVDB_id                        = id if source.startswith( 'tvdb') else ""
  TMDB_id                        = id if source.startswith('tmdb') else ""
  IMDB_id                        = id if source.startswith('imdb') else ""
  AniDBid                        = ""
  TVDBid                         = ""
  TMDBid                         = ""
  IMDBid                         = ""
  tvdb_numbering                 = True if not movie and (TVDB_id or AniDB_id and max(map(int, media.seasons.keys()))>1) else False
  tvdbcounts                     = {}

  ### Search for match ###
  Log.Info("tvdb_numbering: {}".format(tvdb_numbering))
  AniDB_id2, TVDB_id2 = "",""

  AniDBTVDBMapCustom = GetAniDBTVDBMapCustom(media, movie)
  if AniDBTVDBMapCustom:  AniDBTVDBMapFull = MergeMaps(AniDBTVDBMap, AniDBTVDBMapCustom)
  else:                   AniDBTVDBMapFull = AniDBTVDBMap

  def anime_core(anime):
    defaulttvdbseason = anime.get('defaulttvdbseason') if anime.get('defaulttvdbseason') and anime.get('defaulttvdbseason') != 'a' else '1'
    episodeoffset     = anime.get('episodeoffset')     if anime.get('episodeoffset')                                               else '0'
    s1_mapping_count  = len(anime.xpath("mapping-list/mapping[@anidbseason='1'][@tvdbseason='0' or @tvdbseason='1']"))
    s1e1_mapping      = True if anime.xpath("mapping-list/mapping[@anidbseason='1'][@tvdbseason='1'][contains(text(), '-1;')]") else False
    is_primary_series = True if defaulttvdbseason == '1' and episodeoffset == '0' and (s1_mapping_count == 0 or s1e1_mapping)   else False
    return defaulttvdbseason, episodeoffset, s1_mapping_count, is_primary_series

  Log.Info("--- AniDBTVDBMap ---".ljust(157, '-'))
  forcedID={'anidbid':AniDB_id,'tvdbid':TVDB_id,'tmdbid':TMDB_id,'imdbid':IMDB_id}
  for anime in AniDBTVDBMapFull.iter('anime') if AniDBTVDBMapFull else []:
    # gather any manually specified source ids
    foundID,wantedID = {},{}
    for check in forcedID.keys():
      foundID[check]=anime.get(check,"")
      wantedID[check]=True if foundID[check] == forcedID[check] and forcedID[check] != '' else False

    # if this row matches our specified source-id
    if True in wantedID.values():
      # save the found values for later use in other GetMetadata that dont depend on AniDB etc.
      IMDBid,TMDBid,TVDBid,AniDBid = foundID['imdbid'], foundID['tmdbid'],foundID['tvdbid'],foundID['anidbid']
      # use the old check to decide whether to proceed
      if TVDBid == '' and AniDBid == '': continue
    # nothing found, skip
    else: continue
    found = True

    # record the number of entries using the same tvdb id
    SaveDict(Dict(tvdbcounts, TVDBid, default=0)+1, tvdbcounts, TVDBid)

    defaulttvdbseason, episodeoffset, s1_mapping_count, is_primary_series = anime_core(anime)

    if not tvdb_numbering and not TVDB_id:                                                      TVDB_id2  = TVDBid
    if tvdb_numbering and AniDBid and TVDBid.isdigit() and is_primary_series and not AniDB_id:  AniDB_id2 = AniDBid
    Log.Info("[+] AniDBid: {:>5}, TVDBid: {:>6}, defaulttvdbseason: {:>4}, offset: {:>3}, TMDBid: {:>7}, IMDBid: {:>10}, name: {}".format(AniDBid, TVDBid, 
      ("({})".format(anime.get('defaulttvdbseason')) if anime.get('defaulttvdbseason')!=defaulttvdbseason else '')+defaulttvdbseason, episodeoffset, 
      TMDBid, IMDBid, GetXml(anime, 'name')))
    
    ### AniDB/TMDB/IMDB numbered series ###
    if AniDB_id or TMDB_id or IMDB_id:
      AniDB_id2 = AniDBid  # Needs to be set if TMDB/IMDB
      TVDB_id2  = TVDBid
      SaveDict(TMDBid,                                                 mappingList, 'tmdbid'             )
      SaveDict(IMDBid,                                                 mappingList, 'imdbid'             )
      SaveDict(defaulttvdbseason,                                      mappingList, 'defaulttvdbseason'  )
      SaveDict(True if anime.get('defaulttvdbseason')=='a' else False, mappingList, 'defaulttvdbseason_a')
      SaveDict(episodeoffset,                                          mappingList, 'episodeoffset'      )
      SaveDict(GetXml(anime, 'name'         ),                         mappingList, 'name'               )
      SaveDict(GetXml(anime, "supplemental-info/studio"  ),            AnimeLists_dict, 'studio'         )
      SaveDict(GetXml(anime, "supplemental-info/director"),            AnimeLists_dict, 'director'       )
      SaveDict(GetXml(anime, "supplemental-info/credits" ),            AnimeLists_dict, 'writer'         )
      for genre in anime.xpath('supplemental-info/genre'):         SaveDict([genre.text],                                                          AnimeLists_dict, 'genres')
      for art   in anime.xpath('supplemental-info/fanart/thumb'):  SaveDict({art.text:('/'.join(art.text.split('/')[3:]), 1, art.get('preview'))}, AnimeLists_dict, 'art'   )
      
    ### TheTVDB/multi-season numbered series and the Primary/Starting(s1e1) AniDB id ###
    if (TVDB_id or not movie and max(map(int, media.seasons.keys()))>1 and AniDB_id=='') and TVDBid.isdigit() and is_primary_series:
      AniDB_id2 = AniDBid
      SaveDict(TMDBid,                                                 mappingList, 'tmdbid'             )
      SaveDict(IMDBid,                                                 mappingList, 'imdbid'             )
      SaveDict(defaulttvdbseason,                                      mappingList, 'defaulttvdbseason'  )
      SaveDict(True if anime.get('defaulttvdbseason')=='a' else False, mappingList, 'defaulttvdbseason_a')

    ###
    if TVDBid.isdigit():
      SaveDict(episodeoffset, mappingList, 'TVDB', 's-1' if defaulttvdbseason == '0' and s1_mapping_count >= 1 else 's'+defaulttvdbseason, AniDBid)  #mappingList['TVDB'][s1][anidbid]=episodeoffset
      SaveDict({'min': defaulttvdbseason, 'max': defaulttvdbseason}, mappingList, 'season_map', AniDBid)  # Set the min/max season to the 'defaulttvdbseason'
      if source=="tvdb6" and int(episodeoffset)>0:  SaveDict({'min': '0', 'max': '0'}, mappingList, 'season_map', AniDBid)  # Force series as special if not starting the TVDB season

      for season in anime.iter('mapping'):  ### mapping list: <mapping-list> <mapping anidbseason="0" tvdbseason="0">;1-12;2-14;3-16;4-18;</mapping> </mapping-list> 
        anidbseason, tvdbseason, offset, start, end = season.get('anidbseason'), season.get('tvdbseason'), season.get('offset') or '0', season.get('start'), season.get('end')
        Log.Info("    - season: [{:>2}],           [{:>2}], range:       [{:>3}-{:>3}], offset: {:>3}, text: {}".format(anidbseason, tvdbseason, start or '000', end or '000', offset, (season.text or '').strip(';')))
        for ep in range(int(start), int(end)+1)        if start       else []:
          #Log.Info("[?] start: {}, end: {}, ep: {}".format(start, end, ep))
          if not Dict(mappingList, 'TVDB', 's'+tvdbseason+'e'+str(ep+int(offset))):
            SaveDict((anidbseason, str(ep),          AniDBid), mappingList, 'TVDB', 's'+tvdbseason+'e'+str(ep+int(offset)) ) #mappingList['TVDB'][s1e1]=(AniDB_season, AniDB_episode, AniDBid) for start-end mappings
          #else: Log.Info("already present")
        for ep in filter(None, season.text.split(';')) if season.text else []:
          if not '-' in ep:
            Log.Info('[!] MAPPING ERROR, season.text: "{}", ep mapping missing hyphen: "{}"'.format(season.text, ep))
          elif not Dict(mappingList, 'TVDB', 's'+tvdbseason+'e'+ep.split('-')[1]):
            SaveDict((anidbseason, ep.split('-')[0], AniDBid), mappingList, 'TVDB', 's'+tvdbseason+'e'+ep.split('-')[1])     #mappingList['TVDB'][s1e1]=(AniDB_season, AniDB_episode, AniDBid) for manual mapping like '1-12'
          #elif '-' not in (mappingList, 'TVDB', 's'+tvdbseason+'e'+ep.split('-')[1]):
          #  SaveDict((anidbseason, Dict(mappingList, 'TVDB', 's'+tvdbseason+'e'+ep.split('-')[1])[1]+'-'+ep.split('-')[0], AniDBid), mappingList, 'TVDB', 's'+tvdbseason+'e'+ep.split('-')[1])
          #  Log.Info("already present so converting to range but range not supported")
        if int(Dict(mappingList, 'season_map', AniDBid, 'max')) < int(season.get("tvdbseason")):
          SaveDict(season.get("tvdbseason"), mappingList, 'season_map', AniDBid, 'max')  # Update the max season to the largest 'tvdbseason' season seen in 'mapping-list'
    
    ### 
    if TVDBid=="hentai":  SaveDict("X", AnimeLists_dict, 'content_rating')
    elif TVDBid in ("", "unknown", None):
      link = SCHUDLEE_FEEDBACK.format(title="aid:%s &#39;%s&#39; TVDBid:" % (AniDB_id, "title"), body=String.StripTags(XML.StringFromElement(anime, encoding='utf8')))
      error_log['anime-list TVDBid missing'].append('AniDBid: "{}" | Title: "{}" | Has no matching TVDBid "{}" in mapping file | <a href="{}" target="_blank">Submit bug report</a>'.format(AniDB_id, "title", TVDBid, link))
      Log.Info('"anime-list TVDBid missing.htm" log added as tvdb serie id missing in mapping file: "{}"'.format(TVDBid))
        
    # guid need 1 entry only, not an TheTVDB numbered serie with anidb guid
    if (AniDB_id or TMDB_id or IMDB_id) and (movie or max(map(int, media.seasons.keys()))<=1):  break
      
  else:
    # Loop has gone through all entries. This only happens when the exact entry is not found or a TVDB entry that needs to loop through all.
    if not found:
      Log.Info("ERROR: Could not find %s: %s" % (source, id) )
      if AniDB_id != "": error_log['anime-list AniDBid missing'].append("AniDBid: " + common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDB_id, AniDB_id))
      # Reset the variables used for matching so it does not just keep the value of the last entry in the loop
      IMDBid,TMDBid,TVDBid,AniDBid = '','','',''
  
  AniDB_winner = AniDB_id or AniDB_id2
  TVDB_winner  = TVDB_id  or TVDB_id2
  
  Log.Info('             -----          ------')
  Log.Info('             {:>5}          {:>6}'.format(AniDB_winner, TVDB_winner))
  
  SaveDict(Dict(tvdbcounts, TVDB_winner), mappingList, 'tvdbcount')

  if source=="tvdb":
    for s in media.seasons:
      for e in media.seasons[s].episodes:
        if int(e) > 100:  SaveDict(True, mappingList, 'possible_anidb3'); break
    else:  SaveDict(False, mappingList, 'possible_anidb3')
  else:  SaveDict(False, mappingList, 'possible_anidb3')

  for values in Dict(mappingList, 'TVDB', default={}).values():
    if isinstance(values, tuple) and values[0]=='1' and values[1]=='1':  SaveDict(True, mappingList, 's1e1_mapped'); break
  else:  SaveDict(False, mappingList, 's1e1_mapped')

  ### Update collection/studio
  TVDB_collection, title, studio = [], '', ''
  for anime in AniDBTVDBMapFull.iter('anime') if AniDBTVDBMapFull and TVDB_winner.isdigit() else []:
    if anime.get('tvdbid',  "") == TVDB_winner:
      TVDB_collection.append(anime.get("anidbid", ""))
      if anime_core(anime)[3]:  #[3]==is_primary_series
        title = AniDB.GetAniDBTitle(AniDB.AniDBTitlesDB.xpath('/animetitles/anime[@aid="{}"]/title'.format(anime.get("anidbid", ""))))[0]  #returns [title, main, language_rank]
        studio = GetXml(anime, "supplemental-info/studio")
  if len(TVDB_collection)>1 and title:  # Require that there be at least 2 anidb mappings for a collection
    Log.Info("[ ] collection: TVDBid '%s' is part of collection: '%s', related_anime_list: %s" % (TVDB_winner, SaveDict([title + ' Collection'], AnimeLists_dict, 'collections'), TVDB_collection))
  else:  Log.Info("[ ] collection: TVDBid '%s' is not part of any collection" % TVDB_winner)
  Log.Info("[ ] studio: {}".format(SaveDict(studio, AnimeLists_dict, 'studio')))
  
  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("AniDB_id: '{}', AniDB_id2: '{}', AniDBid: '{}', TVDB_id: '{}', TVDB_id2: '{}', TVDBid: '{}'".format(AniDB_id, AniDB_id2, AniDBid, TVDB_id, TVDB_id2, TVDBid))
  Log.Info("mappingList: {}".format(DictString(mappingList, 1)))
  Log.Info("AnimeLists_dict: {}".format(DictString(AnimeLists_dict, 1)))
  return AnimeLists_dict, AniDB_winner, TVDB_winner if TVDB_winner.isdigit() else "", Dict(mappingList, 'tmdbid'), Dict(mappingList, 'imdbid'), mappingList

### Translate AniDB numbering into TVDB numbering ###
def tvdb_ep(mappingList, season, episode, anidbid=''):
  '''
  <anime anidbid="23" tvdbid="76885" defaulttvdbseason="1" episodeoffset="" tmdbid="" imdbid="">
    defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
    episodeoffset     = Dict(mappingList, 'episodeoffset', default="0")
                        Dict(mappingList, 's'+season+'e'+episode.split('-')[0]
    <name>Cowboy Bebop</name>
    <mapping-list>
      <mapping anidbseason="0" tvdbseason="0">;1-5;2-6;</mapping>
      <mapping anidbseason="1" tvdbseason="5" start="13" end="24" offset="-12"/>
      <mapping anidbseason="1" tvdbseason="6" start="25" end="36" offset="-24"/>
      <mapping anidbseason="1" tvdbseason="7" start="37" end="48" offset="-36"/>
    </mapping-list> 
    <before>;1-25;</before>
    <supplemental-info replace="true"> 
      <studio>Sunrise</studio>
      <genre>Comedy</genre>
      <genre>Music</genre>
      <actor /> /not used
      <director>Tetsuya Nomura</director>
      <credits>Kazuhito Yamamoto</credits> =writer
      <fanart>
        <thumb dim="1280x720" colors="" preview="http://www.thetvdb.com/banners/_cache/fanart/original/191221-1.jpg">http://www.thetvdb.com/banners/fanart/original/191221-1.jpg</thumb>
      </fanart>
    </supplemental-info>
</anime>
  '''
  mapping = ('0', '0')#(season or '0', episode)
  debug   = False
  if debug:  Log.Info('[?] (#1) season: {}, episode: {}, anidbid: {}'.format(season, episode, anidbid))
  
  defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
  episodeoffset     = Dict(mappingList, 'episodeoffset')
  for item in Dict(mappingList, 'TVDB') or {}:
    # mappingList: {'TVDB': {'s3': {'13485': '0'}, 's2': {'12233': '0'}, 's1': {'11739': '0'}, 's0': {'12344': '0'}}, 'defaulttvdbseason': '1'}
    if Dict(mappingList, 'TVDB', item, anidbid):
      episodeoffset     = Dict(mappingList, 'TVDB', item, anidbid)
      defaulttvdbseason = item[1:]
      break
  else:  Log.Info('[!] anidbid {} not found in mappingList: {}'.format(anidbid, mappingList))  
    
  # <mapping anidbseason="x" tvdbseason="x" start="13" end="24" offset="-12"> ;1-5;2-6; </mapping>
  value    = (season, episode, anidbid)
  tvdbList = Dict(mappingList, 'TVDB', default={})
  if value in tvdbList.values():
    mapping = list(tvdbList.keys())[list(tvdbList.values()).index(value)][1:].split('e')
    if debug:  Log.Info('[?] (#2) value "{}" in mappingList "{}"'.format(value, mappingList)) 
  
  # if not mapped with mapping, specials are not mapped with tvdb
  elif season=='0':
    mapping = ('0', '0')
    if debug:  Log.Info('[?] (#3) value "{}" not in mappingList "{}" and season 0'.format(value, mappingList)) 
  
  # <anime anidbid="xxxxx" tvdbid="xxxxx" defaulttvdbseason="x" episodeoffset="x">
  elif season=='1':
    if debug:  Log.Info('[?] (#4) value "{}" not in mappingList "{}" and season 1, defaulttvdbseason: {}, episodeoffset: {}'.format(value, mappingList, defaulttvdbseason, episodeoffset))
    mapping = (defaulttvdbseason, str(int(episode) + int(episodeoffset)))
  else:
    Log.Info('[!] error {}'.format(value))
    
  return mapping

### Translate TVDB numbering into AniDB numbering ###
def anidb_ep(mappingList, season, episode):
  debug = False
  if debug:  Log.Info('[?] (#1) season: {}, episode: {}'.format(season, episode))

  # <mapping-list> <mapping anidbseason="0" tvdbseason="0">;1-5;2-6;</mapping>
  # <mapping-list> <mapping anidbseason="1" tvdbseason="5" start="13" end="24" offset="-12"/>
  ep_mapping = Dict(mappingList, 'TVDB', 's'+season+'e'+episode.split('-')[0])
  if ep_mapping:
    if debug:  Log.Info('[?] (#2) Exact mapping: {}'.format(ep_mapping))
    return ep_mapping[0], ep_mapping[1], ep_mapping[2]            #Lvl 3 & 2 direct ep mapping (ep or season with start-end range)
  
  # <mapping-list> <mapping anidbseason="1" tvdbseason="5" offset="-12"/>
  anidbid_list = Dict(mappingList, 'TVDB', 's'+season, default={})
  if debug:  Log.Info('[?] (#3) s{}: {}'.format(season, anidbid_list))
  for offset, anidbid in sorted(zip(anidbid_list.values(), anidbid_list.keys()), key=lambda x: common.natural_sort_key(x[0]), reverse=True):  #reverse value&index and sort per offset
    if debug:  Log.Info("[?] (#3) - offset: {}, anidbid: {}, int(episode.split('-')[0]): {}".format(offset, anidbid, int(episode.split('-')[0])))
    if int(episode.split('-')[0])> int(offset):  return '1', str(int(episode.split('-')[0])-int(offset)), anidbid   #Lvl 1 - defaulttvdbseason + offset
  
  # <anime anidbid="23" tvdbid="76885" defaulttvdbseason="1" episodeoffset="" tmdbid="" imdbid="">
  defaulttvdbseason, episodeoffset, s1e1_mapped = Dict(mappingList, 'defaulttvdbseason'), Dict(mappingList, 'episodeoffset'), Dict(mappingList, 's1e1_mapped')
  if debug:  Log.Info('[?] (#4) defaulttvdbseason: {}, episodeoffset: {}, s1e1_mapped: {}'.format(defaulttvdbseason, episodeoffset, s1e1_mapped))
  if season==defaulttvdbseason and not s1e1_mapped:
    return '1', str(int(episode)-int(episodeoffset)), ''
  
  # Map season 0 episodes directly to tvdb season 0 episodes
  # On condition of being the only anidb id mapped to the tvdbid, its set to season 1, and has no special mappings
  tvdbcount, s1_mapping = Dict(mappingList, 'tvdbcount', default=0), Dict(mappingList, 'TVDB', 's1')
  if debug:  Log.Info('[?] (#5) defaulttvdbseason: {}, episodeoffset: {}, s1e1_mapped: {}'.format(defaulttvdbseason, episodeoffset, s1e1_mapped))
  if season=="0" and tvdbcount==1 and s1_mapping: # Confirm only one entry and its 's1'
    for item in Dict(mappingList, 'TVDB'): # Also that there are no s0 mappings
      if item.startswith("s0"):
        if debug:  Log.Info('[?] (#5) Found: {}'.format(item))
        break
    else:  return season, episode, list(Dict(mappingList, 'TVDB', 's1').keys())[0]
  
  return '0', '0', 'xxxxxxx'
