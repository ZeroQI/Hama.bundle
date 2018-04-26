### TheTVDB.com API v2 ###
# http://thetvdb.com/api/A27AD9BE0DA63333/series/103291/all/en.xml

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
import os
import time
from common     import GetMeta, GetXml, SaveDict, Dict, natural_sort_key
from AnimeLists import tvdb_ep
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
  
def set_JWT_token():
  #Authentication_string = {"apikey": "A27AD9BE0DA63333", "userkey": "4BF214C112AEB9B0", "username": "ZeroQI"}  # username and key are ONLY required for the /user routes.
  #{"token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MjA5NzgzOTYsImlkIjoiSEFNQSIsIm9yaWdfaWF0IjoxNTIwODkxOTk2LCJ1c2VyaWQiOjM4MzM2MiwidXNlcm5hbWUiOiJaZXJvUUkifQ.CXhbF50PqjuNorXDeKy6UR7WUVv4C0Q2EfhXmB2UQ5imcJ7J28l7ZcJYt8KFOzxvBcm_sE6nXcKTdGtZGpMXUGlF0KNzCXnCIhXsivD3vPpcp0SOX_V1aO-FuhmvCLWFiFVjw5uzhlHeFGJ7DemhBEWv3D88ZI_Q-G9_bMmAsYJ9M_LQj6Q5t4dyhuhLw43QVYzF_oVeu6JmnsW5lh2VTI414FYr-CLSmicHLfWfLGnz3OHLPOPo-_bEAn74WHb-UzCo37kjbfuj9hB9zxKukTqi07tqg2epAePWNplrjQkKQ2N89nq_JvC_hC92R2nZu7tkjm4gPfXTFY1BBgSxvQ"}
  try:                    response = JSON.ObjectFromString(HTTP.Request(TVDB_LOGIN_URL, data=JSON.StringFromObject(dict(apikey=TVDB_API_KEY)), headers={'Content-type': 'application/json'}).content)
  except Exception, e:    Log("JWT Error: (%s) - %s" % (e, e.message))
  else:
    if 'token' in response:  
      Log.Info('GetResultFromNetwork -> set_JWT_token() - token: {}'.format(response['token']))
      HEADERS['Authorization'] = 'Bearer ' + response['token']

def GetResultFromNetwork(url, fetchContent=True, additionalHeaders=None, data=None):
  if additionalHeaders is None:  additionalHeaders = {}  #=dict()
  if 'Authorization' not in HEADERS: set_JWT_token()  # Grab New Auth token
  local_headers = HEADERS.copy()
  local_headers.update(additionalHeaders)
  
  Log("Retrieving URL: " + url) #'Accept: application/json'
  try:  result = HTTP.Request(url, headers=local_headers, timeout=60, data=data)
  except Exception:
    try:     set_JWT_token();  result = HTTP.Request(url, headers=local_headers, timeout=60, data=data)
    except Exception, e:  Log.Info(' Exception, e: {}'.format(e));  return None
  if fetchContent:
    try:                  result = result.content
    except Exception, e:  Log('Content Error (%s) - %s' % (e, e.message))
  
  try:
    json = JSON.ObjectFromString(result)
    if 'errors' in json:
      for key in json['errors']:  Log.Info('"{}": "{}", additionalHeaders: "{}"'.format(key, json['errors'][key], additionalHeaders))
  except:  pass
  return json  
      
### TVDB - Load serie JSON ###
def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList, AniDB_movie):
  Log.Info("".ljust(157, '-'))
  Log.Info("TheTVDB.GetMetadata() - TVDBid: '{}', IMDbid: '{}'".format(TVDBid, IMDbid))
  if not TVDBid.isdigit(): return {}, IMDbid
  
  TheTVDB_dict      = {}
  language_episodes = Prefs['EpisodeLanguagePriority'].split(',')
  language_episodes = [language.strip() if language not in ('x-jat') else '' for language in language_episodes if language]
  Log.Info('language_episodes: {}'.format(language_episodes))
  
  ### TVDB Series Actors JSON ###
  if not Prefs["GetSingleOne"]:  #cache= CACHE_1MONTH, url=API_ACTORS_URL.replace('.com', '.plexapp.com')
    try:              actor_json = GetResultFromNetwork(TVDB_ACTORS_URL % TVDBid, additionalHeaders={'Accept-Language': lang} if lang!='en' else {})['data']
    except KeyError:  Log("Bad actor data, no update for TVDB id: %s" % TVDBid);  actor_json = None
    else:             #JSON format: 'data': [{"seriesId", "name", "image", "lastUpdated", "imageAuthor", "role", "sortOrder", "id", "imageAdded", },...]
      Log("TheTVDB.GetMetadata() - TVDB_ACTORS_URL: {}, actor_json: {}".format(TVDB_ACTORS_URL % TVDBid, actor_json))  
      TheTVDB_dict['roles'] = []
      for role in actor_json:
        try:
          SaveDict([{'role': Dict(role, 'role'), 'name': Dict(role, 'name'), 'photo': TVDB_IMG_ROOT + role['image'] if Dict(role, 'image') else ''}], TheTVDB_dict, 'roles')
          Log.Info('TheTVDB.GetMetadata() - role: "{}", name: "{}", photo: "{}"'.format(Dict(role, 'role'), Dict(role, 'name'), Dict(role, 'image')))
        except Exception as e:  Log.Info("TheTVDB.GetMetadata() - 'roles' - error: '{}', role: '{}'".format(str(e), str(role)))
  
  ### TVDB Series JSON ###
  serie_json = {}
  try:     serie_json = GetResultFromNetwork(TVDB_SERIES_URL % TVDBid, additionalHeaders={'Accept-Language': lang} if lang!='en' else {})['data']
  except:  Log("Bad series data, no update for TVDB id: %s" % TVDBid);  return
  else:  #serie_json { "id","seriesId", "airsDayOfWeek", "imdbId", "zap2itId", "added", "addedBy", "lastUpdated", "seriesName", "aliases", "banner", "status", 
         #             "firstAired", "network", "networkId", "runtime", "genre, "overview", "airsTime", "rating" , "siteRating", "siteRatingCount" }
    Log.Info('TheTVDB.GetMetadata() - serie_json: {}'.format(serie_json))
    SaveDict( language_episodes.index(lang) if lang in language_episodes else len(language_episodes), TheTVDB_dict, 'language_rank')
    SaveDict( Dict(serie_json, 'imdbId' or IMDbid), TheTVDB_dict, 'IMDbid'           )
    SaveDict( Dict(serie_json, 'seriesName'), TheTVDB_dict, 'title'                  )
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
  episodes_json, episodes_json_page = [], {'links':{'next':1}}
  while Dict(episodes_json_page, 'links', 'next') not in (None, '', 'null'):
    episodes_json_page = GetResultFromNetwork(TVDB_EPISODES_URL % (TVDBid, Dict(episodes_json_page, 'links', 'next')), additionalHeaders={'Accept-Language': lang} if lang!='en' else {})['data']
    episodes_json.extend(episodes_json_page)  #SaveDict(Dict(episodes_json_page), episodes_json) 
  Log.Info('TheTVDB.GetMetadata() - TVDB_EPISODES_URL: {}'.format(TVDB_EPISODES_URL % (TVDBid, Dict(episodes_json_page, 'links', 'next'))))
  
  tvdb_special_missing, summary_missing_special, summary_missing, summary_present, episode_missing, abs_manual_placement_info = [], [], [], [], [], []
  abs_number, missing_abs_nb = 1, False
  for episode_json in episodes_json:
    
    ### Get the season and episode numbers
    season  = str(Dict(episode_json, 'airedSeason'       ) or Dict(episode_json, 'dvdSeason'       ))
    episode = str(Dict(episode_json, 'airedEpisodeNumber') or Dict(episode_json, 'dvdEpisodeNumber'))
    #Log.Info('s{:>2}e{:>3} ep: {}'.format(season, episode, episode_json))
    if metadata_source in ("tvdb4", "tvdb5") and not season=='0':  season='1'
    if season!='0' and (metadata_source=="anidb" and defaulttvdbseason=="a" and max(map(int, media.seasons.keys()))==1 or metadata_source in ("tvdb3", "tvdb4", "tvdb5")):
      abs_number = str(Dict(episode_json, 'absoluteNumber'))
      if not episode:           episode = abs_number, missing_abs_nb = abs_number, True;  abs_manual_placement_info.append("s%se%s = abs %s" % (str(Dict(episode_json, 'airedSeason')), str(Dict(episode_json, 'airedEpisodeNumber')), str(Dict(episode_json, 'absoluteNumber'))))
      elif not missing_abs_nb:  episode = abs_number #update abs_number with real abs number
      elif episode !=str(abs_number):
        Log.Error("TheTVDB.GetMetadata() - Abs number (s{}e{}) present after manually placing our own abs numbers ({})".format(str(Dict(episode_json, 'airedSeason')), str(Dict(episode_json, 'airedEpisodeNumber')), abs_number))
        continue
    numbering = "s{}e{}".format(season, episode)
    
    SaveDict( abs_number                       , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'absolute_index'         )
    SaveDict( Dict(serie_json  , 'rating'     ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'content_rating'         )
    SaveDict( Dict(serie_json  , 'runtime'    ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'duration'               )
    SaveDict( Dict(episode_json, 'episodeName'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title'                  )
    SaveDict( Dict(episode_json, 'firstAired' ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at') 
      
    ### Missing summaries logs ###
    if SaveDict( Dict(episode_json, 'overview'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary'):  summary_present.append(numbering)
    elif season!='0':                                                                                               summary_missing.append(numbering)
    else:                                                                                                           summary_missing_special.append(numbering)
  
    ### Check for Missing Episodes ### and tvdb mode
    if (not movie and metadata_source.startswith("tvdb") or max(map(int, media.seasons.keys()))>1) and metadata_source != 'tvdb5' and \
      not (metadata_source in ('tvdb',  'tvdb2') and season in media.seasons and episode in media.seasons[season].episodes) and \
      not (metadata_source in ('tvdb3', 'tvdb4') and season >=1 and [True for s in media.seasons if episode in media.seasons[s].episodes]):
      air_date = Dict(episode_json, 'FirstAired')
      air_date = int(air_date.replace('-','')) if air_date.replace('-','').isdigit() and int(air_date.replace('-','')) > 10000000 else 99999999
      if int(time.strftime("%Y%m%d")) <= air_date+1:  pass  #Log.Warn("TheTVDB.GetMetadata() - Episode '{}' missing but not aired/missing '{}'".format(numbering, air_date))
      elif season=='0':                               tvdb_special_missing.append(episode)                                                          #Log.Info("TVDB l176 - type of episode_missing: " + type(episode_missing).__name__)
      else:                                           episode_missing.append( str(abs_number)+" ("+numbering+")" if metadata_source in ('tvdb3', 'tvdb4') else numbering)  #Log.Info("TVDB - type of tvdb_special_missing: " + type(tvdb_special_missing).__name__)
    
    if season!='0':  abs_number += 1
      
    ### Ep advance information ###
    id = str(Dict(episode_json, 'id'))
    episode_details_json = GetResultFromNetwork(TVDB_EPISODE_DETAILS_URL + id, additionalHeaders={'Accept-Language': language_episodes[0]} if language_episodes and language_episodes[0]!='en' else {})['data']
    if episode_details_json:
      #Log.Info(episode_details_json)  #firstAired, overview, episodeName, seriesId, dvdDiscid, absoluteNumber, imdbId, firstAired
      SaveDict( Dict(episode_details_json, 'writers'            ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'writers'                )
      SaveDict( Dict(episode_details_json, 'directors'          ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'directors'              )
      SaveDict( Dict(episode_details_json, 'guestStars'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'guest_stars'            ) 
      SaveDict( Dict(episode_details_json, 'siteRating'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating'                 )
      file = Dict(episode_details_json, 'filename')  # KeyError: u'http://thetvdb.plexapp.com/banners/episodes/81797/383792.jpg' avoided below with str()
      if file:  SaveDict((str("TheTVDB/episodes/"+ os.path.basename(file)), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', str(TVDB_IMG_ROOT+file))
    
    # Std ep info loaded for Library language ten details for 1st language, loading other languages if needed
    rank = len(language_episodes)
    if lang                  in language_episodes and Dict(episode_json,         'episodeName'):  rank=language_episodes.index(lang)
    if language_episodes and language_episodes[0] and Dict(episode_details_json, 'episodeName'):  rank=0
    SaveDict( rank, TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')
    #Log.Info('array: {} after disregarding too high indexes'.format(language_episodes[1:rank-1]))
    for lang_rank, language in enumerate(language_episodes[1:rank-1] if len(language_episodes)>1 and rank>=2 else []):
      if not language:  continue
      episode_details_json = GetResultFromNetwork(TVDB_EPISODE_DETAILS_URL + id, additionalHeaders={'Accept-Language': language} if language!='en' else {})['data']
      if Dict(episode_details_json, 'language', 'episodeName') and Dict(episode_details_json, 'episodeName'):  
        SaveDict( Dict(episode_details_json, 'episodeName'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title')
        SaveDict( lang_rank                                , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')
        rank=lang_rank
        break
      else:  Log.Info('no ep title in language: {}'.format(language_episodes[lang_rank]))
  
  ### Collection ###  # get all anidbids sharing the same tvdbids
  
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
  try:              bannerTypes = GetResultFromNetwork(TVDB_SERIES_IMG_INFO_URL % TVDBid, additionalHeaders={'Accept-Language': language} if language!='en' else {})['data']
  except KeyError:  Log("Invalid image JSON from url: " + TVDB_SERIES_IMG_INFO_URL % TVDBid)
  else:             #JSON format = {"fanart", "poster", "season", "seasonwide", "series"}
    metanames         = {'fanart': "art", 'poster': "posters", 'series': "banners", 'season': "seasons", 'seasonwide': 'seasonwide'}#
    count_valid       = {key: 0 for key in metanames}
    anidb_offset      = sorted(Dict(mappingList, 'poster_id_array', TVDBid).keys()).index(AniDBid) if AniDBid in Dict(mappingList, 'poster_id_array', TVDBid) else 0  
    language_priority = [item.strip() for item in Prefs['EpisodeLanguagePriority'].split(',')]
    Log.Info("TheTVDB.GetMetadata() - bannerTypes: {}, anidb_offset: {}, AniDBid: {}, anidb_array: {}".format(bannerTypes, anidb_offset, AniDBid, str((Dict(mappingList, 'poster_id_array', TVDBid) or {}).keys())))
    for bannerType in bannerTypes:
      
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
        if bannerType == 'season':  SaveDict((image['fileName'], rank, thumbnail), TheTVDB_dict, 'seasons', str(int(image['subKey'])+(0 if Dict(mappingList, 'defaulttvdbseason')=="0" or not Dict(mappingList, 'defaulttvdbseason').isdigit() else int(Dict(mappingList, 'defaulttvdbseason'))-1)), 'posters', TVDB_IMG_ROOT + Dict(image, 'BannerPath'))
        else:                       SaveDict((image['fileName'], rank, thumbnail), TheTVDB_dict, metanames[bannerType], TVDB_IMG_ROOT + image['fileName'])
        if bannerType in ('poster', 'season'):  Log.Info("[!] bannerType: {}, subKey: {:>2}, rank: {:>3}, filename: {}, thumbnail: {}, resolution: {}, average: {}, count: {}".format( metanames[bannerType], Dict(image, 'subKey'), rank, TVDB_IMG_ROOT + Dict(image, 'fileName'), TVDB_IMG_ROOT + Dict(image, 'thumbnail'), Dict(image, 'resolution'), Dict(image, 'ratingsInfo','average'), Dict(image, 'ratingsInfo', 'average', 'count') ))
        count_valid[bannerType] = count_valid[bannerType] + 1  #Otherwise with += SyntaxError: Line 142: Augmented assignment of object items and slices is not allowed
        
    Log.Info("TheTVDB.GetImages() - Posters : {}/{}, Season posters: {}/{}, Art: {}/{}".format(count_valid['poster'], Dict(bannerTypes, 'poster'), count_valid['season'], Dict(bannerTypes, 'season') or 0, count_valid['fanart'], Dict(bannerTypes, 'fanart')))
    if not Dict(bannerTypes, 'poster'):  error_log['TVDB posters missing'       ].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    if not Dict(bannerTypes, 'season'):  error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    
  Log.Info('TheTVDB_dict fields: {}'.format(TheTVDB_dict.keys()))
  Log.Info('TheTVDB_dict["posters"]: {}'.format(Dict(TheTVDB_dict, 'posters')))
  #Log.Info('TheTVDB_dict:        {}'.format(TheTVDB_dict))
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
