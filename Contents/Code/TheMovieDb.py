### TheMovieDb ###  Does movies but also series, for which i call it tsdb in metadata id ##
# TMDB_SEARCH_BY_IMDBID       = "https://api.TheMovieDb.org/3/find/tt0412142?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id"

### Imports ###
# Python Modules #
import os
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###
TMDB_API_KEY                = '7f4a0bd0bd3315bb832e17feda70b5cd'
TMDB_MOVIE_SEARCH           = 'https://api.tmdb.org/3/search/movie?api_key=%s&query={query}&year=&language=en&include_adult=true' % TMDB_API_KEY
TMDB_MOVIE_SEARCH_BY_TMDBID = 'https://api.tmdb.org/3/movie/{id}?api_key=%s&append_to_response=releases,credits,trailers,external_ids&language=en' % TMDB_API_KEY  # Work with IMDbid
TMDB_SERIE_SEARCH_BY_TVDBID = "https://api.TheMovieDb.org/3/find/{id}?api_key=%s&external_source=tvdb_id&append_to_response=releases,credits,trailers,external_ids&language=en" % TMDB_API_KEY
TMDB_CONFIG_URL             = 'https://api.tmdb.org/3/configuration?api_key=%s' % TMDB_API_KEY
#TMDB_MOVIE_GENRE_LIST       = "https://api.TheMovieDb.org/3/genre/movie/list?api_key=%s&language=en" % TMDB_API_KEY
#TMDB_SERIE_GENRE_LIST       = "https://api.TheMovieDb.org/3/genre/tv/list?api_key=%s&language=en" % TMDB_API_KEY
TMDB_MOVIE_IMAGES_URL       = 'https://api.tmdb.org/3/{mode}/{id}/images?api_key=%s' % TMDB_API_KEY

### ###
def GetMetadata(media, movie, TVDBid, TMDbid, IMDbid):
  Log.Info("=== TheMovieDb.GetMetadata() ===".ljust(157, '='))
  TheMovieDb_dict = {}
  TSDbid          = ""
  
  Log.Info("TVDBid: '{}', TMDbid: '{}', IMDbid: '{}'".format(TVDBid, TMDbid, IMDbid))
  if   TMDbid:            url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID.format(id=TMDbid), "TMDB-"+TMDbid+".json"
  elif IMDbid:            url, filename = TMDB_MOVIE_SEARCH_BY_TMDBID.format(id=IMDbid), "IMDb-"+IMDbid+".json"
  elif TVDBid.isdigit():  url, filename = TMDB_SERIE_SEARCH_BY_TVDBID.format(id=TVDBid), "TVDB-"+TVDBid+".json"
  else:                   return TheMovieDb_dict, TSDbid, TMDbid, IMDbid
  
  mode           = "movie" if movie else "tv"
  Log.Info(("--- %s ---" % mode).ljust(157, '-'))
  json           = common.LoadFile(filename=filename,               relativeDirectory=os.path.join('TheMovieDb', 'json'), url=url)
  config_dict    = common.LoadFile(filename="TMDB_CONFIG_URL.json", relativeDirectory="TheMovieDb",                       url=TMDB_CONFIG_URL, cache=CACHE_1MONTH)
  image_base_url = Dict(config_dict, 'images', 'secure_base_url')
  if not json:  Log.Info("TMDB - url: failed to get json" + TMDB_MOVIE_SEARCH_BY_TMDBID.format(id=TMDbid))
  else:  
    if   Dict(json, 'tv_results'   ):  json, mode = json['tv_results'   ][0], "tv"
    elif Dict(json, 'movie_results'):  json, mode = json['movie_results'][0], "movie"
    
    Log.Info("[ ] title: {}"                  .format(SaveDict( Dict(json, 'title') or Dict(json, 'name'),                  TheMovieDb_dict, 'title'                  )))`
    Log.Info("[ ] rating: {}"                 .format(SaveDict( Dict(json, 'vote_average'),                                 TheMovieDb_dict, 'rating'                 )))  #if 'vote_count' in json and json['vote_count'] > 3:  SaveDict( Dict(json, 'vote_average'), TheMovieDb_dict, 'rating')
    Log.Info("[ ] tagline: {}"                .format(SaveDict( Dict(json, 'tagline'),                                      TheMovieDb_dict, 'tagline'                )))
    Log.Info("[ ] summary: {}"                .format(SaveDict( Dict(json, 'overview'),                                     TheMovieDb_dict, 'summary'                )))
    Log.Info("[ ] duration: {}"               .format(SaveDict( Dict(json, 'runtime'),                                      TheMovieDb_dict, 'duration'               )))
    Log.Info("[ ] countries: {}"              .format(SaveDict( Dict(json, 'origin_country'),                               TheMovieDb_dict, 'countries'              )))
    Log.Info("[ ] originally_available_at: {}".format(SaveDict( Dict(json, 'first_air_date') or Dict(json, 'release_date'), TheMovieDb_dict, 'originally_available_at')))
    if Dict(json, 'belongs_to_collection', 'name'):  Log.Info("[ ] collections: {}".format(SaveDict( [ Dict(json, 'belongs_to_collection', 'name')],                                TheMovieDb_dict, 'collections')))
    if Dict(json, 'genres'                       ):  Log.Info("[ ] genres: {}"     .format(SaveDict( sorted([ Dict(genre, 'name') for genre in Dict(json, 'genres', default=[]) ]), TheMovieDb_dict, 'genres'     )))
    if Dict(json, 'poster_path'                  ):  Log.Info("[ ] poster: {}"     .format(image_base_url + 'original' + json['poster_path']  )); SaveDict( (os.path.join('TheMovieDb', 'poster',  json['poster_path'  ].lstrip('/')), common.poster_rank('TheMovieDb', 'posters'), None),                                            TheMovieDb_dict, 'posters', image_base_url + 'original' + json['poster_path']  )
    if Dict(json, 'backdrop_path'                ):  Log.Info("[ ] art: {}"        .format(image_base_url + 'original' + json['backdrop_path'])); SaveDict( (os.path.join('TheMovieDb', 'artwork', json['backdrop_path'].lstrip('/')), common.poster_rank('TheMovieDb', 'art'    ), image_base_url + 'w300' + json['backdrop_path']), TheMovieDb_dict, 'art',     image_base_url + 'original' + json['backdrop_path'])
    try:     Log.Info("[ ] duration: {}".format(SaveDict( int(Dict(json, 'duration')) * 60 * 1000,  TheMovieDb_dict, 'duration')))
    except:  pass
    if mode=='tv':   TSDbid = str(Dict(json, 'id'))
    elif not TMDbid: TMDbid = str(Dict(json, 'id'))
    if not IMDbid:   IMDbid = Dict(json, 'imdb_id')
    
    for studio in Dict(json, 'production_companies', default=[]):
      if studio['id'] <= json['production_companies'][0]['id']:
        Log.Info("[ ] studio: {}".format(SaveDict( studio['name'].strip(), TheMovieDb_dict, 'studio')))
  
  ### More pictures ###
  Log.Info("--- pictures.more ---".ljust(157, '-'))
  Log.Info("TMDbid: '{}', TSDbid: '{}', IMDbid: '{}'".format(TMDbid, TSDbid, IMDbid))
  for id in IMDbid.split(',') if ',' in IMDbid else []:
    json                  = common.LoadFile(filename="TMDB-"+(IMDbid or TMDbid)+".json", relativeDirectory="TMDB", url=TMDB_MOVIE_IMAGES_URL.format(id=id, mode=mode))
    for index, poster in enumerate(Dict(json, 'posters', default=[])):
      if Dict(poster,   'file_path'):  Log.Info("[ ] poster: {}" .format(image_base_url + 'original' + poster['file_path'] )); SaveDict((os.path.join('TheMovieDb', 'poster',  "%s-%s.jpg" % (TMDbid, index)),     common.poster_rank('TheMovieDb', 'posters'), None),                                            TheMovieDb_dict, 'posters', image_base_url + 'original' + poster['file_path']  )
    for index, backdrop in enumerate(Dict(json, 'backdrops', default=[])):
      if Dict(backdrop, 'file_path'):  Log.Info("[ ] artwork: {}".format(image_base_url + 'original'+ backdrop['file_path'])); SaveDict((os.path.join('TheMovieDb', 'artwork', "%s-%s-art.jpg" % (TMDbid, index)), common.poster_rank('TheMovieDb', 'art'),     image_base_url + 'w300' + backdrop['file_path']), TheMovieDb_dict, 'art',     image_base_url + 'original' + backdrop['file_path'])
  
  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("TheMovieDb_dict: {}".format(DictString(TheMovieDb_dict, 4)))
  return TheMovieDb_dict, TSDbid, TMDbid, IMDbid

### TMDB movie search ###
def Search(results, media, lang, manual, movie):
  Log.Info("=== TheMovieDb.Search() ===".ljust(157, '='))
  #'Uchiage Hanabi, Shita kara Miru ka？ Yoko kara Miru ka？ 打ち上げ花火、下から見るか？横から見るか？' Failed with: TypeError: not all arguments converted during string formatting
  #Fixed with:tmdb_url = TMDB_MOVIE_SEARCH.format(query=String.Quote(orig_title)) Log.Info("TMDB - url: " + tmdb_url) try: json = JSON.ObjectFromURL(tmdb_url, sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1WEEK * 2) except Exception as e: Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" % (tmdb_url, e) )
  orig_title = String.Quote(media.name if manual and movie else media.title if movie else media.show)
  maxi = 0
  
  Log.Info("TMDB  - url: " + TMDB_MOVIE_SEARCH.format(query=orig_title))
  try:                    json = JSON.ObjectFromURL(TMDB_MOVIE_SEARCH.format(query=orig_title), sleep=2.0, headers=common.COMMON_HEADERS, cacheTime=CACHE_1WEEK * 2)
  except Exception as e:  Log.Error("get_json - Error fetching JSON page '%s', Exception: '%s'" %( TMDB_MOVIE_SEARCH.format(query=orig_title), e)) # json   = common.get_json(TMDB_MOVIE_SEARCH % orig_title, cache_time=CACHE_1WEEK * 2)
  else:
    if isinstance(json, dict) and 'results' in json:
      for movie in json['results']:
        a, b  = orig_title, movie['title'].encode('utf-8')
        score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
        if maxi<score:  maxi = score
        Log.Info("TMDB  - score: '%3d', id: '%6s', title: '%s'" % (score, movie['id'],  movie['title']) )
        results.Append(MetadataSearchResult(id="tmdb-"+str(movie['id']), name="{} [{}-{}]".format(movie['title'], "tmdb", movie['id']), year=None, lang=lang, score=score) )
        if '' in movie and movie['adult']!="null":  Log.Info("adult: '{}'".format(movie['adult']))
  return maxi
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
  
