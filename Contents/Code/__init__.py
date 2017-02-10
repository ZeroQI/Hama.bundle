# -*- coding: utf-8 -*-
# https://www.python.org/dev/peps/pep-0008/

### Imports ###
import time        # sleep, strftime
import common      # Functions: Logging, SaveFile, LoadFile, metadata_download, WriteLogs, cleanse_title, getImagesFromASS, GetMeta 
                   # Functions: (Direct import) GetElementText, GetPosters, GetSeasons, 
                   # Variables: Too many...
import AnimeLists  # Functions: GetAniDBTVDBMap, GetAniDBMovieSet, anidbTvdbMapping, MergeAniDBTVDBMaps  Variables: MAPPING_FEEDBACK
import AniDB       # Functions: GetMetadata, GetAniDBTitlesDB, GetAniDBTitle, Search                     Variables: ANIDB_SERIE_URL, ANIDB_PIC_BASE_URL
import TheTVDB     # Functions: GetImages, Search, LoadMetadata                                          Variables: TVDB_SERIE_URL
import TheMovieDB  # Functions: GetImages, Search, Tagline_Trailers, get_TMDbid_per_IMDbid               Variables: TVDB_SERIE_URL
import FanartTV    # Functions: GetImages                                                                Variables: None
import MyAnimeList # Functions: GetImages                                                                Variables: None
import OMDb        # Functions: GetImages                                                                Variables: None
import Plex        # Functions: GetThemes                                                                Variables: None

### Variables ###
AniDBTitlesDB  = None
AniDBMovieSets = None
AniDBTVDBMap   = None

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info ("ValidatePrefs()")
  DefaultPrefs = ("GetSingleOne", "Posters", "Seasons", "Fanarts", "Banners", "Themes", "TheTVDB", "AniDB", "TMDb", "Omdb", "FanartTV", "MyAnimeList", "ASSPosters", 
                  "localart", "adult", "MinimumWeight", "SerieLanguage1", "SerieLanguage2", "SerieLanguage3", "EpisodeLanguage1", "EpisodeLanguage2")
  try:  
    for key in DefaultPrefs:
      Log.Info("Prefs[{key:<{width}}] = {value}".format(key=key, width=max(map(len, DefaultPrefs)), value=Prefs[key]))
      if Prefs[key] == None:  Log.Error("Some Pref values do not exist. Edit and save your preferences.")
  except:  Log.Error("ValidatePrefs() - DefaultPrefs.json, Value '%s' missing, update it and save." % key);  return MessageContainer ('Error', "Value '%s' missing from 'DefaultPrefs.json'" % key)
  else:    Log.Info( "ValidatePrefs() - DefaultPrefs.json valid");                                           return MessageContainer ('Success', "DefaultPrefs.json valid")

### Pre-Defined Start function ##################################################################################################################################################
def Start():
  common.Logging()
  Log.Info("".ljust(157, '='))
  Log.Info("HTTP Anidb Metadata Agent (HAMA)v By ZeroQI (Forked from Atomicstrawberry's v0.4 - AniDB, TVDB mod agent using SdudLee XML's ###")
  Log.Info("".ljust(157, '='))
  
  HTTP.CacheTime                   = CACHE_1DAY  # in sec - was (=3600): CACHE_1HOUR
  HTTP.Headers['User-Agent'      ] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'
  HTTP.Headers['X-Requested-With'] = 'XMLHttpRequest'

  global AniDBTitlesDB ;  AniDBTitlesDB  =      AniDB.GetAniDBTitlesDB()
  global AniDBMovieSets;  AniDBMovieSets = AnimeLists.GetAniDBMovieSets()
  global AniDBTVDBMap  ;  AniDBTVDBMap   = AnimeLists.GetAniDBTVDBMap()
  Log.Info("".ljust(157, '='))
  #msgContainer = ValidatePrefs();  if msgContainer.header == 'Error': return
  
### Movie/Serie search ##########################################################################################################################################################
def Search(results, media, lang, manual, movie):
  Log.Info('--- Search Begin -------------------------------------------------------------------------------------------')
  if movie and media.title == "clear-cache" or not movie and media.show == "clear-cache":  HTTP.ClearCache()  ### Clear Plex http cache manually by searching a serie named "clear-cache" ###
  maxi = AniDB.Search(results, media, lang, manual, movie, AniDBTitlesDB)
  
### Update Movie/Serie from metadata.id assigned ################################################################################################################################
def Update(metadata, media, lang, force, movie):
  
  ### Variables initialisation ###
  error_log = { 'AniDB summaries missing'   :[], 'AniDB posters missing'      :[], 'Missing Episodes'         :[], 'Missing Specials'         :[], 'anime-list AniDBid missing':[], 'anime-list TVDBid missing':[], 
                'TVDB posters missing'      :[], 'TVDB season posters missing':[], 'Missing Episode Summaries':[], 'Missing Special Summaries':[], 'anime-list studio logos'   :[], 'Plex themes missing'      :[]}
  AniDBid, TVDBid, TMDbid, IMDbid, ANNid, MALid, mappingList, TheTVDB_dict, current_date           = "", "", "", "", "", "", {}, {}, int(time.strftime("%Y%m%d"))
  AniDB_dict, MyAnimeList_dict, FanartTV_dict, OMDb_dict, TheTVDB_dict, TheMovieDB_dict, Plex_dict = {}, {}, {}, {}, {}, {}, {}
  
  ### Metadata source/id separation and finding other metadata ids ###
  Log.Info('--- Update Begin -------------------------------------------------------------------------------------------')
  Log.Info("Update() - metadata.id: '%s', Title: '%s', lang: '%s', force: '%s', movie: '%s', max(media.seasons.keys()): '%s'" % (metadata.id, metadata.title, lang, force, movie, str(max(int(x) for x in media.seasons.keys())>1)))
  source, id = metadata.id.split('-', 1)
  if   source.startswith("tvdb" ) and id.isdigit():  TVDBid  = id; 
  elif source.startswith("anidb") and id.isdigit():
    AniDBid = id
    TVDBid, TMDbid, IMDbid, mappingList  = AnimeLists.anidbTvdbMapping(metadata, media, movie, AniDBid,                                      error_log, AniDBTVDBMap)
    ANNid,  MALid,          AniDB_dict   = AniDB.GetMetadata          (metadata, media, movie, AniDBid, TVDBid, mappingList, AniDBMovieSets, error_log, current_date)
  
  if  TVDBid.isdigit():                              TheTVDB_dict = TheTVDB.GetMetadata (metadata, media, movie, lang, source, TVDBid, IMDbid, mappingList['defaulttvdbseason'] if 'defaulttvdbseason' in mappingList else "", error_log, current_date)  # Updates IMDbid from TVDBid, used by omdb
  if  TVDBid.isdigit():                                 Plex_Dict =    Plex.GetMetadata (metadata, TVDBid, TheTVDB_dict, error_log)                                                            ### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###  # Prefs['Themes'  ]
  if  IMDbid.startswith("tt"):                          OMDb_dict =    OMDb.GetMetadata (metadata, IMDbid, movie, mappingList['name'])                                                                    ### OMDB - Posters - Using IMDbid ###  return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
  #if  TMDbid.isdigit() and movie:                       TMDb.TaglineTrailers (metadata, movie, lang, TMDbid, IMDbid)                                                               ### Populate Movie Metadata Extras (e.g. Taglines) from TMDB for Movies ###
  #if  TVDBid.isdigit():                              TheTVDB.GetImages       (metadata, media, error_log, TVDBid, TheTVDB_dict, movie, force, mappingList['defaulttvdbseason'], 1)  #if Prefs['TheTVDB' ] and (GetPosters() or GetSeasons() or GetFanarts() or GetBanners()):
  #if  IMDbid.startswith("tt") or TMDbid.isdigit():      TMDb.GetImages       (metadata, IMDbid, TMDbid)                                                                            ### - TMDB - background, Poster - using IMDbid or TMDbid ### The Movie Database is least prefered by the mapping file, only when IMDbid missing
  #if  IMDbid.startswith("tt") or TMDbid.isdigit():  FanartTV.GetImages       (metadata, TVDBid, IMDbid, TMDbid, movie)                                             ### fanart.tv - Background, Poster and Banner - Using IMDbid ###
  #if   MALid.isdigit():                          MyAnimeList.GetImages       (metadata, MALid)
  #if source == "tvdb4":                               common.getImages       (metadata, media, TVDBid, movie, 0)                                                                   ### ASS tvdb4 ark posters ###
  
  ### Update other metadata ###
  MetaSources = {'AniDB': AniDB_dict, 'MyAnimeList': MyAnimeList_dict, 'FanartTV': FanartTV_dict, 'OMDb': OMDb_dict, 'TheTVDB': TheTVDB_dict, 'TheMovieDB':   TheMovieDB_dict, 'Plex':         Plex_dict}
  common.UpdateMeta(metadata, MetaSources, movie)
  common.write_logs(media, movie, error_log, source, source, AniDBid, TVDBid)
Log.Info('--- Update end -------------------------------------------------------------------------------------------------')

### Agent declaration ###########################################################################################################################################################
class HamaTVAgent(Agent.TV_Shows):
  name             = 'HamaTV'
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none'] # 'com.plexapp.agents.opensubtitles'
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, False)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  False)

class HamaMovieAgent(Agent.Movies):
  name             = 'HamaMovies'
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none'] # 'com.plexapp.agents.opensubtitles'
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, True)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  True)
