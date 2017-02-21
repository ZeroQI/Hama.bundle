### omdbapi.com ###  
# tt0412142   1408  House md   http://www.omdbapi.com/?i=tt0412142
# tt0186151  10559  Frequency  http://www.omdbapi.com/?i=tt0186151

### Imports ###
import common
from common import GetPosters
import re
          
### Variables ###

### Functions ###
def GetMetadata(metadata, imdbid, movie, num=98, name=""):  # return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
  OMDB_HTTP_API_URL = "http://www.omdbapi.com/?i="
  OMDb_dict = {}
  Log.Info("".ljust(157, '-'))
  Log.Info("OMDb.GetMetadata() - background, Poster - imdbid: '%s'" % imdbid)
  if imdbid.startswith("tt"):
    for imdbid_single in imdbid.split(","):
      json = common.LoadFile(filename=imdbid_single+".json", relativeDirectory="OMDB", url=OMDB_HTTP_API_URL + imdbid_single, cache=CACHE_1WEEK)
      if json:
      
        ### Common to Movies and Series Libraries
        # 'tags'  # 'collections'  # 'art'  # 'themes'  # 'tagline'
        if "Title"      in json and json["Title"     ]:  OMDb_dict['title'    ] = json["Title"     ]            # 'title'
        if "Plot"       in json and json["Plot"      ]:  OMDb_dict['summary'  ] = json["Plot"      ]            # 'summary'
        if "Released"   in json and json["Released"  ]:  OMDb_dict["Released" ] = json["Released"  ]            # 'originally_available_at'
        if "imdbRating" in json and json["imdbRating"]:  OMDb_dict['rating'   ] = json["imdbRating"]            # 'rating'
        if "Director"   in json and json["Director"  ]:  OMDb_dict['directors'] = json["Director"  ].split(',') # 'directors'
        if "Genre"      in json and json["Genre"     ]:  OMDb_dict['genres'   ] = json["Genre"     ].split(',') # 'genres'
        if "Writer"     in json and json["Writer"    ]:  OMDb_dict['writers'  ] = re.sub(r'\([^)]*\)', '', json["Writer"]).split(',')   # 'studio'  # 'producers'  # 'writers'
        if "Runtime"    in json and json["Runtime"   ]:                                            # 'duration'
          try:     OMDb_dict['duration'] = int(json["Runtime"].replace(' min','')) * 60 *1000  # Plex save duration in millisecs
          except:  pass
        #if "Metascore"  in json and json["Metascore" ]:  OMDb_dict['rating'] = float(json["Metascore"])/10  #:"76"
                
        if GetPosters('OMDb') and 'Poster' in json and json['Poster'] not in ("N/A", "", None):  OMDb_dict['Posters'][json['Poster']] = ("OMDB/%s.jpg" % imdbid_single, num, None) # 'posters'
       
        Type = json["Type"] if "Type" in json and json["Type"] else "" # "movie", "serie"
        #if Type=="series" and "totalSeasons" in json and json["totalSeasons"]:  totalSeasons = json["totalSeasons"]
        if movie:  #Movie Library
          # 'original_title'  # 'year'  # 'quotes'  # 'trivia'  # 'actors'
          if "Rated"    in json and json["Rated"   ] and Type=="movie":  OMDb_dict['content_rating_age'] = json["Rated"]   # 'content_rating_age'
        else:  # TV Series Library
          # 'banners'  # 'seasons'  
          if "Country"  in json and json["Country"  ]:  OMDb_dict['countries' ] = [ json["Country"] ]  # 'countries'
          if "Rated"    in json and json["Rated"    ]:  # 'content_rating'
            if Type=="series":                                      OMDb_dict['content_rating' ] = json["Rated"]
            elif json["Rated"] in common.Movie_to_Serie_US_rating:  OMDb_dict['content_rating' ] = common.Movie_to_Serie_US_rating[json["Rated"]]
          
  return OMDb_dict
