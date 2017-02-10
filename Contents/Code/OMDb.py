### omdbapi.com ###  

### Imports ###
import common
from common import GetPosters

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name' ###

### Functions ###
def GetMetadata(metadata, imdbid, movie, num=98, name=""):  # return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
  OMDB_HTTP_API_URL = "http://www.omdbapi.com/?i="
  OMDb_dict = {}
  if imdbid.startswith("tt"):
    Log.Info("[X] OMDB - background, Poster - imdbid: '%s'" % imdbid)
    for imdbid_single in imdbid.split(","):
      json = common.LoadFile(filename=imdbid_single+".json", relativeDirectory="OMDB", url=OMDB_HTTP_API_URL + imdbid_single, cache=CACHE_1WEEK)
      if json:
        
        ### Common to Movies and Series Libraries
        # 'title'
        if "Title"    in json and json["Title"   ]:  OMDb_dict['title'   ] = json["Title"]
    
        # 'summary'
        if "Plot"     in json and json["Plot"    ]:  OMDb_dict['summary' ] = json["Plot"]
    
        # 'originally_available_at'
        if "Released" in json and json["Released"]:  OMDb_dict["Released"] = json["Released"]
    
        # 'duration'  # Plex save duration in millisecs
        if "Runtime"  in json and json["Runtime" ]:
          try:     OMDb_dict['duration'] = int(json["Runtime"].replace(' min','')) * 60 *1000
          except:  pass
        
        # 'studio'
        # 'producers'
        
        # 'writers'
        if "Writer" in json and json["Writer"]: # remove parenthesis before adding
          import re
          OMDb_dict['writers'] = re.sub(r'\([^)]*\)', '', json["Writer"]).split(',') 
    
        # 'directors'
        if "Director" in json and json["Director"]:  OMDb_dict['directors'] = json["Director"].split(',')
        
        
        # 'rating'
        if "imdbRating" in json and json["imdbRating"]:  OMDb_dict['rating'] = json["imdbRating"]          #:"8.1"
        #if "Metascore"  in json and json["Metascore" ]:  OMDb_dict['rating'] = float(json["Metascore"])/10  #:"76"
        
        # 'genres'
        if "Genre"    in json and json["Genre"   ]:  OMDb_dict['genres' ] = json["Genre"].split(',')
    
        # 'tags'
        # 'collections'
        # 'art'
        # 'posters'
        if GetPosters('OMDb') and 'Poster' in json and json['Poster'] not in ("N/A", "", None):
          OMDb_dict['Posters'][json['Poster']] = ("OMDB/%s.jpg" % imdbid_single, num, None)
       
        # 'themes'
    
        if "Type"    in json and json["Type"]:  Type = json["Type"]  # "movie", "serie"
        #if Type=="series":
        #  if "totalSeasons"    in json and json["totalSeasons"]:  totalSeasons = json["Type"]
        if movie:  #Movie Library
          # 'original_title'
          # 'year'
          if "Rated"    in json and json["Rated"   ] and Type=="movie":  OMDb_dict['content_rating_age'] = json["Rated"]
    
          # 'actors'
          
          
          # 'tagline'
          # 'quotes'
          # 'trivia'
          # 'content_rating_age'
        
        else:  # TV Series Library
          # 'content_rating'
          if "Rated"    in json and json["Rated"   ]:
            if Type=="series":                                      OMDb_dict['content_rating' ] = json["Rated"]
            elif json["Rated"] in common.Movie_to_Serie_US_rating:  OMDb_dict['content_rating' ] = common.Movie_to_Serie_US_rating[json["Rated"]]
          #Type
          
          # 'seasons'
          # 'countries'
          if "Country"  in json and json["Country"  ]:  OMDb_dict['countries' ] = [ json["Country"] ]
    
          # 'banners'
  else:  Log.Info("[ ] OMDB - background, Poster - imdbid: '%s'" % imdbid)
  return OMDb_dict
