### MyAnimeList.net ###
# Source agent:     https://github.com/Fribb/MyAnimeList.bundle/blob/master/Contents/Code/__init__.py
# API xml exemple:  https://atarashii.fribbtastic.net/web/2.1/anime/33487

### Imports ###
#import math
import re, ssl, urllib2
import difflib
from datetime import datetime
from common   import Log, Dict, SaveDict, DictString

### Constants ###
MYANIMELIST_URL_SEARCH   = "https://atarashii.fribbtastic.net/web/2.1/anime/search?q={title}"
MYANIMELIST_URL_DETAILS  = "https://atarashii.fribbtastic.net/web/2.1/anime/{id}"
MYANIMELIST_URL_EPISODES = "https://atarashii.fribbtastic.net/web/2.1/anime/episodes/{id}?page={page}"
MYANIMELIST_CACHE_TIME   = CACHE_1HOUR * 24 * 7

### Functions ###
'''
def search(name, results, lang):
  forceID   = re.match(r'^[mal-([0-9]+)]$', str(name))
  searchUrl = MYANIMELIST_URL_DETAILS.format(id=str(forceID.group(1))) if forceID else MYANIMELIST_URL_SEARCH.format(title=String.Quote(name, usePlus=True))
  Log.Info("[MyAnimeList Search() - forceID {}, name: {}, searchUrl: {}".format(forceID, name, searchUrl))
  try:                    searchResults = JSON.ObjectFromString(HTTP.Request(searchUrl, sleep=2.0, cacheTime=MYANIMELIST_CACHE_TIME).content)
  except Exception as e:  Log.Info("search results could not be requested " + str(e));  return
  Log.Info("Results found: " + str(len(searchResults)))
  for series in [searchResults] if forceID else searchResults:      
    apiAnimeId      = str(Dict(series, "id"        ))
    apiAnimeTitle   = str(Dict(series, "title"     ))
    apiAnimeYear    = str(Dict(series, "start_date")).split("-")[0]
    animeMatchScore = 100 if forceID else int(difflib.SequenceMatcher(None, apiAnimeTitle, name).ratio()*100) if len(apiAnimeTitle) > 0 else 0
    Log.Debug("Anime Found - ID={}, Title={},  Year={},  MatchScore={}".format(apiAnimeId, apiAnimeTitle, apiAnimeYear, animeMatchScore))
    results.Append(MetadataSearchResult(id=apiAnimeId, name=apiAnimeTitle, year=apiAnimeYear, score=animeMatchScore, lang=lang))
  return
'''
def GetMetadata(myanimelistId, type, media):
  Log.Info("=== MyAnimeList.GetMetadata() ===".ljust(157, '='))
  detailUrl        = MYANIMELIST_URL_DETAILS.format(id=myanimelistId)
  Log.Info("URL : "+ str(detailUrl))
  try:                    json = JSON.ObjectFromString(HTTP.Request(detailUrl, sleep=2.0, cacheTime=MYANIMELIST_CACHE_TIME).content)
  except Exception as e:  Log.Error("No Detail Information were available " + str(e));  return
  result = {}
  if json:
    if Dict(json, "id"            ):  SaveDict(                                str(Dict(json, "id"            )  ), result, "id"                             );  Log.Debug("ID:             " + str(Dict(json, "id"            )))
    if Dict(json, "title"         ):  SaveDict(                                str(Dict(json, "title"         )  ), result, "title"                          );  Log.Debug("Title:          " + str(Dict(json, "title"         )))
    if Dict(json, "synopsis"      ):  SaveDict(str(re.sub(re.compile('<.*?>'), '', Dict(json, "synopsis"     ))  ), result, "summary"                        );  Log.Debug("Summary:        " + str(Dict(json, "synopsis"      )))
    if Dict(json, "members_score" ):  SaveDict(                              float(Dict(json, "members_score" )  ), result, "rating"                         );  Log.Debug("Rating:         " + str(Dict(json, "members_score" )))
    if Dict(json, "classification"):  SaveDict(                                str(Dict(json, "classification")  ), result, "content_rating"                 );  Log.Debug("Content Rating: " + str(Dict(json, "classification")))
    if Dict(json, "duration"      ):  SaveDict(                                int(Dict(json, "duration")*60000  ), result, "duration"                       );  Log.Debug("Duration:       " + str(Dict(json, "duration")*60000))
    if Dict(json, "start_date"    ):  SaveDict(                                    Dict(json, "start_date"       ), result, "originally_available_at"        );  Log.Debug("Release date:   " + str(Dict(json, "start_date"    )))
    if Dict(json, "image_url"     ):  SaveDict(                                   (Dict(json, "image_url"),1,None), result, 'poster', Dict(json, "image_url"));  Log.Debug("Cover:          " + str(Dict(json, "image_url"     )))
    for genre in Dict(json, "genres") if Dict(json, "genres") and len(Dict(json, "genres")) > 0 else []:
      SaveDict([str(genre)], result, "genres")
      Log.Debug("Genres: " + str(Dict(json, "genres")))
    
    ### TODO: Switch to Studios when they are available in the API (or add Producers to metadata when this is possible in Plex) 
    #if Dict(json, "producers") and len(Dict(json, "producers")) > 0:
    #  apiAnimeProducers = ""
    #  for idx, producer in enumerate(Dict(json, "producers")):  apiAnimeProducers += str(producer) + ", "
    #  SaveDict(str(apiAnimeProducers[:-2]), result, "studio")
    #  Log.Debug("Producers: " + str(Dict(json, "producers")))
    
    if type == "tvshow":
      Log.Debug("Adding TV-Show specific data")        
      Log.Debug("Episodes: " + str(Dict(json, "episodes")))
    #   metadata.seasons[1].episode_count = int( Dict(json, "episodes") or len(media.seasons[1].episodes))
    #   pages = int(math.ceil(float(metadata.seasons[1].episode_count) / 100))  # fetch the episodes in 100 chunks
    #   if pages is not None:
    #     for page in range(1, pages + 1):
    #       episodesUrl = MYANIMELIST_URL_EPISODES.format(id=metadata.id,page=page)
    #       try:
    #         Log.Info("Fetching URL " + str(episodesUrl))
    #         episodeResult = JSON.ObjectFromString(HTTP.Request(episodesUrl, sleep=2.0, cacheTime=MYANIMELIST_CACHE_TIME).content)
    #       except Exception as e:  Log.Info("episode results could not be requested " + str(e));  return
    #       if "error" in episodeResult:
    #         Log.Warn("Episode Information are not available (" + str(episodeResult["error"]) + ") (might want to add them to MyAnimeList.net)!")
    #         break
    #
    #       for episode in episodeResult:
    #         apiEpisodeNumber  = Dict(json, "number"  )
    #         apiEpisodeTitle   = Dict(json, "title"   )
    #         apiEpisodeAirDate = Dict(json, "air_date")
    #         if apiEpisodeNumber is not None:
    #           plexEpisode                         = metadata.seasons[1].episodes[int(apiEpisodeNumber)]
    #           plexEpisode.title                   = str(apiEpisodeTitle) if apiEpisodeTitle else "Episode: #" + str(apiEpisodeNumber)
    #           plexEpisode.originally_available_at = datetime.strptime(str(apiEpisodeAirDate), "%Y-%m-%d") if apiEpisodeAirDate else datetime.now()
    #         Log.Debug("Episode " + str(apiEpisodeNumber) + ": " + str(apiEpisodeTitle) + " - " + str(apiEpisodeAirDate))
    #
    if type == "movie":
      Log.Debug("Adding Movie specific data, nothing specific to add")

  Log.Info("MyAnimeList_dict: {}".format(DictString(result, 4)))
  Log.Info("--- return ---".ljust(157, '-'))
  return result
