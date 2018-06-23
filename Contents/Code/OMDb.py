### omdbapi.com ###  
# API               http://www.omdbapi.com/
# API xml exemple:  tt0412142   1408  House md   http://www.omdbapi.com/?i=tt0412142
# API xml exemple:  tt0186151  10559  Frequency  http://www.omdbapi.com/?i=tt0186151

### Imports ###
import common
from common import SaveDict, Dict
import os

### Variables ###

### Functions ###
def GetMetadata(movie, imdbid, num=98):  # return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
  OMDB_HTTP_API_URL = "http://www.omdbapi.com/?apikey={api_key}&i=".format(api_key=Prefs['OMDbApiKey']) #'
  OMDb_dict         = {}
  
  Log.Info("".ljust(157, '-'))
  Log.Info("OMDb.GetMetadata() - background, Poster - imdbid: '%s'" % imdbid)
  for imdbid_single in imdbid.split(",") if imdbid.startswith("tt") else []:
    json = common.LoadFile(filename=imdbid_single+".json", relativeDirectory=os.path.join('OMDb', 'json'), url=OMDB_HTTP_API_URL + imdbid_single, cache=CACHE_1WEEK)
    if json:
      SaveDict( Dict(json,'title')     , OMDb_dict, 'title'                  )
      SaveDict( Dict(json,'Plot')      , OMDb_dict, 'summary'                )
      SaveDict( Dict(json,'Released')  , OMDb_dict, 'originally_available_at')
      SaveDict( Dict(json,'Country')   , OMDb_dict, 'countries'              )
      SaveDict( Dict(json,'Director')  , OMDb_dict, 'directors'              )
      SaveDict( Dict(json,'Genre')     , OMDb_dict, 'genres'                 )
      SaveDict( Dict(json,'Writer')    , OMDb_dict, 'writers'                )
      SaveDict( Dict(json,'imdbRating'), OMDb_dict, 'rating'                 )
      if Dict(json,'Metascore').isdigit() and not Dict(OMDb_dict,'rating'):
        SaveDict( float(json['Metascore'])/10, OMDb_dict, 'rating')
      if SaveDict( Dict(json,'Rated'), OMDb_dict, 'content_rating') in common.Movie_to_Serie_US_rating and not movie and Dict(json,'Type')=="movie":
        SaveDict( common.Movie_to_Serie_US_rating[json['Rated']], OMDb_dict, 'content_rating')
      if Dict(json,'Poster'):  SaveDict(os.path.join('OMDb', 'poster', imdbid_single+'.jpg', num, None), OMDb_dict, 'posters', json['Poster'])
      try:     SaveDict( int(Dict(json,'Runtime').replace(' min','')) * 60 * 1000, OMDb_dict, 'duration')  # Plex save duration in millisecs
      except:  pass
  return OMDb_dict