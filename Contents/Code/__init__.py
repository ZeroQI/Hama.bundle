# -*- coding: utf-8 -*-
#
# To Do
# - 'Debug' mode: logs per serie folder, need to use scanner logging
# - search word pick serie, do levenstein i partially match only (few chars difference)

### Imports ###
import common      # Functions: Logging, SaveFile, LoadFile, metadata_download, WriteLogs, cleanse_title, GetMetadata, UpdateMeta, UpdateMetaField
                   # Functions: GetMeta, natural_sort_key, SaveDict, Dict, GetXml, GetStatusCode
from   common import Dict  #import Simkl       # Functions: GetMetadata, Register                                      Variables: None
import AnimeLists  # Functions: GetMetadata, GetAniDBTVDBMap, GetAniDBMovieSet, MergeMaps  Variables: MAPPING_FEEDBACK
import AniDB       # Functions: GetMetadata, Search, GetAniDBTitlesDB, GetAniDBTitle       Variables: ANIDB_SERIE_URL
import TheTVDB     # Functions: GetMetadata, Search                                        Variables: TVDB_SERIE_URL, TVDB_IMAGES_URL
import TheMovieDb  # Functions: GetMetadata, Search                                        Variables: None
import MyAnimeList # Functions: GetMetadata                                                Variables: None
import OMDb        # Functions: GetMetadata                                                Variables: None
import FanartTV    # Functions: GetMetadata                                                Variables: None
import Plex        # Functions: GetMetadata                                                Variables: None
import TVTunes     # Functions: GetMetadata                                                Variables: None
import os
    
### Variables ###
AniDBMovieSets = AnimeLists.GetAniDBMovieSets()

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info("".ljust(157, '='))
  Log.Info ("ValidatePrefs()")
  DefaultPrefs   = ("GetSingleOne", "localart", "adult", "MinimumWeight", "SerieLanguagePriority", "EpisodeLanguagePriority") #"Simkl", 
  PrefsFieldList = list(set(common.FieldListMovies + common.FieldListSeries + common.FieldListEpisodes + DefaultPrefs))  # set is un-ordered lsit so order is lost
  try:  
    for key in PrefsFieldList:  Log.Info("Prefs[{key:<{width}}] = {value}".format(key=key, width=max(map(len, PrefsFieldList)), value=Prefs[key] or "EMPTY, MODIFY AND SAVE"))
  except:  Log.Error("DefaultPrefs.json, Value '%s' missing, update+save" % key);  return MessageContainer ('Error',   "Value '%s' missing from 'DefaultPrefs.json'" % key)
  Log.Info("".ljust(157, '='))
  return MessageContainer('Success', "DefaultPrefs.json valid")

### Pre-Defined Start function ############################################################################################################################################
def Start():
  Log.Info("".ljust(157, '='))
  Log.Info("HTTP Anidb Metadata Agent by ZeroQI (Forked from Atomicstrawberry's v0.4, AnimeLists XMLs by SdudLee) - CPU: {}, OS: {}".format(Platform.CPU, Platform.OS))
  HTTP.CacheTime = CACHE_1DAY  # in sec: CACHE_1MINUTE, CACHE_1HOUR, CACHE_1DAY, CACHE_1WEEK, CACHE_1MONTH
  ValidatePrefs() #if Prefs['Simkl']:  Simkl.Register()
  
### Movie/Serie search ###################################################################################################################################################
def Search(results, media, lang, manual, movie):
  log = common.PlexLog(media=media, movie=movie, search=True)
  orig_title = media.title if movie else media.show
  Log.Info('=== Search ============================================================================================================')
  Log.Info("Title: '%s', name: '%s', filename: '%s', manual: '%s', year: '%s'" % (orig_title, media.name, media.filename, str(manual), media.year))  #if media.filename is not None: filename = String.Unquote(media.filename) #auto match only
  if orig_title == "clear-cache":  HTTP.ClearCache();  return
  if not orig_title:  return
  
  ### Check if a guid is specified "Show name [anidb-id]" ###
  import re
  match = re.search(u"(?P<show>.*?) ?\[(?P<source>([a-zA-Z0-9]*))-(tt)?(?P<guid>[0-9]{1,7})\]", orig_title, re.IGNORECASE) if ' [' in orig_title else False
  if match:
    guid=match.group('source') + '-' + match.group('guid')
    results.Append(MetadataSearchResult(id=guid, name=match.group('show')+" ["+guid+']', year=media.year, lang=lang, score=100))
    Log.Info("Forced ID - source: {}, id: {}, title: '{}'".format(match.group('source'), match.group('guid'), match.group('show')))
  else:  #if media.year is not None:  orig_title = orig_title + " (" + str(media.year) + ")"  ### Year - if present (manual search or from scanner but not mine), include in title ###
    maxi, n = 0, 0
    if movie or max(map(int, media.seasons.keys()))<=1:  maxi, n =       AniDB.Search(results, media, lang, manual, movie)
    if maxi<50 and movie:                                maxi    =  TheMovieDb.Search(results, media, lang, manual, movie)
    if maxi<80 and not movie or n>1:                     maxi    = max(TheTVDB.Search(results, media, lang, manual, movie), maxi)
  Log.Info("".ljust(157, '='))
  
  ###test
  if not movie:  log.stop()
        
### Update Movie/Serie from metadata.id assigned #########################################################################################################################
def Update(metadata, media, lang, force, movie):
  log = common.PlexLog(media=media, movie=movie, search=False)
  source    = metadata.id.split('-', 1)[0]
  error_log = { 'AniDB summaries missing'   :[], 'AniDB posters missing'      :[], 'anime-list AniDBid missing':[], 'anime-list studio logos'  :[],  
                'TVDB posters missing'      :[], 'TVDB season posters missing':[], 'anime-list TVDBid missing' :[], 'Plex themes missing'      :[],
                'Missing Episodes'          :[], 'Missing Specials'           :[], 'Missing Episode Summaries' :[], 'Missing Special Summaries':[]}
  Log.Info('=== Update ==='.ljust(157, '='))
  Log.Info("id: {}, title: {}, lang: {}, force: {}, movie: {}".format(metadata.id, metadata.title, lang, force, movie))
  
  dict_AnimeLists, AniDBid, TVDBid, TMDbid, IMDbid, mappingList =  AnimeLists.GetMetadata(media, movie, error_log, metadata.id,                   AniDBMovieSets) #, AniDBTVDBMap
  dict_AniDB, ANNid, MALid                                      =       AniDB.GetMetadata(media, movie, error_log,       source, AniDBid, TVDBid, AniDBMovieSets, mappingList)
  dict_TheTVDB,                             IMDbid              =     TheTVDB.GetMetadata(media, movie, error_log, lang, source, AniDBid, TVDBid, IMDbid,         mappingList, Dict(AniDB, 'movie'))
  dict_TheMovieDb,          TSDbid, TMDbid, IMDbid              =  TheMovieDb.GetMetadata(media, movie,                                   TVDBid, TMDbid, IMDbid)
  dict_FanartTV                                                 =    FanartTV.GetMetadata(       movie,                                   TVDBid, TMDbid, IMDbid)
  dict_tvdb4                                                    =      common.GetMetadata(media, movie, source, TVDBid)
  dict_Plex                                                     =        Plex.GetMetadata(metadata, error_log, TVDBid, Dict(dict_TheTVDB, 'title'))
  dict_TVTunes                                                  =     TVTunes.GetMetadata(metadata, Dict(dict_TheTVDB, 'title'), Dict(mappingList, 'name'))  #Sources[m:eval('dict_'+m)]
  dict_OMDb                                                     =        OMDb.GetMetadata(movie, IMDbid) if Prefs['OMDbApiKey'] not in ('None', '', 'N/A') else {}  #TVDBid=='hentai'
  dict_MyAnimeList                                              = MyAnimeList.GetMetadata(movie, MALid ) if MALid                                          else {}  #TVDBid=='hentai'
  Log.Info("".ljust(157, '-')) 
  Log.Info("Update() - AniDBid: '{}', TVDBid: '{}', TMDbid: '{}', IMDbid: '{}', ANNid:'{}', MALid: '{}'".format(AniDBid, TVDBid, TMDbid, IMDbid, ANNid, MALid))
  common.write_logs(media, movie, error_log, source, id, AniDBid, TVDBid)
  common.UpdateMeta(metadata, media, movie, {'AnimeLists': dict_AnimeLists, 'TheTVDB': dict_TheTVDB, 'AniDB': dict_AniDB, 'Plex': dict_Plex, 'MyAnimeList': dict_MyAnimeList, 
    'TheMovieDb': dict_TheMovieDb, 'TVTunes': dict_TVTunes, 'tvdb4': dict_tvdb4, 'OMDb': dict_OMDb, 'FanartTV': dict_FanartTV}, mappingList)

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
