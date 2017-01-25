### Fanart.TV ###

### Fetch extra images from fanart.tv ###################################################################################################################
def fanarttv_posters(metadata, movie, tmdbid="", tvdbid="", imdbid="", season=0, num=100):
  FANART_TV_TV_URL     = 'http://webservice.fanart.tv/v3/tv/{tvdbid}?api_key={api_key}'
  FANART_TV_MOVIES_URL = 'http://webservice.fanart.tv/v3/movies/{tmdbid}?api_key={api_key}'
  FANART_TV_API_KEY    = 'cfa9dc054d221b8d107f8411cd20b13f'
  
  if imdbid and not tmdbid:
    tmdb.get_tmdbid_per_imdbid(imdbid, tmdbid)
    if not tmdbid: return
  
  if movie and tmdbid and "," in tmdbid:  #recusive call for each tmdbid to reduce complexity
    for tmdbid_unique in tmdbid.split(","):  fanarttv_posters(metadata, movie, tmdbid_unique, None, season, num)
    if tvdbid: tmdbid=None
    else:      return
  
  Log.Info("Fetching from fanart.tv")
  if not movie and tvdbid:
    try:
      FanartTV = common.get_json(FANART_TV_TV_URL.format(tvdbid=tvdbid, api_key=FANART_TV_API_KEY))   # It's a series, grab the list of fanart using the TVDB ID.
      if FanartTV:
        if Prefs['GetFanartTVBackground'] and 'showbackground' in FanartTV:
          Log.Debug("fanart.tv has {count} background images/art".format(count=len(FanartTV['showbackground'])))
          for art in FanartTV['showbackground']:  common.metadata_download(metadata.art, art['url'], num, "FanartTV/series-{filename}.jpg".format(filename=art['id']))
        if Prefs['GetFanartTVPoster'] and 'tvposter' in FanartTV:
          Log.Debug("fanart.tv has {count} series posters".format(count=len(FanartTV['tvposter'])))
          for tvposter in FanartTV['tvposter']:  common.metadata_download(metadata.posters, tvposter['url'], num, "FanartTV/series-{filename}.jpg".format(filename=tvposter['id']))
        if Prefs['GetFanartTVPoster'] and 'seasonposter' in FanartTV:
          Log.Debug("fanart.tv has {count} season posters".format(count=len(FanartTV['seasonposter'])))
          for seasonposter in FanartTV['seasonposter']:
            common.metadata_download(metadata.posters, seasonposter['url'], num, "FanartTV/series-{filename}.jpg".format(filename=seasonposter['id']))                                                    # Add all of the 'season' posters as potential main show posters. Now add season posters to their respective seasons within the show.
            if   seasonposter['season'] == 0:       common.metadata_download(metadata.seasons[0].posters, seasonposter['url'], num, "FanartTV/series-{filename}.jpg".format(filename=seasonposter['id'])) # Special
            elif seasonposter['season'] == season:  common.metadata_download(metadata.seasons[1].posters, seasonposter['url'], num, "FanartTV/series-{filename}.jpg".format(filename=seasonposter['id'])) # Non-special. Add any posters to "Season 1" entry if they match this 'actual' season.
        if Prefs['GetFanartTVBanner'] and 'tvbanner' in FanartTV:
          Log.Debug("fanart.tv has {count} banners".format(count=len(FanartTV['tvbanner'])))
          for tvbanner in FanartTV['tvbanner']:  common.metadata_download(metadata.banners, tvbanner['url'], num, "FanartTV/series-{filename}.jpg".format(filename=tvbanner['id']))
    except Exception as e:  Log.Error("Exception - FanartTV - tvdbid: '{tvdbid}', url: '{url}', Exception: '{exception}'".format(tvdbid=tvdbid, url=FANART_TV_TV_URL.format(tvdbid=tvdbid, api_key=FANART_TV_API_KEY), exception=e))
  if movie and tmdbid:
    try:
      FanartTV = common.get_json(FANART_TV_MOVIES_URL.format(tmdbid=tmdbid, api_key=FANART_TV_API_KEY))       # It's a movie, grab the list of fanart using the TMDB ID.
      if FanartTV:
        if Prefs['GetFanartTVBackground'] and 'moviebackground' in FanartTV:
          Log.Debug("fanart.tv has {count} movie background images/art".format(count=len(FanartTV['moviebackground'])))
          for art in FanartTV['moviebackground']:  common.metadata_download(metadata.art, art['url'], num, "FanartTV/movie-{filename}.jpg".format(filename=art['id']))
        if Prefs['GetFanartTVPoster'] and 'movieposter' in FanartTV: 
          Log.Debug("fanart.tv has {count} movie posters".format(count=len(FanartTV['movieposter'])))
          for movieposter in FanartTV['movieposter']: common.metadata_download(metadata.posters, movieposter['url'], num, "FanartTV/movie-{filename}.jpg".format(filename=movieposter['id']))
    except Exception as e:  Log.Error("Exception - FanartTV - tmdbid: '{tmdbid}', url: '{url}', Exception: 'movie-{exception}'".format(tmdbid=tmdbid, url=FANART_TV_MOVIES_URL.format(tmdbid=tmdbid, api_key=FANART_TV_API_KEY), exception=e))
