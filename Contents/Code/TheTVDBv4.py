### TheTVDB.com API v4 ###
# https://thetvdb.github.io/v4-api

### Imports ###
# Python Modules #
import os
import time
import re
from urllib import quote
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions
import AnimeLists

### Variables ###
TVDB_API_KEY               = None  # add your API key here to use the v4 API
TVDB_API_PIN               = None  # add your PIN here to use the v4 API
TVDB_IMG_ROOT              = 'https://artworks.thetvdb.com/banners/'
TVDB_BASE_URL              = 'https://api4.thetvdb.com/v4'
TVDB_LOGIN_URL             = TVDB_BASE_URL + '/login'
TVDB_SERIES_URL            = TVDB_BASE_URL + '/series/{id}'
TVDB_SERIES_EXTENDED_URL   = TVDB_SERIES_URL + '/extended'
TVDB_SERIES_EPISODES_URL   = TVDB_SERIES_URL + '/episodes/default?page={page}'
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
TVDB_LANGUAGES_ISO         = {tvdb: iso for iso, tvdb in TVDB_LANGUAGES_CODE.items()}

TVDB_HEADERS   = {}
TVDB_AUTH_TIME = None
netLocked      = {}

### Functions ###
def HasCredentials():
  return bool(TVDB_API_KEY and TVDB_API_PIN)

def Login():
  global TVDB_AUTH_TIME

  # If no auth or auth is >12hrs old, authenticate from scratch
  if 'Authorization' not in TVDB_HEADERS or (TVDB_AUTH_TIME and (time.time()-TVDB_AUTH_TIME) > CACHE_1DAY/2):
    try:
      TVDB_HEADERS['Authorization'] = 'Bearer ' + JSON.ObjectFromString(HTTP.Request(TVDB_LOGIN_URL, data=JSON.StringFromObject({'apikey': TVDB_API_KEY, 'pin': TVDB_API_PIN}), headers=common.COMMON_HEADERS, cacheTime=0).content)['data']['token']
      TVDB_AUTH_TIME = time.time()
    except Exception as e: Log.Root('TheTVDBv4.Login() - Authorization Error: {}'.format(e))
    else:                  Log.Root('TheTVDBv4.Login() - URL {}'.format(TVDB_LOGIN_URL))

def LoadFileTVDB(id='', filename='', url=''):
  """ Wrapper around "common.LoadFile()" to remove the need to consistently define arguments 'relativeDirectory'/'cache'/'headers'
  """
  while 'LoadFileTVDB' in netLocked and netLocked['LoadFileTVDB'][0]:
    Log.Root("TheTVDBv4.LoadFileTVDB() - Waiting for lock: 'LoadFileTVDB'"); time.sleep(1)
  netLocked['LoadFileTVDB'] = (True, int(time.time())) #Log.Root("Lock acquired: 'LoadFile'")
  try:
    Login()
    return common.LoadFile(filename=filename, relativeDirectory=os.path.join('TheTVDBv4', 'json', id), url=url, headers=TVDB_HEADERS)
  finally:
    netLocked['LoadFileTVDB'] = (False, 0)  # Always released, a failed request must not block every later one

def GetEpisodes(TVDBid):
  """ Load every page of the series' episodes in its default season order (pages start at 0)
  """
  episodes, page = [], 0
  while True:
    page_json = LoadFileTVDB(id=TVDBid, filename='episodes_default_page{}.json'.format(page), url=TVDB_SERIES_EPISODES_URL.format(id=TVDBid, page=page))
    episodes.extend(Dict(page_json, 'data', 'episodes', default=[]))
    if not Dict(page_json, 'links', 'next'):  return episodes
    page += 1

def LinkedMovie(TVDBid, episode_json):
  """ Extended record of the movie a special links to, {} if there is none
  """
  movie_id = Dict(episode_json, 'linkedMovie')
  if not movie_id:  return {}
  return Dict(LoadFileTVDB(id=TVDBid, filename='movie_{}.json'.format(movie_id), url=TVDB_MOVIE_EXTENDED_URL.format(id=movie_id)), 'data', default={})

def FillFromLinkedMovie(TVDBid, episode_json):
  """ Specials that are movies may hold little data themselves: only fill what the episode lacks, the episode's own values always win
  """
  if not Dict(episode_json, 'linkedMovie') or (Dict(episode_json, 'aired') and Dict(episode_json, 'runtime') and Dict(episode_json, 'image')):  return
  movie_json = LinkedMovie(TVDBid, episode_json)
  if not Dict(episode_json, 'aired'):    episode_json['aired']   = Dict(movie_json, 'first_release', 'date')
  if not Dict(episode_json, 'runtime'):  episode_json['runtime'] = Dict(movie_json, 'runtime')
  if not Dict(episode_json, 'image'):    episode_json['image']   = Dict(movie_json, 'image')

def First(values):
  """ First value, None if empty. The Plex sandbox has no next()
  """
  for value in values:  return value

def LanguageCodes(pref):
  """ TVDB codes of a language priority pref, skipping entries TVDB has no code for (ex: 'main', 'x-jat')
  """
  codes = [TVDB_LANGUAGES_CODE.get(language.strip()) for language in Prefs[pref].split(',')]
  return [code for code in codes if code]

def RemoteId(series_json, source):
  return First(Dict(x, 'id') for x in Dict(series_json, 'remoteIds') if Dict(x, 'sourceName') == source)

def MainArtwork(series_json, image_type, lang):
  """ First artwork of a type that is language neutral or in the library language
  """
  return First(Dict(x, 'image') for x in Dict(series_json, 'artworks') if Dict(x, 'type') == image_type and (not Dict(x, 'language') or Dict(x, 'language') == lang))

def PeopleNames(characters, people_type):
  return [Dict(x, 'personName') for x in characters if Dict(x, 'peopleType') == people_type]

def CollapseMissingSeason(episode_missing, episode_missing_season, episode_missing_season_all):
  """ Replace all the individual episodes reported as missing with a single season 'sX' entry when the whole season is missing
  """
  if not episode_missing_season_all:  episode_missing.extend(episode_missing_season)
  elif episode_missing_season:
    fm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', episode_missing_season[0] ).groupdict()
    lm = re.match(r'((?P<abs>\d+) \()?s(?P<s>\d+)e(?P<e>\d+)\)?', episode_missing_season[-1]).groupdict()
    episode_missing.append("s{}e{}-{}".format(fm['s'], fm['e'], lm['e']) if fm['abs'] is None else "{}-{} (s{}e{}-{})".format(fm['abs'], lm['abs'], fm['s'], fm['e'], lm['e']))

def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList):
  ''' TVDB - Load serie JSON
  '''
  Log.Info("=== TheTVDBv4.GetMetadata() ===".ljust(157, '='))
  TheTVDB_dict      = {}
  max_season        = 0
  anidb_numbering   = metadata_source=="anidb" and (movie or max(map(int, media.seasons.keys()))<=1)
  anidb_prefered    = anidb_numbering and Dict(mappingList, 'defaulttvdbseason') != '1'
  library_lang      = lang
  lang              = TVDB_LANGUAGES_CODE.get(lang, 'eng')
  language_series   = LanguageCodes('SerieLanguagePriority')
  language_episodes = LanguageCodes('EpisodeLanguagePriority')
  Log.Info("TVDBid: '{}', IMDbid: '{}', language_series : {}, language_episodes: {}".format(TVDBid, IMDbid, language_series , language_episodes))

  if not TVDBid.isdigit(): Log.Info('TVDBid non-digit'); return TheTVDB_dict, IMDbid

  ### TVDB Series JSON ###
  Log.Info("--- series ---".ljust(157, '-'))
  series_overview = ""
  if lang not in language_series:    language_series.insert(0, lang) #for summary in lang (library setting) language
  if 'eng' not in language_series:   language_series.insert(0, 'eng') #for failover title
  if lang not in language_episodes:  language_episodes.append(lang) #for summary in lang (library setting) language
  if 'eng' not in language_episodes: language_episodes.append('eng') #for failover title
  series_json = Dict(LoadFileTVDB(id=TVDBid, filename='series.json', url=TVDB_SERIES_EXTENDED_URL.format(id=TVDBid)), 'data')
  for language in language_series:
    lang_json = Dict(LoadFileTVDB(id=TVDBid, filename='series_{}.json'.format(language), url=TVDB_SERIES_TRANSLATION_URL.format(id=TVDBid, lang=language)), 'data')
    if Dict(lang_json, 'name') and not Dict(TheTVDB_dict, 'title'):
      SaveDict( language_series.index(language) if not anidb_prefered else len(language_series), TheTVDB_dict, 'language_rank')
      Log.Info("[ ] language_rank: {}"          .format(Dict(TheTVDB_dict, 'language_rank')))
      Log.Info("[ ] title: {}"                  .format(SaveDict( Dict(lang_json, 'name'), TheTVDB_dict, 'title')))
    if Dict(lang_json, 'overview') and not series_overview: series_overview = Dict(lang_json, 'overview').strip(" \n\r")
    if series_overview and Dict(TheTVDB_dict, 'title'):  break  #only need json in lang for summary, in 'eng' for most things
  if not anidb_prefered: SaveDict( series_overview or Dict(series_json, 'overview').strip(" \n\r"), TheTVDB_dict, 'summary')
  if series_json:
    #JSON format: { "id","name", "slug", "image", "nameTranslations", "overviewTranslations", "aliases", "firstAired", "lastAired", "nextAired", "score", "status",
    #               "originalCountry", "originalLanguage", "defaultSeasonType", "isOrderRandomized", "lastUpdated, "averageRuntime", "episodes", "overview" , "year", "artworks","companies",
    #               "originalNetwork", "latestNetwork", "genres", "trailers", "lists", "remoteIds", "characters", "airsDays", "airsTime", "seasons", "tags", "contentRatings", "seasonTypes"}
    imdbid    = RemoteId(series_json, 'IMDB')
    zap2it_id = RemoteId(series_json, 'TMS (Zap2It)')
    rating    = First(Dict(x, 'name') for x in Dict(series_json, 'contentRatings') if Dict(x, 'country') == 'usa')
    genres    = sorted(Dict(x, 'name') for x in Dict(series_json, 'genres'))
    Log.Info("[ ] IMDbid: {}"                 .format(SaveDict(imdbid or IMDbid,                             TheTVDB_dict, 'IMDbid'                 )))
    Log.Info("[ ] zap2itId: {}"               .format(SaveDict(zap2it_id,                                    TheTVDB_dict, 'zap2itId'               )))
    Log.Info("[ ] content_rating: {}"         .format(SaveDict(rating,                                       TheTVDB_dict, 'content_rating'         )))
    Log.Info("[ ] originally_available_at: {}".format(SaveDict(Dict(series_json, 'firstAired'),              TheTVDB_dict, 'originally_available_at')))
    Log.Info("[ ] studio: {}"                 .format(SaveDict(Dict(series_json, 'originalNetwork', 'name'), TheTVDB_dict, 'studio'                 )))
    Log.Info("[ ] status: {}"                 .format(SaveDict(Dict(series_json, 'status', 'name'),          TheTVDB_dict, 'status'                 )))
    Log.Info("[ ] genres: {}"                 .format(SaveDict(genres,                                       TheTVDB_dict, 'genres'                 )))
    Log.Info('[ ] duration: {}'               .format(SaveDict(Dict(series_json, 'averageRuntime')*60*1000,  TheTVDB_dict, 'duration'               ))) # in ms in plex
    
    series_images = {  # The primary image of each artwork type used for the series entry
      1: MainArtwork(series_json, 1, lang),
      2: Dict(series_json, 'image'),
      3: MainArtwork(series_json, 3, lang)}

    ### TVDB Series Actors JSON ###
    Log.Info("--- actors ---".ljust(157, '-'))
    characters_json = Dict(series_json, 'characters', default=[])
    if characters_json: #JSON format: {"id", "name", "peopleId", "seriesId", "image", "isFeatured", "url", "peopleType", "personName", "personImgURL"},...]
      for role in characters_json:
        if Dict(role, 'peopleType') != 'Actor':  continue  # 'characters' also lists directors, writers, etc
        try:
          role_dict = {'role': Dict(role, 'name'), 'name': Dict(role, 'personName'), 'photo': Dict(role, 'image')}
          SaveDict([role_dict], TheTVDB_dict, 'roles')
          Log.Info("[ ] role: {:<50}, name: {:<20}, photo: {}".format(role_dict['role'], role_dict['name'], role_dict['photo']))
        except Exception as e: Log.Info(" role: {}, error: '{}'".format(str(role), str(e)))
      
    ### Load pages of episodes ###
    Log.Info("--- episodes ---".ljust(157, '-'))
    episodes_by_number = {}
    for episode_json in GetEpisodes(TVDBid):
      if not isinstance(episode_json.get('seasonNumber'), int) or not isinstance(episode_json.get('number'), int):  continue
      FillFromLinkedMovie(TVDBid, episode_json)
      episodes_by_number[(episode_json['seasonNumber'], episode_json['number'])] = episode_json
    episodes_json = [episodes_by_number[key] for key in sorted(episodes_by_number)]  # Numeric order, series can pass 999 episodes

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

    save_ep = lambda value, field: SaveDict(value, TheTVDB_dict, 'seasons', season, 'episodes', episode, field)  # For the episode currently in the loop
    ep_info = lambda field:        Dict(TheTVDB_dict, 'seasons', season, 'episodes', episode, field)

    # To avoid duplicate mapping we will remember episodes that have been mapped to a different value
    mapped_episodes = []
    for episode_json in episodes_json:
      season, episode, anidbid = AnimeLists.anidb_ep(mappingList, str(episode_json['seasonNumber']), str(episode_json['number']))
      if anidbid != 'xxxxxxx': mapped_episodes.append((season, episode))

    for episode_json in episodes_json:

      # Episode and Absolute number calculation engine, episode translation
      episode    = str(episode_json['number'      ])
      season     = str(episode_json['seasonNumber'])
      numbering  = "s{}e{}".format(season, episode)

      if episode == "1":
        CollapseMissingSeason(episode_missing, episode_missing_season, episode_missing_season_all)
        episode_missing_season, episode_missing_season_all = [], True

      # Get the max season number from TVDB API
      if int(season) > max_season: max_season = int(season)
      
      ### ep translation [Thetvdb absolute numbering followed, including in specials to stay accurate with scudlee's mapping]
      anidbid = ""
      abs_number = Dict(episode_json, 'absoluteNumber') or (0 if season=='0' else abs_number + 1)  # v4 returns 0 rather than null when unset
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
        if not anidb_numbering:  save_ep(abs_number, 'absolute_index')
        save_ep(rating,                      'content_rating')
        save_ep(Dict(episode_json, 'runtime')*60*1000 if Dict(episode_json, 'runtime') else Dict(TheTVDB_dict, 'duration'), 'duration')  # in ms in plex
        save_ep(Dict(episode_json, 'aired'), 'originally_available_at')

        ### Ep advance information ###
        episode_id, movie_id = str(Dict(episode_json, 'id')), Dict(episode_json, 'linkedMovie')
        for lang_rank, language in enumerate(language_episodes):
          episode_details_json = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}_{}.json'.format(episode_id, language), url=TVDB_EPISODE_TRANSLATION_URL.format(id=episode_id, lang=language)), 'data')
          if movie_id and not (Dict(episode_details_json, 'name') and Dict(episode_details_json, 'overview')):
            movie_details_json   = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}_movie_{}_{}.json'.format(episode_id, movie_id, language), url=TVDB_MOVIE_TRANSLATION_URL.format(id=movie_id, lang=language)), 'data')
            episode_details_json = {'name': Dict(episode_details_json, 'name') or Dict(movie_details_json, 'name'), 'overview': Dict(episode_details_json, 'overview') or Dict(movie_details_json, 'overview')}
          if not ep_info('title') and Dict(episode_details_json, 'name'):
            save_ep(lang_rank, 'language_rank')
            save_ep(Dict(episode_details_json, 'name').strip(" \n\r"), 'title')
            Log.Info(" - [{}] title:   [{}] {}".format(lang_rank + 1, language, ep_info('title')))
          if not ep_info('summary') and Dict(episode_details_json, 'overview'):
            save_ep(Dict(episode_details_json, 'overview').strip(" \n\r"), 'summary')
            Log.Info(" - [{}] summary:   [{}] {}".format(lang_rank + 1, language, ep_info('summary')))
          if ep_info('title') and ep_info('summary'):  break

        episode_extended = Dict(LoadFileTVDB(id=TVDBid, filename='episode_{}.json'.format(episode_id), url=TVDB_EPISODE_EXTENDED_URL.format(id=episode_id)), 'data')
        characters = Dict(episode_extended, 'characters', default=[])
        writers    = PeopleNames(characters, 'Writer')
        directors  = PeopleNames(characters, 'Director')
        if movie_id and not (writers and directors):
          movie_characters = Dict(LinkedMovie(TVDBid, episode_json), 'characters', default=[])
          writers   = writers   or PeopleNames(movie_characters, 'Writer')
          directors = directors or PeopleNames(movie_characters, 'Director')
        save_ep(writers,   'writers')
        save_ep(directors, 'directors')

        # Episode screenshot/Thumbnail
        if Dict(episode_json, 'image'):
          imagePath = RelativeImagePath(Dict(episode_json, 'image'))
          imageURL  = ImageURL(Dict(episode_json, 'image'))
          SaveDict((os.path.join("TheTVDBv4", "images", "episodes", os.path.basename(imagePath)), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', imageURL)
          Log.Info(' - [ ] thumb: {}'.format(imageURL))

    CollapseMissingSeason(episode_missing, episode_missing_season, episode_missing_season_all)  # Last season

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
    languages = LanguageCodes('PosterLanguagePriority')
    Log.Info('languages: {}'.format(languages))

    metanames   = {3: "art", 2: "posters", 1: "banners", 7: "seasons"}
    image_types = (1, 2, 3) if movie else (1, 2, 3, 7)
    count_valid = {key: 0 for key in metanames}
    default_seasons = [x for x in Dict(series_json, 'seasons', default=[]) if not Dict(series_json, 'defaultSeasonType') or Dict(x, 'type', 'id') == Dict(series_json, 'defaultSeasonType')]  # Other orders reuse the same season numbers
    season_numbers  = {Dict(x, 'id'): str(Dict(x, 'number')) for x in default_seasons}
        
    for image in sorted(Dict(series_json, 'artworks'), key = lambda x: Dict(x, 'score', default=0), reverse=True):
      #JSON format [{"id", "image", "thumbnail", "language", "type", "score", "width", "height", "seasonId"}, ...]
      bannerType = Dict(image, 'type')
      if not Dict(image, 'image') or bannerType not in image_types: continue
      if Dict(image, 'language') and Dict(image, 'language') not in languages: continue
      if bannerType == 7 and Dict(image, 'seasonId') not in season_numbers: continue

      imagePath    = RelativeImagePath(Dict(image, 'image'))
      imageURL     = ImageURL(Dict(image, 'image'))
      thumbnailURL = ImageURL(Dict(image, 'thumbnail')) if Dict(image, 'thumbnail') else None

      count_valid[bannerType] = count_valid[bannerType] + 1  # Plex's restricted Python does not allow += on items
      image_lang = TVDB_LANGUAGES_ISO.get(Dict(image, 'language'), library_lang)  # Language neutral images rank as the library language
      rank = common.poster_rank('TheTVDB', metanames[bannerType], image_lang, 0 if Dict(image, 'image') == series_images.get(bannerType) else count_valid[bannerType])
      if anidb_prefered and bannerType != 7:  rank += 10
      imageTuple = (os.path.join('TheTVDBv4', 'images', imagePath.replace('/', os.sep)), rank, thumbnailURL)

      seasonNum = None
      if bannerType == 7:
        seasonNum = season_numbers[Dict(image, 'seasonId')]
        #tvdb season posters or anidb specials and defaulttvdb season  ## season 0 et empty+ season ==defaulttvdbseason(a=1)
        if not anidb_numbering: 
          SaveDict(imageTuple, TheTVDB_dict, 'seasons', seasonNum, 'posters', imageURL)
        else:
          if seasonNum == Dict(mappingList, 'defaulttvdbseason'):         # If the TVDB season is the AniDB default season, add season poster as series poster
            SaveDict(imageTuple, TheTVDB_dict, 'posters', imageURL)
          if seasonNum in ['0', Dict(mappingList, 'defaulttvdbseason')]:  # If the TVDB season is the season 0 OR AniDB default season, add season poster
            SaveDict(imageTuple, TheTVDB_dict, 'seasons', '0' if seasonNum == '0' else '1', 'posters', imageURL)
      else:
        SaveDict(imageTuple, TheTVDB_dict, metanames[bannerType], imageURL)
      Log.Info("[!] bannerType: {:>7} seasonNum: {:>3} rank: {:>3} filename: {} thumbnail: {} resolution: {} score: {}".format( metanames[bannerType], seasonNum or '', rank, imageURL, thumbnailURL, "{}x{}".format(Dict(image, 'width'), Dict(image, 'height')), Dict(image, 'score') ))
              
    if not Dict(series_json, 'image'): error_log['TVDB posters missing'       ].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    for season in default_seasons:
      if not Dict(season, 'image'): error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s' | Season: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), Dict(season, 'number')))
            
    Log.Info("--- final summary info ---".ljust(157, '-'))
    Log.Info("url: '{}', IMDbid: {}, Present episodes: {}, Missing: {}".format(TVDB_SERIES_URL.format(id=TVDBid), IMDbid, len(episodes_json), sorted(episode_missing, key=common.natural_sort_key)))
    
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
    headers = dict(common.COMMON_HEADERS, **TVDB_HEADERS)  # Copied so the bearer token is never sent to other providers
    request = lambda title: JSON.ObjectFromString(HTTP.Request(TVDB_SEARCH_URL % quote(title.encode('utf-8')), headers=headers, cacheTime=0).content)['data']
    searchResult = request(orig_title)
    title_no_year = re.sub(r'\s*\(\d{4}\)$', '', orig_title)
    if not searchResult and title_no_year != orig_title:  # Second try with the year removed from the title
      orig_title   = title_no_year
      searchResult = request(orig_title)
  except Exception as e: Log.Error("TVDB search failed, Exception: '%s'" % e)
  else:
    for serie in searchResult or []:
      tvdb_id = Dict(serie, 'tvdb_id') or str(Dict(serie, 'id')).split('-')[-1]  # 'id' is prefixed, ex: 'series-81189'
      maxi = max(maxi, ScoreSearch(results, orig_title, Dict(serie, 'name'), tvdb_id, lang))
      for alias in Dict(serie, 'aliases', default=[]):
        maxi = max(maxi, ScoreSearch(results, orig_title, alias, tvdb_id, lang))
  return maxi

def ScoreSearch(results, orig_title, name, id, lang):
  a, b = orig_title, name
  score = 100 - 100 * Util.LevenshteinDistance(a, b) / max(len(a), len(b)) if a != b else 100
  Log.Info("TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, id, name))
  results.Append(MetadataSearchResult(id="%s-%s" % ('tvdb', id), name="%s [%s-%s]" % (name, 'tvdb', id), year=None, lang=lang, score=score) )
  return score

def RelativeImagePath(imagePath):
  """Remove the image host and return the path below /banners/, keeping any 'v4/' prefix as it is part of the file's location"""
  for prefix in (TVDB_IMG_ROOT, 'https://artworks.thetvdb.com/', 'http://artworks.thetvdb.com/', '/banners/'):
    if imagePath.startswith(prefix):  return imagePath[len(prefix):].lstrip('/')
  return imagePath.lstrip('/')

def ImageURL(imagePath):
  """v4 normally returns full urls, only build one when it did not"""
  return imagePath if imagePath.startswith('http') else TVDB_IMG_ROOT + RelativeImagePath(imagePath)
