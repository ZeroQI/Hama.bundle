### TheTVDB.com ###
# http://thetvdb.com/api/A27AD9BE0DA63333/series/103291/all/en.xml

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
import os
import time
from common import GetMeta, GetXml, SaveDict, Dict, natural_sort_key
from AnimeLists import tvdb_ep

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'
TVDB_IMAGES_URL  = 'http://thetvdb.plexapp.com/banners/'  
      
### Functions ###  

### TVDB - Load serie XML ###
def GetMetadata(media, movie, error_log, lang, metadata_source, AniDBid, TVDBid, IMDbid, mappingList):
  Log.Info("".ljust(157, '-'))
  Log.Info("TheTVDB.GetMetadata() - TVDBid: '{}', IMDbid: '{}'".format(TVDBid, IMDbid))
  if not TVDBid.isdigit(): return {}, IMDbid
  
  API_SERIE_URL     = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/{}/all/{}.xml'.format(TVDBid, lang)    # Serie XML from TVDB ID
  API_ACTORS_URL    = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/{}/actors.xml'.format(TVDBid)  # roles with pics
  TVDB_BANNERS_URL  = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/{}/banners.xml'                        # TVDB Serie pictures xml: fanarts, posters, banners
  defaulttvdbseason = Dict(mappingList, 'defaulttvdbseason')
  TheTVDB_dict      = {}
  xml               = common.LoadFile(filename=TVDBid+".xml", relativeDirectory=os.path.join('TheTVDB', 'xml'), url=API_SERIE_URL.replace('.com', '.plexapp.com'), cache= CACHE_1WEEK) or \
                      common.LoadFile(filename=TVDBid+".xml", relativeDirectory=os.path.join('TheTVDB', 'xml'), url=API_SERIE_URL,                                 cache= CACHE_1WEEK)
  if not xml:  Log.Info("TheTVDB.GetMetadata() - url failed: '{}'".format(API_SERIE_URL))
  else:
    try:     xml = xml.xpath('/Data')[0]
    except:  return {}, ""
    IMDbid    = IMDbid or GetXml(xml, 'Series/IMDB_ID')
    zap2it_id = GetXml(xml, 'Series/zap2it_id');
    Log.Info("TheTVDB.GetMetadata() - TVDBid: '{}', IMDbid: {}, url: '{}'".format(TVDBid, IMDbid, API_SERIE_URL))
    
    SaveDict( GetXml(xml, 'Series/Overview'         ),                  TheTVDB_dict, 'summary'                )
    SaveDict( GetXml(xml, 'Series/ContentRating'    ),                  TheTVDB_dict, 'content_rating'         )
    SaveDict( GetXml(xml, 'Series/Network'          ),                  TheTVDB_dict, 'studio'                 )
    SaveDict( GetXml(xml, 'Series/Rating'           ),                  TheTVDB_dict, 'rating'                 )
    SaveDict( GetXml(xml, 'Series/FirstAired'       ),                  TheTVDB_dict, 'originally_available_at')
    SaveDict( GetXml(xml, 'Series/Status'           ),                  TheTVDB_dict, 'status'                 )
    SaveDict( GetXml(xml, 'Series/Genre' ).strip('|'),                  TheTVDB_dict, 'genres'                 )
    SaveDict( GetXml(xml, 'Series/Actors').strip('|'),                  TheTVDB_dict, 'roles'                  )  #|Kana Hanazawa|Mamiko Noto|Yui Horie|Atsushi Abe|Yukari Tamura|
    SaveDict( GetXml(xml, 'Series/SeriesName'       ),                  TheTVDB_dict, 'title'                  )
    SaveDict( common.SortTitle(GetXml(xml, 'Series/SeriesName'), "en" if lang ==Locale.Language.English else lang), TheTVDB_dict, 'title_sort'             )
        
    if GetXml(xml, 'Series/Runtime').isdigit():  SaveDict(int(GetXml(xml, 'Series/Runtime'))*60*1000,                      TheTVDB_dict, 'duration')  #in ms in plex
    if GetXml(xml, 'poster'                  ):  SaveDict((os.path.join('TheTVDB', 'xml', GetXml(ep, 'poster')), 1, None), TheTVDB_dict, 'posters', TVDB_IMAGES_URL+GetXml(ep, 'poster'))
    if GetXml(xml, 'fanart'                  ):  SaveDict((os.path.join('TheTVDB', 'xml', GetXml(ep, 'fanart')), 1, None), TheTVDB_dict, 'art'    , TVDB_IMAGES_URL+GetXml(ep, 'fanart'))
    if GetXml(xml, 'banner'                  ):  SaveDict((os.path.join('TheTVDB', 'xml', GetXml(ep, 'banner')), 1, None), TheTVDB_dict, 'banners', TVDB_IMAGES_URL+GetXml(ep, 'banner'))
    
    ### Absolute mode ###
    tvdb_special_missing, summary_missing_special, summary_missing, summary_present, episode_missing, abs_manual_placement_info = [], [], [], [], [], []
    abs_number, missing_abs_nb = 1, False
    for ep in xml.xpath('Episode') if not movie else []:
      season = GetXml(ep, 'SeasonNumber')
      if metadata_source in ("tvdb4", "tvdb5") and not season=='0':  season='1'
      if season!='0' and (metadata_source=="anidb" and defaulttvdbseason=="a" and max(map(int, media.seasons.keys()))==1 or metadata_source in ("tvdb3", "tvdb4", "tvdb5")):
        episode = GetXml(ep, 'absolute_number') 
        if episode and not missing_abs_nb:  abs_number = int(GetXml(ep, 'absolute_number') ) #update abs_number with real abs number
        if not episode :
          episode, missing_abs_nb = str(abs_number), True
          abs_manual_placement_info.append("s%se%s = abs %s" % (GetXml(ep, 'SeasonNumber'), GetXml(ep, 'EpisodeNumber'), GetXml(ep, 'absolute_number')))
        elif missing_abs_nb and episode !=str(abs_number):
          Log.Error("TheTVDB.GetMetadata() - Abs number (s{}e{}) present after manually placing our own abs numbers ({})".format(GetXml(ep, 'SeasonNumber'), GetXml(ep, 'EpisodeNumber'), abs_number))
          continue
      else:  episode = GetXml(ep, 'EpisodeNumber')
      numbering = "s{}e{}".format(season, episode)
      
      SaveDict( GetXml(ep, 'EpisodeName'     ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'title'                  )
      SaveDict( GetXml(ep, 'Director'        ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'directors'              )
      SaveDict( GetXml(ep, 'Writer'          ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'writers'                )
      SaveDict( GetXml(ep, 'Rating'          ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'rating'                 )
      SaveDict( GetXml(ep, 'GuestStars'      ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'guest_stars'            ) 
      SaveDict( GetXml(ep, 'FirstAired'      ), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at') 
            
      file = GetXml(ep, 'filename')  # KeyError: u'http://thetvdb.plexapp.com/banners/episodes/81797/383792.jpg' avoided below with str ???
      if file:  SaveDict((str("TVDB/episodes/"+ os.path.basename(file)), 1, None), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'thumbs', str(TVDB_IMAGES_URL+file))
      if file:  Log.Info("TheTVDB.GetMetadata() - numbering: '{}', file: '{}'".format(numbering, file))
  
      ### Missing summaries logs ###
      if SaveDict( GetXml(ep, 'Overview'), TheTVDB_dict, 'seasons', season, 'episodes', episode, 'summary'):  summary_present.append(numbering)
      elif season!='0':                                                                                       summary_missing.append(numbering)
      else:                                                                                                   summary_missing_special.append(numbering)
    
      ### Check for Missing Episodes ### and tvdb mode
      if (not movie and metadata_source.startswith("tvdb") or max(map(int, media.seasons.keys()))>1) and metadata_source != 'tvdb5' and \
        not (metadata_source in ('tvdb',  'tvdb2') and season in media.seasons and episode in media.seasons[season].episodes) and \
        not (metadata_source in ('tvdb3', 'tvdb4') and season >=1 and [True for s in media.seasons if episode in media.seasons[s].episodes]):
        air_date = GetXml(ep, 'FirstAired')
        air_date = int(air_date.replace('-','')) if air_date.replace('-','').isdigit() and int(air_date.replace('-','')) > 10000000 else 99999999
        if int(time.strftime("%Y%m%d")) <= air_date+1:  Log.Warn("TheTVDB.GetMetadata() - Episode '{}' missing but not aired/missing '{}'".format(numbering, air_date))
        elif season=='0':  tvdb_special_missing.append(episode)                                                          #Log.Info("TVDB l176 - type of episode_missing: " + type(episode_missing).__name__)
        else:              episode_missing.append( str(abs_number)+" ("+numbering+")" if metadata_source in ('tvdb3', 'tvdb4') else numbering)  #Log.Info("TVDB - type of tvdb_special_missing: " + type(tvdb_special_missing).__name__)
      
      if season!='0':  abs_number += 1
      
    ### Logging ###
    Log.Info("TheTVDB.GetMetadata(): abs_manual_placement_info: "+str(abs_manual_placement_info))
    if summary_missing:          error_log['Missing Episode Summaries'].append("TVDBid: %s | Title: '%s' | Missing Episode Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing        )))
    if summary_missing_special:  error_log['Missing Special Summaries'].append("TVDBid: %s | Title: '%s' | Missing Special Summaries: %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(summary_missing_special)))
    if episode_missing:          error_log['Missing Episodes'         ].append("TVDBid: %s | Title: '%s' | Missing Episodes: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(episode_missing        )))
    if tvdb_special_missing:     error_log['Missing Specials'         ].append("TVDBid: %s | Title: '%s' | Missing Specials: %s"          % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title'), str(tvdb_special_missing   )))
    Log.Debug("TheTVDB.GetMetadata() - TVDB - Episodes without Summary: " + str(sorted(summary_missing, key=natural_sort_key)))
    Log.Debug("TheTVDB.GetMetadata() - TVDB - Episodes missing: "         + str(sorted(episode_missing, key=natural_sort_key)))
    
  ### Actors ###
  if not Prefs["GetSingleOne"]: ###disabled for now
    if Dict(TheTVDB_dict, 'roles'):    #|Kana Hanazawa|Mamiko Noto|Yui Horie|Atsushi Abe|Yukari Tamura|
      xml = common.LoadFile(filename=TVDBid+"-actors.xml", relativeDirectory=os.path.join('TheTVDB', 'xml', 'actors'), url=API_ACTORS_URL.replace('.com', '.plexapp.com'), cache= CACHE_1WEEK) or \
            common.LoadFile(filename=TVDBid+"-actors.xml", relativeDirectory=os.path.join('TheTVDB', 'xml', 'actors'), url=API_ACTORS_URL,                                 cache= CACHE_1WEEK)  # AniDB title database loaded once every 2 weeks
      TheTVDB_dict['roles'] = []
      for role in xml.xpath('/Actors/Actor') if xml else []:
        try:                    SaveDict([{'role': role.find('Role').text, 'name': role.find('Name').text, 'photo': TVDB_IMAGES_URL + role.find('Image').text}], TheTVDB_dict, 'roles')
        except Exception as e:  Log.Info("TheTVDB.GetMetadata() - 'roles' - error: '{}', role: '{}'".format(str(e), str(role)))
  
  ### Picture XML download ###
  xml=common.LoadFile(filename=TVDBid+".banners.xml", relativeDirectory=os.path.join('TheTVDB', 'xml', 'banners'), url=TVDB_BANNERS_URL.format(TVDBid), cache= CACHE_1HOUR * 24 * 7)  # AniDB title database loaded once every 2 weeks
  if not xml:  Log.Info("TheTVDB.GetMetadata() - XML loading failed")
  else:
    metanames     = {'fanart': "art", 'poster': "posters", 'series': "banners", 'season': "seasons"}
    count         = {key: 0 for key in metanames}
    count_valid   = {key: 0 for key in metanames}
    poster_total  = len([True for banner in xml.xpath('/Banners/Banner') if GetXml(banner, 'BannerType')=="poster"])
    anidb_array   = Dict(mappingList, 'poster_id_array', TVDBid) or {}
    anidb_offset  = sorted(anidb_array.keys()).index(AniDBid) if AniDBid in anidb_array else 0  
    Log.Info( "TheTVDB.GetMetadata() - anidb_offset: {}, AniDBid: {}, anidb_array: {}".format(anidb_offset, AniDBid, str(anidb_array.keys())))
    for banner in xml.xpath('/Banners/Banner'): 
      
      ### Banner Types ###  #seriesName  = GetXml(banner, 'SeriesName'   )
      bannerType        = GetXml(banner, 'BannerType' )
      bannerType2       = GetXml(banner, 'BannerType2')
      metaname          = metanames['poster' if bannerType=='season' else bannerType]
      count[bannerType] = count[bannerType] + 1
      
      ### Season Posters ###
      season = GetXml(banner, 'Season')
      #if bannerType=='season':  season = str( (int(season) if season.isdigit() else 1) + (0 if defaulttvdbseason=="0" or not defaulttvdbseason.isdigit() else int(defaulttvdbseason)-1))
        
      ### Rank ###
      rank = 1 if bannerType=='poster' and anidb_offset == divmod(count_valid['poster'], poster_total)[1] else count_valid[bannerType]+2
      language = GetXml(banner, 'Language')
      if Prefs['localart']:
        language_priority = [item.strip() for item in Prefs['EpisodeLanguagePriority'].split(',')]
        rank += 10*language_priority.index(language) if language and language in language_priority else 50
      if bannerType in ('poster', 'season'):  Log.Info("[!] bannerType: {}, season: {:>2}, rank: {:>3}, language: {:>2}, filename: {}".format(bannerType, season, rank, language, GetXml(banner, 'BannerPath')))
      
      ### Adding picture ###
      url       = TVDB_IMAGES_URL + GetXml(banner, 'BannerPath')
      filename  = "TVDB/"         + GetXml(banner, 'BannerPath')
      thumb_url = TVDB_IMAGES_URL + GetXml(banner, 'ThumbnailPath') if GetXml(banner, 'ThumbnailPath') else None
      if not GetMeta('TheTVDB', metaname):                                               continue
      if movie and not bannerType in ('fanart', 'poster') or bannerType2=='seasonwide':  continue
      if bannerType == 'season':  SaveDict((filename, rank, thumb_url), TheTVDB_dict, 'seasons', season, 'posters', url)
      else:                       SaveDict((filename, rank, thumb_url), TheTVDB_dict, metaname, url)
      count_valid[bannerType] = count_valid[bannerType] + 1  #Otherwise SyntaxError: Line 142: Augmented assignment of object items and slices is not allowed
      
    Log.Info("TheTVDB.GetImages() - Posters : {}/{}, Season posters: {}/{}, Art: {}/{}".format(count_valid['poster'], count['poster'], count_valid['season'], count['season'], count_valid['fanart'], count['fanart']))
    if count['poster'] == 0:  error_log['TVDB posters missing'       ].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    if count['season'] == 0:  error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, TVDBid), Dict(TheTVDB_dict, 'title')))
    Log.Info("TheTVDB_dict: "+str(TheTVDB_dict))
  return TheTVDB_dict, IMDbid
  
### search for TVDB id series ###
def Search (results,  media, lang, manual, movie):  #if maxi<50:  maxi = tvdb.Search_TVDB(results, media, lang, manual, movie)
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
