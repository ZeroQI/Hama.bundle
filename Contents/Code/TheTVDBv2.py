### TheTVDB.com API v2 ###
# http://thetvdb.com/api/A27AD9BE0DA63333/series/103291/all/en.xml

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
import os
import time
from common     import GetMeta, GetXml, SaveDict, UpdateDict, Dict, natural_sort_key
from AnimeLists import tvdb_ep, anidb_ep
#import re, unicodedata, hashlib, types
#from collections import defaultdict

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'
TVDB_API_KEY               = 'A27AD9BE0DA63333'
TVDB_BASE_URL              = 'https://api.thetvdb.com'  #'https://api-beta.thetvdb.com' #tvdb v2 plex proxy site'' # TODO Start using TVDB's production api (TVDB is behind CF) when available and possibly a plex proxy for it
TVDB_LOGIN_URL             = TVDB_BASE_URL + '/login'
TVDB_SERIES_URL            = TVDB_BASE_URL + '/series/%s'
TVDB_EPISODES_URL          = TVDB_BASE_URL + '/series/%s/episodes?page=%s'
TVDB_EPISODE_DETAILS_URL   = TVDB_BASE_URL + '/episodes/'                          #+EpId
TVDB_ACTORS_URL            = TVDB_BASE_URL + '/series/%s/actors'
TVDB_SERIES_IMG_INFO_URL   = TVDB_BASE_URL + '/series/%s/images'
TVDB_SERIES_IMG_QUERY_URL  = TVDB_BASE_URL + '/series/%s/images/query?keyType=%s'
TVDB_SEARCH_URL            = TVDB_BASE_URL + '/search/series?name=%s'
TVDB_IMG_ROOT              = 'https://thetvdb.plexapp.com/banners/' 

THETVDB_LANGUAGES_CODE     = { 'cs': '28', 'da': '10', 'de': '14', 'el': '20', 'en':  '7', 'es': '16', 'fi': '11', 'fr': '17', 'he': '24', 
                               'hr': '31', 'hu': '19', 'it': '15', 'ja': '25', 'ko': '32', 'nl': '13', 'no':  '9', 'pl': '18', 'pt': '26',
                               'ru': '22', 'sv':  '8', 'tr': '21', 'zh': '27', 'sl': '30'}
HEADERS                    = {'User-agent': 'Plex/Nine'}
   
### Functions ###  
  
### Download from API v2 Json which requires auth token in headers  # DO NOT CALL additionalHeaders WITH VARIABLE
def GetResultFromNetwork(url, additionalHeaders={}, data=None):
  result = None
  if 'Authorization' in HEADERS:  # Normal loading, already Authentified
    try:                  result = HTTP.Request(url, headers=UpdateDict(additionalHeaders, HEADERS), timeout=60, data=data).content  #if not result:    set_JWT_token();  result = HTTP.Request(url, headers=local_headers, timeout=60, data=data)
    except Exception, e:  Log.Info('Error: (%s) - %s' % (e, e.message))
  
  # Access Token if needed
  if 'Authorization' not in HEADERS or not result:  # Grab New Auth token
    try:
      HEADERS['Authorization'] = 'Bearer ' + JSON.ObjectFromString(HTTP.Request(TVDB_LOGIN_URL, data=JSON.StringFromObject(dict(apikey=TVDB_API_KEY)), headers={'Content-type': 'application/json'}).content)['token']
      result = HTTP.Request(url, headers=UpdateDict(additionalHeaders, HEADERS), timeout=60, data=data).content
    except Exception, e:    Log.Info('Error: (%s) - %s' % (e, e.message))
    else:                   Log.Info('Access token: {}'.format(HEADERS['Authorization']))
  
  # JSON
  try:                    json = JSON.ObjectFromString(result)
  except Exception as e:  json = None;    Log.Info(' Exception, e: {}, e.message: {}'.format(e, e.message))
  for key in Dict(json, 'errors') or []:  Log.Info('"{}": "{}", additionalHeaders: "{}"'.format(key, json['errors'][key], additionalHeaders))
  return json
  
### TVDB - Load serie JSON ###
def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList, AniDB_movie):
  Log.Info("".ljust(157, '-'))
  Log.Info("TheTVDB.GetMetadata() - TVDBid: '{}', IMDbid: '{}'".format(TVDBid, IMDbid))
  if not TVDBid.isdigit(): return {}, IMDbid
  
  TheTVDB_dict      = {}
  language_series   = [language.strip() for language in Prefs['SerieLanguagePriority'  ].split(',') if language.strip() not in ('x-jat',)]
  language_episodes = [language.strip() for language in Prefs['EpisodeLanguagePriority'].split(',') if language.strip() not in ('x-jat',)]
  Log.Info('language_series : {}, language_episodes: {}'.format(language_series , language_episodes))
  
  ### TVDB Series Actors JSON ###
  if not Prefs["GetSingleOne"]:  #cache= CACHE_1MONTH, url=API_ACTORS_URL.replace('.com', '.plexapp.com')
    try:
      Log.Info('test7')
      actor_json = GetResultFromNetwork(TVDB_ACTORS_URL % TVDBid, additionalHeaders={'Accept-Language': lang} if lang!='en' else {})
      Log.Info('test8'+str(actor_json))
      actor_json = Dict(actor_json, 'data')
      
    except KeyError:  Log("Bad actor data, no update for TVDB id: %s" % TVDBid);  actor_json = None
    else:             #JSON format: 'data': [{"seriesId", "name", "image", "lastUpdated", "imageAuthor", "role", "sortOrder", "id", "imageAdded", },...]
      Log("TheTVDB.GetMetadata() - TVDB_ACTORS_URL: {}".format(TVDB_ACTORS_URL % TVDBid))  
      TheTVDB_dict['roles'] = []
      for role in actor_json or []:
        try:
          SaveDict([{'role': Dict(role, 'role'), 'name': Dict(role, 'name'), 'photo': TVDB_IMG_ROOT + role['image'] if Dict(role, 'image') else ''}], TheTVDB_dict, 'roles')
          Log.Info('TheTVDB.GetMetadata() - role: "{}", name: "{}", photo: "{}"'.format(Dict(role, 'role'), Dict(role, 'name'), Dict(role, 'image')))
        except Exception as e:  Log.Info("TheTVDB.GetMetadata() - 'roles' - error: '{}', role: '{}'".format(str(e), str(role)))
  
  ### TVDB Series JSON ###
  serie_json = {}
  try:
    serie_json = GetResultFromNetwork(TVDB_SERIES_URL % TVDBid, additionalHeaders={'Accept-Language': lang} if lang!='en' else {})
    Log.Info('serie_json: {}'.format(serie_json))
    serie_json = Dict(serie_json, 'data')
  except:  Log("Bad series data, no update for TVDB id: %s" % TVDBid);  return
  else:  #serie_json { "id","seriesId", "airsDayOfWeek", "imdbId", "zap2itId", "added", "addedBy", "lastUpdated", "seriesName", "aliases", "banner", "status", 
         #             "firstAired", "network", "networkId", "runtime", "genre, "overview", "airsTime", "rating" , "siteRating", "siteRatingCount" }
    #Log.Info('TheTVDB.GetMetadata() - serie_json: {}'.format(serie_json))
    SaveDict( language_series.index(lang) if lang in language_series else len(language_series), TheTVDB_dict, 'language_rank')
    SaveDict( Dict(serie_json, 'seriesName'), TheTVDB_dict, 'title'                  )
    SaveDict( Dict(serie_json, 'imdbId' or IMDbid), TheTVDB_dict, 'IMDbid'           )
    SaveDict( Dict(serie_json, 'zap2it_id' ), TheTVDB_dict, 'zap2itId'               )
    SaveDict( Dict(serie_json, 'rating'    ), TheTVDB_dict, 'content_rating'         )
    SaveDict( Dict(serie_json, 'overview'  ), TheTVDB_dict, 'summary'                )
    SaveDict( Dict(serie_json, 'firstAired'), TheTVDB_dict, 'originally_available_at')
    SaveDict( Dict(serie_json, 'genre'     ), TheTVDB_dict, 'genres'                 )
    SaveDict( Dict(serie_json, 'network'   ), TheTVDB_dict, 'studio'                 )
    SaveDict( Dict(serie_json, 'siteRating'), TheTVDB_dict, 'rating'                 )
    SaveDict( Dict(serie_json, 'status'    ), TheTVDB_dict, 'status'                 )
    if Dict(serie_json, 'runtime') and Dict(serie_json, 'runtime').isdigit():  SaveDict(int(Dict(serie_json, 'runtime'))*60*1000, TheTVDB_dict, 'duration')  #in ms in plex
    if Dict(serie_json, 'banner'):                                             SaveDict((os.path.join('TheTVDB', 'banner', Dict(serie_json, 'banner')), 1, None), TheTVDB_dict, 'banners', TVDB_IMG_ROOT+Dict(serie_json, 'banner'))
    Log.Info("TheTVDB.GetMetadata() - TVDBid: '{}', IMDbid: {}, url: '{}'".format(TVDBid, IMDbid, TVDB_SERIES_URL % TVDBid))
  
  ### Absolute mode ###  #Load pages of episodes
  episodes_json, page = [], 1
  while page not in (None, '', 'null'):
    episodes_json_page = GetResultFromNetwork(TVDB_EPISODES_URL % (TVDBid, page), additionalHeaders={'Accept-Language': lang} if lang!='en' else {})
    episodes_json.extend(episodes_json_page['data'])  #SaveDict(Dict(episodes_json_page), episodes_json)
    #Log.Info('TVDB_EPISODES_URL: {}, links: {}'.format(TVDB_EPISODES_URL % (TVDBid, page), Dict(episodes_json_page, 'links')))
    page = Dict(episodes_json_page, 'links', 'next')
  sorted_episodes_json = {}
  for episode_json in episodes_json: sorted_episodes_json['s{:02d}e{:03d}'.format(Dict(episode_json, 'airedSeason'), Dict(episode_json, 'airedEpisodeNumber'))] = episode_json
  sorted_episodes_index_list = sorted(sorted_episodes_json, key=natural_sort_key)
  #Log.Info('len: {}, sorted_episodes_index_list: {}'.format(len(sorted_episodes_index_list), sorted_episodes_index_list))
  
  tvdb_special_missing, summary_missing_special, summary_missing, summary_present, episode_missing, abs_manual_placement_info = [], [], [], [], [], []
  abs_number, missing_abs_nb, ep_count = 1, False, 0
  for index in sorted_episodes_index_list:
    episode_json = sorted_episodes_json[index]
    #Log.Info('s{:02d}e{:03d} abs: {:03d} ep: {}'.format(Dict(episode_json, 'airedSeason') or 0, Dict(episode_json, 'airedEpisodeNumber') or 0, Dict(episode_json, 'absoluteNumber') or 0, episode_json))
    
    ### Get the season and episode numbers
    season  = str(Dict(episode_json, 'airedSeason'       ))
    episode = str(Dict(episode_json, 'airedEpisodeNumber'))
    if metadata_source in ('tvdb3', "tvdb4", "tvdb5") and season!='0':  season='1'
    elif metadata_source=="anidb" and (Dict(mappingList, 'defaulttvdbseason')!="a" or season=='0'):
      Log.Info('TVDB numbering, season: {}, episode: {}'.format(season, episode))
      season, episode, x = anidb_ep(mappingList, season, episode)
      Log.Info('AniDB numbering, season: {}, episode: {}'.format(season, episode))
    elif season!='0':
      if (metadata_source=="anidb" and Dict(mappingList, 'defaulttvdbseason')=="a" and not movie and max(map(int, media.seasons.keys()))==1 or metadata_source in ("tvdb3", "tvdb4", "tvdb5")):
        if Dict(episode_json, 'absoluteNumber'):  abs_number = Dict(episode_json, 'absoluteNumber')
        if not episode:                           episode = str(abs_number); missing_abs_nb = True;  abs_manual_placement_info.append("s%se%s = abs %s" % (str(Dict(episode_json, 'airedSeason')), str(Dict(episode_json, 'airedEpisodeNumber')), str(Dict(episode_json, 'absoluteNumber'))))
        elif not missing_abs_nb:                  episode = str(abs_number) #update abs_number with real abs number
        elif (episode if metadata_source not in ('tvdb3', 'tvdb4') else Dict(episode_json, 'absoluteNumber')) != abs_number:
          Log.Error("TheTVDB.GetMetadata() - Abs number (s{}e{}) present after manually placing our own abs numbers ({}), type: {}".format(Dict(episode_json, 'airedSeason'), Dict(episode_json, 'airedEpisodeNumber'), abs_number, type(season)))
          continue
        
    numbering = "s{}e{}".format(season, episode)
    
    SaveDict( abs_number                       , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'absolute_index'         )
    SaveDict( Dict(serie_json  , 'rating'     ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'content_rating'         )
    SaveDict( Dict(serie_json  , 'runtime'    ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'duration'               )
    SaveDict( Dict(episode_json, 'firstAired' ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at') 
    if Dict(episode_json, 'episodeName'):
      SaveDict( Dict(episode_json, 'episodeName'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title')
      SaveDict( language_episodes.index(lang) if lang in language_episodes else len(language_episodes), TheTVDB_dict, 'language_rank')
      rank=language_episodes.index(lang) if lang in language_episodes else len(language_episodes)
    else:  rank = len(language_episodes)
    
    ### Missing summaries logs ###
    if SaveDict( Dict(episode_json, 'overview'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary'):  summary_present.append(numbering)
    elif season!='0':                                                                                               summary_missing.append(numbering)
    else:                                                                                                           summary_missing_special.append(numbering)
      
    ### Check for Missing Episodes ###
    if not movie and (( metadata_source.startswith("tvdb") or max(map(int, media.seasons.keys()))>1) and \
         metadata_source != 'tvdb5' and \
         not (metadata_source in ('tvdb',  'tvdb2') and season in media.seasons and episode in media.seasons[season].episodes) and \
         not (metadata_source in ('tvdb3', 'tvdb4') and season >=1 and [True for s in media.seasons if episode in media.seasons[s].episodes])) \
      or movie and metadata_source=='anidb' and tvdb_ep(mappingList, '1', '1', source)==(season, episode):
      
      air_date = Dict(episode_json, 'FirstAired')
      air_date = int(air_date.replace('-','')) if air_date.replace('-','').isdigit() and int(air_date.replace('-','')) > 10000000 else 99999999
      if int(time.strftime("%Y%m%d")) <= air_date+1:  pass  #Log.Warn("TheTVDB.GetMetadata() - Episode '{}' missing but not aired/missing '{}'".format(numbering, air_date))
      elif season=='0':                               tvdb_special_missing.append(episode)                                                          #Log.Info("TVDB l176 - type of episode_missing: " + type(episode_missing).__name__)
      else:                                           episode_missing.append( str(abs_number)+" ("+numbering+")" if metadata_source in ('tvdb3', 'tvdb4') else numbering)  #Log.Info("TVDB - type of tvdb_special_missing: " + type(tvdb_special_missing).__name__)
    
    else:
      if metadata_source=="anidb" and max(map(int, media.seasons.keys()))==1 and (season not in media.seasons or not episode in media.seasons[season].episodes):  continue
      Log.Info('AniDB numbering2, season: {}, episode: {}'.format(season, episode))
   
      ### Ep advance information ###
      ep_count += 1
      id        = str(Dict(episode_json, 'id'))
      episode_details_json = Dict(GetResultFromNetwork(TVDB_EPISODE_DETAILS_URL + id, additionalHeaders={'Accept-Language': language_episodes[0]} if language_episodes and language_episodes[0]!='en' else {}), 'data')
      if episode_details_json:
        #Log.Info(episode_details_json)  #firstAired, overview, episodeName, seriesId, dvdDiscid, absoluteNumber, imdbId, firstAired
        SaveDict( Dict(episode_details_json, 'writers'            ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'writers'                )
        SaveDict( Dict(episode_details_json, 'directors'          ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'directors'              )
        SaveDict( Dict(episode_details_json, 'guestStars'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'guest_stars'            ) 
        SaveDict( Dict(episode_details_json, 'siteRating'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating'                 )
        file = Dict(episode_details_json, 'filename')  # KeyError: u'http://thetvdb.plexapp.com/banners/episodes/81797/383792.jpg' avoided below with str()
        if file:
          SaveDict((str("TheTVDB/episodes/"+ os.path.basename(file)), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', str(TVDB_IMG_ROOT+file))
          Log.Info('AniDB numbering, season: {}, episode: {} thumb: {}'.format(season, episode, str(TVDB_IMG_ROOT+file)))
   
      # Std ep info loaded for Library language ten details for 1st language, loading other languages if needed
      rank = len(language_episodes)
      if lang                  in language_episodes and Dict(episode_json,         'episodeName'):  rank=language_episodes.index(lang)
      if language_episodes and language_episodes[0] and Dict(episode_details_json, 'episodeName'):  rank=0
      SaveDict( rank, TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')
      #Log.Info('array: {} after disregarding too high indexes'.format(language_episodes[1:rank-1]))
      for lang_rank, language in enumerate(language_episodes[1:rank-1] if len(language_episodes)>1 and rank>=2 else []):
        if not language:  continue
        episode_details_json = GetResultFromNetwork(TVDB_EPISODE_DETAILS_URL + id, additionalHeaders={'Accept-Language': language} if language!='en' else {})['data']
        if Dict(episode_details_json, 'episodeName') :  
          SaveDict( Dict(episode_details_json, 'episodeName'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title')
          SaveDict( lang_rank                                , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')
          #Log.Info('language: {}, lang_rank: {}, title: '.format(language, lang_rank, Dict(episode_details_json, 'episodeName')))
          rank=lang_rank
          break
        else:  Log.Info('no ep title in language: {}'.format(language_episodes[lang_rank]))

    if season!='0':  abs_number += 1
  Log.Info('Episodes specific metadata loaded: {} (need to match episodes presents physically)'.format(ep_count))
  
  ### Collection ###  # get all anidbids sharing the same tvdbids
  
  if not movie:
    ### Logging ###
    Log.Info("TheTVDB.GetMetadata(): abs_manual_placement_info: "+str(abs_manual_placement_info))
    if summary_missing:          error_log['Missing Episode Summaries'].append("TVDBid: %s | Title: '%s' | Missing Episode Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing        )))
    if summary_missing_special:  error_log['Missing Special Summaries'].append("TVDBid: %s | Title: '%s' | Missing Special Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing_special)))
    if episode_missing:          error_log['Missing Episodes'         ].append("TVDBid: %s | Title: '%s' | Missing Episodes: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(episode_missing        )))
    if tvdb_special_missing:     error_log['Missing Specials'         ].append("TVDBid: %s | Title: '%s' | Missing Specials: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(tvdb_special_missing   )))
    Log.Debug("TheTVDB.GetMetadata() - TVDB - Episodes without Summary: " + str(sorted(summary_missing, key=natural_sort_key)))
    Log.Debug("TheTVDB.GetMetadata() - TVDB - Episodes missing: "         + str(sorted(episode_missing, key=natural_sort_key)))
    
  ### Picture types JSON download ###
  Log.Info("TheTVDB.GetMetadata() - Images")
  try:
    bannerTypes = Dict(GetResultFromNetwork(TVDB_SERIES_IMG_INFO_URL % TVDBid, additionalHeaders={'Accept-Language': language} if language!='en' else {}),'data') or \
                  Dict(GetResultFromNetwork(TVDB_SERIES_IMG_INFO_URL % TVDBid, additionalHeaders={'Accept-Language': 'en'}),'data')
  except KeyError:  Log("Invalid image JSON from url: " + TVDB_SERIES_IMG_INFO_URL % TVDBid)
  else:             #JSON format = {"fanart", "poster", "season", "seasonwide", "series"}
    metanames         = {'fanart': "art", 'poster': "posters", 'series': "banners", 'season': "seasons", 'seasonwide': 'seasonwide'}#
    count_valid       = {key: 0 for key in metanames}
    anidb_offset      = sorted((Dict(mappingList, 'poster_id_array', TVDBid) or {}).keys()).index(AniDBid) if AniDBid and AniDBid in Dict(mappingList, 'poster_id_array', TVDBid) else 0  
    language_priority = [item.strip() for item in Prefs['EpisodeLanguagePriority'].split(',')]
    Log.Info("TheTVDB.GetMetadata() - bannerTypes: {}, anidb_offset: {}, AniDBid: {}, anidb_array: {}".format(bannerTypes, anidb_offset, AniDBid, str((Dict(mappingList, 'poster_id_array', TVDBid) or {}).keys())))
    for bannerType in bannerTypes or []:
      
      #Loop per banner type ("fanart", "poster", "season", "series") skip 'seasonwide' - Load bannerType images list JSON
      if bannerTypes[bannerType]==0 or bannerType in ('seasonwide', 'series') or not GetMeta('TheTVDB', metanames[bannerType]) or movie and not bannerType in ('fanart', 'poster'):  continue  #Loop if no images
      try:              images = GetResultFromNetwork(TVDB_SERIES_IMG_QUERY_URL % (TVDBid, bannerType), additionalHeaders={'Accept-Language': lang} if lang!='en' else {})['data']
      except KeyError:  Log("Bad image type query data for TVDB id: %s (bannerType: %s)" % (TVDBid, bannerType)) 
      for image in images:  #JSON format = {"data": [{"id", "keyType", "subKey"(season/graphical/text), "fileName", "resolution", "ratingsInfo": {"average", "count"}, "thumbnail"}]}
        
        #rank
        rank = 1 if bannerType=='poster' and anidb_offset == divmod(count_valid['poster'], bannerTypes['poster'])[1] else count_valid[bannerType]+2
        if AniDB_movie: rank = rank+bannerTypes['poster'] if rank+bannerTypes['poster']<99 else 99
        
        #language
        #language = Dict(image, 'languageId')
        #if Prefs['localart']:  rank += 10*language_priority.index(language) if language and language in language_priority else 50
        
        ### Adding picture ###
        thumbnail = TVDB_IMG_ROOT + image['thumbnail'] if Dict(image, 'thumbnail') else None
        if bannerType == 'season':  
          season = str(int(image['subKey'])+(0 if Dict(mappingList, 'defaulttvdbseason')=="0" or not Dict(mappingList, 'defaulttvdbseason').isdigit() else int(Dict(mappingList, 'defaulttvdbseason'))-1))
          SaveDict((                          'TheTVDB'+image['fileName'], rank, thumbnail), TheTVDB_dict, 'seasons', season, 'posters', TVDB_IMG_ROOT + image['fileName'])
        else:                       SaveDict(('TheTVDB'+image['fileName'], rank, thumbnail), TheTVDB_dict, metanames[bannerType],        TVDB_IMG_ROOT + image['fileName'])
        if bannerType in ('poster', 'season'):  Log.Info("[!] bannerType: {}, subKey: {:>2}, rank: {:>3}, filename: {}, thumbnail: {}, resolution: {}, average: {}, count: {}".format( metanames[bannerType], Dict(image, 'subKey'), rank, TVDB_IMG_ROOT + Dict(image, 'fileName'), TVDB_IMG_ROOT + Dict(image, 'thumbnail'), Dict(image, 'resolution'), Dict(image, 'ratingsInfo','average'), Dict(image, 'ratingsInfo', 'average', 'count') ))
        count_valid[bannerType] = count_valid[bannerType] + 1  #Otherwise with += SyntaxError: Line 142: Augmented assignment of object items and slices is not allowed
        
    Log.Info("TheTVDB.GetImages() - Posters : {}/{}, Season posters: {}/{}, Art: {}/{}".format(count_valid['poster'], Dict(bannerTypes, 'poster'), count_valid['season'], Dict(bannerTypes, 'season') or 0, count_valid['fanart'], Dict(bannerTypes, 'fanart')))
    if not Dict(bannerTypes, 'poster'):  error_log['TVDB posters missing'       ].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    if not Dict(bannerTypes, 'season'):  error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    
  #Log.Info('TheTVDB_dict fields: {}'.format(TheTVDB_dict.keys()))
  #Log.Info('TheTVDB_dict["posters"]: {}'.format(Dict(TheTVDB_dict, 'posters')))
  #Log.Info('TheTVDB_dict["seasons"]["1"]: {}'.format(Dict(TheTVDB_dict, 'seasons', '1')))
  Log.Info('TheTVDB_dict:        {}'.format(TheTVDB_dict))
  Log.Info('TheTVDB_dict:        {}'.format(Dict(TheTVDB_dict, 'seasons', '1')))
  return TheTVDB_dict, IMDbid
  
### search for TVDB id series ###
def Search (results,  media, lang, manual, movie):  #if maxi<50:  maxi = tvdb.Search_TVDB(results, media, lang, manual, movie)
  #series_data = JSON.ObjectFromString(GetResultFromNetwork(TVDB_SEARCH_URL % mediaShowYear, additionalHeaders={'Accept-Language': lang}))['data'][0]
  TVDB_SERIE_SEARCH = 'http://thetvdb.com/api/GetSeries.php?seriesname='
  orig_title = ( media.title if movie else media.show )
  maxi = 0
  try:                    TVDBsearchXml = XML.ElementFromURL( TVDB_SERIE_SEARCH + orig_title.replace(" ", "%20"), cacheTime=CACHE_1HOUR * 24)
  except Exception as e:  Log.Error("TVDB Loading search XML failed, Exception: '%s'" % e)
  else:
    for serie in TVDBsearchXml.xpath('Series'):
      a, b = orig_title, GetXml(serie, 'SeriesName').encode('utf-8') #a, b  = cleansedTitle, cleanse_title (serie.xpath('SeriesName')[0].text)
      score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
      if maxi<score:  maxi = score
      Log.Info("TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, GetXml(serie, 'seriesid'), GetXml(serie, 'SeriesName')))
      results.Append(MetadataSearchResult(id="%s-%s" % ("tvdb", GetXml(serie, 'seriesid')), name="%s [%s-%s]" % (GetXml(serie, 'SeriesName'), "tvdb", GetXml(serie, 'seriesid')), year=None, lang=lang, score=score) )
  return maxi
