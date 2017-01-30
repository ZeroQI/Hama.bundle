# -*- coding: utf-8 -*-
import common          # HAMA generic   functions: getImagesFromASS, write_logs
import AnimeLists      # AnimeLists     functions: anidbTvdbMapping
import AniDB           # AniDB     .net functions: Search_AniDB, 
import tvdb            # TheTVDB   .com functions: Search_TVDB, get_tvdb_metadata, tvdb_update_meta, plex_theme_song, getImagesFromTVDB
import tmdb            # TheMovieDB.net functions: Search_TMDB, TMDB_Tagline_Trailers, Update_TMDB
import FanartTv        # FanartTV  .com functions: fanarttv_posters, get_tmdbid_per_imdbid
import OMDb            # OMDbAPI   .com functions: omdb_poster

### Pre-Defined Start function #########################################################################################################################################
def Start():
  import logging
  for handler in logging.getLogger('com.plexapp.agents.hama').handlers:  handler.setFormatter(logging.Formatter('%(asctime)-15s - %(name)s (%(thread)x) : %(levelname)s (%(module)s/%(funcName)s:%(lineno)d) - %(message)s'))
  Log.Info("HTTP Anidb Metadata Agent (HAMA)v By ZeroQI (Forked from Atomicstrawberry's v0.4 - AniDB, TVDB mod agent using SdudLee XML's ###")
  HTTP.CacheTime = CACHE_1HOUR * 24 * 2  

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info( "ValidatePrefs()")
  DefaultPrefs = ("GetTvdbFanart", "GetTvdbPosters", "GetTvdbBanners", "GetAnidbPoster", "GetTmdbFanart", "GetTmdbPoster", "GetOmdbPoster", "GetFanartTVBackground", "GetFanartTVPoster", "GetFanartTVBanner", "GetASSPosters", "localart", "adult", 
                  "GetPlexThemes", "MinimumWeight", "SerieLanguage1", "SerieLanguage2", "SerieLanguage3", "EpisodeLanguage1", "EpisodeLanguage2")
  try:  
    for key in DefaultPrefs: Log.Info("Prefs[{key:<{width}}] = {value}".format(key=key, width=max(map(len, DefaultPrefs)), value=Prefs[key]))
    if [Prefs[key] == None for key in DefaultPrefs].count(True) > 0: Log.Error("Some Pref values do not exist. Edit and save your preferences.")
  except:  Log.Error("DefaultPrefs.json invalid, Value '%s' missing, update it and save." % key);  return MessageContainer ('Error', "Value '%s' missing from 'DefaultPrefs.json'" % key)
  else:    Log.Info( "DefaultPrefs.json is valid, Provided preference values are ok");             return MessageContainer ('Success', "DefaultPrefs.json valid")
  
### Movie/Serie search #############################################################################################################################
def Search(results, media, lang, manual, movie):
  Log.Info('--- Search Begin -------------------------------------------------------------------------------------------')
  if movie and media.title == "clear-cache" or not movie and media.show == "clear-cache":  HTTP.ClearCache()  ### Clear Plex http cache manually by searching a serie named "clear-cache" ###
  maxi = AniDB.Search_AniDB(results, media, lang, manual, movie)
  #if maxi<50:  maxi = tvdb.Search_TVDB(results, media, lang, manual, movie)
  #if maxi<50:  tmdb.Search_TMDB(results, media, lang, manual, movie)
    
### Update Movie/Serie from metadata.id assigned ###################################################################################################
def Update(metadata, media, lang, force, movie):
  Log.Info('--- Update Begin -------------------------------------------------------------------------------------------')
  import time # sleep, strftime

  ### Variables initialisation ###
  anidbid, tvdbid, tmdbid, imdbid, mappingList, tvdb_table, current_date = "", "", "", "", {}, {}, int(time.strftime("%Y%m%d"))
  error_log = { 'anime-list anidbid missing':[], 'anime-list tvdbid missing'  :[], 'anime-list studio logos'  :[], 'Plex themes missing'      :[],
                'AniDB summaries missing'   :[], 'AniDB posters missing'      :[], 'Missing Episodes'         :[], 'Missing Specials'         :[], 
                'TVDB posters missing'      :[], 'TVDB season posters missing':[], 'Missing Episode Summaries':[], 'Missing Special Summaries':[]}
  
  ### Metadata source/id separation and finding other metadata ids ###
  metadata_source, metadata_id = metadata.id.split('-', 1)
  Log.Info("metadata source: '%s', id: '%s', Title: '%s', lang: '%s', force: '%s', movie: '%s'" % (metadata_source, metadata_id, metadata.title, lang, force, movie))
  if metadata_source.startswith("anidb"):
    anidbid = metadata_id
    if anidbid.isdigit():  tvdbid, tmdbid, imdbid, mappingList = AnimeLists.anidbTvdbMapping(metadata, media, movie, anidbid, error_log)  
  elif metadata_source.startswith("tvdb"):  tvdbid = metadata_id_number
  #elif metadata_source.startswith("tmdb"):  tmdbid = metadata_id_number
  #elif metadata_source.startswith("tsdb"):  tsdbid = metadata_id_number
  if tvdbid.isdigit():  tvdb_table = tvdb.get_tvdb_metadata(metadata, media, lang, movie, metadata_source, tvdbid, imdbid, mappingList['defaulttvdbseason'], error_log)         # Updates imdbid from tvdbid, used by omdb
  
  ### Recover Backgrounds, posters, theme song ###
  if (tvdbid.isdigit()                    ) and (Prefs['GetPlexThemes'    ]                                  ):  tvdb.plex_theme_song      (metadata, tvdbid, tvdb_table, error_log)                           ### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###
  if (tvdbid.isdigit()                    ) and (Prefs['GetTvdbPosters'   ] or Prefs['GetTvdbFanart'        ]):  tvdb.getImagesFromTVDB    (metadata, media, error_log, tvdbid, tvdb_table, movie, force, mappingList['defaulttvdbseason'], 1)
  if (imdbid.isdigit()                    ) and (Prefs['GetOmdbPoster'    ]                                  ):  omdb.omdb_poster          (metadata, imdbid)                                                 ### OMDB - Posters - Using imdbid ###  return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
  if (imdbid.isdigit() or tmdbid.isdigit()) and (Prefs['GetTmdbPoster'    ] or Prefs['GetTmdbFanart'        ]):  tmdb.tmdb_posters         (metadata, imdbid, tmdbid)                                         ### - TMDB - background, Poster - using imdbid or tmdbid ### The Movie Database is least prefered by the mapping file, only when imdbid missing
  if (imdbid.isdigit() or tmdbid.isdigit()) and (Prefs['GetFanartTVPoster'] or Prefs['GetFanartTVBackground']):  FanartTv.fanarttv_posters (metadata, movie, tmdbid, tvdbid, imdbid, mappingList)       ### fanart.tv - Background, Poster and Banner - Using imdbid ###
  if (tmdbid.isdigit()                    ) and (movie                                                       ):  tmdb.TMDB_Tagline_Trailers(metadata, movie, lang, tmdbid, imdbid)                            ### Populate Movie Metadata Extras (e.g. Taglines) from TMDB for Movies ###
  if (metadata_source == "tvdb4"          ) and (Prefs['GetASSPosters']                                      ):  common.getImagesFromASS   (metadata, media, tvdbid, movie, 0)                                ### ASS tvdb4 ark posters ###
  
  ### Update other metadata ###
  if not movie and tvdbid.isdigit() and (max(int(x) for x in media.seasons.keys())>1 or metadata_source.startswith("tvdb")):  
    Log.Info("meta source: '%s', max(media.seasons.keys()): '%s', media.seasons.keys(): '%s'" % (str(metadata_source.startswith("tvdb")), str(max(int(x) for x in media.seasons.keys())>1), str(media.seasons.keys())))
    tvdb.tvdb_update_meta     (metadata, media, metadata_source, mappingList['defaulttvdbseason'], tvdb_table)  ### TVDB mode when a season 2 or more exist ###
  elif metadata_source.startswith("anidb"):                                                                       AniDB.anidb_update_meta   (metadata, media, movie, anidbid, tvdbid, tvdb_table, mappingList, AnimeLists.AniDB_collection_tree, error_log, current_date)
  #elif metadata_source.startswith("tmdb" ):                                                                      tmdb.Update_TMDB          (metadata, media, lang, force, movie)
  #elif metadata_source.startswith("tsdb" ):                                                                      tmdb.Update_TMDB          (metadata, media, lang, force, movie)
  common.write_logs(media, movie, error_log, metadata_source, metadata_id, anidbid, tvdbid)
  Log.Info('--- Update end -------------------------------------------------------------------------------------------------')

### Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows):
  name             = 'HamaTV'
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none'] # 'com.plexapp.agents.opensubtitles'
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search(self, results,  media, lang, manual):  Search(results,  media, lang, manual, False )
  def update(self, metadata, media, lang, force ):  Update(metadata, media, lang, force,  False )

class HamaMovieAgent(Agent.Movies):
  name             = 'HamaMovies'
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none'] # 'com.plexapp.agents.opensubtitles'
  def search(self, results,  media, lang, manual):  Search(results,  media, lang, manual, True )
  def update(self, metadata, media, lang, force ):  Update(metadata, media, lang, force,  True )
