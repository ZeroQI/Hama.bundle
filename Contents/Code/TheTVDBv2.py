### TheTVDB.com API v2 ###
# http://thetvdb.com/api/A27AD9BE0DA63333/series/103291/all/en.xml

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
import os
import time
from common     import GetXml, SaveDict, UpdateDict, Dict, natural_sort_key
from AnimeLists import tvdb_ep, anidb_ep
#import re, unicodedata, hashlib, types
#from collections import defaultdict

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'
TVDB_API_KEY               = 'A27AD9BE0DA63333'
TVDB_IMG_ROOT              = 'https://thetvdb.plexapp.com/banners/' 
TVDB_BASE_URL              = 'https://api.thetvdb.com'  #'https://api-beta.thetvdb.com' #tvdb v2 plex proxy site'' # TODO Start using TVDB's production api (TVDB is behind CF) when available and possibly a plex proxy for it
TVDB_LOGIN_URL             = TVDB_BASE_URL + '/login'
TVDB_SERIES_URL            = TVDB_BASE_URL + '/series/%s'
TVDB_EPISODES_URL          = TVDB_BASE_URL + '/series/%s/episodes?page=%s'
TVDB_EPISODE_DETAILS_URL   = TVDB_BASE_URL + '/episodes/'                          #+EpId
TVDB_ACTORS_URL            = TVDB_BASE_URL + '/series/%s/actors'
TVDB_SERIES_IMG_INFO_URL   = TVDB_BASE_URL + '/series/%s/images'
TVDB_SERIES_IMG_QUERY_URL  = TVDB_BASE_URL + '/series/{}/images/query?keyType={}'
TVDB_SEARCH_URL            = TVDB_BASE_URL + '/search/series?name=%s'
#THETVDB_LANGUAGES_CODE     = { 'cs': '28', 'da': '10', 'de': '14', 'el': '20', 'en':  '7', 'es': '16', 'fi': '11', 'fr': '17', 'he': '24', 
#                               'hr': '31', 'hu': '19', 'it': '15', 'ja': '25', 'ko': '32', 'nl': '13', 'no':  '9', 'pl': '18', 'pt': '26',
#                               'ru': '22', 'sv':  '8', 'tr': '21', 'zh': '27', 'sl': '30'}
HEADERS                    = {'User-agent': 'Plex/Nine'}
   
### Functions ###  
  
def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList, AniDB_movie):
  ''' TVDB - Load serie JSON
  '''
  Log.Info("".ljust(157, '-'))
  if not TVDBid.isdigit(): Log.Info('TheTVDB.GetMetadata() - TVDBid empty');  return {}, IMDbid
  TheTVDB_dict      = {}
  anidb_numbering   = metadata_source=="anidb" and (movie or max(map(int, media.seasons.keys()))<=1)
  anidb_prefered    = anidb_numbering and Dict(mappingList, 'defaulttvdbseason') not in ('a', '1')
  language_series   = [language.strip() if language.strip() not in ('x-jat', 'zh-Hans', 'zh-Hant', 'zh-x-yue', 'zh-x-cmn', 'zh-x-nan') else '' for language in Prefs['SerieLanguagePriority'  ].split(',') ]
  language_episodes = [language.strip() if language.strip() not in ('x-jat', 'zh-Hans', 'zh-Hant', 'zh-x-yue', 'zh-x-cmn', 'zh-x-nan') else '' for language in Prefs['EpisodeLanguagePriority'].split(',') ]
  Log.Info("TheTVDB.GetMetadata() - TVDBid: '{}', IMDbid: '{}', language_series : {}, language_episodes: {}".format(TVDBid, IMDbid, language_series , language_episodes))
  
  ### TVDB Series JSON ###
  serie_json = Dict(common.LoadFile(filename='series_{}.json'.format(lang), relativeDirectory="TheTVDB/json/"+TVDBid, url=(TVDB_SERIES_URL % TVDBid)+'?'+lang, cache=CACHE_1DAY, headers={'Content-type': 'application/json', 'Accept-Language': lang}), 'data')
  if serie_json:
    #serie_json { "id","seriesId", "airsDayOfWeek", "imdbId", "zap2itId", "added", "addedBy", "lastUpdated", "seriesName", "aliases", "banner", "status", 
    #             "firstAired", "network", "networkId", "runtime", "genre, "overview", "airsTime", "rating" , "siteRating", "siteRatingCount" }
    SaveDict( language_series.index(lang) if lang in language_series and not anidb_prefered else len(language_series), TheTVDB_dict, 'language_rank')
    SaveDict( Dict(serie_json, 'seriesName'), TheTVDB_dict, 'title'                  )
    SaveDict( Dict(serie_json, 'seriesName'), TheTVDB_dict, 'original_title'         )
    SaveDict( Dict(serie_json, 'imdbId' or IMDbid), TheTVDB_dict, 'IMDbid'           )
    SaveDict( Dict(serie_json, 'zap2it_id' ), TheTVDB_dict, 'zap2itId'               )
    SaveDict( Dict(serie_json, 'rating'    ), TheTVDB_dict, 'content_rating'         )
    if not anidb_prefered:  SaveDict( Dict(serie_json, 'overview'  ), TheTVDB_dict, 'summary'                )
    SaveDict( Dict(serie_json, 'firstAired'), TheTVDB_dict, 'originally_available_at')
    SaveDict( Dict(serie_json, 'genre'     ), TheTVDB_dict, 'genres'                 )
    SaveDict( Dict(serie_json, 'network'   ), TheTVDB_dict, 'studio'                 )
    SaveDict( Dict(serie_json, 'siteRating'), TheTVDB_dict, 'rating'                 )
    SaveDict( Dict(serie_json, 'status'    ), TheTVDB_dict, 'status'                 )
    if Dict(serie_json, 'runtime') and Dict(serie_json, 'runtime').isdigit():
      Log.Info('[ ] duration: {}'.format(Dict(serie_json, 'runtime')))
      SaveDict(int(Dict(serie_json, 'runtime'))*60*1000, TheTVDB_dict, 'duration')  #in ms in plex
    if Dict(serie_json, 'banner'):                                             
      Log.Info('[ ] banner: {}'.format(TVDB_IMG_ROOT+Dict(serie_json, 'banner')))
      SaveDict((os.path.join('TheTVDB', 'banner', Dict(serie_json, 'banner')), 1, None), TheTVDB_dict, 'banners', TVDB_IMG_ROOT+Dict(serie_json, 'banner'))
    
    ### TVDB Series Actors JSON ###
    actor_json = Dict(common.LoadFile(filename='actors_{}.json'.format(lang), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_ACTORS_URL % TVDBid, cache=CACHE_1DAY, headers={'Content-type': 'application/json', 'Accept-Language': lang}), 'data')
    if actor_json:               #JSON format: 'data': [{"seriesId", "name", "image", "lastUpdated", "imageAuthor", "role", "sortOrder", "id", "imageAdded", },...]
      for role in actor_json or []:
        try:                    SaveDict([{'role': Dict(role, 'role'), 'name': Dict(role, 'name'), 'photo': TVDB_IMG_ROOT + role['image'] if Dict(role, 'image') else ''}], TheTVDB_dict, 'roles')
        except Exception as e:  Log.Info("'roles' - error: '{}', role: '{}'".format(str(e), str(role)))
      #common.DisplayDict(actor_json, ['role', 'name', 'image'])
      
    ### Load pages of episodes ###
    episodes_json, page = [], 1
    while page not in (None, '', 'null'):
      episodes_json_page = common.LoadFile(filename='episodes_page{}_{}.json'.format(page, lang), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_EPISODES_URL % (TVDBid, page), cache=CACHE_1DAY, headers={'Content-type': 'application/json', 'Accept-Language': lang})
      episodes_json.extend(Dict(episodes_json_page, 'data'))  #Log.Info('TVDB_EPISODES_URL: {}, links: {}'.format(TVDB_EPISODES_URL % (TVDBid, page), Dict(episodes_json_page, 'links')))
      page = Dict(episodes_json_page, 'links', 'next')
    
    sorted_episodes_json = {}
    for episode_json in episodes_json: sorted_episodes_json['s{:02d}e{:03d}'.format(Dict(episode_json, 'airedSeason'), Dict(episode_json, 'airedEpisodeNumber'))] = episode_json
    sorted_episodes_index_list = sorted(sorted_episodes_json, key=natural_sort_key)  #Log.Info('len: {}, sorted_episodes_index_list: {}'.format(len(sorted_episodes_index_list), sorted_episodes_index_list))
    
    ### Build list_abs_eps for tvdb 3/4/5 ###
    list_abs_eps, list_sp_eps={}, []
    if metadata_source in ('tvdb3', 'tvdb4'):
      for s in media.seasons:
        for e in media.seasons[s].episodes:
           if s=='0':  list_sp_eps.append(e)
           else:       list_abs_eps[e]=s 
      Log.Info('Present abs eps: {}'.format(list_abs_eps))
    
    absolute_numering = metadata_source in ('tvdb3', 'tvdb4', 'tvdb5')
    
    ### episode loop ###
    tvdb_special_missing, summary_missing_special, summary_missing, summary_present, episode_missing, abs_manual_placement_info = [], [], [], [], [], []
    abs_number, missing_abs_nb, ep_count = 0, False, 0
    for index in sorted_episodes_index_list:
      
      # Episode and Absolute number calculation engine, episode translation
      episode_json = sorted_episodes_json[index]  #Log.Info('s{:02d}e{:03d} abs: {:03d} ep: {}'.format(Dict(episode_json, 'airedSeason') or 0, Dict(episode_json, 'airedEpisodeNumber') or 0, Dict(episode_json, 'absoluteNumber') or 0, episode_json))
      season       = str(Dict(episode_json, 'airedSeason'       ))
      episode      = str(Dict(episode_json, 'airedEpisodeNumber'))
      if season!='0':  
        abs_number = abs_number + 1
        if not Dict(episode_json, 'absoluteNumber'):  missing_abs_nb = True
        elif missing_abs_nb or Dict(episode_json, 'absoluteNumber')!=abs_number:  
          Log.Error("(s{}e{}) Abs number {:>3} different from readings ({}), possibly tv special".format(season, episode, abs_number, Dict(episode_json, 'absoluteNumber')))
          abs_manual_placement_info.append("s{}e{} = json abs ep {} / abs_number {}".format(season, episode, Dict(episode_json, 'absoluteNumber'), abs_number))
          missing_abs_nb = False
          abs_number     = Dict(episode_json, 'absoluteNumber')
          
      ### Missing summaries logs ###
      numbering = "s{}e{}".format(season, episode)
      if Dict(episode_json, 'overview'):  summary_present.append(numbering)
      elif season!='0':                   summary_missing.append(numbering)
      else:                       summary_missing_special.append(numbering)
      
      ### ep translation
      anidbid=""
      #if anidb_numbering: 
      #  if Dict(mappingList, 'defaulttvdbseason')!="a" or season=='0':      season, episodex, anidbid = anidb_ep(mappingList, season, episode)
      #  else:                                                               season, episode = '1', str(abs_number)
      #elif metadata_source in ('tvdb3', "tvdb4", "tvdb5") and season!='0':  season, episode = '1', str(abs_number)
      if anidb_numbering: season, episode, anidbid = anidb_ep(mappingList, season, episode)
      elif metadata_source in ('tvdb3', "tvdb4", "tvdb5") and season!='0':  season, episode = '1', str(abs_number)
      
      ### Check for Missing Episodes ###
      if not(season =='0' and episode in list_sp_eps) and \
         not(metadata_source in ('tvdb3', 'tvdb4') and str(abs_number) in list_abs_eps) and \
         not(not movie and season in media.seasons and episode in media.seasons[season].episodes):
        Log.Info('[ ] {:>7} s{:0>2}e{:0>3} anidbid: {:>7} air_date: {}'.format(numbering, season, episode, anidbid, Dict(episode_json, 'FirstAired')))
        air_date = Dict(episode_json, 'FirstAired')
        air_date = int(air_date.replace('-','')) if air_date.replace('-','').isdigit() and int(air_date.replace('-','')) > 10000000 else 99999999
        if int(time.strftime("%Y%m%d")) <= air_date+1:  pass #Log.Info("TVDB - Episode '{}' missing but not aired/missing '{}'".format(numbering, air_date))
        elif season=='0':                               Log.Info("TVDB - type of episode_missing: "      +      type(episode_missing).__name__);  tvdb_special_missing.append(episode)
        else:                                           Log.Info("TVDB - type of tvdb_special_missing: " + type(tvdb_special_missing).__name__);  episode_missing.append( str(abs_number)+" ("+numbering+")" if metadata_source in ('tvdb3', 'tvdb4') else numbering)
        
      ### File present on disk
      else:
        #Log.Info('[?] episode_json: {}'.format(episode_json))
        Log.Info('[X] {:>7} s{:0>2}e{:0>3} anidbid: {:>7} air_date: {} abs_number: {}, title: {}'.format(numbering, season, episode, anidbid, Dict(episode_json, 'FirstAired'), abs_number, Dict(episode_json, 'episodeName')))
        if not anidb_numbering:  
          SaveDict( abs_number                       , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'absolute_index'         )
        SaveDict( Dict(serie_json  , 'rating'     ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'content_rating'         )
        SaveDict( Dict(serie_json  , 'runtime'    ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'duration'               )
        SaveDict( Dict(episode_json, 'overview'   ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary'                );  Log.Info('[ ] summary: {}'.format(Dict(episode_json, 'overview')))
        SaveDict( Dict(episode_json, 'firstAired' ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at') 
        
        # Title from serie page
        if Dict(episode_json, 'episodeName'):
          rank  = language_episodes.index(lang) if lang in language_episodes else len(language_episodes)
          title = Dict(episode_json, 'episodeName')
        else:                                  rank, title = len(language_episodes)+1, ''
        Log.Info("[1] rank: {:>1}, language: {:>4}, title: {}".format(rank, Dict(episode_json, 'language', 'episodeName'), title))
        
        ### Ep advance information ###
        ep_count += 1
        for lang2 in language_episodes:
          if lang2 not in (lang, ''):  break
        else: lang2 = 'en' 
        episode_details_json = Dict(common.LoadFile(filename='episode_{}_{}.json'.format(Dict(episode_json, 'id'), lang2), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_EPISODE_DETAILS_URL + str(Dict(episode_json, 'id')), cache=CACHE_1DAY, headers={'Content-type': 'application/json', 'Accept-Language': lang2}), 'data')
        if episode_details_json:
          
          # Std ep info loaded for Library language ten details for 1st language, loading other languages if needed
          if lang2 in language_episodes and language_episodes.index(lang2)<rank and Dict(episode_details_json, 'language', 'episodeName')==lang2:
            rank  = language_episodes.index(lang2) 
            title = Dict(episode_details_json, 'episodeName')
            Log.Info('[2] language_rank: {:>1}, language: {:>4}, title: {}'.format(rank, lang2, title))
          
          SaveDict( Dict(episode_details_json, 'writers'            ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'writers'    )
          SaveDict( Dict(episode_details_json, 'directors'          ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'directors'  )
          SaveDict( Dict(episode_details_json, 'guestStars'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'guest_stars') 
          SaveDict( Dict(episode_details_json, 'siteRating'         ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating'     )
          
          # Episode screenshoT/Thumbnail
          if Dict(episode_details_json, 'filename'):  SaveDict((str("TheTVDB/episodes/"+ os.path.basename(Dict(episode_details_json, 'filename'))), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', str(TVDB_IMG_ROOT+Dict(episode_details_json, 'filename')))
          else:                                       Log.Info('[!] episode_details_json: {}'.format(episode_details_json))
        
          Log.Info('[ ] thumb: {}'.format(TVDB_IMG_ROOT+Dict(episode_details_json, 'filename') if Dict(episode_details_json, 'filename') else ''))
        
        #  
        for lang_rank, language in enumerate(language_episodes[1:rank-1] if len(language_episodes)>1 and rank>=2 else []):
          if not language:  continue
          episode_details_json = Dict(common.LoadFile(filename='episode_{}_{}.json'.format(Dict(episode_json, 'id'), language), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_EPISODE_DETAILS_URL + str(Dict(episode_json, 'id')), cache=CACHE_1DAY, headers={'Content-type': 'application/json', 'Accept-Language': lang}), 'data', default={})
          if Dict(episode_details_json, 'episodeName') :  
            title = Dict(episode_details_json, 'episodeName')
            rank  = lang_rank
            Log.Info('[3] language_rank: {}, title: {}'.format(rank, title))
            break
          else:  Log.Info('no ep title in language: {}'.format(language_episodes[lang_rank]))
        SaveDict( title, TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title'        )
        SaveDict( rank , TheTVDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')      
        #Log.Info('[?] numbering: {} => s{:>1}e{:>3} language_rank: {:>1}, title: "{}"'.format(numbering, season, episode, rank, title))
        Log.Info('-------------')
            
    ### Collection ###  # get all anidbids sharing the same tvdbids
    if not movie:
      ### Logging ###
      if summary_missing:          error_log['Missing Episode Summaries'].append("TVDBid: %s | Title: '%s' | Missing Episode Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing        )))
      if summary_missing_special:  error_log['Missing Special Summaries'].append("TVDBid: %s | Title: '%s' | Missing Special Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing_special)))
      if episode_missing:          error_log['Missing Episodes'         ].append("TVDBid: %s | Title: '%s' | Missing Episodes: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(episode_missing        )))
      if tvdb_special_missing:     error_log['Missing Specials'         ].append("TVDBid: %s | Title: '%s' | Missing Specials: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(tvdb_special_missing   )))
      #Log.Info("abs_manual_placement_info: " + str(abs_manual_placement_info))
      #Log.Debug("Episodes without Summary: " + str(sorted(summary_missing, key=natural_sort_key)))
      
    ### Picture types JSON download ###
    language_posters = [language.strip() for language in Prefs['PosterLanguagePriority'].split(',')]
    priority_posters = [  source.strip() for source   in Prefs['posters'               ].split(',')]
    Log.Info('language_posters: {}'.format(language_posters))
    Log.Info('==========================')
    for language in language_posters:
      try:
        if not language=='ja':  bannerTypes = Dict(common.LoadFile(filename='images_{}.json'.format(language), relativeDirectory="TheTVDB/json/"+TVDBid, url=(TVDB_SERIES_IMG_INFO_URL % TVDBid), cache=0, headers={'Content-type': 'application/json', 'Accept-Language': language}), 'data', default={})
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
          #if anidb_numbering and Dict(mappingList, 'defaulttvdbseason') not in ('a', '1') and bannerType=='poster':  continue  #skip if anidb numbered serie mapping to season 0 or 2+
          
          Log.Info('------------------------------')
          try:     images = Dict( common.LoadFile(filename='images_{}_{}.json'.format(bannerType, language), relativeDirectory="TheTVDB/json/"+TVDBid, url=TVDB_SERIES_IMG_QUERY_URL.format(TVDBid, bannerType), cache=CACHE_1DAY, headers={'Accept-Language': language}), 'data', default={})
          except:  images = {};  Log("Bad image type query data for TVDB id: %s (bannerType: %s)" % (TVDBid, bannerType)) 
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
                  if Dict(mappingList, 'defaulttvdbseason')==str(image['subKey']) or Dict(mappingList, 'defaulttvdbseason')=='a' and str(image['subKey'])=='1': #anidb numbering, season poster as poster
                    SaveDict(('TheTVDB/'+image['fileName'], rank, thumbnail), TheTVDB_dict, 'posters', TVDB_IMG_ROOT + image['fileName'])
                  #if str(image['subKey'])=='0' or Dict(mappingList, 'defaulttvdbseason')==str(image['subKey']) or Dict(mappingList, 'defaulttvdbseason')=='a' and str(image['subKey'])=='1':
                  if str(image['subKey']) in ('0', '1' if Dict(mappingList, 'defaulttvdbseason')=='a' else Dict(mappingList, 'defaulttvdbseason')):
                    SaveDict(('TheTVDB/'+image['fileName'], 1 if rank==3 else 3 if rank==1 else rank, thumbnail), TheTVDB_dict, 'seasons', '0' if str(image['subKey'])=='0' else '1', 'posters', TVDB_IMG_ROOT + image['fileName'])  #if anidb_numbering else str(image['subKey'])
              elif bannerType=='fanart' or not anidb_numbering or Dict(mappingList, 'defaulttvdbseason') in ('a', '1') or str(image['subKey'] or '1')==Dict(mappingList, 'defaulttvdbseason') or not Dict(bannerTypes, 'season') and bannerType=='poster':
                SaveDict(('TheTVDB/'+image['fileName'], rank, thumbnail), TheTVDB_dict, metanames[bannerType], TVDB_IMG_ROOT + image['fileName'])   #use art + posters tvdb
              #if bannerType == 'season':  
              #  if anidb_numbering and ('1' if Dict(mappingList, 'defaulttvdbseason')=='a' else Dict(mappingList, 'defaulttvdbseason'))==str(image['subKey']):
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
      Log.Info('==========================')

    Log.Info("url: '{}', IMDbid: {}, Present episodes: {}, Missing: {}".format(TVDB_SERIES_URL % TVDBid, IMDbid, ep_count, sorted(episode_missing, key=natural_sort_key)))
    
  Log.Info('TheTVDB_dict: {}'.format(TheTVDB_dict))
  return TheTVDB_dict, IMDbid
  
def Search (results,  media, lang, manual, movie):  #if maxi<50:  maxi = tvdb.Search_TVDB(results, media, lang, manual, movie)
  '''search for TVDB id series
  '''
  #series_data = JSON.ObjectFromString(GetResultFromNetwork(TVDB_SEARCH_URL % mediaShowYear, additionalHeaders={'Accept-Language': lang}))['data'][0]
  TVDB_SERIE_SEARCH = 'http://thetvdb.com/api/GetSeries.php?seriesname='
  orig_title = ( media.title if movie else media.show )
  maxi = 0
  try:                    TVDBsearchXml = XML.ElementFromURL( TVDB_SERIE_SEARCH + orig_title.replace(" ", "%20"), cacheTime=CACHE_1HOUR * 24)
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
