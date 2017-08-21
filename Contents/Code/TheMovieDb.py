### TheMovieDb ###  Does movies but also series, for which i call it tsdb in metadata id ##
# tt0412142   1408  House md   http://www.omdbapi.com/?i=tt0412142 tvdb 73255
# tt0186151  10559  Frequency  http://www.omdbapi.com/?i=tt0186151
# tt5311514         Your Name
#TMDB_SEARCH_BY_IMDBID       = "https://api.TheMovieDb.org/3/find/tt0412142?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id"

### Imports ###
import common
from   common import GetMeta, SaveDict, Dict
import os
### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'
  
### ###
def GetMetadata (media, movie, TVDBid, TMDbid, IMDbid):
  TMDB_MOVIE_SEARCH_BY_TMDBID = 'http://api.tmdb.org/3/movie/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=releases,credits,trailers,external_ids&language=en'  #Work with IMDbid
  TMDB_SERIE_SEARCH_BY_TVDBID = "http://api.TheMovieDb.org/3/find/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=tvdb_id&append_to_response=releases,credits,trailers,external_ids&language=en"
  TMDB_CONFIG_URL             = 'http://api.tmdb.org/3/configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
  #TMDB_MOVIE_GENRE_LIST       = "https://api.TheMovieDb.org/3/genre/movie/list?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&language=en-US"
  #TMDB_SERIE_GENRE_LIST       = "https://api.TheMovieDb.org/3/genre/tv/list?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&language=en-US"
  dict_TheMovieDb = {}
  TSDbid = ""
  
  Log.Info("".ljust(157, '-'))
  Log("TheMovieDb.GetMetadata() - TVDBid: {}, TMDbid: {}, IMDbid: {}".format(TVDBid, TMDbid, IMDbid))
  if   TMDbid:                      url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID % TMDbid, "TMDB-"+TMDbid+".json"
  elif IMDbid and TVDBid=='movie':  url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID % IMDbid, "IMDb-"+IMDbid+".json"
  elif TVDBid.isdigit():            url, filename = TMDB_SERIE_SEARCH_BY_TVDBID % TVDBid, "TVDB-"+TVDBid+".json"
  else:                             return dict_TheMovieDb, TSDbid, TMDbid, IMDbid
  
  json        = common.LoadFile(filename=filename,               relativeDirectory=os.path.join('TheMovieDb', 'json'), url=url,             cache=CACHE_1WEEK)
  config_dict = common.LoadFile(filename="TMDB_CONFIG_URL.json", relativeDirectory="TheMovieDb",                       url=TMDB_CONFIG_URL, cache= CACHE_1DAY *30 )
  mode        = "movie" if movie else "tv"
  if not json:  Log.Info("TMDB - url: failed to get json" + TMDB_MOVIE_SEARCH_BY_TMDBID % TMDbid)
  else:  
    if   'tv_results'    in json and json['tv_results'   ]:  json, mode = json['tv_results'   ][0], "tv"
    elif 'movie_results' in json and json['movie_results']:  json, mode = json['movie_results'][0], "movie"
    
    SaveDict( Dict(json, 'title'),                                                      dict_TheMovieDb, 'title')
    SaveDict( Dict(json, 'vote_average'),                                               dict_TheMovieDb, 'rating')  #if 'vote_count' in json and json['vote_count'] > 3:  SaveDict( Dict(json, 'vote_average'), dict_TheMovieDb, 'rating')
    SaveDict( Dict(json, 'tagline'),                                                    dict_TheMovieDb, 'tagline')
    SaveDict( Dict(json, 'overview'),                                                   dict_TheMovieDb, 'summary')
    SaveDict( Dict(json, 'runtime'),                                                    dict_TheMovieDb, 'duration')
    SaveDict( Dict(json, 'origin_country'),                                             dict_TheMovieDb, 'countries')
    SaveDict( Dict(json, 'first_air_date'),                                             dict_TheMovieDb, 'originally_available_at')
    if Dict(json, 'belongs_to_collection', 'name'):  SaveDict( [ Dict(json, 'belongs_to_collection', 'name').replace(' Collection','')], dict_TheMovieDb, 'collections')
    if Dict(json, 'genres'                       ):  SaveDict( [ Dict(genre, 'name') for genre in Dict(json, 'genres') or [] ],          dict_TheMovieDb, 'genres')
    if Dict(json, 'poster_path'                  ):  dict_TheMovieDb['posters'] = { config_dict['images']['base_url']+'original'+json['poster_path'  ]: (os.path.join('TheMovieDb', 'poster',  json['poster_path'  ].lstrip('/')), 90, None)}
    if Dict(json, 'backdrop_path'                ):  dict_TheMovieDb['art'    ] = { config_dict['images']['base_url']+'original'+json['backdrop_path']: (os.path.join('TheMovieDb', 'artwork', json['backdrop_path'].lstrip('/')), 90, config_dict['images']['base_url']+'w300'+json['backdrop_path']) }
    try:     SaveDict( int(Dict(json, 'duration')) * 60 * 1000,  dict_TheMovieDb, 'duration')
    except:  pass
    #Log.Info(str(dict_TheMovieDb))
    if mode=='tv':   TSDbid = Dict(json, 'id')
    elif not TMDbid: TMDbid = Dict(json, 'id')
    if not IMDbid:   IMDbid = Dict(json, 'imdb_id')
    
    #SaveDict( studio['name'].strip(), dict_TheMovieDb, 'studio')
    for studio in Dict(json, 'production_companies') or []:
      if studio['id'] <= json['production_companies'][0]['id']:
        SaveDict( studio['name'].strip(), dict_TheMovieDb, 'studio')
  
  ### More pictures ###
  Log.Info("TheMovieDb.GetMetadata() - TMDbid: '{}', TSDbid: '{}', IMDbid: '{}'".format(TMDbid, TSDbid, IMDbid))
  for id in IMDbid.split(',') if ',' in IMDbid and not Prefs['GetSingleOne'] else []:
    TMDB_MOVIE_IMAGES_URL = 'https://api.tmdb.org/3/{mode}/{id}/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
    json                  = common.LoadFile(filename="TMDB-"+(IMDbid or TMDbid)+".json", relativeDirectory="TMDB", url=TMDB_MOVIE_IMAGES_URL.format(id=id, mode=mode), cache=CACHE_1WEEK)
    for index, poster in enumerate(Dict(json, 'posters') or []):
      if GetMeta("TheMovieDb", 'posters') and Dict(json, 'posters', index, 'file_path'):
        SaveDict((os.path.join('TheMovieDb', 'poster', "%s-%s.jpg" % (TMDbid, index)), 40, None), dict_TheMovieDb, 'posters', config_dict['images']['base_url'] + 'original' + json['posters'][index]['file_path'])
    for index, poster in enumerate(Dict(json, 'backdrops') or []):
      if GetMeta("TheMovieDb", 'art') and Dict(json, 'backdrops', index, 'file_path'):
        SaveDict((os.path.join('TheMovieDb', 'artwork', "%s-%s-art.jpg" % (TMDbid, index)), 40, config_dict['images']['base_url'] + 'w300'+ json['backdrops'][index]['file_path']), dict_TheMovieDb, 'art', config_dict['images']['base_url']+'original'+ json['backdrops'][index]['file_path'])
  
  return dict_TheMovieDb, TSDbid, TMDbid, IMDbid

### TMDB movie search ###
def Search (results, media, lang, manual, movie):
  TMDB_MOVIE_SEARCH = 'http://api.tmdb.org/3/search/movie?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&query={}&year=&language=en&include_adult=true'
  orig_title        = media.title if movie else media.show
  Log.Info("TMDB  - url: " + TMDB_MOVIE_SEARCH.format(orig_title))
  try:                    json = JSON.ObjectFromURL(TMDB_MOVIE_SEARCH % String.Quote(orig_title), sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1WEEK * 2)
  except Exception as e:  Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %( TMDB_MOVIE_SEARCH % orig_title, e)) # json   = common.get_json(TMDB_MOVIE_SEARCH % orig_title, cache_time=CACHE_1WEEK * 2)
  else:
    if isinstance(json, dict) and 'results' in json:
      for i, movie in enumerate(json['results']):
        a, b  = orig_title, movie['title'].encode('utf-8')
        score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
        id    = movie['id']
        Log.Info("TMDB  - score: '%3d', id: '%6s', title: '%s'" % (score, movie['id'],  movie['title']) )
        results.Append(MetadataSearchResult(id="tmdb-"+movie['id'], name="{} [{}-{}]".format(movie['title'], "tmdb", movie['id']), year=None, lang=lang, score=score) )
        if '' in movie and movie['adult']!="null":  Log.Info("adult: '{}'".format(movie['adult']))

### Trailers (Movie Library Only) ###
### For when youtube mp4 url can be gotten again
'''
  YOUTUBE_VIDEO_DETAILS = 'https://m.youtube.com/watch?ajax=1&v=%s'
  TYPE_MAP =  { 'primary_trailer'   : TrailerObject,          'trailer'           : TrailerObject,       'interview'         : InterviewObject,
                'behind_the_scenes' : BehindTheScenesObject,  'scene_or_sample'   : SceneOrSampleObject
              }  #https://github.com/plexinc-agents/PlexMovie.bundle/blob/master/Contents/Code/__init__.py
  #metadata.extras.add(Trailer(title=title, file=os.path.join(folder_path, f)))  #https://github.com/gboudreau/XBMCnfoMoviesImporter.bundle/blob/master/Contents/Code/__init__.py
  extras = []
  if movie:  # https://github.com/sander1/YouTube-Agent.bundle/blob/master/Contents/Code/__init__.py
    if 'trailers' in json and json['trailers']:
      if "quicktime" in json['trailers'] and json['trailers']["quicktime"]:
        for trailer in json['trailers']["quicktime"]:
          Log.Info("Trailer detected: " + str (json['trailers']["quicktime"]))
          #metadata.extras.add( TrailerObject(url = "???"+trailer["source"]), title = trailer["name"], thumb = None) )
      if "youtube" in json['trailers'] and json['trailers']["youtube"]:
        for trailer in json['trailers']["youtube"]:
          Log.Info("Trailer detected: name: '%s', size: '%s', source: '%s', type: '%s', link: '%s'" % (trailer["name"], trailer["size"], trailer["source"], trailer["type"], "https://www.youtube.com/watch?v="+trailer["source"]))
          json_obj = None
          try:     json_obj = JSON.ObjectFromString( HTTP.Request(YOUTUBE_VIDEO_DETAILS % trailer["source"]).content[4:] )['content']
          except:  Log("TheMovieDb.GetMetadata() - Trailers - Could not retrieve data from YouTube for: '%s'" % trailer["source"])
          if json_obj:
            Log.Info("TheMovieDb.GetMetadata() - Trailers - json_obj: '%s'" % str(json_obj))
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
  '''
  