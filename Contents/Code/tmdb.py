### TheMovieDB - Does movies but also series, for which i call it tsdb in metadata id ##
TMDB_CONFIG_URL = 'http://api.tmdb.org/3/configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
config_dict     = common.get_json(TMDB_CONFIG_URL, cache_time=CACHE_1WEEK * 2) #not to download every time the json file

def get_tmdbid_per_imdbid(imdbid, tmdbid):
  TMDB_SEARCH_URL_BY_IMDBID = 'http://api.tmdb.org/3/find/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id'   #
  if imdbid and not tmdbid:
    Log.Info("TMDB ID missing. Attempting to lookup using IMDB ID {imdbid}".format(imdbid=imdbid))
    Log.Info("using IMDBID url: " + TMDB_SEARCH_URL_BY_IMDBID % imdbid)
    try:                   tmdbid = str(common.get_json(TMDB_SEARCH_URL_BY_IMDBID %(imdbid.split(",")[0] if ',' in imdbid else imdbid), cache_time=CACHE_1WEEK * 2)['movie_results'][0]['id'])
    except Exception as e: Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %(TMDB_SEARCH_URL_BY_IMDBID % (imdbid.split(",")[0] if ',' in imdbid else imdbid), e))
    else:                  Log.Info ("TMDB ID found for IMBD ID {imdbid}. tmdbid: '{tmdbid}'".format(imdbid=(imdbid.split(",")[0] if ',' in imdbid else imdbid), tmdbid=tmdbid))

### Download TMDB poster and background through IMDB or TMDB ID ##########################################################################################
def  tmdb_posters(metadata, imdbid="", tmdbid="", num=90):
  TMDB_MOVIE_IMAGES_URL     = 'https://api.tmdb.org/3/movie/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'                  #
  TMDB_SERIE_IMAGES_URL     = 'https://api.tmdb.org/3/tv/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'                     #
  images                    = {}
  
  Log.Info("TMDB - background, Poster - imdbid: '%s', tmdbid: '%s'" % (imdbid, tmdbid))
  if "," in imdbid:  #recusive call for each tmdbid to reduce complexity
    for imdbid_unique in imdbid.split(","):  tmdb_posters(metadata, imdbid_unique, "", num)
    if tmdbid: imdbid=""
    else:      return
  
  #if not Prefs["GetTmdbFanart"] and not Prefs["GetTmdbPoster"]: return
  if imdbid.startswith("tt"):
    for type in ['movie_results', 'tv_results']:
      if tmdb_json is not None and type in tmdb_json:
        for index, poster in enumerate(tmdb_json[type]):
          if Prefs["GetTmdbPoster"] and 'poster_path'   in tmdb_json[type][index] and tmdb_json[type][index]['poster_path'  ] not in (None, "", "null"):  images[ tmdb_json[type][index]['poster_path'  ]] = metadata.posters
          if Prefs["GetTmdbFanart"] and 'backdrop_path' in tmdb_json[type][index] and tmdb_json[type][index]['backdrop_path'] not in (None, "", "null"):  images[ tmdb_json[type][index]['backdrop_path']] = metadata.art
  if tmdbid:
    Log.Info("using TMDBID  url: '%s'" % ((TMDB_SERIE_IMAGES_URL if metadata.id.startswith("tsdb") else TMDB_MOVIE_IMAGES_URL) % tmdbid))
    tmdb_json = common.get_json(url=(TMDB_SERIE_IMAGES_URL if metadata.id.startswith("tsdb") else TMDB_MOVIE_IMAGES_URL) % tmdbid, cache_time=CACHE_1WEEK * 2)
    if tmdb_json and 'posters'    in tmdb_json and len(tmdb_json['posters'  ]):
      for index, poster in enumerate(tmdb_json['posters']):
        if Prefs["GetTmdbPoster"] and 'file_path' in tmdb_json['posters'][index] and tmdb_json['posters'][index]['file_path'] not in (None, "", "null"):  images[ tmdb_json['posters'  ][index]['file_path']] = metadata.posters
    if tmdb_json is not None and 'backdrops' in tmdb_json and len(tmdb_json['backdrops']):
      for index, poster in enumerate(tmdb_json['backdrops']):
        if Prefs["GetTmdbFanart"] and 'file_path' in tmdb_json['backdrops'][index] and tmdb_json['backdrops'][index]['file_path'] not in (None, "", "null"):  images[ tmdb_json['backdrops'][index]['file_path']] = metadata.art
  if len(images):
    for filename in images.keys():
      if filename:
        image_url, thumb_url = config_dict['images']['base_url'] + 'original' + filename, config_dict['images']['base_url'] + 'w300'     + filename
        common.metadata_download (images[filename], image_url, num, "TMDB/%s%s.jpg" % (tmdbid, "" if images[filename]==metadata.posters else "-art"), thumb_url) 

### ###
def TMDB_Tagline_Trailers(metadata, movie, lang, tmdbid, imdbid):
  TMDB_MOVIE_SEARCH_BY_ID = 'http://api.tmdb.org/3/movie/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=trailers&language=en'
  TMDB_SERIE_SEARCH_BY_ID = 'http://api.tmdb.org/3/tv/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=trailers&language=en'      #
  try:                    tmdb_json = JSON.ObjectFromURL((TMDB_MOVIE_SEARCH_BY_ID if metadata.id.startswith("tmdb") else TMDB_SERIE_SEARCH_BY_ID)% tmdbid if tmdbid else imdbid.split(",")[0] , sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1DAY)
  except Exception as e:  Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %(TMDB_MOVIE_SEARCH_BY_ID % tmdbid, e))
  else:  ### Populate Movie Metadata Extras (e.g. Taglines) from TMDB for Movies ###
    Log.Info("tmdbid/imdbid present, populating extras from TMDB - url: " + (TMDB_MOVIE_SEARCH_BY_ID if metadata.id.startswith("tmdb") else TMDB_SERIE_SEARCH_BY_ID)% tmdbid if tmdbid else imdbid.split(",")[0])
    
    if movie and (tmdbid or imdbid) and tmdb_json and 'tagline' in tmdb_json and tmdb_json['tagline']:
      Log.Info("Movie tagline: '{tagline}'.".format(tagline=tmdb_json['tagline']))
      try:                    metadata.tagline = tmdb_json['tagline']
      except Exception as e:  Log.Error("Couldn't fetch tagline from TMDB, Exception: '{exception}'".format(e))
      
    if (tmdbid or imdbid) and tmdb_json:
      if 'trailers' in tmdb_json and tmdb_json['trailers']:
        if "youtube" in tmdb_json['trailers'] and tmdb_json['trailers']["youtube"]:
          for trailer in tmdb_json['trailers']["youtube"]:
            Log.Info("Trailer detected: name: '%s', size: '%s', source: '%s', type: '%s', link: '%s'" % (trailer["name"], trailer["size"], trailer["source"], trailer["type"], "https://www.youtube.com/watch?v="+trailer["source"]))
            #if movie: metadata.extras.add( TrailerObject(url = "https://www.youtube.com/watch?v="+trailer["source"]), title = trailer["name"], thumb = None) )
        if "quicktime" in tmdb_json['trailers'] and tmdb_json['trailers']["quicktime"]:
          for trailer in tmdb_json['trailers']["quicktime"]:
            Log.Info("Trailer detected: " + str (tmdb_json['trailers']["quicktime"]))
            #if movie: metadata.extras.add( TrailerObject(url = "???"+trailer["source"]), title = trailer["name"], thumb = None) )
    if 'belongs_to_collection' in tmdb_json and tmdb_json['belongs_to_collection']:  Log.Info("Collection detected: " + str (tmdb_json['belongs_to_collection']))

### TMDB movie search ###
def Search_TMDB(results, media, lang, manual, movie):
  TMDB_MOVIE_SEARCH = 'http://api.tmdb.org/3/search/movie?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&query=%s&year=&language=en&include_adult=true'

  orig_title = ( media.title if movie else media.show )
  Log.Info("TMDB  - url: " + TMDB_MOVIE_SEARCH % orig_title)
  try:                    tmdb_json = JSON.ObjectFromURL(TMDB_MOVIE_SEARCH % orig_title.replace(" ", "%20"), sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1WEEK * 2)
  except Exception as e:  Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %( TMDB_MOVIE_SEARCH % orig_title, e)) # tmdb_json   = common.get_json(TMDB_MOVIE_SEARCH % orig_title, cache_time=CACHE_1WEEK * 2)
  else:
    if isinstance(tmdb_json, dict) and 'results' in tmdb_json:
      for i, movie in enumerate(tmdb_json['results']):
        a, b = orig_title, movie['title'].encode('utf-8')
        score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
        id = movie['id']
        Log.Info("TMDB  - score: '%3d', id: '%6s', title: '%s'" % (score, movie['id'],  movie['title']) )
        results.Append(MetadataSearchResult(id="%s-%s" % ("tmdb", movie['id']), name="%s [%s-%s]" % (movie['title'], "tmdb", movie['id']), year=None, lang=lang, score=score) )
        if '' in movie and movie['adult']!="null":  Log.Info("adult: '%s'" % movie['adult'])
        # genre_ids, original_language, id, original_language, original_title, overview, release_date, poster_path, popularity, video, vote_average, vote_count, adult, backdrop_path

  ### TMDB - background, Poster - using imdbid or tmdbid ### The Movie Database is least prefered by the mapping file, only when imdbid missing
  Log.Info("TMDB - background, Poster - imdbid: '%s', tmdbid: '%s'" % (imdbid, tmdbid))
  if Prefs["GetTmdbFanart"] or Prefs["GetTmdbPoster"]:
    if imdbid.startswith("tt"): [getImagesFromTMDB(metadata, id_multiple, 97) for id_multiple in imdbid.split(",")]
    if tmdbid:                  [getImagesFromTMDB(metadata, id_multiple, 97) for id_multiple in tmdbid.split(",")]

### ###
def Update_TMDB(metadata, media, lang, force, movie):
  TMDB_MOVIE_SEARCH_BY_TMDBID = 'http://api.tmdb.org/3/movie/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=releases,credits,trailers&language=en'  #Work with imdbid
  TMDB_SERIE_SEARCH_BY_TMDBID = 'http://api.tmdb.org/3/tv/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=releases,credits&language=en'      #
  metadata_id_source, tmdbid  = metadata.id.split('-', 1)
      
  Log.Info("TMDB - url: " + TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid)
  try:                    tmdb_json = JSON.ObjectFromURL((TMDB_MOVIE_SEARCH_BY_TMDBID if metadata_id_source.startswith("tmdb") else TMDB_SERIE_SEARCH_BY_TMDBID)% tmdbid , sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1DAY)
  except Exception as e:  Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %(TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid, e))
  else:
    Log('Update() - get_json - worked: ' + TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid)
    if 'vote_average' in tmdb_json and isinstance(tmdb_json['vote_average'], float):                                             metadata.rating                  = tmdb_json['vote_average']  # if not ep.isdigit() and "." in ep and ep.split(".", 1)[0].isdigit() and ep.split(".")[1].isdigit():  
    if 'runtime'      in tmdb_json and isinstance(tmdb_json['runtime'     ], int):                                               metadata.duration                = int(tmdb_json['runtime']) * 60 * 1000
    if 'title'        in tmdb_json and tmdb_json['title']:                                                                       metadata.title                   = tmdb_json['title']
    if 'overview'     in tmdb_json and tmdb_json['overview']:                                                                    metadata.summary                 = tmdb_json['overview']
    if 'release_date' in tmdb_json and tmdb_json['release_date']:                                                                metadata.originally_available_at = Datetime.ParseDate(tmdb_json['release_date']).date()
    if 'imdb_id'      in tmdb_json and tmdb_json['imdb_id'] and not imdbid:                                                      imdbid                           = tmdb_json['imdb_id']
    if 'vote_average' in tmdb_json and tmdb_json['vote_average'] and 'vote_count' in tmdb_json and tmdb_json['vote_count'] > 3:  metadata.rating = tmdb_json['vote_average']
    if 'genres'       in tmdb_json and tmdb_json['genres']!=[]:
      metadata.genres.clear()
      for genre in tmdb_json['genres']: metadata.genres.add(genre['name'].strip()) #metadata.genres = tmdb_json['genres'] ???
    if 'production_companies' in tmdb_json and len(tmdb_json['production_companies']) > 0:  # Studio.
      index, company = tmdb_json['production_companies'][0]['id'],""
      for studio in tmdb_json['production_companies']:
        if studio['id'] <= index:  index, company = studio['id'], studio['name'].strip()
      metadata.studio = company
    if 'belongs_to_collection' in tmdb_json and tmdb_json['belongs_to_collection']:  
      metadata.collections.clear()
      metadata.collections.add(tmdb_json['belongs_to_collection']['name'].replace(' Collection',''))
    if movie:
      if tmdb_json['tagline']:  metadata.tagline = tmdb_json['tagline']
      metadata.year = metadata.originally_available_at.year    
