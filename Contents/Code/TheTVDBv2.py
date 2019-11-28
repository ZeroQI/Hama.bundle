### TheTVDB.com API v2 ###
# http://thetvdb.com/api/A27AD9BE0DA63333/series/103291/all/en.xml

### Imports ###
# Python Modules #
import os
import time
import re
# Plex Modules #
#from collections import defaultdict
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict, GetXml # Direct import of heavily used functions
import AnimeLists

### Variables ###
TVDB_API_KEY               = 'A27AD9BE0DA63333'
TVDB_IMG_ROOT              = 'https://thetvdb.plexapp.com/banners/' 
TVDB_BASE_URL              = 'https://api.thetvdb.com'  #'https://api-beta.thetvdb.com' #tvdb v2 plex proxy site'' # TODO Start using TVDB's production api (TVDB is behind CF) when available and possibly a plex proxy for it
TVDB_LOGIN_URL             = TVDB_BASE_URL + '/login'
TVDB_SERIES_URL            = TVDB_BASE_URL + '/series/{id}'
TVDB_EPISODE_URL           = TVDB_BASE_URL + '/episodes/{id}'
TVDB_EPISODE_PAGE_URL      = TVDB_SERIES_URL + '/episodes?page={page}'
TVDB_ACTORS_URL            = TVDB_SERIES_URL + '/actors'
TVDB_SERIES_IMG_INFO_URL   = TVDB_SERIES_URL + '/images'
TVDB_SERIES_IMG_QUERY_URL  = TVDB_SERIES_URL + '/images/query?keyType={type}'

TVDB_SEARCH_URL            = TVDB_BASE_URL + '/search/series?name=%s'
TVDB_SERIE_SEARCH          = 'http://thetvdb.com/api/GetSeries.php?seriesname='

#THETVDB_LANGUAGES_CODE     = { 'cs': '28', 'da': '10', 'de': '14', 'el': '20', 'en':  '7', 'es': '16', 'fi': '11', 'fr': '17', 'he': '24', 
#                               'hr': '31', 'hu': '19', 'it': '15', 'ja': '25', 'ko': '32', 'nl': '13', 'no':  '9', 'pl': '18', 'pt': '26',
#                               'ru': '22', 'sv':  '8', 'tr': '21', 'zh': '27', 'sl': '30'}

### Functions ###  
def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList, AniDB_movie):
  ''' TVDB - Load serie JSON
  '''
  Log.Info("=== TheTVDB.GetMetadata() ===".ljust(157, '='))
  TheTVDB_dict      = {}
  max_season        = 0
  anidb_numbering   = metadata_source=="anidb" and (movie or max(map(int, media.seasons.keys()))<=1)
  anidb_prefered    = anidb_numbering and Dict(mappingList, 'defaulttvdbseason') != '1'
  language_series   = [language.strip() for language in Prefs['SerieLanguagePriority'  ].split(',') if language.strip() not in ('x-jat', 'zh-Hans', 'zh-Hant', 'zh-x-yue', 'zh-x-cmn', 'zh-x-nan', 'main')]
  language_episodes = [language.strip() for language in Prefs['EpisodeLanguagePriority'].split(',') if language.strip() not in ('x-jat', 'zh-Hans', 'zh-Hant', 'zh-x-yue', 'zh-x-cmn', 'zh-x-nan', 'main')]
  Log.Info("TVDBid: '{}', IMDbid: '{}', language_series : {}, language_episodes: {}".format(TVDBid, IMDbid, language_series , language_episodes))
  
  if not TVDBid.isdigit(): Log.Info('TVDBid non-digit');  return TheTVDB_dict, IMDbid

  ### TVDB Series JSON ###
  Log.Info("--- series ---".ljust(157, '-'))
  json = {}
  if lang not in language_series:    language_series.insert(0, lang) #for summary in lang (library setting) language
  if 'en' not in language_series:    language_series.insert(0, 'en') #for failover title
  if lang not in language_episodes:  language_episodes.append(lang) #for summary in lang (library setting) language
  if 'en' not in language_episodes:  language_episodes.append('en') #for failover title
  for language in language_series:
    json[language] = Dict(common.LoadFile(filename='series_{}.json'.format(language), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_SERIES_URL.format(id=TVDBid)+'?'+language, cache=CACHE_1DAY, headers={'Accept-Language': language}), 'data')
    if Dict(json[language], 'seriesName'):  # and not Dict(TheTVDB_dict, 'language_rank'):
      SaveDict( language_series.index(language) if not anidb_prefered else len(language_series), TheTVDB_dict, 'language_rank')
      Log.Info("[ ] language_rank: {}"          .format(Dict(TheTVDB_dict, 'language_rank')))
      Log.Info("[ ] title: {}"                  .format(SaveDict( Dict(json[language], 'seriesName') or Dict(serie2_json, 'seriesName'), TheTVDB_dict, 'title'                  )))
      Log.Info("[ ] original_title: {}"         .format(SaveDict( Dict(json[language], 'seriesName') or Dict(serie2_json, 'seriesName'), TheTVDB_dict, 'original_title'         )))
    if Dict(json, lang) and (Dict(json, lang, 'overview') or Dict(TheTVDB_dict, 'language_rank')):  break  #only need json in lang for summary, in 'en' for most things
  if not anidb_prefered:  SaveDict( Dict(json, lang, 'overview'  ).strip(" \n\r") or Dict(json, 'en', 'overview').strip(" \n\r"), TheTVDB_dict, 'summary')  
  if Dict(json, lang):
    #format:   { "id","seriesId", "airsDayOfWeek", "imdbId", "zap2itId", "added", "addedBy", "lastUpdated", "seriesName", "aliases", "banner", "status", 
    #             "firstAired", "network", "networkId", "runtime", "genre, "overview", "airsTime", "rating" , "siteRating", "siteRatingCount" }
    Log.Info("[ ] IMDbid: {}"                 .format(SaveDict(        Dict(json[lang], 'imdbId' or IMDbid),                              TheTVDB_dict, 'IMDbid'                 )))
    Log.Info("[ ] zap2itId: {}"               .format(SaveDict(        Dict(json[lang], 'zap2it_id' ),                                    TheTVDB_dict, 'zap2itId'               )))
    Log.Info("[ ] content_rating: {}"         .format(SaveDict(        Dict(json[lang], 'rating'    ),                                    TheTVDB_dict, 'content_rating'         )))
    Log.Info("[ ] originally_available_at: {}".format(SaveDict(        Dict(json[lang], 'firstAired'),                                    TheTVDB_dict, 'originally_available_at')))
    Log.Info("[ ] studio: {}"                 .format(SaveDict(        Dict(json[lang], 'network'   ),                                    TheTVDB_dict, 'studio'                 )))
    Log.Info("[ ] rating: {}"                 .format(SaveDict(        Dict(json[lang], 'siteRating'),                                    TheTVDB_dict, 'rating'                 )))
    Log.Info("[ ] status: {}"                 .format(SaveDict(        Dict(json[lang], 'status'    ),                                    TheTVDB_dict, 'status'                 )))
    Log.Info("[ ] genres: {}"                 .format(SaveDict( sorted(Dict(json[lang], 'genre')),                                        TheTVDB_dict, 'genres'                 )))
    if Dict(json[lang], 'runtime') and Dict(json[lang], 'runtime').isdigit():
      Log.Info('[ ] duration: {}'             .format(SaveDict(     int(Dict(json[lang], 'runtime'))*60*1000, TheTVDB_dict, 'duration'               )))  #in ms in plex
    if Dict(json[lang], 'banner'):
      SaveDict((os.path.join('TheTVDB', 'banner', Dict(json[lang], 'banner')), 1, None), TheTVDB_dict, 'banners', TVDB_IMG_ROOT+Dict(json[lang], 'banner'))
      Log.Info('[ ] banner: {}'               .format(Dict(TheTVDB_dict, 'banners')))
    
    ### TVDB Series Actors JSON ###
    Log.Info("--- actors ---".ljust(157, '-'))
    actor_json = Dict(common.LoadFile(filename='actors_{}.json'.format(lang), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_ACTORS_URL.format(id=TVDBid), cache=CACHE_1DAY, headers={'Accept-Language': lang}), 'data')
    if actor_json:               #JSON format: 'data': [{"seriesId", "name", "image", "lastUpdated", "imageAuthor", "role", "sortOrder", "id", "imageAdded", },...]
      for role in actor_json or []:
        try:
          role_dict = {'role': Dict(role, 'role'), 'name': Dict(role, 'name'), 'photo': TVDB_IMG_ROOT + role['image'] if Dict(role, 'image') else ''}
          SaveDict([role_dict], TheTVDB_dict, 'roles')
          Log.Info("[ ] role: {:<50}, name: {:<20}, photo: {}".format(role_dict['role'], role_dict['name'], role_dict['photo']))
        except Exception as e:  Log.Info(" role: {}, error: '{}'".format(str(role), str(e)))
      #common.DisplayDict(actor_json, ['role', 'name', 'image'])
      
    ### Load pages of episodes ###
    Log.Info("--- episodes ---".ljust(157, '-'))
    episodes_json, sorted_episodes_json, next_page = [], {}, 1
    while next_page not in (None, '', 'null'):
      episodes_json_page = common.LoadFile(filename='episodes_page{}_{}.json'.format(next_page, lang), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_EPISODE_PAGE_URL.format(id=TVDBid, page=next_page), cache=CACHE_1DAY, headers={'Accept-Language': lang})
      next_page          = Dict(episodes_json_page, 'links', 'next')
      episodes_json.extend(Dict(episodes_json_page, 'data'))
    for episode_json in episodes_json: sorted_episodes_json['s{:02d}e{:03d}'.format(Dict(episode_json, 'airedSeason'), Dict(episode_json, 'airedEpisodeNumber'))] = episode_json
    
    ### Build list_abs_eps for tvdb 3/4/5 ###
    list_abs_eps, list_sp_eps={}, []
    if metadata_source in ('tvdb3', 'tvdb4'):
      for s in media.seasons:
        for e in media.seasons[s].episodes:
           if s=='0':  list_sp_eps.append(e)
           else:       list_abs_eps[e]=s 
      Log.Info('Present abs eps: {}'.format(list_abs_eps))
    
    ### episode loop ###
    tvdb_special_missing, summary_missing_special, summary_missing, summary_present, episode_missing, episode_missing_season, episode_missing_season_all, abs_number, ep_count = [], [], [], [], [], [], True, 0, 0
    for key in sorted(sorted_episodes_json):
      
      # Episode and Absolute number calculation engine, episode translation
      episode_json = sorted_episodes_json[key]
      episode      = str(Dict(episode_json, 'airedEpisodeNumber'))
      season       = str(Dict(episode_json, 'airedSeason'       ))
      numbering    = "s{}e{}".format(season, episode)
      
      # Replace all the individual episodes reported as missing with a single season 'sX' entry
      if episode=="1":
        if not episode_missing_season_all:  episode_missing.extend(episode_missing_season)
        elif episode_missing_season:
          first_entry, last_entry = episode_missing_season[0], episode_missing_season[-1]
          fm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', first_entry).groupdict()
          lm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', last_entry ).groupdict()
          episode_missing.append("s{}e{}-{}".format(fm['s'], fm['e'], lm['e']) if fm['abs'] is None else "{}-{} (s{}e{}-{})".format(fm['abs'], lm['abs'], fm['s'], fm['e'], lm['e']))
        episode_missing_season, episode_missing_season_all = [], True

      # Get the max season number from TVDB API
      if int(season) > max_season:  max_season = int(season)
      
      ### ep translation [Thetvdb absolute numbering followed, including in specials to stay accurate with scudlee's mapping]
      anidbid=""
      abs_number = Dict(episode_json, 'absoluteNumber', default=0 if season=='0' else abs_number+1)
      if anidb_numbering:
        if Dict(mappingList, 'defaulttvdbseason_a'):  season, episode          = '1', str(abs_number)
        else:                                         season, episode, anidbid = AnimeLists.anidb_ep(mappingList, season, episode)
      elif metadata_source in ('tvdb3', 'tvdb4'):  
        if str(abs_number) in list_abs_eps:  #if abs id exists on disk, leave specials with no translation
          for s in media.seasons:
            if str(abs_number) in media.seasons[s].episodes:
              season, episode = s, str(abs_number)
              break
          else:  continue
      elif metadata_source=='tvdb5':  
        episode = str(abs_number)
      
      # Record absolute number mapping for AniDB metadata pull
      if metadata_source=='tvdb3':  SaveDict((str(Dict(episode_json, 'airedSeason')), str(Dict(episode_json, 'airedEpisodeNumber'))), mappingList, 'absolute_map', str(abs_number))

      ### Missing summaries logs ###
      if Dict(episode_json, 'overview'):  summary_present.append(numbering)
      elif season!='0':                   summary_missing.append(numbering)
      else:                       summary_missing_special.append(numbering)
      
      ### Check for Missing Episodes ###
      is_missing = False
      if not(str(Dict(episode_json, 'airedSeason'))=='0' and str(Dict(episode_json, 'airedEpisodeNumber')) in list_sp_eps) and \
         not(metadata_source in ('tvdb3', 'tvdb4') and str(abs_number) in list_abs_eps) and \
         not(not movie and season in media.seasons and episode in media.seasons[season].episodes):
        is_missing = True
        Log.Info('[ ] {:>7} s{:0>2}e{:0>3} anidbid: {:>7} air_date: {}'.format(numbering, season, episode, anidbid, Dict(episode_json, 'firstAired')))
        air_date = Dict(episode_json, 'firstAired')
        air_date = int(air_date.replace('-','')) if air_date.replace('-','').isdigit() and int(air_date.replace('-','')) > 10000000 else 99999999
        if int(time.strftime("%Y%m%d")) <= air_date+1:  pass #Log.Info("TVDB - Episode '{}' missing but not aired/missing '{}'".format(numbering, air_date))
        elif season=='0':                               tvdb_special_missing.append(episode)
        elif metadata_source!='tvdb6':                  episode_missing_season.append( str(abs_number)+" ("+numbering+")" if metadata_source in ('tvdb3', 'tvdb4') else numbering)
        
      ### File present on disk
      if not is_missing or metadata_source in ["tvdb", "tvdb6"]:  # Only pull all if anidb3(tvdb)/anidb4(tvdb6) usage for tvdb ep/season adjustments
        episode_missing_season_all = False
        if not is_missing:       Log.Info('[X] {:>7} s{:0>2}e{:0>3} anidbid: {:>7} air_date: {} abs_number: {}, title: {}'.format(numbering, season, episode, anidbid, Dict(episode_json, 'firstAired'), abs_number, Dict(episode_json, 'episodeName')))
        if not anidb_numbering:  SaveDict( abs_number, TheTVDB_dict, 'seasons', season, 'episodes', episode, 'absolute_index')
        SaveDict( Dict(json[lang]  , 'rating'    ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'content_rating'         )
        SaveDict( Dict(TheTVDB_dict, 'duration'  ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'duration'               )
        SaveDict( Dict(episode_json, 'firstAired'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at')
        
        # Title from serie page
        rank, title = len(language_episodes)+1, ''
        if Dict(episode_json, 'episodeName'):
          rank  = language_episodes.index(lang) if lang in language_episodes else len(language_episodes)
          title = Dict(episode_json, 'episodeName')
          Log.Info(" - [1] title:   [{}] {}".format(language_episodes[rank], title))
        
        #Summary from serie page
        if Dict(episode_json, 'overview').strip(" \n\r"):
          SaveDict( Dict(episode_json, 'overview').strip(" \n\r"), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary' )
          Log.Info(' - [1] summary: [{}] {}'.format(lang, Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary' )))
                
        ### Ep advance information ###
        ep_count += 1
        lang2 = 'en' if len(language_episodes)<=1 else language_episodes[1]
        episode_details_json = Dict(common.LoadFile(filename='episode_{}_{}.json'.format(Dict(episode_json, 'id'), lang2), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_EPISODE_URL.format(id=str(Dict(episode_json, 'id'))), cache=CACHE_1DAY, headers={'Accept-Language': lang2}), 'data')
        if episode_details_json:
          
          # Std ep info loaded for Library language ten details for 1st language, loading other languages if needed
          if lang2 in language_episodes and language_episodes.index(lang2)<rank and Dict(episode_details_json, 'language', 'episodeName')==lang2 and Dict(episode_details_json, 'episodeName'):
            rank  = language_episodes.index(lang2)
            title = Dict(episode_details_json, 'episodeName')
            Log.Info(" - [2] title:   [{}] {}".format(language_episodes[rank], title))
            
          #Summary
          if not Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary') and Dict(episode_details_json, 'overview'):
            SaveDict( Dict(episode_details_json, 'overview').strip(" \n\r"), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary')
            Log.Info(' - [2] summary: [{}] {}'.format(lang2, Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary' )))
        
          SaveDict( Dict(episode_details_json, 'writers'            ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'writers'    )
          SaveDict( Dict(episode_details_json, 'directors'          ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'directors'  )
          SaveDict( Dict(episode_details_json, 'siteRating'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating'     )
          #SaveDict( Dict(episode_details_json, 'guestStars'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'guest_stars') 
          
          # Episode screenshot/Thumbnail
          if Dict(episode_details_json, 'filename'):
            SaveDict((str("TheTVDB/episodes/"+ os.path.basename(Dict(episode_details_json, 'filename'))), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', str(TVDB_IMG_ROOT+Dict(episode_details_json, 'filename')))
            Log.Info(' - [ ] thumb: {}'.format(TVDB_IMG_ROOT+Dict(episode_details_json, 'filename') if Dict(episode_details_json, 'filename') else ''))
        
        #Ep title fallback (first lang title come from ep list, second from ep details)
        for lang_rank, language in enumerate(language_episodes[2:rank-1] if len(language_episodes)>1 and rank>=2 and not title else []):
          if not language:  continue
          episode_details_json = Dict(common.LoadFile(filename='episode_{}_{}.json'.format(Dict(episode_json, 'id'), language), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_EPISODE_URL.format(id=str(Dict(episode_json, 'id'))), cache=CACHE_1DAY, headers={'Accept-Language': lang}), 'data', default={})
          if Dict(episode_details_json, 'episodeName') :  
            title = Dict(episode_details_json, 'episodeName')
            rank  = lang_rank
            Log.Info(" - [3] title:   [{}] {}".format(language_episodes[rank], title))
          if not Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary') and Dict(episode_details_json, 'overview'):
            SaveDict( Dict(episode_details_json, 'overview')[:160].strip(" \n\r"), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary')
            Log.Info(' - [3] summary: [{}] {}'.format(language_episodes[lang_rank], Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary' )))
          if title and Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary'):  break
        SaveDict( title, TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title'        )
        SaveDict( rank , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')      
    
    # (last season) Replace all the individual episodes reported as missing with a single season 'sX' entry
    if not episode_missing_season_all:  episode_missing.extend(episode_missing_season)
    elif episode_missing_season:
      first_entry, last_entry = episode_missing_season[0], episode_missing_season[-1]
      fm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', first_entry).groupdict()
      lm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', last_entry ).groupdict()
      episode_missing.append("s{}e{}-{}".format(fm['s'], fm['e'], lm['e']) if fm['abs'] is None else "{}-{} (s{}e{}-{})".format(fm['abs'], lm['abs'], fm['s'], fm['e'], lm['e']))

    # Set the min/max season to ints & update max value to the next min-1 to handle multi tvdb season anidb entries
    map_min_values = [int(Dict(mappingList, 'season_map')[x]['min']) for x in Dict(mappingList, 'season_map', default={}) for y in Dict(mappingList, 'season_map')[x] if y=='min']
    for entry in Dict(mappingList, 'season_map', default={}):
      entry_min, entry_max = int(mappingList['season_map'][entry]['min']), int(mappingList['season_map'][entry]['max'])
      while entry_min!=0 and entry_max+1 not in map_min_values and entry_max < max_season:  entry_max += 1
      mappingList['season_map'][entry] = {'min': entry_min, 'max': entry_max}
    SaveDict(max_season, mappingList, 'season_map', 'max_season')

    ### Logging ###
    if not movie:
      if summary_missing:          error_log['Missing Episode Summaries'].append("TVDBid: %s | Title: '%s' | Missing Episode Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing        )))
      if summary_missing_special:  error_log['Missing Special Summaries'].append("TVDBid: %s | Title: '%s' | Missing Special Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing_special)))
    if metadata_source.startswith("tvdb") or metadata_source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))>1:
      if episode_missing:          error_log['Missing Episodes'         ].append("TVDBid: %s | Title: '%s' | Missing Episodes: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(episode_missing        )))
      if tvdb_special_missing:     error_log['Missing Specials'         ].append("TVDBid: %s | Title: '%s' | Missing Specials: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(tvdb_special_missing   )))
      #Log.Debug("Episodes without Summary: " + str(sorted(summary_missing, key=common.natural_sort_key)))
      
    ### Picture types JSON download ###
    Log.Info("--- images ---".ljust(157, '-'))
    language_posters = [language.strip() for language in Prefs['PosterLanguagePriority'].split(',')]
    priority_posters = [  source.strip() for source   in Prefs['posters'               ].split(',')]
    Log.Info('language_posters: {}'.format(language_posters))
    for language in language_posters:
      try:     bannerTypes = Dict(common.LoadFile(filename='images_{}.json'.format(language), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_SERIES_IMG_INFO_URL.format(id=TVDBid), cache=0, headers={'Accept-Language': language}), 'data', default={})
      except:  Log.Info("Invalid image JSON from url: " + TVDB_SERIES_IMG_INFO_URL % TVDBid)
      else:             #JSON format = {"fanart", "poster", "season", "seasonwide", "series"}
        metanames         = {'fanart': "art", 'poster': "posters", 'series': "banners", 'season': "seasons", 'seasonwide': 'seasonwide'}#
        count_valid       = {key: 0 for key in metanames}
        anidb_offset      = sorted((Dict(mappingList, 'poster_id_array', TVDBid) or {}).keys()).index(AniDBid) if AniDBid and AniDBid in Dict(mappingList, 'poster_id_array', TVDBid) else 0  
        language_priority = [item.strip() for item in Prefs['EpisodeLanguagePriority'].split(',')]
        Log.Info("bannerTypes: {}, anidb_offset: {}, AniDBid: {}, anidb_array: {}".format(bannerTypes, anidb_offset, AniDBid, str((Dict(mappingList, 'poster_id_array', TVDBid) or {}).keys())))
        
        #Loop per banner type ("fanart", "poster", "season", "series") skip 'seasonwide' - Load bannerType images list JSON
        for bannerType in bannerTypes or []:
          if bannerTypes[bannerType]==0 or bannerType in ('seasonwide', 'series') or movie and not bannerType in ('fanart', 'poster'):  continue  #Loop if no images
          #if anidb_numbering and Dict(mappingList, 'defaulttvdbseason') != '1' and bannerType=='poster':  continue  #skip if anidb numbered serie mapping to season 0 or 2+
          
          Log.Info(("--- images.%s ---" % bannerType).ljust(157, '-'))
          try:     images = Dict( common.LoadFile(filename='images_{}_{}.json'.format(bannerType, language), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_SERIES_IMG_QUERY_URL.format(id=TVDBid, type=bannerType), cache=CACHE_1DAY, headers={'Accept-Language': language}), 'data', default={})
          except:  images = {};  Log.Info("Bad image type query data for TVDB id: %s (bannerType: %s)" % (TVDBid, bannerType)) 
          else:
            images = sorted(images, key = lambda x: Dict(x, "ratingsInfo", "average", default=0), reverse=True)
            for image in images:  #JSON format = {"data": [{"id", "keyType", "subKey"(season/graphical/text), "fileName", "resolution", "ratingsInfo": {"average", "count"}, "thumbnail"}]}
              
              #rank
              rank = 1 if bannerType=='poster' and anidb_offset == divmod(count_valid['poster'], Dict(bannerTypes, 'poster', default=0))[1] else count_valid[bannerType]+2
              if language  in language_posters:  rank = (rank//30)*30*language_posters.index(language)+rank%30
              if 'TheTVDB' in priority_posters:  rank = rank+ 6*priority_posters.index('TheTVDB')
              rank = rank + language_posters.index(language)*20
              if AniDB_movie: rank = rank+Dict(bannerTypes, 'poster', default=0) if rank+Dict(bannerTypes, 'poster', default=0)<99 else 99
              
              ### Adding picture ###
              thumbnail = TVDB_IMG_ROOT + image['thumbnail'] if Dict(image, 'thumbnail') else None
              Log.Info("[!] bannerType: {:>7} subKey: {:>9} rank: {:>3} filename: {} thumbnail: {} resolution: {} average: {} count: {}".format( metanames[bannerType], Dict(image, 'subKey'), rank, TVDB_IMG_ROOT + Dict(image, 'fileName'), TVDB_IMG_ROOT + Dict(image, 'thumbnail'), Dict(image, 'resolution'), Dict(image, 'ratingsInfo','average'), Dict(image, 'ratingsInfo', 'average', 'count') ))
              if bannerType=='season':  #tvdb season posters or anidb specials and defaulttvdb season  ## season 0 et empty+ season ==defaulttvdbseason(a=1)
                if not anidb_numbering:  SaveDict(('TheTVDB/'+image['fileName'], rank, thumbnail), TheTVDB_dict, 'seasons', str(image['subKey']), 'posters', TVDB_IMG_ROOT + image['fileName'])
                else:
                  if str(image['subKey']) in [Dict(mappingList, 'defaulttvdbseason')]:
                    SaveDict(('TheTVDB/'+image['fileName'], rank, thumbnail), TheTVDB_dict, 'posters', TVDB_IMG_ROOT + image['fileName'])
                  if str(image['subKey']) in ['0', Dict(mappingList, 'defaulttvdbseason')]:
                    SaveDict(('TheTVDB/'+image['fileName'], 1 if rank==3 else 3 if rank==1 else rank, thumbnail), TheTVDB_dict, 'seasons', '0' if str(image['subKey'])=='0' else '1', 'posters', TVDB_IMG_ROOT + image['fileName'])  #if anidb_numbering else str(image['subKey'])
              else:
                new_rank = rank + 10 if anidb_numbering and Dict(mappingList, 'defaulttvdbseason') != '1' else rank
                SaveDict(('TheTVDB/'+image['fileName'], new_rank, thumbnail), TheTVDB_dict, metanames[bannerType], TVDB_IMG_ROOT + image['fileName'])   #use art + posters tvdb
              #if bannerType == 'season':  
              #  if anidb_numbering and Dict(mappingList, 'defaulttvdbseason')==str(image['subKey']):
              #    SaveDict(('TheTVDB/'+image['fileName'], 1 if rank==3 else 3 if rank==1 else rank, thumbnail), TheTVDB_dict, 'seasons', '0' if str(image['subKey'])=='0' else '1', 'posters', TVDB_IMG_ROOT + image['fileName'])
              #  elif not anidb_numbering:  
              #    season = str(int(image['subKey'])+(0 if Dict(mappingList, 'defaulttvdbseason')=="0" or not Dict(mappingList, 'defaulttvdbseason').isdigit() else int(Dict(mappingList, 'defaulttvdbseason'))-1))
              #    SaveDict(   ('TheTVDB/'+image['fileName'], rank, thumbnail), TheTVDB_dict, 'seasons', season, 'posters', TVDB_IMG_ROOT + image['fileName'])
              #if bannerType != 'season':
              #  SaveDict(('TheTVDB/'+image['fileName'], rank, thumbnail), TheTVDB_dict, metanames[bannerType],        TVDB_IMG_ROOT + image['fileName'])
              count_valid[bannerType] = count_valid[bannerType] + 1  #Otherwise with += SyntaxError: Line 142: Augmented assignment of object items and slices is not allowed
              
        #Log.Info("Posters : {}/{}, Season posters: {}/{}, Art: {}/{}".format(count_valid['poster'], Dict(bannerTypes, 'poster'), count_valid['season'], Dict(bannerTypes, 'season') or 0, count_valid['fanart'], Dict(bannerTypes, 'fanart')))
        if not Dict(bannerTypes, 'poster'):  error_log['TVDB posters missing'       ].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
        if not Dict(bannerTypes, 'season'):  error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
          
    Log.Info("--- final summary info ---".ljust(157, '-'))
    Log.Info("url: '{}', IMDbid: {}, Present episodes: {}, Missing: {}".format(TVDB_SERIES.format(id=TVDBid), IMDbid, ep_count, sorted(episode_missing, key=common.natural_sort_key)))
    
  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("absolute_map: {}".format(DictString(Dict(mappingList, 'absolute_map', default={}), 0)))
  Log.Info("season_map: {}".format(DictString(Dict(mappingList, 'season_map', default={}), 0)))
  Log.Info("TheTVDB_dict: {}".format(DictString(TheTVDB_dict, 4)))
  return TheTVDB_dict, IMDbid
  
def Search(results,  media, lang, manual, movie):  #if maxi<50:  maxi = tvdb.Search_TVDB(results, media, lang, manual, movie)
  '''search for TVDB id series
  '''
  Log.Info("=== TheTVDB.Search() ===".ljust(157, '='))
  #series_data = JSON.ObjectFromString(GetResultFromNetwork(TVDB_SEARCH_URL % mediaShowYear, additionalHeaders={'Accept-Language': lang}))['data'][0]
  orig_title = ( media.title if movie else media.show )
  maxi = 0
  try:                    TVDBsearchXml = XML.ElementFromURL( TVDB_SERIE_SEARCH + orig_title.replace(" ", "%20"), headers=common.HEADERS_CORE, cacheTime=CACHE_1HOUR * 24)
  except Exception as e:  Log.Error("TVDB Loading search XML failed, Exception: '%s'" % e)
  else:
    for serie in TVDBsearchXml.xpath('Series'):
      a, b = orig_title, GetXml(serie, 'SeriesName').encode('utf-8') #a, b  = cleansedTitle, cleanse_title (serie.xpath('SeriesName')[0].text)
      if b=='** 403: Series Not Permitted **': continue
      score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
      if maxi<score:  maxi = score
      Log.Info("TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, GetXml(serie, 'seriesid'), GetXml(serie, 'SeriesName')))
      results.Append(MetadataSearchResult(id="%s-%s" % ("tvdb", GetXml(serie, 'seriesid')), name="%s [%s-%s]" % (GetXml(serie, 'SeriesName'), "tvdb", GetXml(serie, 'seriesid')), year=None, lang=lang, score=score) )
  return maxi
