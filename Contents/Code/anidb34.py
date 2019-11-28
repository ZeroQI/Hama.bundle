### anidb34 ###

### Imports ###               ### Functions used ###
# Python Modules #
import re
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###

### Functions ###
def AdjustMapping(source, mappingList, dict_AniDB, dict_TheTVDB):
  """ EX:
  season_map: {'max_season': 2, '12560': {'max': 1, 'min': 1}, '13950': {'max': 0, 'min': 0}}
  relations_map: {'12560': {'Sequel': ['13950']}, '13950': {'Prequel': ['12560']}}
  TVDB Before: {'s1': {'12560': '0'}, 's0': {'13950': '0'}, '13950': (0, '')}
    's0e5': ('1', '4', '9453')
    's1': {'12560': '0'}
    '13950': (0, '')
  """
  Log.Info("=== anidb34.AdjustMapping() ===".ljust(157, '=')) 
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
    for id in sorted(season_map, key=common.natural_sort_key):
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
    for entry in sorted(adjustments, key=common.natural_sort_key):
      # EX: {'s6e0': {'added': ['6', '0'], 'deleted': {'s0e16': ('1', '1', '12909'), 's-1': {'12909': '0'}}}}
      added_season, added_offset = adjustments[entry]['added']  # 'added': ['6', '0']
      Log.Info("added_season: '{}', added_offset: '{}'".format(added_season, added_offset))
      for deleted in sorted(adjustments[entry]['deleted'], key=common.natural_sort_key):
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
    if is_banned:  Log.Info("Expected exception hit as you were banned from AniDB so you have incomplete data to proceed")
    else:          Log.Error("Unexpected exception hit")
    Log.Info('Exception: "{}"'.format(e))
    Log.Info("If a key error, look at the 'season_map'/'relations_map' info to see why it is missing")
    if source=="tvdb":   Log.Info("Source is 'tvdb' so metadata will be loaded but it will not be complete for any 'anidb3' end of season additions")
    if source=="tvdb6":  Log.Info("Source is 'tvdb6' so removing AniDB & TVDB metadata from memory to prevent incorrect data from being loaded"); dict_AniDB.clear(); dict_TheTVDB.clear()
    is_modified = False

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("is_modified: {}".format(is_modified))
  return is_modified
