### TheTVDB.com API v4 ###
# https://thetvdb.github.io/v4-api

### Imports ###
# Python Modules #
import os
import time
import re
from urllib import quote
# Plex Modules #
#from collections import defaultdict
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions
import AnimeLists

### Variables ###
TVDB_API_KEY               = 'TODO' # TODO: Need v4 key
TVDB_API_PIN               = 'TODO'
TVDB_IMG_ROOT              = 'https://thetvdb.plexapp.com/banners/' 
TVDB_BASE_URL              = 'https://api4.thetvdb.com/v4'
TVDB_LOGIN_URL             = TVDB_BASE_URL + '/login'
TVDB_SERIES_URL            = TVDB_BASE_URL + '/series/{id}'
TVDB_SERIES_EXTENDED_URL   = TVDB_SERIES_URL + '/extended?meta=episodes'
TVDB_SERIES_TRANSLATION_URL= TVDB_SERIES_URL + '/translations/{lang}'
TVDB_EPISODE_URL           = TVDB_BASE_URL + '/episodes/{id}'
TVDB_EPISODE_EXTENDED_URL  = TVDB_EPISODE_URL + '/extended'
TVDB_EPISODE_TRANSLATION_URL= TVDB_EPISODE_URL + '/translations/{lang}'
TVDB_MOVIE_URL             = TVDB_BASE_URL + '/movies/{id}'
TVDB_MOVIE_EXTENDED_URL    = TVDB_MOVIE_URL + '/extended'
TVDB_MOVIE_TRANSLATION_URL = TVDB_MOVIE_URL + '/translations/{lang}'
TVDB_SEARCH_URL            = TVDB_BASE_URL + '/search?type=series&query=%s'

TVDB_LANGUAGES_CODE        = { 'cs': 'ces', 'da': 'dan', 'de': 'deu', 'el': 'ell', 'en': 'eng', 'es': 'spa', 'fi': 'fin', 'fr': 'fra', 'he': 'heb', 
                               'hr': 'hrv', 'hu': 'hun', 'it': 'ita', 'ja': 'jpn', 'ko': 'kor', 'nl': 'nld', 'no': 'nor', 'pl': 'pol', 'pt': 'por',
                               'ru': 'rus', 'sv': 'swe', 'tr': 'tur', 'zh': 'zho', 'sl': 'slv'}

TVDB_HEADERS   = {}
TVDB_AUTH_TIME = None
netLocked      = {}

### Functions ###
def Login():
  global TVDB_HEADERS
  global TVDB_AUTH_TIME

  # If no auth or auth is >12hrs old, authenticate from scratch
  if 'Authorization' not in TVDB_HEADERS or (TVDB_AUTH_TIME and (time.time()-TVDB_AUTH_TIME) > CACHE_1DAY/2):
    try:
      TVDB_HEADERS['Authorization'] = 'Bearer ' + JSON.ObjectFromString(HTTP.Request(TVDB_LOGIN_URL, data=JSON.StringFromObject( {'apikey':TVDB_API_KEY,'pin':TVDB_API_PIN} ), headers=common.COMMON_HEADERS, cacheTime=0).content)['data']['token']
      TVDB_AUTH_TIME = time.time()
    except Exception as e: Log.Root('TheTVDBv4.Login() - Authorization Error: {}'.format(e))
    else:                  Log.Root('TheTVDBv4.Login() - URL {}'.format(TVDB_LOGIN_URL))

def LoadFileTVDB(id='', filename='', url=''):
  """ Wrapper around "common.LoadFile()" to remove the need to consistently define arguments 'relativeDirectory'/'cache'/'headers'
  """
  while 'LoadFileTVDB' in netLocked and netLocked['LoadFileTVDB'][0]:
    Log.Root("TheTVDBv4.LoadFileTVDB() - Waiting for lock: 'LoadFileTVDB'"); time.sleep(1)
  netLocked['LoadFileTVDB'] = (True, int(time.time())) #Log.Root("Lock acquired: 'LoadFile'")
  Login()
  data = common.LoadFile(filename=filename, relativeDirectory=os.path.join('TheTVDBv4', 'json', id), url=url, headers=TVDB_HEADERS)
  netLocked['LoadFileTVDB'] = (False, 0)  #Log.Root("Lock released: 'LoadFile'")
  return data

def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList):
  ''' TVDB - Load serie JSON
  '''
  Log.Info("=== TheTVDBv4.GetMetadata() ===".ljust(157, '='))
  TheTVDB_dict      = {}
  max_season        = 0
  anidb_numbering   = metadata_source=="anidb" and (movie or max(map(int, media.seasons.keys()))<=1)
  anidb_prefered    = anidb_numbering and Dict(mappingList, 'defaulttvdbseason') != '1'
  lang = TVDB_LANGUAGES_CODE[lang]
  language_series   = [TVDB_LANGUAGES_CODE[language.strip()] for language in Prefs['SerieLanguagePriority'  ].split(',') if language.strip() not in ('x-jat', 'zh-Hans', 'zh-Hant', 'zh-x-yue', 'zh-x-cmn', 'zh-x-nan', 'main')]
  language_episodes = [TVDB_LANGUAGES_CODE[language.strip()] for language in Prefs['EpisodeLanguagePriority'].split(',') if language.strip() not in ('x-jat', 'zh-Hans', 'zh-Hant', 'zh-x-yue', 'zh-x-cmn', 'zh-x-nan', 'main')]
  Log.Info("TVDBid: '{}', IMDbid: '{}', language_series : {}, language_episodes: {}".format(TVDBid, IMDbid, language_series , language_episodes))

  if not TVDBid.isdigit(): Log.Info('TVDBid non-digit'); return TheTVDB_dict, IMDbid

  ### TVDB Series JSON ###
  Log.Info("--- series ---".ljust(157, '-'))
  json = {}
  if lang not in language_series:    language_series.insert(0, lang) #for summary in lang (library setting) language
  if 'eng' not in language_series:   language_series.insert(0, 'eng') #for failover title  if lang not in language_episodes:  language_episodes.append(lang) #for summary in lang (library setting) language
  if lang not in language_episodes:  language_episodes.append(lang) #for summary in lang (library setting) language
  if 'eng' not in language_episodes: language_episodes.append('eng') #for failover title
  series_json = Dict(LoadFileTVDB(id=TVDBid, filename='series.json', url=TVDB_SERIES_EXTENDED_URL.format(id=TVDBid)), 'data')
  for language in language_series:
    lang_json = Dict(LoadFileTVDB(id=TVDBid, filename='series_{}.json'.format(language), url=TVDB_SERIES_TRANSLATION_URL.format(id=TVDBid, lang=language)), 'data')
    if Dict(lang_json, 'name'):
      SaveDict( language_series.index(language) if not anidb_prefered else len(language_series), TheTVDB_dict, 'language_rank')
      Log.Info("[ ] language_rank: {}"          .format(Dict(TheTVDB_dict, 'language_rank')))
      Log.Info("[ ] title: {}"                  .format(SaveDict( Dict(lang_json, 'name'), TheTVDB_dict, 'title')))
    if lang_json and (Dict(lang_json, 'overview') or Dict(TheTVDB_dict, 'language_rank')):  break  #only need json in lang for summary, in 'eng' for most things
  if not anidb_prefered: SaveDict( Dict(json, lang, 'overview').strip(" \n\r") or Dict(json, 'eng', 'overview').strip(" \n\r"), TheTVDB_dict, 'summary')  
  if series_json:
    #JSON format: { "id","name", "slug", "image", "nameTranslations", "overviewTranslations", "aliases", "firstAired", "lastAired", "nextAired", "score", "status",
    #               "originalCountry", "originalLanguage", "defaultSeasonType", "isOrderRandomized", "lastUpdated, "averageRuntime", "episodes", "overview" , "year", "artworks","companies",
    #               "originalNetwork", "latestNetwork", "genres", "trailers", "lists", "remoteIds", "characters", "airsDays", "airsTime", "seasons", "tags", "contentRatings", "seasonTypes"}
    imdbid    = [Dict(x, 'id') for x in Dict(series_json, 'remoteIds') if Dict(x, 'sourceName') == 'IMDB']
    imdbid    = imdbid[0] if len(imdbid) > 0 else None
    zap2it_id = [Dict(x, 'id') for x in Dict(series_json, 'remoteIds') if Dict(x, 'sourceName') == 'TMS (Zap2It)']
    zap2it_id = zap2it_id[0] if len(zap2it_id) > 0 else None
    rating    = [Dict(x, 'name') for x in Dict(series_json, 'contentRatings') if Dict(x, 'country') == 'usa']
    rating    = rating[0] if len(rating) > 0 else None
    genres    = sorted([Dict(x, 'name') for x in Dict(series_json, 'genres')])
    Log.Info("[ ] IMDbid: {}"                 .format(SaveDict(imdbid or IMDbid,                             TheTVDB_dict, 'IMDbid'                 )))
    Log.Info("[ ] zap2itId: {}"               .format(SaveDict(zap2it_id,                                    TheTVDB_dict, 'zap2itId'               )))
    Log.Info("[ ] content_rating: {}"         .format(SaveDict(rating,                                       TheTVDB_dict, 'content_rating'         )))
    Log.Info("[ ] originally_available_at: {}".format(SaveDict(Dict(series_json, 'firstAired'),              TheTVDB_dict, 'originally_available_at')))
    Log.Info("[ ] studio: {}"                 .format(SaveDict(Dict(series_json, 'originalNetwork', 'name'), TheTVDB_dict, 'studio'                 )))
    Log.Info("[ ] rating: {}"                 .format(SaveDict(Dict(series_json, 'siteRating'),              TheTVDB_dict, 'rating'                 ))) # TODO: where to get this from?
    Log.Info("[ ] status: {}"                 .format(SaveDict(Dict(series_json, 'status', 'name'),          TheTVDB_dict, 'status'                 )))
    Log.Info("[ ] genres: {}"                 .format(SaveDict(genres,                                       TheTVDB_dict, 'genres'                 )))
    Log.Info('[ ] duration: {}'               .format(SaveDict(Dict(series_json, 'averageRuntime')*60*1000,  TheTVDB_dict, 'duration'               ))) # in ms in plex
    
    banner = [Dict(x, 'image') for x in Dict(series_json, 'artworks') if Dict(x, 'type') == 1 and not Dict(x, 'language') or Dict(x, 'language') == lang]
    banner = banner[0] if len(banner) > 0 else None
    fanart = [Dict(x, 'image') for x in Dict(series_json, 'artworks') if Dict(x, 'type') == 3 and not Dict(x, 'language') or Dict(x, 'language') == lang]
    fanart = fanart[0] if len(fanart) > 0 else None
    series_images = {  # Pull the primary images used for the series entry
      'poster':     Dict(series_json, 'image'),
      'banner':     banner,
      'fanart':     fanart,
      'seasonwide': None,
      'series':     None}

    ### TVDB Series Actors JSON ###
    Log.Info("--- actors ---".ljust(157, '-'))
    characters_json = Dict(series_json, 'characters', default=[])
    if characters_json: #JSON format: {"id", "name", "peopleId", "seriesId", "image", "isFeatured", "url", "peopleType", "personName", "personImgURL"},...]
      for role in characters_json:
        try:
          role_dict = {'role': Dict(role, 'name'), 'name': Dict(role, 'personName'), 'photo': Dict(role, 'image')}
          SaveDict([role_dict], TheTVDB_dict, 'roles')
          Log.Info("[ ] role: {:<50}, name: {:<20}, photo: {}".format(role_dict['role'], role_dict['name'], role_dict['photo']))
        except Exception as e: Log.Info(" role: {}, error: '{}'".format(str(role), str(e)))
      
    ### Load pages of episodes ###
    Log.Info("--- episodes ---".ljust(157, '-'))
    sorted_episodes_json = {}
    episodes_json = Dict(series_json, 'episodes')
    for episode_json in episodes_json:
      key = 's{:02d}e{:03d}'.format(Dict(episode_json, 'seasonNumber'), Dict(episode_json, 'number'))
      if Dict(episode_json, 'linkedMovie'):
        sorted_episodes_json[key] = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}_movie_{}.json'.format(Dict(episode_json, 'id'), Dict(episode_json, 'linkedMovie')), url=TVDB_MOVIE_EXTENDED_URL.format(id=str(Dict(episode_json, 'linkedMovie')))), 'data')
        sorted_episodes_json[key]['isMovie'] = True
        sorted_episodes_json[key]['aired'] = Dict(episode_json, 'aired')
        sorted_episodes_json[key]['number'] = Dict(episode_json, 'number')
        sorted_episodes_json[key]['seasonNumber'] = Dict(episode_json, 'seasonNumber')
        sorted_episodes_json[key]['absoluteNumber'] = Dict(episode_json, 'absoluteNumber')
        sorted_episodes_json[key]['linkedEpisode'] = Dict(episode_json, 'id')
      else:
        sorted_episodes_json[key] = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}.json'.format(Dict(episode_json, 'id')), url=TVDB_EPISODE_EXTENDED_URL.format(id=str(Dict(episode_json, 'id')))), 'data')
    
    ### Build list_abs_eps for tvdb 3/4/5 ###
    list_abs_eps, list_sp_eps={}, []
    if metadata_source in ('tvdb3', 'tvdb4'):
      for s in media.seasons:
        for e in media.seasons[s].episodes:
           if s=='0': list_sp_eps.append(e)
           else:      list_abs_eps[e]=s 
      Log.Info('Present abs eps: {}'.format(list_abs_eps))
    
    ### episode loop ###
    tvdb_special_missing, summary_missing_special, summary_missing, summary_present, episode_missing, episode_missing_season, episode_missing_season_all, abs_number = [], [], [], [], [], [], True, 0

    # To avoid duplicate mapping we will remember episodes that have been mapped to a different value
    mapped_episodes = []
    for key in sorted(sorted_episodes_json):
      episode_json = sorted_episodes_json[key]
      episode    = str(Dict(episode_json, 'number'      ))
      season     = str(Dict(episode_json, 'seasonNumber'))
      season, episode, anidbid = AnimeLists.anidb_ep(mappingList, season, episode)
      if anidbid != 'xxxxxxx': mapped_episodes.append((season, episode))

    for key in sorted(sorted_episodes_json):
      
      # Episode and Absolute number calculation engine, episode translation
      episode_json = sorted_episodes_json[key]
      episode    = str(Dict(episode_json, 'number'      ))
      season     = str(Dict(episode_json, 'seasonNumber'))
      numbering  = "s{}e{}".format(season, episode)
      
      # Replace all the individual episodes reported as missing with a single season 'sX' entry
      if episode == "1":
        if not episode_missing_season_all: episode_missing.extend(episode_missing_season)
        elif episode_missing_season:
          first_entry, last_entry = episode_missing_season[0], episode_missing_season[-1]
          fm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', first_entry).groupdict()
          lm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', last_entry ).groupdict()
          episode_missing.append("s{}e{}-{}".format(fm['s'], fm['e'], lm['e']) if fm['abs'] is None else "{}-{} (s{}e{}-{})".format(fm['abs'], lm['abs'], fm['s'], fm['e'], lm['e']))
        episode_missing_season, episode_missing_season_all = [], True

      # Get the max season number from TVDB API
      if int(season) > max_season: max_season = int(season)
      
      ### ep translation [Thetvdb absolute numbering followed, including in specials to stay accurate with scudlee's mapping]
      anidbid = ""
      abs_number = Dict(episode_json, 'absoluteNumber', default=0 if season=='0' else abs_number + 1)
      if anidb_numbering:
        if Dict(mappingList, 'defaulttvdbseason_a'): season, episode          = '1', str(abs_number)
        else:                                        season, episode, anidbid = AnimeLists.anidb_ep(mappingList, season, episode)
      elif metadata_source in ('tvdb3', 'tvdb4'):  
        for s in media.seasons:  #if abs id exists on disk, leave specials with no translation
          if str(abs_number) in list_abs_eps and str(abs_number) in media.seasons[s].episodes and s != "0": season, episode = s, str(abs_number); break
      elif metadata_source=='tvdb5':  
        if abs_number: season, episode = '1', str(abs_number)
      
      # Record absolute number mapping for AniDB metadata pull
      if metadata_source=='tvdb3':  SaveDict((str(Dict(episode_json, 'seasonNumber')), str(Dict(episode_json, 'number'))), mappingList, 'absolute_map', str(abs_number))

      ### Missing summaries logs ###
      if Dict(episode_json, 'overview'):  summary_present.append(numbering)
      elif season!='0':                   summary_missing.append(numbering)
      else:                       summary_missing_special.append(numbering)
      
      ### Check for Missing Episodes ###
      is_missing = False
      if (not(str(Dict(episode_json, 'seasonNumber'))=='0' and str(Dict(episode_json, 'number')) in list_sp_eps) and
         not(metadata_source in ('tvdb3', 'tvdb4') and str(abs_number) in list_abs_eps) and
         not(not movie and season in media.seasons and episode in media.seasons[season].episodes)) or \
         (not movie and season in media.seasons and episode in media.seasons[season].episodes and
         anidbid == 'xxxxxxx' and (season, episode) in mapped_episodes):
        is_missing = True
        Log.Info('[ ] {:>7} s{:0>2}e{:0>3} anidbid: {:>7} air_date: {}'.format(numbering, season, episode, anidbid, Dict(episode_json, 'aired')))
        air_date = Dict(episode_json, 'aired')
        air_date = int(air_date.replace('-','')) if air_date.replace('-','').isdigit() and int(air_date.replace('-','')) > 10000000 else 99999999
        if int(time.strftime("%Y%m%d")) <= air_date+1:  pass #Log.Info("TVDB - Episode '{}' missing but not aired/missing '{}'".format(numbering, air_date))
        elif season=='0':                               tvdb_special_missing.append(episode)
        elif metadata_source!='tvdb6':                  episode_missing_season.append( str(abs_number)+" ("+numbering+")" if metadata_source in ('tvdb3', 'tvdb4') else numbering)
        
      ### File present on disk
      if not is_missing or Dict(mappingList, 'possible_anidb3') or metadata_source=="tvdb6":  # Only pull all if anidb3(tvdb)/anidb4(tvdb6) usage for tvdb ep/season adjustments
        episode_missing_season_all = False
        if not is_missing:       Log.Info('[X] {:>7} s{:0>2}e{:0>3} anidbid: {:>7} air_date: {} abs_number: {}, title: {}'.format(numbering, season, episode, anidbid, Dict(episode_json, 'aired'), abs_number, Dict(episode_json, 'name')))
        if not anidb_numbering:  SaveDict( abs_number, TheTVDB_dict, 'seasons', season, 'episodes', episode, 'absolute_index')
        SaveDict( rating,                        TheTVDB_dict, 'seasons', season, 'episodes', episode, 'content_rating'         )
        SaveDict( Dict(episode_json, 'runtime'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'duration'               )
        SaveDict( Dict(episode_json, 'aired'),   TheTVDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at')
                
        ### Ep advance information ###
        for lang_rank, language in enumerate(language_episodes):
          if Dict(episode_json, 'isMovie'):
            episode_details_json = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}_movie_{}_{}.json'.format(Dict(episode_json, 'id'), Dict(episode_json, 'linkedEpisode'), language), url=TVDB_MOVIE_TRANSLATION_URL.format(id=str(Dict(episode_json, 'id')), lang=language)), 'data')
          else:
            episode_details_json = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}_{}.json'.format(Dict(episode_json, 'id'), language), url=TVDB_EPISODE_TRANSLATION_URL.format(id=str(Dict(episode_json, 'id')), lang=language)), 'data')
          if episode_details_json:
            if not Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title') and Dict(episode_details_json, 'name'):
              SaveDict( lang_rank , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')
              SaveDict( Dict(episode_details_json, 'name').strip(" \n\r"), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title')
              Log.Info(" - [{}] title:   [{}] {}".format(lang_rank + 1, language_episodes[lang_rank], Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title')))
            if not Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary') and Dict(episode_details_json, 'overview'):
              SaveDict( Dict(episode_details_json, 'overview').strip(" \n\r"), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary')
              Log.Info(" - [{}] summary:   [{}] {}".format(lang_rank + 1, language_episodes[lang_rank], Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary')))
          if Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title') and Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary'):
            break

        writers   = [Dict(x, 'personName') for x in Dict(episode_json, 'characters') if Dict(x, 'peopleType') == 'Writer']   if Dict(episode_json, 'characters') else []
        directors = [Dict(x, 'personName') for x in Dict(episode_json, 'characters') if Dict(x, 'peopleType') == 'Director'] if Dict(episode_json, 'characters') else []
        SaveDict( writers,                          TheTVDB_dict, 'seasons', season, 'episodes', episode, 'writers'    )
        SaveDict( directors,                        TheTVDB_dict, 'seasons', season, 'episodes', episode, 'directors'  )
        SaveDict( Dict(episode_json, 'siteRating'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating'     ) # TODO: where to get this from?
        
        # Episode screenshot/Thumbnail
        if Dict(episode_json, 'image'):
          imagePath = RelativeImagePath(Dict(episode_json, 'image'))
          SaveDict((os.path.join("TheTVDBv4", "images", "episodes", os.path.basename(imagePath).replace('/', os.sep)), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', TVDB_IMG_ROOT + imagePath)
          Log.Info(' - [ ] thumb: {}'.format(TVDB_IMG_ROOT + imagePath))  
    
    # (last season) Replace all the individual episodes reported as missing with a single season 'sX' entry
    if not episode_missing_season_all: episode_missing.extend(episode_missing_season)
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
    languages = [TVDB_LANGUAGES_CODE[language.strip()] for language in Prefs['PosterLanguagePriority'].split(',')]
    Log.Info('languages: {}'.format(languages))

    metanames   = {3: "art", 2: "posters", 1: "banners", 7: "seasons", 6: 'seasonwide'}
    count_valid = {key: 0 for key in metanames}
        
    for image in sorted(Dict(series_json, 'artworks'), key = lambda x: Dict(x, 'score', default=0), reverse=True):
      if Dict(image, 'language') and Dict(image, 'language') not in languages: continue
      if Dict(image, 'type') not in (1, 2, 3, 7): continue
      if movie and not Dict(image, 'type') in (1, 2, 3): continue

      #JSON format [{"id", "image", "thumbnail", "lanaguage", "type", "score", "width", "height", "seasonId"}, ...]
      imagePath    = RelativeImagePath(Dict(image, 'image'))
      imageURL     = TVDB_IMG_ROOT + imagePath
      thumbnailURL = TVDB_IMG_ROOT + RelativeImagePath(Dict(image, 'thumbnail')) if Dict(image, 'thumbnail') else None
      bannerType   = Dict(image, 'type')
      
      count_valid[bannerType] = count_valid[bannerType] + 1
      orig_lang = [x for x in TVDB_LANGUAGES_CODE if TVDB_LANGUAGES_CODE[x] == lang][0]
      rank = common.poster_rank('TheTVDB', metanames[bannerType], orig_lang, 0 if Dict(image, 'image') == Dict(series_images, bannerType) else count_valid[bannerType])
      imageTuple = (os.path.join('TheTVDBv4', 'images', imagePath.replace('/', os.sep)), rank, thumbnailURL)

      seasonNum = None
      if Dict(image, 'type') == 7:
        #get the season number
        seasonNum = str([Dict(x, 'number') for x in Dict(series_json, 'seasons') if Dict(x, 'id') == Dict(image, 'seasonId')][0])
        Log.Info("[!] bannerType: {:>7} seasonNum: {:>3} rank: {:>3} filename: {} thumbnail: {} resolution: {} score: {}".format( metanames[bannerType], seasonNum, rank, imageURL, thumbnailURL, "{}x{}".format(Dict(image, 'width'), Dict(image, 'height')), Dict(image, 'score') ))
        #tvdb season posters or anidb specials and defaulttvdb season  ## season 0 et empty+ season ==defaulttvdbseason(a=1)
        if not anidb_numbering: 
          SaveDict(imageTuple, TheTVDB_dict, 'seasons', seasonNum, 'posters', imageURL)
        else:
          if seasonNum == Dict(mappingList, 'defaulttvdbseason'):         # If the TVDB season is the AniDB default season, add season poster as series poster
            SaveDict(imageTuple, TheTVDB_dict, 'posters', imageURL)
          if seasonNum in ['0', Dict(mappingList, 'defaulttvdbseason')]:  # If the TVDB season is the season 0 OR AniDB default season, add season poster
            SaveDict(imageTuple, TheTVDB_dict, 'seasons', '0' if seasonNum == '0' else '1', 'posters', imageURL)
      else:
        if anidb_prefered: rank = rank + 10
        SaveDict(imageTuple, TheTVDB_dict, metanames[bannerType], imageURL)
      Log.Info("[!] bannerType: {:>7} seasonNum: {:>3} rank: {:>3} filename: {} thumbnail: {} resolution: {} score: {}".format( metanames[bannerType], seasonNum, rank, imageURL, thumbnailURL, "{}x{}".format(Dict(image, 'width'), Dict(image, 'height')), Dict(image, 'score') ))
              
    if not Dict(series_json, 'image'): error_log['TVDB posters missing'       ].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    for season in Dict(series_json, 'seasons'):
      if not Dict(season, 'image'): error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s' | Season: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), Dict(season, 'number')))
            
    Log.Info("--- final summary info ---".ljust(157, '-'))
    Log.Info("url: '{}', IMDbid: {}, Present episodes: {}, Missing: {}".format(TVDB_SERIES_URL.format(id=TVDBid), IMDbid, len(Dict(series_json, 'episodes')), sorted(episode_missing, key=common.natural_sort_key)))
    
  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("absolute_map: {}".format(DictString(Dict(mappingList, 'absolute_map', default={}), 0)))
  Log.Info("season_map: {}".format(DictString(Dict(mappingList, 'season_map', default={}), 0)))
  Log.Info("TheTVDB_dict: {}".format(DictString(TheTVDB_dict, 4)))
  return TheTVDB_dict, IMDbid
  
def Search(results, media, lang, manual, movie):
  '''search for TVDB id series
  '''
  Log.Info("=== TheTVDBv4.Search() ===".ljust(157, '='))
  orig_title = ( media.title if movie else media.show )
  maxi = 0
  try:
    Login()
    searchType = 'movie' if movie else 'series'
    searchResult = JSON.ObjectFromString(HTTP.Request(TVDB_SEARCH_URL.format(type=searchType,name=orig_title), headers=common.UpdateDict(common.COMMON_HEADERS, TVDB_HEADERS), cacheTime=0).content)['data']
    if not searchResult:
      # Do a second try with the year removed from the title, if any
      orig_title = re.sub(r'\s*\(\d{4}\)$', '', orig_title)
      searchResult = JSON.ObjectFromString(HTTP.Request(TVDB_SEARCH_URL.format(type=searchType,name=orig_title), headers=common.UpdateDict(common.COMMON_HEADERS, TVDB_HEADERS), cacheTime=0).content)['data']
  except Exception as e: Log.Error("TVDB search failed, Exception: '%s'" % e)
  else:
    for serie in searchResult:
      ScoreSearch(results, orig_title, Dict(serie, 'name'), Dict(serie, 'tvdb_id'), lang)
      if Dict(serie, 'aliases'):
        for alias in Dict(serie, 'aliases'):
          ScoreSearch(results, orig_title, alias, Dict(serie, 'tvdb_id'), lang)
  return maxi

def ScoreSearch(results, orig_title, name, id, lang):
  a, b = orig_title, name
  score = 100 - 100 * Util.LevenshteinDistance(a, b) / max(len(a), len(b)) if a != b else 100
  if maxi < score: maxi = score
  Log.Info("TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, id, name))
  results.Append(MetadataSearchResult(id="%s-%s" % ('tvdb', id), name="%s [%s-%s]" % (name, 'tvdb', id), year=None, lang=lang, score=score) )

def RelativeImagePath(imagePath):
  return imagePath.replace('https://artworks.thetvdb.com/banners/v4','').replace('https://artworks.thetvdb.com/banners/','').replace('/banners/','')