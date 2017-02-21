# -*- coding: utf-8 -*-

### Imports ###
import time        # sleep, strftime
import common      # Functions: Logging, SaveFile, LoadFile, metadata_download, WriteLogs, cleanse_title, GetMetadata, UpdateMeta, UpdateMetaField
                   # Functions: GetElementText, GetPosters, GetSeasons, GetFanarts, GetBanners, natural_sort_key
import AnimeLists  # Functions: GetMetadata, GetAniDBTVDBMap, GetAniDBMovieSet, MergeMaps                  Variables: MAPPING_FEEDBACK
import AniDB       # Functions: GetMetadata, Search, GetAniDBTitlesDB, GetAniDBTitle                       Variables: ANIDB_SERIE_URL, ANIDB_PIC_BASE_URL
import TheTVDB     # Functions: GetMetadata, Search                                                        Variables: TVDB_SERIE_URL
import TheMovieDB  # Functions: GetMetadata, Search, Tagline_Trailers, get_TMDbid_per_IMDbid               Variables: TVDB_SERIE_URL
import FanartTV    # Functions: GetMetadata                                                                Variables: None
import MyAnimeList # Functions: GetMetadata                                                                Variables: None
import OMDb        # Functions: GetMetadata                                                                Variables: None
import Plex        # Functions: GetMetadata                                                                Variables: None
import Simkl       # Functions: GetMetadata                                                                Variables: None

### Variables ###
AniDBTitlesDB  =      AniDB.GetAniDBTitlesDB()
AniDBTVDBMap   = AnimeLists.GetAniDBTVDBMap()
AniDBMovieSets = AnimeLists.GetAniDBMovieSets()

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info("".ljust(157, '='))
  Log.Info ("ValidatePrefs()")
  DefaultPrefs = ("GetSingleOne", "Posters", "Seasons", "Fanarts", "Banners", "Themes", "TheTVDB", "AniDB", "TheMovieDB", "OMDb", "FanartTV", "MyAnimeList", "ASSPosters", 
                  "Simkl", "localart", "adult", "MinimumWeight", "SerieLanguage1", "SerieLanguage2", "SerieLanguage3", "EpisodeLanguage1", "EpisodeLanguage2")
  try:  
    for key in DefaultPrefs:
      Log.Info("Prefs[{key:<{width}}] = {value}".format(key=key, width=max(map(len, DefaultPrefs)), value=Prefs[key]))
      if Prefs[key] == None:  Log.Error("Some Pref values do not exist. Edit and save your preferences.")
  except:  Log.Error("ValidatePrefs() - DefaultPrefs.json, Value '%s' missing, update it and save." % key);  return MessageContainer ('Error', "Value '%s' missing from 'DefaultPrefs.json'" % key)
  else:    Log.Info( "ValidatePrefs() - DefaultPrefs.json valid");                                           return MessageContainer ('Success', "DefaultPrefs.json valid")
  Log.Info("".ljust(157, '='))
  
### Pre-Defined Start function ##################################################################################################################################################
def Start():
  common.Logging()
  Log.Info("".ljust(157, '='))
  Log.Info("HTTP Anidb Metadata Agent (HAMA)v By ZeroQI (Forked from Atomicstrawberry's v0.4 - AniDB, TVDB mod agent using SdudLee XML's ###")
  Log.Info("".ljust(157, '='))
  HTTP.CacheTime = CACHE_1DAY  # in sec - was (=3600): CACHE_1HOUR
  if Prefs['Simkl']:  Simkl.Register()
  
def SetRating(key, rating):  pass
  
### Movie/Serie search ##########################################################################################################################################################
def Search(results, media, lang, manual, movie):
  Log.Info('=== Search Begin ============================================================================================================')
  if movie and media.title == "clear-cache" or not movie and media.show == "clear-cache":  HTTP.ClearCache()  ### Clear Plex http cache manually by searching a serie named "clear-cache" ###
  maxi = AniDB.Search(results, media, lang, manual, movie, AniDBTitlesDB)
  
### Update Movie/Serie from metadata.id assigned ################################################################################################################################
def Update(metadata, media, lang, force, movie):
  
  ### Variables initialisation ###
  error_log = { 'AniDB summaries missing'   :[], 'AniDB posters missing'      :[], 'Missing Episodes'         :[], 'Missing Specials'         :[], 'anime-list AniDBid missing':[], 'anime-list TVDBid missing':[], 
                'TVDB posters missing'      :[], 'TVDB season posters missing':[], 'Missing Episode Summaries':[], 'Missing Special Summaries':[], 'anime-list studio logos'   :[], 'Plex themes missing'      :[]}
  AnimeLists_dict, AniDB_dict, TheTVDB_dict, MyAnimeList_dict, FanartTV_dict, OMDb_dict, TheTVDB_dict, TheMovieDB_dict, Plex_dict, tvdb4_dict, Simkl_dict, TVTunes_dict = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
  ANNid, MALid  = "", ""
  
  ### Metadata source/id separation and finding other metadata ids ###
  Log.Info('=== Update Begin ============================================================================================================' + Platform.OS + "  " + Platform.CPU)
  Log.Info("Update() - metadata.id: '%s', Title: '%s', lang: '%s', force: '%s', movie: '%s', max(media.seasons.keys()): '%s'" % (metadata.id, metadata.title, lang, force, movie, str(max(int(x) for x in media.seasons.keys())>1)))
  AniDBid, TVDBid, TMDbid, IMDbid, mappingList, AnimeLists_dict = AnimeLists.GetMetadata(metadata, media, movie, error_log, AniDBMovieSets, AniDBTVDBMap)
  if AniDBid.isdigit():                ANNid, MALid, AniDB_dict =      AniDB.GetMetadata(metadata, media, movie, error_log, AniDBMovieSets, AniDBid, TVDBid, mappingList)
  if  TVDBid.isdigit():                    IMDbid, TheTVDB_dict =    TheTVDB.GetMetadata(metadata, media, movie, error_log, lang, source, TVDBid, IMDbid, mappingList['defaulttvdbseason'] if 'defaulttvdbseason' in mappingList else "")
  if Prefs['TheMovieDB' ]:  TMDbid, IMDbid, TheMovieDB_dict = TheMovieDB.GetMetadata(metadata, media, movie, IMDbid, TMDbid, TVDBid)
  if Prefs['Simkl'      ]:  Simkl_dict       =       Simkl.GetMetadata(metadata, media, movie, AniDBid, TVDBid)
  if Prefs['OMDb'       ]:  OMDb_dict        =        OMDb.GetMetadata(metadata, IMDbid, mappingList['name'])   
  if Prefs['FanartTV'   ]:  FanartTV_dict    =    FanartTV.GetMetadata(metadata, TVDBid, IMDbid, TMDbid, movie)  ### fanart.tv - Background, Poster and Banner - Using IMDbid ###
  if Prefs['MyAnimeList']:  MyAnimeList_dict = MyAnimeList.GetMetadata(metadata, movie, MALid)
  if Prefs['tvdb4'      ]:  tvdb4_dict       =      common.GetMetadata(metadata, media, TVDBid, movie, 0)  ### ASS tvdb4 ark posters ###
  if Prefs['Plex'       ]:  Plex_dict        =        Plex.GetMetadata(metadata, TVDBid, TheTVDB_dict, error_log)
  if Prefs['Plex'       ]:  TVTunes_dict     =        Plex.TVTunes(metadata, TVDBid, TheTVDB_dict, mappingList)
  common.write_logs(media, movie, error_log, source, source, AniDBid, TVDBid)
  
  ### Update metadata ###
  Log.Info("".ljust(157, '-'))
  Log.Info("Update() - AniDBid: {}, TVDBid: {}, TMDbid: {}, IMDbid: {}, ANNid:{}, MALid: {}".format(AniDBid, TVDBid, TMDbid, IMDbid, ANNid, MALid))
  MetaSources = {'AniDB': AniDB_dict, 'MyAnimeList': MyAnimeList_dict, 'FanartTV': FanartTV_dict, 'OMDb': OMDb_dict, 'TheTVDB': TheTVDB_dict, 'TheMovieDB':   TheMovieDB_dict, 'Plex': Plex_dict, 'AnimeLists': AnimeLists_dict, 'tvdb4': tvdb4_dict, "Simkl": Simkl_dict, "TVTunes": TVTunes_dict}
  common.UpdateMeta(metadata, MetaSources, movie)

### Agent declaration ###########################################################################################################################################################
class HamaTVAgent(Agent.TV_Shows):
  name, primary_provider, fallback_agent, contributes_to, accepts_from = 'HamaTV', True, False, None, ['com.plexapp.agents.localmedia'] # 'com.plexapp.agents.none', 'com.plexapp.agents.opensubtitles'
  languages  = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, False)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  False)

class HamaMovieAgent(Agent.Movies):
  name, primary_provider, fallback_agent, contributes_to, accepts_from = 'HamaMovies', True, False, None, ['com.plexapp.agents.localmedia'] # 'com.plexapp.agents.none', 'com.plexapp.agents.opensubtitles'
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, True)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  True)
