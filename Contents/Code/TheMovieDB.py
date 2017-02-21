### TheMovieDB ###  Does movies but also series, for which i call it tsdb in metadata id ##
# tt0412142   1408  House md   http://www.omdbapi.com/?i=tt0412142 tvdb 73255
# tt0186151  10559  Frequency  http://www.omdbapi.com/?i=tt0186151
  
### Imports ###
import common
from common import GetPosters, GetSeasons, GetFanarts, GetBanners, GetElementText

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### ###
def GetMetadata (metadata, media, movie, IMDbid, TMDbid, TVDBid):
  TMDB_MOVIE_SEARCH_BY_TMDBID = 'http://api.tmdb.org/3/movie/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=releases,credits,trailers&language=en'  #Work with imdbid
  TMDB_SEARCH_BY_IMDBID       = "https://api.themoviedb.org/3/find/tt0412142?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id"
  TMDB_SERIE_SEARCH_BY_TVDBID = "http://api.themoviedb.org/3/find/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=tvdb_id&append_to_response=releases,credits,trailers&language=en"
  TMDB_CONFIG_URL             = 'http://api.tmdb.org/3/configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
  genre_dict = {12:"Adventure", 16:"Animation", 14:"Fantasy", 18:"Drama", 27:"Horror", 28:"Action", 35:"Comedy", 36:"History", 37:"Western",
                53:"Thriller", 80:"Crime",99:"Documentary", 878:"Science Fiction", 
                9648:"Mystery", 10402:"Music", 10749:"Romance", 10751:"Family", 10752:"War", 10759:"Action & Adventure", 10762:"Kids", 10763:"News",
                10764:"Reality", 10765:"Sci-Fi & Fantasy", 10766:"Soap", 10767:"Talk", 10768:"War & Politics", 10770:"TV Movie"}
  #TMDB_MOVIE_GENRE_LIST       = "https://api.themoviedb.org/3/genre/movie/list?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&language=en-US"
  #TMDB_SERIE_GENRE_LIST       = "https://api.themoviedb.org/3/genre/tv/list?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&language=en-US"
  TheMovieDB_dict = {}
  
  Log.Info("".ljust(157, '-'))
  Log("TheMovieDB.GetMetadata() - IMDbid: {}, TMDbid: {}, TVDBid: {}".format(IMDbid, TMDbid, TVDBid))
  if   TMDbid:  url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID % TMDbid, "TMDB-"+TMDbid+".json"
  elif IMDbid:  url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID % IMDbid, "IMDb-"+IMDbid+".json"
  elif TVDBid:  url, filename = TMDB_SERIE_SEARCH_BY_TVDBID % TVDBid, "TVDB-"+TVDBid+".json"
  else:         return {}
  
  TheMovieDB_json = common.LoadFile(filename=filename, relativeDirectory="OMDB", url=url, cache=CACHE_1WEEK)
  config_dict     = common.LoadFile(filename="TMDB_CONFIG_URL.json", relativeDirectory="", url=TMDB_CONFIG_URL, cache= CACHE_1DAY *30 )
  if TheMovieDB_json:
    if   'tv_results'    in TheMovieDB_json and TheMovieDB_json['tv_results'   ]:  TheMovieDB_json = TheMovieDB_json['tv_results'   ][0]
    elif 'movie_results' in TheMovieDB_json and TheMovieDB_json['movie_results']:  TheMovieDB_json = TheMovieDB_json['movie_results'][0]
    
    if 'id'             in TheMovieDB_json and TheMovieDB_json['id'] and not TMDbid:                TMDbid                                     = str(TheMovieDB_json['id'])
    if 'imdb_id'        in TheMovieDB_json and TheMovieDB_json['imdb_id'] and not imdbid:           IMDbid                                     = str(TheMovieDB_json['imdb_id'])
    if 'vote_average'   in TheMovieDB_json and isinstance(TheMovieDB_json['vote_average'], float):  TheMovieDB_dict['rating'                 ] = TheMovieDB_json['vote_average'] if 'vote_count' in TheMovieDB_json and TheMovieDB_json['vote_count'] > 3 else None
    if 'runtime'        in TheMovieDB_json and isinstance(TheMovieDB_json['runtime'     ],   int):  TheMovieDB_dict['duration'               ] = int(TheMovieDB_json['runtime']) * 60 * 1000
    if 'title'          in TheMovieDB_json and TheMovieDB_json['title']:                            TheMovieDB_dict['title'                  ] = TheMovieDB_json['title']
    if 'overview'       in TheMovieDB_json and TheMovieDB_json['overview']:                         TheMovieDB_dict['summary'                ] = TheMovieDB_json['overview']
    if 'first_air_date' in TheMovieDB_json and TheMovieDB_json['first_air_date']:                   TheMovieDB_dict['originally_available_at'] = Datetime.ParseDate(TheMovieDB_json['first_air_date']).date()
    if movie: TheMovieDB_dict['year'] = TheMovieDB_dict['originally_available_at'].year
    if 'tagline'        in TheMovieDB_json and TheMovieDB_json['tagline']:                          TheMovieDB_dict['tagline']                 = TheMovieDB_json['tagline']
    if 'belongs_to_collection' in TheMovieDB_json and TheMovieDB_json['belongs_to_collection']:     TheMovieDB_dict['collections'            ] =[TheMovieDB_json['belongs_to_collection']['name'].replace(' Collection','')]
    if 'genres'       in TheMovieDB_json and TheMovieDB_json['genres']:                             TheMovieDB_dict['genres']                 = [ genre_dict[x] for x in TheMovieDB_json['genres'] if x in genre_dict]
    if 'production_companies' in TheMovieDB_json and len(TheMovieDB_json['production_companies']) > 0:  # Studio.
      index, company = TheMovieDB_json['production_companies'][0]['id'],""
      for studio in TheMovieDB_json['production_companies']:
        if studio['id'] <= index:  TheMovieDB_dict['studio'] = studio['name'].strip()
    if 'poster_path'   in TheMovieDB_json and TheMovieDB_json['poster_path'  ] not in (None, "", "null") and GetPosters("TheMovieDB"):  TheMovieDB_dict['art'    ] = { config_dict['images']['base_url']+'original'+TheMovieDB_json['poster_path'  ]: (TheMovieDB_json['poster_path'  ].strip("/"), 90, None)}
    if 'backdrop_path' in TheMovieDB_json and TheMovieDB_json['backdrop_path'] not in (None, "", "null") and GetFanarts("TheMovieDB"):  TheMovieDB_dict['posters'] = { config_dict['images']['base_url']+'original'+TheMovieDB_json['backdrop_path']: (TheMovieDB_json['backdrop_path'].strip("/"), 90, config_dict['images']['base_url']+'w300'+TheMovieDB_json['backdrop_path']) }
        
  else:  Log.Info("TMDB - url: failed to get json" + TMDB_MOVIE_SEARCH_BY_TMDBID % TMDbid)  
  
  ### More pictures ###
  Log.Info("TheMovieDB.GetMetadata() - IMDbid: '%s', TMDbid: '%s'" % (IMDbid, TMDbid))
  for id in IMDbid.split(",") if IMDbid else TMDbid.split(",") if TMDbid else []:
    TMDB_MOVIE_IMAGES_URL     = 'https://api.tmdb.org/3/movie/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'                  #
    TMDB_SERIE_IMAGES_URL     = 'https://api.tmdb.org/3/tv/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'                     #
    TMDB_MOVIE_SEARCH         = 'http://api.tmdb.org/3/search/movie?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&query=%s&year=&language=en&include_adult=true'
    
    if   TMDbid:  url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID % TMDbid, "TMDB-"+TMDbid+".json"
    elif IMDbid:  url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID % IMDbid, "IMDb-"+IMDbid+".json"
    elif TVDBid:  url, filename = TMDB_SERIE_SEARCH_BY_TVDBID % TVDBid, "TVDB-"+TVDBid+".json"
    TheMovieDB_json = common.LoadFile(filename=filename, relativeDirectory="TMDB", url=url, cache=CACHE_1WEEK)
    if TheMovieDB_json and 'posters'    in TheMovieDB_json and len(TheMovieDB_json['posters'  ]):
      for index, poster in enumerate(TheMovieDB_json['posters']):
        if GetPosters("TheMovieDB") and 'file_path' in TheMovieDB_json['posters'][index] and TheMovieDB_json['posters'][index]['file_path'] not in (None, "", "null"):
          TheMovieDB_dict['posters'][ config_dict['images']['base_url'] + 'original' + TheMovieDB_json['posters'][index]['file_path'] ] = ("TMDB/%s-%s.jpg" % (TMDbid, index), 40, None) 
    if TheMovieDB_json is not None and 'backdrops' in TheMovieDB_json and len(TheMovieDB_json['backdrops']):
      for index, poster in enumerate(TheMovieDB_json['backdrops']):
        if GetFanarts("TheMovieDB") and 'file_path' in TheMovieDB_json['backdrops'][index] and TheMovieDB_json['backdrops'][index]['file_path'] not in (None, "", "null"):
          TheMovieDB_dict['posters'][ config_dict['images']['base_url']+'original'+ TheMovieDB_json['backdrops'][index]['file_path'] ] = ("TMDB/%s-%s-art.jpg" % (TMDbid, index), 40, config_dict['images']['base_url'] + 'w300'+ TheMovieDB_json['backdrops'][index]['file_path']) 
  
  ### Trailers (Movie Library Only) ###
  YOUTUBE_VIDEO_DETAILS = 'https://m.youtube.com/watch?ajax=1&v=%s'
  TYPE_MAP =  { 'primary_trailer'   : TrailerObject,
                'trailer'           : TrailerObject,
                'interview'         : InterviewObject,
                'behind_the_scenes' : BehindTheScenesObject,
                'scene_or_sample'   : SceneOrSampleObject
              }  #https://github.com/plexinc-agents/PlexMovie.bundle/blob/master/Contents/Code/__init__.py
  #metadata.extras.add(Trailer(title=title, file=os.path.join(folder_path, f)))  #https://github.com/gboudreau/XBMCnfoMoviesImporter.bundle/blob/master/Contents/Code/__init__.py
  extras = []
  if movie:  # https://github.com/sander1/YouTube-Agent.bundle/blob/master/Contents/Code/__init__.py
    if 'trailers' in TheMovieDB_json and TheMovieDB_json['trailers']:
      if "quicktime" in TheMovieDB_json['trailers'] and TheMovieDB_json['trailers']["quicktime"]:
        for trailer in TheMovieDB_json['trailers']["quicktime"]:
          Log.Info("Trailer detected: " + str (TheMovieDB_json['trailers']["quicktime"]))
          #metadata.extras.add( TrailerObject(url = "???"+trailer["source"]), title = trailer["name"], thumb = None) )
      if "youtube" in TheMovieDB_json['trailers'] and TheMovieDB_json['trailers']["youtube"]:
        for trailer in TheMovieDB_json['trailers']["youtube"]:
          Log.Info("Trailer detected: name: '%s', size: '%s', source: '%s', type: '%s', link: '%s'" % (trailer["name"], trailer["size"], trailer["source"], trailer["type"], "https://www.youtube.com/watch?v="+trailer["source"]))
          json_obj = None
          try:     json_obj = JSON.ObjectFromString( HTTP.Request(YOUTUBE_VIDEO_DETAILS % trailer["source"]).content[4:] )['content']
          except:  Log("TheMovieDB.GetMetadata() - Trailers - Could not retrieve data from YouTube for: '%s'" % trailer["source"])
          if json_obj:
            Log.Info("TheMovieDB.GetMetadata() - Trailers - json_obj: '%s'" % str(json_obj))
            #metadata.extras.add( TrailerObject(url = "https://www.youtube.com/watch?v="+trailer["source"]), title = json_obj['video']['title'], thumb = 'https://%s' % (json_obj['video']['thumbnail_for_watch'].split('//')[-1])) )
            #metadata.extras.add( TrailerObject(url = "https://www.youtube.com/watch?v="+trailer["source"]), title = json_obj['video']['title'], thumb = Proxy.Preview(HTTP.Request('https://%s' % (json_obj['video']['thumbnail_for_watch'].split('//')[-1])  ).content, sort_order=1))
            metadata.extras.add(TrailerObject(url                     = "https://www.youtube.com/watch?v="+trailer["source"],
                                              title                   = json_obj['video']['title'],
                                              #year                    = avail.year,
                                              #originally_available_at = avail,
                                              thumb                   = 'https://%s' % (json_obj['video']['thumbnail_for_watch'].split('//')[-1]) if 'thumbnail_for_watch' in json_obj['video'] else None
                                             )
                               )
            #metadata.title                   = json_obj['video']['title']
            #metadata.duration                = json_obj['video']['length_seconds'] * 1000
            #thumb                            = 'https://%s' % (json_obj['video']['thumbnail_for_watch'].split('//')[-1])
            #metadata.posters[thumb]          = Proxy.Preview(HTTP.Request(thumb).content, sort_order=1)
            #metadata.summary                 = json_obj['video_main_content']['contents'][0]['description']['runs'][0]['text']
            #date                             = Datetime.ParseDate(json_obj['video_main_content']['contents'][0]['date_text']['runs'][0]['text'].split('Published on ')[-1])
            #metadata.originally_available_at = date.date()
            #metadata.year                    = date.year
            # Add YouTube user as director
             #metadata.directors.clear()
            #if Prefs['add_user_as_director']:
            #  meta_director = metadata.directors.new()
            #  meta_director.name  = json_obj['video_main_content']['contents'][0]['short_byline_text']['runs'][0]['text']
            #  meta_director.photo = json_obj['video_main_content']['contents'][0]['thumbnail']['url'].replace('/s88-', '/s512-')
            #	

  return TMDbid, IMDbid, TheMovieDB_dict

### TMDB movie search ###
def Search (results, media, lang, manual, movie):
  
  orig_title = ( media.title if movie else media.show )
  Log.Info("TMDB  - url: " + TMDB_MOVIE_SEARCH % orig_title)
  try:                    TheMovieDB_json = JSON.ObjectFromURL(TMDB_MOVIE_SEARCH % orig_title.replace(" ", "%20"), sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1WEEK * 2)
  except Exception as e:  Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %( TMDB_MOVIE_SEARCH % orig_title, e)) # TheMovieDB_json   = common.get_json(TMDB_MOVIE_SEARCH % orig_title, cache_time=CACHE_1WEEK * 2)
  else:
    if isinstance(TheMovieDB_json, dict) and 'results' in TheMovieDB_json:
      for i, movie in enumerate(TheMovieDB_json['results']):
        a, b = orig_title, movie['title'].encode('utf-8')
        score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
        id = movie['id']
        Log.Info("TMDB  - score: '%3d', id: '%6s', title: '%s'" % (score, movie['id'],  movie['title']) )
        results.Append(MetadataSearchResult(id="%s-%s" % ("tmdb", movie['id']), name="%s [%s-%s]" % (movie['title'], "tmdb", movie['id']), year=None, lang=lang, score=score) )
        if '' in movie and movie['adult']!="null":  Log.Info("adult: '%s'" % movie['adult'])
        # genre_ids, original_language, id, original_language, original_title, overview, release_date, poster_path, popularity, video, vote_average, vote_count, adult, backdrop_path
