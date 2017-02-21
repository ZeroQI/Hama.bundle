### TheTVDB.com ###
# http://thetvdb.com/api/A27AD9BE0DA63333/series/103291/all/en.xml

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
import os
from common import GetPosters, GetSeasons, GetFanarts, GetBanners, GetElementText

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'
TVDB_SERIE_URL  = 'http://thetvdb.com/?tab=series&id=%s'
TVDB_IMAGES_URL = 'http://thetvdb.com/banners/'  

### Functions ###  

### ###
def Search (results,  media, lang, manual, movie):  #if maxi<50:  maxi = tvdb.Search_TVDB(results, media, lang, manual, movie)
  TVDB_SERIE_SEARCH = 'http://thetvdb.com/api/GetSeries.php?seriesname='
  orig_title = ( media.title if movie else media.show )
  maxi = 0
  try:                    TVDBsearchXml = XML.ElementFromURL( TVDB_SERIE_SEARCH + orig_title.replace(" ", "%20"), cacheTime=CACHE_1HOUR * 24)
  except Exception as e:  Log.Error("TVDB Loading search XML failed, Exception: '%s'" % e)
  else:
    for serie in TVDBsearchXml.xpath('Series'):
      a, b = orig_title, serie.xpath('SeriesName')[0].text.encode('utf-8') #a, b  = cleansedTitle, cleanse_title (serie.xpath('SeriesName')[0].text)
      score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
      if maxi<score:  maxi = score
      Log.Info("TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, serie.xpath('seriesid')[0].text, serie.xpath('SeriesName')[0].text) )
      results.Append(MetadataSearchResult(id="%s-%s" % ("tvdb", serie.xpath('seriesid')[0].text), name="%s [%s-%s]" % (serie.xpath('SeriesName')[0].text, "tvdb", serie.xpath('seriesid')[0].text), year=None, lang=lang, score=score) )
  return maxi
  
### ###
def GetImages (metadata, TheTVDB_dict, media, error_log, TVDBid, TheTVDB_dict, movie, poster_id=1, force=False, defaulttvdbseason="", num=0):  # [banners.xml] Attempt to get the TVDB's image data
  TVDB_BANNERS_URL = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/banners.xml'                                    # TVDB Serie pictures xml: fanarts, posters, banners
  TVDB_IMAGES_URL  = 'http://thetvdb.com/banners/'                                                                      # TVDB picture directory

  posternum, seasonposternum, poster_total = 0, 0, 0
  defaulttvdbseason = int(defaulttvdbseason)-1 if isinstance(defaulttvdbseason, str) and defaulttvdbseason.isdigit() else 0
  try:                    bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % TVDBid, cacheTime=CACHE_1HOUR * 24) # don't bother with the full zip, all we need is the banners
  except Exception as e:  Log.Error("Loading picture XML failed: '%s', Exception: '%s'" %(TVDB_BANNERS_URL % TVDBid, e)); return
  else:                   Log.Info( "Loaded picture XML: '%s'" % (TVDB_BANNERS_URL % TVDBid))
  for banner in bannersXml.xpath('Banner'): 
    if banner.xpath('BannerType')[0].text=="poster":  poster_total +=1
  for banner in bannersXml.xpath('Banner'): #rating   = banner.xpath('Rating'     )[0].text if banner.xpath('Rating') else ""  #Language = banner.xpath('Language'   )[0].text #if Language not in ['en', 'jp']: continue  #id       = banner.xpath('id'         )[0].text
    num, bannerType, bannerType2, bannerPath  = num+1, banner.xpath('BannerType' )[0].text, banner.xpath('BannerType2')[0].text, banner.xpath('BannerPath' )[0].text
    if bannerType == 'poster':                            posternum       += 1
    if bannerType == 'season' and bannerType2=='season':  seasonposternum += 1
    season = banner.xpath('Season')[0].text if banner.xpath('Season') else ""
    if season.isdigit() and defaulttvdbseason!=0:
      if   int(season)-defaulttvdbseason>0:  Log.Debug("Setting season '%s' to '%s' with offset of '%s'" % (season, int(season)-defaulttvdbseason, defaulttvdbseason)); season = str( int(season)-defaulttvdbseason )
      elif season=="0":                             Log.Debug("Keeping season '0' as '0'")
      else:                                         Log.Debug("New season would be <1 (%s-%s) so skipping poster '%s'" % (season, defaulttvdbseason, bannerPath)); continue
    if movie and not bannerType in ('fanart', 'poster') or season and season not in media.seasons:  continue
    if GetPosters('TheTVDB')    and                  ( bannerType == 'poster' or bannerType2 == 'season' and not movie ) or \
       GetFanarts('TheTVDB')    and                    bannerType == 'fanart' or \
       GetBanners('TheTVDB')    and not movie and    ( bannerType == 'series' or bannerType2 == 'seasonwide'):
      metatype, metaname = ((metadata.art,                     "art"    ) if bannerType == 'fanart' else \
                            (metadata.posters,                 "posters") if bannerType == 'poster' else \
                            (metadata.banners,                 "banners") if bannerType == 'series' or bannerType2=='seasonwide' else \
                            (metadata.seasons[season].posters, "seasons") if bannerType == 'season' and bannerType2=='season' else None)
      if metatype == metadata.posters:  rank = 1 if poster_id and poster_total and posternum == divmod(poster_id, poster_total)[1] + 1 else posternum+1
      else:                             rank = num
      bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
      
      if bannerType == 'season' and bannerType2=='season':
        if not 'seasons'  in TheTVDB_dict:                     TheTVDB_dict['seasons']                    = {}
        if not  season    in TheTVDB_dict['seasons']:          TheTVDB_dict['seasons'][season]            = {}
        if not 'posters'  in TheTVDB_dict['seasons'][season]:  TheTVDB_dict['seasons'][season]['posters'] = {}
        TheTVDB_dict['seasons'][season]['posters'][TVDB_IMAGES_URL + bannerPath] = ("TVDB/"+bannerPath, rank, None)
      else:
        if not metaname in TheTVDB_dict: TheTVDB_dict[metaname] = {}
        TheTVDB_dict[metaname][TVDB_IMAGES_URL + bannerPath] = ("TVDB/"+bannerPath, rank, None)
        
  if posternum == 0:                    error_log['TVDB posters missing'].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid), TheTVDB_dict['title']))
  if seasonposternum == 0:              error_log['TVDB season posters missing'].append("TVDBid: %s | Title: '%s'" % (common.WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid), TheTVDB_dict['title']))
  if posternum * seasonposternum == 0:  Log.Warn("TVDB - No poster, check logs in ../../Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB posters missing.htm to update Metadata Source")

### TVDB - Load serie XML ###
def GetMetadata(metadata, media, movie, error_log, lang, metadata_source, TVDBid, IMDbid, defaulttvdbseason):
  TVDB_HTTP_API_URL = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/%s.xml'                                     # TVDB Serie XML for episodes sumaries for now
  Log.Info("".ljust(157, '-'))
  Log.Info("TheTVDB.GetMetadata() - TVDBid: '%s', url: '%s'" % (TVDBid, TVDB_HTTP_API_URL % (TVDBid, lang)))
  IMDbid_serie=""
  TheTVDB_xml=common.LoadFile(filename=TVDBid+".xml", relativeDirectory="TVDB", url=TVDB_HTTP_API_URL % (TVDBid, lang), cache= CACHE_1HOUR * 24 * 7)  # AniDB title database loaded once every 2 weeks
  if TheTVDB_xml:
    TheTVDB_xml = TheTVDB_xml.xpath('/Data')[0]
    TheTVDB_dict = { 'title'                  : GetElementText(TheTVDB_xml, 'Series/SeriesName'),
                     'summary'                : GetElementText(TheTVDB_xml, 'Series/Overview'  ),
                     'content_rating'         : GetElementText(TheTVDB_xml, 'Series/ContentRating'),
                     'studio'                 : GetElementText(TheTVDB_xml, 'Series/Network'),
                     'rating'                 : GetElementText(TheTVDB_xml, 'Series/Rating'),
                     'originally_available_at': GetElementText(TheTVDB_xml, 'Series/FirstAired'),
                     'genres'                 : filter(None, GetElementText(TheTVDB_xml, 'Series/Genre').split("|")),
                     'episode_mapping'        : {}
                   }
    if not IMDbid and GetElementText(TheTVDB_xml, 'Series/IMDB_ID'):  
        IMDbid = GetElementText(TheTVDB_xml, 'Series/IMDB_ID')
        Log.Warn("IMDB ID was empty, loaded through tvdb serie xml, IMDBID: '%s'" % IMDbid)
    
    ### Absolute mode ###
    episode_missing, tvdb_special_missing, summary_missing_special, summary_missing, summary_present, abs_manual_placement_worked = [], [], [], [], [], True
    ep_count, abs_manual_placement_info, number_set = 0, [], False
    if not movie and defaulttvdbseason != "0" and max(int(x) for x in media.seasons.keys())==1 or metadata_source in ["tvdb3", "tvdb4"]:
      for episode in TheTVDB_xml.xpath('Episode'):
        if episode.xpath('SeasonNumber')[0].text != '0' and episode.xpath('EpisodeNumber')[0].text!= '0':
          ep_count = ep_count + 1
          if not episode.xpath('absolute_number')[0].text:
            episode.xpath('absolute_number')[0].text, number_set = str(ep_count), True
            if episode.xpath('EpisodeName')[0].text: episode.xpath('EpisodeName')[0].text = "(Guessed) " + episode.xpath('EpisodeName')[0].text
            if episode.xpath('Overview')[0].text:    episode.xpath('Overview'   )[0].text = "(Guessed mapping as TVDB absolute numbering is missing)\n" + episode.xpath('Overview')[0].text
            abs_manual_placement_info.append("s%se%s = abs %s" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text, episode.xpath('absolute_number')[0].text))
          elif not number_set:  ep_count = int(episode.xpath('absolute_number')[0].text)
          else:
            Log.Error("TheTVDB.GetMetadata() - Abs number found on ep (s%se%s) after manually placing our own abs numbers (%d)" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text, ep_count))
            abs_manual_placement_worked = False
            break
    Log.Info("TheTVDB.GetMetadata() - abs_manual_placement_worked: '%s', abs_manual_placement_info: '%s'" % (str(abs_manual_placement_worked), str(abs_manual_placement_info)))
    if abs_manual_placement_worked:
      for ep in TheTVDB_xml.xpath('Episode'):  # Combined_episodenumber, Combined_season, DVD(_chapter, _discid, _episodenumber, _season), Director, EpImgFlag, EpisodeName, EpisodeNumber, FirstAired, GuestStars, IMDB_ID #seasonid, imdbd
        currentSeasonNum = GetElementText(ep, 'SeasonNumber')
        currentEpNum     = GetElementText(ep, 'EpisodeNumber')
        currentAbsNum    = GetElementText(ep, 'absolute_number') 
        
        if currentSeasonNum.isdigit() and int(currentSeasonNum) > 0 and (metadata_source in ("tvdb3", "tvdb4", "tvdb5") or metadata_source=="anidb" and defaulttvdbseason=="a" and max(map(int, media.seasons.keys()))==1):  season, episode, numbering =                1, currentAbsNum, "s1e" + currentAbsNum
        else:                                                                                                                                                                                                                season, episode, numbering = currentSeasonNum,  currentEpNum, "s%se%s" % (currentSeasonNum, currentEpNum)
        
        if not 'seasons'  in TheTVDB_dict:                                 TheTVDB_dict['seasons']                              = {}
        if not  season    in TheTVDB_dict['seasons']:                      TheTVDB_dict['seasons'][season]                      = {}
        if not 'episodes' in TheTVDB_dict['seasons'][season]:              TheTVDB_dict['seasons'][season]['episodes']          = {}
        if not  episode   in TheTVDB_dict['seasons'][season]['episodes']:  TheTVDB_dict['seasons'][season]['episodes'][episode] = {}
        
        if        GetElementText(ep, 'EpisodeName'):  TheTVDB_dict['seasons'][season]['episodes'][episode]['title'    ] = GetElementText(ep, 'EpisodeName')
        if        GetElementText(ep, 'Director'   ):  TheTVDB_dict['seasons'][season]['episodes'][episode]['directors'] = GetElementText(ep, 'Director'   ).split(',')
        if        GetElementText(ep, 'Writer'     ):  TheTVDB_dict['seasons'][season]['episodes'][episode]['writers'  ] = GetElementText(ep, 'Writer'     ).split(',')
        if        GetElementText(ep, 'filename'   ):  TheTVDB_dict['seasons'][season]['episodes'][episode]['thumbs'   ] = {TVDB_IMAGES_URL+GetElementText(ep, 'filename'): ("TVDB/episodes/"+ os.path.basename(GetElementText(ep, 'filename')), 1, None) } if GetElementText(ep, 'filename') else {}
        if "." in GetElementText(ep, 'Rating'     ):  TheTVDB_dict['seasons'][season]['episodes'][episode]['rating'   ] = GetElementText(ep, 'Rating'     )
        #if currentAbsNum:                             TheTVDB_dict['seasons'][season]['episodes'][episode]['absolute_number'] = currentAbsNum
        
        if GetElementText(ep, 'FirstAired'):
          TheTVDB_dict['seasons'][season]['episodes'][episode]['originally_available_at'] = Datetime.ParseDate(GetElementText(ep, 'FirstAired')).date()
          currentAirDate = GetElementText(ep, 'FirstAired').replace('-','')
          currentAirDate = int(currentAirDate) if currentAirDate.isdigit() and int(currentAirDate) > 10000000 else 99999999
        else:  currentAirDate = 99999999
          
        if GetElementText(ep, 'Overview'):  summary_present.append        (numbering);  TheTVDB_dict['seasons'][season]['episodes'][episode]['summary'] = GetElementText(ep, 'Overview')
        elif currentSeasonNum == '0':       summary_missing_special.append(numbering)
        else:                               summary_missing.append        (numbering)
        
        ### Check for Missing Episodes ###
        if not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1 or metadata_source == "tvdb"):
          if int(time.strftime("%Y%m%d")) <= (currentAirDate+1):  Log.Warn("TheTVDB.GetMetadata() - Episode '%s' is missing in Plex but air date '%s+1' is either missing (99999999) or in the future" % (numbering, currentAirDate))
          elif currentSeasonNum and not (
              ((not metadata_source in ["tvdb3","tvdb4"] or currentSeasonNum==0) and currentSeasonNum in media.seasons and currentEpNum in media.seasons[currentSeasonNum].episodes) or
              (metadata_source in ["tvdb3","tvdb4"] and [currentAbsNum in media.seasons[season].episodes for season in media.seasons].count(True) > 0)
            ):
            if currentSeasonNum == '0': tvdb_special_missing.append(numbering)
            else:                       episode_missing.append(numbering)
    ### End of for episode in TheTVDB_xml.xpath('Episode'): ###
  ### End of if abs_manual_placement_worked: ###

  ### Logging ###
  Log.Debug("TheTVDB.GetMetadata() - TVDB - Episodes with    Summary: " + str(sorted(summary_present)))
  Log.Debug("TheTVDB.GetMetadata() - TVDB - Episodes without Summary: " + str(sorted(summary_missing)))
  if summary_missing:         error_log['Missing Episode Summaries'].append("TVDBid: %s | Title: '%s' | Missing Episode Summaries: %s" % (common.WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid), TheTVDB_dict['title'], str(summary_missing        )))
  if summary_missing_special: error_log['Missing Special Summaries'].append("TVDBid: %s | Title: '%s' | Missing Special Summaries: %s" % (common.WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid), TheTVDB_dict['title'], str(summary_missing_special)))
  if episode_missing:         error_log['Missing Episodes'         ].append("TVDBid: %s | Title: '%s' | Missing Episodes: %s"          % (common.WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid), TheTVDB_dict['title'], str(episode_missing        )))
  if tvdb_special_missing:    error_log['Missing Specials'         ].append("TVDBid: %s | Title: '%s' | Missing Specials: %s"          % (common.WEB_LINK % (TVDB_SERIE_URL % TVDBid, TVDBid), TheTVDB_dict['title'], str(tvdb_special_missing   )))
  
  GetImages (metadata, TheTVDB_dict, media, error_log, TVDBid, TheTVDB_dict, movie, poster_id=1, force=False, defaulttvdbseason=defaulttvdbseason, num=1)
  return IMDbid, TheTVDB_dict
