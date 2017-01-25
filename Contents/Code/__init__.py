# -*- coding: utf-8 -*-
### HTTP Anidb Metadata Agent (HAMA) By ZeroQI (Forked from Atomicstrawberry's v0.4 - AniDB, TVDB, AniDB mod agent for XBMC XML's ###
import os, re, time, datetime, string, thread, threading, urllib, copy, io # Functions used per module: os (read), re (sub, match), time (sleep), datetim (datetime).
from lxml import etree                                                     # fromstring
import common, AnimeLists, AniDB, tvdb, tmdb, FanartTv, OMDb               # Hama source splitted modules

class HamaCommonAgent:
  Log.Info('### HTTP Anidb Metadata Agent (HAMA) Class Started ########################################################################################################')
  
  ### Serie search ######################################################################################################################################################
  def Search(self, results, media, lang, manual, movie):
    AniDB.Search_AniDB(results, media, lang, manual, movie)
    #if maxi<50:           Search_TVDB(self, results,  media, lang, manual, movie)
    #if not len(results):  Search_TMDB(self, results, media, lang, manual, movie)
    
  ### Parse the AniDB anime title XML ##################################################################################################################################
  def Update(self, metadata, media, lang, force, movie):
    Log.Info('--- Update Begin -------------------------------------------------------------------------------------------')
    
    ### Variables initialisation ###
    tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio, anidbid_table, poster_id = "", "", "", "", {}, "", [], ""          # anidbTvdbMapping
    tvdbtitle, tvdbOverview, tvdbFirstAired, tvdbContentRating, tvdbNetwork, tvdbGenre, tvdbRating   = "", "", "", "", "", "", None            # get_tvdb_meta
    current_date, anidbid, tvdbanime                                                                 = int(time.strftime("%Y%m%d")), "", None  # Other variables to set
    error_log = { 'anime-list anidbid missing': [], 'anime-list tvdbid missing'  : [], 'anime-list studio logos'   : [],
                  'AniDB summaries missing'   : [], 'AniDB posters missing'      : [], 
                  'TVDB posters missing'      : [], 'TVDB season posters missing': [], 'Plex themes missing'       : [],
                  'Missing Episodes'          : [], 'Missing Episode Summaries'  : [], 'Missing Specials'          : [], 'Missing Special Summaries'  : []  
                }
    ### Metadata source/id separation and finding other metadata ids ###
    metadata_source, metadata_id = metadata.id.split('-', 1)
    Log.Info("metadata source: '%s', id: '%s', Title: '%s', lang: '%s', force: '%s', movie: '%s'" % (metadata_source, metadata_id, metadata.title, lang, force, movie))
    if metadata_source.startswith("anidb"):
      anidbid = metadata_id
      if anidbid.isdigit():  tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio, anidbid_table, poster_id = AnimeLists.anidbTvdbMapping(metadata, media, movie, anidbid, error_log)  
    elif metadata_source.startswith("tvdb"):  tvdbid = metadata_id_number
    elif metadata_source.startswith("tmdb"):  tmdbid = metadata_id_number #; tmdb.Update_TMDB(self, metadata, media, lang, force, movie)
    elif metadata_source.startswith("tsdb"):  tsdbid = metadata_id_number #; tmdb.Update_TMDB(self, metadata, media, lang, force, movie)
    
    ### Recover other metadata ids ###
    if tvdbid.isdigit():
      tvdb_table = tvdb.get_tvdb_metadata(metadata, media, lang, movie, defaulttvdbseason, metadata_source, tvdbid, imdbid, error_log)         # Updates imdbid from tvdbid, used by omdb
      if (Prefs['GetPlexThemes'    ]                                  ):                                           tvdb.plex_theme_song      (metadata, tvdbid, tvdbtitle, error_log)                           ### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###
      if (Prefs['GetTvdbPosters'   ] or Prefs['GetTvdbFanart' ]       ):                                           tvdb.getImagesFromTVDB    (metadata, media, error_log, tvdbid, tvdbtitle, movie, poster_id, force, defaulttvdbseason, 1)
    if (imdbid.isdigit()                    ) and (Prefs['GetOmdbPoster'    ]                                  ):  omdb.omdb_poster          (metadata, imdbid)                                                 ### OMDB - Posters - Using imdbid ###  return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
    if (imdbid.isdigit() or tmdbid.isdigit()) and (Prefs['GetTmdbPoster'    ] or Prefs['GetTmdbFanart'        ]):  tmdb.tmdb_posters         (metadata, imdbid, tmdbid)                                         ### - TMDB - background, Poster - using imdbid or tmdbid ### The Movie Database is least prefered by the mapping file, only when imdbid missing
    if (imdbid.isdigit() or tmdbid.isdigit()) and (Prefs['GetFanartTVPoster'] or Prefs['GetFanartTVBackground']):  FanartTv.fanarttv_posters (metadata, movie, tmdbid, tvdbid, imdbid, defaulttvdbseason)       ### fanart.tv - Background, Poster and Banner - Using imdbid ###
    if tmdbid.isdigit() and movie:                                                                                 tmdb.TMDB_Tagline_Trailers(metadata, movie, lang, tmdbid, imdbid)                            ### Populate Movie Metadata Extras (e.g. Taglines) from TMDB for Movies ###
    if metadata_source == "tvdb4"             and (Prefs['GetASSPosters']                                      ):  common.getImagesFromASS   (metadata, media, tvdbid, movie, 0)                                ### ASS tvdb4 ark posters ###
    if not movie and (max(media.seasons.iterkeys())>1 or metadata_source.startswith("tvdb")):                      tvdb.tvdb_update_meta     (metadata, media, metadata_source, defaulttvdbseason, tvdb_table)  ### TVDB mode when a season 2 or more exist ###
    elif metadata_source.startswith("anidb"):                                                                      AniDB.anidb_update_meta   (metadata, media, metadata_id)
    
    common.write_logs(media, movie, error_log, metadata_source, metadata_id, anidbid, tvdbid)
    Log.Info('--- Update end -------------------------------------------------------------------------------------------------')

### Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows, HamaCommonAgent):
  name             = 'HamaTV'
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none'] # 'com.plexapp.agents.opensubtitles'
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  def search(self, results,  media, lang, manual): self.Search(results,  media, lang, manual, False )
  def update(self, metadata, media, lang, force ): self.Update(metadata, media, lang, force,  False )

class HamaMovieAgent(Agent.Movies, HamaCommonAgent):
  name             = 'HamaMovies'
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  languages        = [Locale.Language.English, 'fr', 'zh', 'sv', 'no', 'da', 'fi', 'nl', 'de', 'it', 'es', 'pl', 'hu', 'el', 'tr', 'ru', 'he', 'ja', 'pt', 'cs', 'ko', 'sl', 'hr']
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none'] # 'com.plexapp.agents.opensubtitles'
  def search(self, results,  media, lang, manual): self.Search(results,  media, lang, manual, True )
  def update(self, metadata, media, lang, force ): self.Update(metadata, media, lang, force,  True )

 ### Pre-Defined Start function #########################################################################################################################################
def Start():
  Log.Info('### HTTP Anidb Metadata Agent (HAMA) Started ##############################################################################################################')
  HTTP.CacheTime = CACHE_1HOUR * 24 * 2  
  msgContainer   = common.ValidatePrefs()
  if msgContainer.header == 'Error': return
  common.SetLogging()
 
