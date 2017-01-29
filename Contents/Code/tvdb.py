### TVDB ###
import common
from common import getElementText
TVDB_SERIE_URL  = 'http://thetvdb.com/?tab=series&id=%s'                                                             #
TVDB_IMAGES_URL = 'http://thetvdb.com/banners/'                                                                      # TVDB picture directory
  
def Search_TVDB(results,  media, lang, manual, movie):
  TVDB_SERIE_SEARCH = 'http://thetvdb.com/api/GetSeries.php?seriesname='                                                 #
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
  
### TVDB - Load serie XML ###
def get_tvdb_metadata(metadata, media, lang, movie, metadata_source, tvdbid, imdbid, defaulttvdbseason, error_log):
  TVDB_HTTP_API_URL = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/%s.xml'                                     # TVDB Serie XML for episodes sumaries for now
  Log.Info("TVDB - tvdbid: '%s', url: '%s'" % (tvdbid, TVDB_HTTP_API_URL % (tvdbid, lang)))
  
  tvdbanime=common.LoadFile(filename=tvdbid+".xml", relativeDirectory="TVDB", url=TVDB_HTTP_API_URL % (tvdbid, lang), cache= CACHE_1HOUR * 24 * 7)  # AniDB title database loaded once every 2 weeks
  if tvdbanime:
    tvdbanime = tvdbanime.xpath('/Data')[0]
    if not imdbid and getElementText(tvdbanime, 'Series/IMDB_ID'):
      imdbid = getElementText(tvdbanime, 'Series/IMDB_ID')
      Log.Warn("IMDB ID was empty, loaded through tvdb serie xml, IMDBID: '%s'" % imdbid)
    tvdb_table = { 'SeriesName'   : getElementText(tvdbanime, 'Series/SeriesName'),
                   'Overview'     : getElementText(tvdbanime, 'Series/Overview'  ),
                   'ContentRating': getElementText(tvdbanime, 'Series/ContentRating'),
                   'Network'      : getElementText(tvdbanime, 'Series/Network'),
                   'Rating'       : float(getElementText(tvdbanime, 'Series/Rating')) if '.' in getElementText(tvdbanime, 'Series/Rating') else None,
                   'FirstAired'   : Datetime.ParseDate(getElementText(tvdbanime, 'Series/FirstAired')).date(),
                   'Genre'        : filter(None, getElementText(tvdbanime, 'Series/Genre').split("|")),
    } 
    ### Absolute mode ###
    tvdb_episode_missing, tvdb_special_missing, special_summary_missing, summary_missing, summary_present, abs_manual_placement_worked = [], [], [], [], [], True
    ep_count, abs_manual_placement_info, number_set = 0, [], False
    if not movie and defaulttvdbseason != "0" and max(int(x) for x in media.seasons.keys())==1 or metadata_source in ["tvdb3", "tvdb4"]:
      for episode in tvdbanime.xpath('Episode'):
        if episode.xpath('SeasonNumber')[0].text != '0' and episode.xpath('EpisodeNumber')[0].text!= '0':
          ep_count = ep_count + 1
          if not episode.xpath('absolute_number')[0].text:
            episode.xpath('absolute_number')[0].text, number_set = str(ep_count), True
            if episode.xpath('EpisodeName')[0].text: episode.xpath('EpisodeName')[0].text = "(Guessed) " + episode.xpath('EpisodeName')[0].text
            if episode.xpath('Overview')[0].text:    episode.xpath('Overview'   )[0].text = "(Guessed mapping as TVDB absolute numbering is missing)\n" + episode.xpath('Overview')[0].text
            abs_manual_placement_info.append("s%se%s = abs %s" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text, episode.xpath('absolute_number')[0].text))
          elif not number_set:  ep_count = int(episode.xpath('absolute_number')[0].text)
          else:
            Log.Error("Abs number found on ep (s%se%s) after manually placing our own abs numbers (%d)" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text, ep_count))
            abs_manual_placement_worked = False
            break
    Log.Info("abs_manual_placement_worked: '%s', abs_manual_placement_info: '%s'" % (str(abs_manual_placement_worked), str(abs_manual_placement_info)))
    if abs_manual_placement_worked:
      for episode in tvdbanime.xpath('Episode'):  # Combined_episodenumber, Combined_season, DVD(_chapter, _discid, _episodenumber, _season), Director, EpImgFlag, EpisodeName, EpisodeNumber, FirstAired, GuestStars, IMDB_ID #seasonid, imdbd
        currentSeasonNum = getElementText(episode, 'SeasonNumber')
        currentEpNum     = getElementText(episode, 'EpisodeNumber')
        currentAbsNum    = getElementText(episode, 'absolute_number')
        currentAirDate   = getElementText(episode, 'FirstAired').replace('-','')
        currentAirDate   = int(currentAirDate) if currentAirDate.isdigit() and int(currentAirDate) > 10000000 else 99999999
        if currentSeasonNum.isdigit() and int(currentSeasonNum) > 0 and (metadata_source in ("tvdb3", "tvdb4") or metadata_source=="anidb" and defaulttvdbseason=="a" and max(map(int, media.seasons.keys()))==1):  numbering = currentAbsNum
        elif metadata_source=="tvdb5":                                                                                                                                                                              numbering = "s1e" + currentAbsNum
        else:                                                                                                                                                                                                       numbering = "s" + currentSeasonNum + "e" + currentEpNum 
        tvdb_table [numbering] = { 'EpisodeName': getElementText(episode, 'EpisodeName'), 
                                   'FirstAired':  getElementText(episode, 'FirstAired' ),
                                   'filename':    getElementText(episode, 'filename'   ),
                                   'Overview':    getElementText(episode, 'Overview'   ), 
                                   'Director':    getElementText(episode, 'Director'   ),
                                   'Writer':      getElementText(episode, 'Writer'     ),
                                   'Rating':      getElementText(episode, 'Rating'     ) if '.' in getElementText(episode, 'Rating') else None
                                 }
        ### Check for Missing Summaries ### 
        if tvdb_table [numbering]['Overview']:  summary_present.append        (numbering)
        elif currentSeasonNum == '0':           special_summary_missing.append(numbering)
        else:                                   summary_missing.append        (numbering)
        
        ### Check for Missing Episodes ###
        if not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1 or metadata_source == "tvdb"):
          if current_date <= (currentAirDate+1):  Log.Warn("Episode '%s' is missing in Plex but air date '%s+1' is either missing (99999999) or in the future" % (numbering, currentAirDate))
          elif currentSeasonNum and not (
              ((not metadata_source in ["tvdb3","tvdb4"] or currentSeasonNum==0) and currentSeasonNum in media.seasons and currentEpNum in media.seasons[currentSeasonNum].episodes) or
              (metadata_source in ["tvdb3","tvdb4"] and [currentAbsNum in media.seasons[season].episodes for season in media.seasons].count(True) > 0)
            ):
            if currentSeasonNum == '0': tvdb_special_missing.append(numbering)
            else:                       tvdb_episode_missing.append(numbering)
    ### End of for episode in tvdbanime.xpath('Episode'): ###
  ### End of if abs_manual_placement_worked: ###

  Log.Debug("TVDB - Episodes with    Summary: " + str(sorted(summary_present)))
  Log.Debug("TVDB - Episodes without Summary: " + str(sorted(summary_missing)))
  if summary_missing:         error_log['Missing Episode Summaries'].append("tvdbid: %s | Title: '%s' | Missing Episode Summaries: %s" % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid), tvdb_table['SeriesName'], str(summary_missing)        ))
  if special_summary_missing: error_log['Missing Special Summaries'].append("tvdbid: %s | Title: '%s' | Missing Special Summaries: %s" % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid), tvdb_table['SeriesName'], str(special_summary_missing)))
  if tvdb_episode_missing:    error_log['Missing Episodes'         ].append("tvdbid: %s | Title: '%s' | Missing Episodes: %s"          % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid), tvdb_table['SeriesName'], str(tvdb_episode_missing)   ))
  if tvdb_special_missing:    error_log['Missing Specials'         ].append("tvdbid: %s | Title: '%s' | Missing Specials: %s"          % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid), tvdb_table['SeriesName'], str(tvdb_special_missing)   ))
  return tvdb_table

### Update tvdb metadata ###
def tvdb_update_meta(metadata, media, metadata_source, defaulttvdbseason, tvdb_table):
  Log.Info("using TVDB numbering mode (seasons)")
  if tvdb_table['SeriesName'   ] and not tvdb_table['SeriesName'   ] == metadata.title:                    metadata.title                   = tvdb_table['SeriesName'   ]
  if tvdb_table['Rating'       ] and not tvdb_table['Rating'       ] == metadata.rating:                   metadata.rating                  = tvdb_table['Rating'       ]
  if tvdb_table['Overview'     ] and not tvdb_table['Overview'     ] == metadata.summary:                  metadata.summary                 = tvdb_table['Overview'     ]
  if tvdb_table['Network'      ] and not tvdb_table['Network'      ] == metadata.studio:                   metadata.studio                  = tvdb_table['Network'      ]
  if tvdb_table['ContentRating'] and not tvdb_table['ContentRating'] == metadata.content_rating:           metadata.content_rating          = tvdb_table['ContentRating']
  if tvdb_table['FirstAired'   ] and not tvdb_table['FirstAired'   ] == metadata.originally_available_at:  metadata.originally_available_at = tvdb_table['FirstAired']
  if tvdb_table['Genre'        ] and not len(set(tvdb_table['Genre']).intersection(metadata.genres)) == len(metadata.genres):
    Log.Info("TVDB - tvdbGenre: '%s'" % str(tvdb_table['Genre']))
    metadata.genres.clear()
    for genre in tvdb_table['Genre']: metadata.genres.add(genre)
  list_eps = []
  for media_season in media.seasons:
    metadata.seasons[media_season].summary      = "#" + tvdb_table['Overview'  ]
    metadata.seasons[media_season].title        = "#" + tvdb_table['SeriesName']
    metadata.seasons[media_season].show         = "#" + tvdb_table['SeriesName']
    metadata.seasons[media_season].source_title = "#" + tvdb_table['Network'   ]
    for media_episode in media.seasons[media_season].episodes:
      ep, episode_count = media_episode if defaulttvdbseason=="a" and max(map(int, media.seasons.keys()))==1 or metadata_source in ["tvdb3", "tvdb4"] and media_season != "0" else "s%se%s" % (media_season, media_episode), 0
      if ep in tvdb_table:
        if 'EpisodeName' in tvdb_table[ep] and not tvdb_table[ep]['EpisodeName'] == metadata.seasons[media_season].episodes[media_episode].title:    metadata.seasons[media_season].episodes[media_episode].title   = tvdb_table[ep]['EpisodeName']
        if 'Overview'    in tvdb_table[ep] and not tvdb_table[ep]['Overview'   ] == metadata.seasons[media_season].episodes[media_episode].summary:  metadata.seasons[media_season].episodes[media_episode].summary = tvdb_table[ep]['Overview']
        if 'filename'    in tvdb_table[ep] and tvdb_table[ep]['filename'       ]:                                                                    common.metadata_download (metadata.seasons[media_season].episodes[media_episode].thumbs, TVDB_IMAGES_URL + tvdb_table[ep]['filename'], 1, "TVDB/episodes/"+ os.path.basename(tvdb_table[ep]['filename']))
          #try:                    metadata.seasons[media_season].episodes[media_episode].summary = tvdb_table [ep] ['Overview']
          #except Exception as e:  Log.Error("Error adding summary - ep: '%s', media_season: '%s', media_episode: '%s', summary:'%s', Exception: '%s'" % (ep, media_season, media_episode, tvdb_table [ep] ['Overview'], e))
        metadata.seasons[media_season].episodes[media_episode].directors.clear()
        metadata.seasons[media_season].episodes[media_episode].writers.clear()
        if 'Director'    in tvdb_table[ep] and tvdb_table [ep] ['Director']:
          for this_director in re.split(',|\|', tvdb_table[ep]['Director']):
            meta_director = metadata.seasons[media_season].episodes[media_episode].directors.new()
            Log.Debug("Adding new Director {name}".format(name=this_director))
            meta_director.name = this_director
        if 'Writer'      in tvdb_table[ep] and tvdb_table [ep] ['Writer']:
          for this_writer in re.split(',|\|', tvdb_table[ep]['Writer']):
            meta_writer = metadata.seasons[media_season].episodes[media_episode].writers.new()
            Log.Debug("Adding new Writer {name}".format(name=this_writer))
            meta_writer.name = this_writer
        if 'Rating'      in tvdb_table[ep] and tvdb_table [ep] ['Rating']:
          try:                    metadata.seasons[media_season].episodes[media_episode].rating  = float(tvdb_table [ep] ['Rating'])
          except Exception as e:  Log.Error("float issue: '%s', Exception: '%s'" % (tvdb_table [ep] ['Rating'], e)) #ValueError
        if 'FirstAired'  in tvdb_table[ep] and tvdb_table [ep] ['FirstAired']:
          match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", tvdb_table [ep] ['FirstAired'])
          if match:
            try:   metadata.seasons[media_season].episodes[media_episode].originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError, e: Log.Error("TVDB parseAirDate - Date out of range: " + str(e))
      #for media_item in media.seasons[media_season].episodes[media_episode].items:
      #  for item_part in media_item.parts:  Log("File: '%s' '%s'" % (ep, item_part.file))
      episode_count += 1
      list_eps.append(ep)
    metadata.seasons[media_season].episode_count = episode_count #An integer specifying the number of episodes in the season.
  if list_eps:  Log.Debug("List_eps: %s" % str(sorted(list_eps)))
  Log.Debug("TVDB table: '%s'" % str(tvdb_table))

### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###
def plex_theme_song(metadata, tvdbid, tvdb_table, error_log):
  THEME_URL = 'http://tvthemes.plexapp.com/%s.mp3'                                                               # Plex TV Theme url
  if THEME_URL % tvdbid in metadata.themes:  Log.Info("Theme song - already added")
  elif Prefs['GetPlexThemes']:
    common.metadata_download (metadata.themes, THEME_URL % tvdbid, 1, "Plex/%s.mp3" % tvdbid)
    if not THEME_URL % tvdbid in metadata.themes:  
      Log.Info("Theme song - Missing in Plex server. Please check 'Plex themes missing' log.")
      error_log['Plex themes missing'].append("tvdbid: %s | Title: '%s' | %s" % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdb_table['SeriesName']), tvdb_table['SeriesName'], common.WEB_LINK % ("mailto:themes@plexapp.com?cc=&subject=Missing%%20theme%%20song%%20-%%20&#39;%s%%20-%%20%s.mp3&#39;" % (tvdb_table['SeriesName'], tvdbid), 'Upload')))

### [banners.xml] Attempt to get the TVDB's image data ###############################################################################################################
def getImagesFromTVDB(metadata, media, error_log, tvdbid, tvdb_table, movie, poster_id=1, force=False, defaulttvdbseason="", num=0):
  TVDB_BANNERS_URL = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/banners.xml'                                    # TVDB Serie pictures xml: fanarts, posters, banners
  TVDB_IMAGES_URL  = 'http://thetvdb.com/banners/'                                                                      # TVDB picture directory

  posternum, seasonposternum, poster_total = 0, 0, 0
  defaulttvdbseason = int(defaulttvdbseason)-1 if isinstance(defaulttvdbseason, str) and defaulttvdbseason.isdigit() else 0
  try:                    bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % tvdbid, cacheTime=CACHE_1HOUR * 24) # don't bother with the full zip, all we need is the banners
  except Exception as e:  Log.Error("Loading picture XML failed: '%s', Exception: '%s'" %(TVDB_BANNERS_URL % tvdbid, e)); return
  else:                   Log.Info( "Loaded picture XML: '%s'" % (TVDB_BANNERS_URL % tvdbid))
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
    if Prefs['GetTvdbPosters'] and                  ( bannerType == 'poster' or bannerType2 == 'season' and not movie ) or \
       Prefs['GetTvdbFanart' ] and                    bannerType == 'fanart' or \
       Prefs['GetTvdbBanners'] and not movie and    ( bannerType == 'series' or bannerType2 == 'seasonwide'):
      metatype = (metadata.art                     if bannerType == 'fanart' else \
                  metadata.posters                 if bannerType == 'poster' else \
                  metadata.banners                 if bannerType == 'series' or bannerType2=='seasonwide' else \
                  metadata.seasons[season].posters if bannerType == 'season' and bannerType2=='season' else None)
      if metatype == metadata.posters:  rank = 1 if poster_id and poster_total and posternum == divmod(poster_id, poster_total)[1] + 1 else posternum+1
      else:                             rank = num
      bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
      common.metadata_download (metatype, TVDB_IMAGES_URL + bannerPath, rank, "TVDB/"+bannerPath, bannerThumbUrl)
  if posternum == 0:                    error_log['TVDB posters missing'].append("tvdbid: %s | Title: '%s'" % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid), tvdb_table['SeriesName']))
  if seasonposternum == 0:              error_log['TVDB season posters missing'].append("tvdbid: %s | Title: '%s'" % (common.WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid), tvdb_table['SeriesName']))
  if posternum * seasonposternum == 0:  Log.Warn("TVDB - No poster, check logs in ../../Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB posters missing.htm to update Metadata Source")
