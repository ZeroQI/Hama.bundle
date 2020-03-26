# -*- coding: utf-8 -*-
#
# To Do
# - 'Debug' mode: logs per serie folder, need to use scanner logging
# - search word pick serie, do levenstein i partially match only (few chars difference)

### Imports ###
# Python Modules #
import re
import os
import datetime
# HAMA Modules #
import common            # Functions: GetPlexLibraries, write_logs, UpdateMeta                   Variables: PlexRoot, FieldListMovies, FieldListSeries, FieldListEpisodes, DefaultPrefs, SourceList
from common import Dict
import AnimeLists        # Functions: GetMetadata, GetAniDBTVDBMap, GetAniDBMovieSets            Variables: AniDBMovieSets
import tvdb4             # Functions: GetMetadata                                                Variables: None
import TheTVDBv2         # Functions: GetMetadata, Search                                        Variables: None
import AniDB             # Functions: GetMetadata, Search, GetAniDBTitlesDB                      Variables: None
import TheMovieDb        # Functions: GetMetadata, Search                                        Variables: None
import FanartTV          # Functions: GetMetadata                                                Variables: None
import Plex              # Functions: GetMetadata                                                Variables: None
import TVTunes           # Functions: GetMetadata                                                Variables: None
import OMDb              # Functions: GetMetadata                                                Variables: None
#import MyAnimeList       # Functions: GetMetadata                                                Variables: None
import Local             # Functions: GetMetadata                                                Variables: None
import anidb34           # Functions: AdjustMapping                                              Variables: None

### Variables ###
  
### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info("".ljust(157, '='))
  Log.Info ("ValidatePrefs(), PlexRoot: "+Core.app_support_path)

  #Reset to default agent setting
  Prefs['reset_to_defaults']  #avoid logs message on first accesslike: 'Loaded preferences from DefaultPrefs.json' + 'Loaded the user preferences for com.plexapp.agents.lambda'
  filename_xml  = os.path.join(common.PlexRoot, 'Plug-in Support', 'Preferences', 'com.plexapp.agents.hama.xml')
  filename_json = os.path.join(common.PlexRoot, 'Plug-ins', 'Hama.bundle', 'Contents', 'DefaultPrefs.json')
  Log.Info ("[?] agent settings json file: '{}'".format(os.path.relpath(filename_json, common.PlexRoot)))
  Log.Info ("[?] agent settings xml prefs: '{}'".format(os.path.relpath(filename_xml , common.PlexRoot)))
  if Prefs['reset_to_defaults'] and os.path.isfile(filename_xml):  os.remove(filename_xml)  #delete filename_xml file to reset settings to default

  PrefsFieldList = list(set(common.FieldListMovies + common.FieldListSeries + common.FieldListEpisodes + common.DefaultPrefs))  # set is un-ordered lsit so order is lost
  filename       = os.path.join(Core.app_support_path, 'Plug-ins', 'Hama.bundle', 'Contents', 'DefaultPrefs.json')
  if os.path.isfile(filename):
    try:   json = JSON.ObjectFromString(Core.storage.load(filename), encoding=None)  ### Load 'DefaultPrefs.json' to have access to default settings ###
    except Exception as e:  json = None; Log.Info("Error :"+str(e)+", filename: "+filename)
    if json:
      Log.Info ("Loaded: "+filename)
      Pref_list={}
      for entry in json:  #Build Pref_list dict from json file
        Pref_list[entry['id']]=entry   #if key in Prefs gives: KeyError: "No preference named '0' found." so building dict
        if entry['type']=='bool':
          if entry['type']==1:  Pref_list[entry['id']]['value'] = 'true'
          else:                 Pref_list[entry['id']]['value'] = 'false'
      for entry in Pref_list:  # Check fields not in PrefsFieldList and sources mispelled
        if   entry not in PrefsFieldList:  Log.Info("Next entry not in PrefsFieldList, so will not be updated by the engine") 
        elif entry not in common.DefaultPrefs:  # Check for mispelled metadata sources
          for source in Prefs[entry].replace('|', ',').split(','):
            if source.strip() not in common.SourceList+('None', ''):
              Log.Info(" - Source '{}' invalid".format(source.strip()))
        Log.Info("Prefs[{key:<{width}}] = {value:<{width2}}{default}".format(key=entry, width=max(map(len, PrefsFieldList)), value=Prefs[entry] if Prefs[entry]!='' else "Error, go in agent settings, set value and save", width2=max(map(len, [Pref_list[x]['default'] for x in Pref_list])), default=' (still default value)' if Prefs[entry] == Pref_list[entry]['default'] else " (Default: "+Pref_list[entry]['default']+")"))
      for entry in PrefsFieldList:
        if entry not in Pref_list:
          Log.Info("Prefs[{key:<{width}}] does not exist".format(key=entry, width=max(map(len, PrefsFieldList))))
  #Plex Media Server\Plug-in Support\Preferences\com.plexapp.agents.hama.xml
  Log.Info("".ljust(157, '='))
  return MessageContainer('Success', "DefaultPrefs.json valid")

### Pre-Defined Start function ############################################################################################################################################
def Start():
  Log.Info("".ljust(157, '='))
  Log.Info("HTTP Anidb Metadata Agent by ZeroQI (Forked from Atomicstrawberry's v0.4, AnimeLists XMLs by SdudLee) - CPU: {}, OS: {}".format(Platform.CPU, Platform.OS))
  #HTTP.CacheTime = CACHE_1DAY  # in sec: CACHE_1MINUTE, CACHE_1HOUR, CACHE_1DAY, CACHE_1WEEK, CACHE_1MONTH
  HTTP.CacheTime = CACHE_1MINUTE*30
  ValidatePrefs()
  common.GetPlexLibraries()
  # Load core files
  AnimeLists.GetAniDBTVDBMap()
  AnimeLists.GetAniDBMovieSets()
  AniDB.GetAniDBTitlesDB()
  
### Movie/Serie search ###################################################################################################################################################
def Search(results, media, lang, manual, movie):
  from common import Log  #Import here for startup logging to go to the plex pms log
  orig_title = media.title if movie else media.show
  Log.Open(media=media, movie=movie, search=True)
  Log.Info('=== Search() ==='.ljust(157, '='))
  Log.Info("title: '%s', name: '%s', filename: '%s', manual: '%s', year: '%s'" % (orig_title, media.name, media.filename, str(manual), media.year))  #if media.filename is not None: filename = String.Unquote(media.filename) #auto match only
  Log.Info("start: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")))
  Log.Info("".ljust(157, '='))
  if not orig_title:  return
  
  #clear-cache directive
  if orig_title == "clear-cache":  
    HTTP.ClearCache()
    results.Append(MetadataSearchResult(id='clear-cache', name='Plex web cache cleared', year=media.year, lang=lang, score=0))
    return
  
  ### Check if a guid is specified "Show name [anidb-id]" ###
  Log.Info('--- force id ---'.ljust(157, '-'))
  match = re.search(r"(?P<show>.*?) ?\[(?P<source>(anidb(|[2-9])|tvdb(|[2-9])|tmdb|tsdb|imdb))-(tt)?(?P<guid>[^\[\]]*)\]", orig_title, re.IGNORECASE)
  if match is not None:
    guid=match.group('source') + '-' + match.group('guid')
    if guid.startswith('anidb') and not movie and max(map(int, media.seasons.keys()))>1:  Log.Info('[!] multiple seasons = tvdb numbering, BAKA!')
    results.Append(MetadataSearchResult(id=guid, name=match.group('show')+" ["+guid+']', year=media.year, lang=lang, score=100))
    Log.Info("Forced ID - source: {}, id: {}, title: '{}'".format(match.group('source'), match.group('guid'), match.group('show')))
  else:  #if media.year is not None:  orig_title = orig_title + " (" + str(media.year) + ")"  ### Year - if present (manual search or from scanner but not mine), include in title ###
    Log.Info('--- source searches ---'.ljust(157, '-'))
    maxi, n = 0, 0
    if movie or max(map(int, media.seasons.keys()))<=1:  maxi, n =         AniDB.Search(results, media, lang, manual, movie)
    if maxi<50 and movie:                                maxi    =    TheMovieDb.Search(results, media, lang, manual, movie)
    if maxi<80 and not movie or n>1:                     maxi    = max(TheTVDBv2.Search(results, media, lang, manual, movie), maxi)
  Log.Info("".ljust(157, '='))
  Log.Info("end: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")))
  Log.Close()
        
### Update Movie/Serie from metadata.id assigned #########################################################################################################################
def Update(metadata, media, lang, force, movie):
  from common import Log  #Import here for startup logging to go to the plex pms log
  Log.Open(media=media, movie=movie, search=False)
  source    = metadata.id.split('-', 1)[0]
  error_log = { 'AniDB summaries missing'   :[], 'AniDB posters missing'      :[], 'anime-list AniDBid missing':[], 'anime-list studio logos'  :[],  
                'TVDB posters missing'      :[], 'TVDB season posters missing':[], 'anime-list TVDBid missing' :[], 'Plex themes missing'      :[],
                'Missing Episodes'          :[], 'Missing Specials'           :[], 'Missing Episode Summaries' :[], 'Missing Special Summaries':[]}
  Log.Info('=== Update() ==='.ljust(157, '='))
  Log.Info("id: {}, title: {}, lang: {}, force: {}, movie: {}".format(metadata.id, metadata.title, lang, force, movie))
  Log.Info("start: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")))
  
  # Major meta source hard required orders (ignoring id info):
  #   mappingList:                  AnimeLists->TheTVDBv2/tvdb4/AniDB->AdjustMapping
  #   mappingList['season_map']:    AnimeLists->TheTVDBv2->AdjustMapping
  #   mappingList['relations_map']: AniDB->AdjustMapping
  #   mappingList['absolute_map']:  tvdb4->TheTVDBv2->AniDB
  dict_AnimeLists, AniDBid, TVDBid, TMDbid, IMDbid, mappingList =  AnimeLists.GetMetadata(media, movie, error_log, metadata.id)
  dict_tvdb4                                                    =       tvdb4.GetMetadata(media, movie,                  source,          TVDBid,                 mappingList)
  dict_TheTVDB,                             IMDbid              =   TheTVDBv2.GetMetadata(media, movie, error_log, lang, source, AniDBid, TVDBid, IMDbid,         mappingList)
  dict_AniDB, ANNid, MALid                                      =       AniDB.GetMetadata(media, movie, error_log,       source, AniDBid, TVDBid, AnimeLists.AniDBMovieSets, mappingList)
  dict_TheMovieDb,          TSDbid, TMDbid, IMDbid              =  TheMovieDb.GetMetadata(media, movie,                                   TVDBid, TMDbid, IMDbid)
  dict_FanartTV                                                 =    FanartTV.GetMetadata(       movie,                                   TVDBid, TMDbid, IMDbid)
  dict_Plex                                                     =        Plex.GetMetadata(metadata, error_log, TVDBid, Dict(dict_TheTVDB, 'title'))
  dict_TVTunes                                                  =     TVTunes.GetMetadata(metadata, Dict(dict_TheTVDB, 'title'), Dict(mappingList, AniDBid, 'name'))  #Sources[m:eval('dict_'+m)]
  dict_OMDb                                                     =        OMDb.GetMetadata(movie, IMDbid)  #TVDBid=='hentai'
  #dict_MyAnimeList                                              = MyAnimeList.GetMetadata(movie, MALid )
  dict_Local                                                    =       Local.GetMetadata(media, movie)
  if anidb34.AdjustMapping(source, mappingList, dict_AniDB, dict_TheTVDB):
    dict_AniDB, ANNid, MALid                                    =       AniDB.GetMetadata(media, movie, error_log,       source, AniDBid, TVDBid, AnimeLists.AniDBMovieSets, mappingList)
  Log.Info('=== Update() ==='.ljust(157, '='))
  Log.Info("AniDBid: '{}', TVDBid: '{}', TMDbid: '{}', IMDbid: '{}', ANNid:'{}', MALid: '{}'".format(AniDBid, TVDBid, TMDbid, IMDbid, ANNid, MALid))
  common.write_logs(media, movie, error_log, source, AniDBid, TVDBid)
  common.UpdateMeta(metadata, media, movie, {'AnimeLists': dict_AnimeLists, 'AniDB':       dict_AniDB,       'TheTVDB': dict_TheTVDB, 'TheMovieDb': dict_TheMovieDb, 
                                             'FanartTV':   dict_FanartTV,   'tvdb4':       dict_tvdb4,       'Plex':    dict_Plex,    'TVTunes':    dict_TVTunes, 
                                             'OMDb':       dict_OMDb,       'Local':   dict_Local}, mappingList)  #'MyAnimeList': dict_MyAnimeList, 
  Log.Info("end: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")))
  Log.Close()

### Agent declaration ##################################################################################################################################################
class HamaTVAgent(Agent.TV_Shows):  # 'com.plexapp.agents.none', 'com.plexapp.agents.opensubtitles'
  name, primary_provider, fallback_agent, contributes_to, accepts_from = 'HamaTV', True, False, None, ['com.plexapp.agents.localmedia'] 
  languages = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, False)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  False)

class HamaMovieAgent(Agent.Movies):
  name, primary_provider, fallback_agent, contributes_to, accepts_from = 'HamaMovies', True, False, None, ['com.plexapp.agents.localmedia']
  languages = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, True)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  True)
