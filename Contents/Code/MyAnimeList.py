### MyAnimeList.net ###
# MyAnimeList API (beta ver.) (2):  https://api.myanimelist.net/v2/
# API json exemple:                 https://api.myanimelist.net/v2/anime/{id}
# MyAnimeList API Documentation:    https://myanimelist.net/apiconfig/references/api/v2

### Imports ###
#import math
import re
import os
import time
from common   import Log, Dict, SaveDict, DictString, UpdateDict, poster_rank, natural_sort_key, COMMON_HEADERS

### Constants ###
MYANIMELIST_URL_SEARCH   = "https://api.myanimelist.net/v2/anime?q={title}&limit=10"
MYANIMELIST_URL_DETAILS  = "https://api.myanimelist.net/v2/anime/{id}?fields=id,title,pictures,start_date,synopsis,mean,genres,rating,studios,media_type"
MYANIMELIST_CACHE_TIME   = CACHE_1HOUR * 24 * 7
RATING_VALUES            = { "g": "G - All Ages", "pg": "PG - Children", "pg_13": "PG-13 - Teens 13 and Older", "r": "R - 17+ (violence & profanity)", "r+": "R+ - Profanity & Mild Nudity", "rx": "Rx - Hentai" }

### Functions ###
def GetMetadata(myanimelistIds, media_type, dict_AniDB):
  Log.Info("=== MyAnimeList.GetMetadata() ===".ljust(157, '='))
  MainMALid = ""
  ### Skip if Api client ID has not been initialized
  if not (Prefs['MalApiClientID']) or Prefs['MalApiClientID'] in ('None', '', 'N/A'):
    Log.Info("No api key found - Prefs['MalApiClientID']: '{}'".format(Prefs['MalApiClientID']))
    ### If Mal id list exist, return first random id from first found season
    if Dict(myanimelistIds, 'seasons'):
      for season in sorted(Dict(myanimelistIds, 'seasons'), key=natural_sort_key):
        MainMALid = str(Dict(myanimelistIds, 'seasons', season)[0])
        Log.Debug("Selected MainMALid: '{}'".format(MainMALid)); break
    return {}, MainMALid

  ### Setup variables for api call
  apiClientId = Prefs['MalApiClientID']
  headers, return_result = {}, {}
  headers = UpdateDict(headers, COMMON_HEADERS)
  headers = UpdateDict(headers, { 'X-MAL-CLIENT-ID': apiClientId })
  ### Each anidb season/entry might have multiple related MAL ids. Iterate through all of them and make a 'sophisticated' guess, which one is the main entry
  for season in sorted(Dict(myanimelistIds, 'seasons'), key=natural_sort_key):
    best_match, best_score = {}, -1
    season_mal_id_list = Dict(myanimelistIds, 'seasons', season)
    Log.Debug("Season: {}, MAL id list: {}".format(season, DictString(season_mal_id_list, 4)))
    for myanimelistId in season_mal_id_list:
      parsed_response, current_score = {}, 0
      detailUrl = MYANIMELIST_URL_DETAILS.format(id=myanimelistId)
      Log.Info("=== MAL ID: {} ===".ljust(157, '=').format(myanimelistId))
      Log.Info("URL : "+ str(detailUrl))
      try:                    json = JSON.ObjectFromString(HTTP.Request(detailUrl, headers=headers, sleep=2.0, cacheTime=MYANIMELIST_CACHE_TIME, timeout=60).content)
      except Exception as e:  Log.Error("No Detail Information were available " + str(e));  continue
      ### Parse json data
      if json:
        parsed_id = Dict(json, "id")
        if parsed_id:
          SaveDict(str(parsed_id), parsed_response, "id")
          Log.Debug("ID: " + str(parsed_id))
        
        parsed_title = Dict(json, "title")
        if parsed_title: 
          SaveDict(str(parsed_title), parsed_response, "title")
          Log.Debug("Title: " + str(parsed_title))
          if str(Dict(dict_AniDB, 'original_title')) == str(parsed_title): current_score += 2
          elif str(Dict(dict_AniDB, 'original_title')) in str(parsed_title): current_score += 1
        
        parsed_summary = Dict(json, "synopsis")
        if parsed_summary:
          SaveDict(str(re.sub(re.compile('<.*?>'), '', parsed_summary)), parsed_response, "summary")
          Log.Debug("Summary: " + str(parsed_summary))
        
        parsed_rating = Dict(json, "mean")
        if parsed_rating:
          SaveDict(float(parsed_rating), parsed_response, "rating")
          Log.Debug("Rating: " + str(parsed_rating))
        
        parsed_content_rating = Dict(json, "rating")
        if parsed_content_rating:
          content_rating_value = Dict(RATING_VALUES, parsed_content_rating)
          SaveDict(str(content_rating_value), parsed_response, "content_rating")
          Log.Debug("Content Rating: " + str(content_rating_value))
        
        parsed_start_date = Dict(json, "start_date")
        if parsed_start_date:
          SaveDict(parsed_start_date, parsed_response, "originally_available_at")
          Log.Debug("Release date: " + str(parsed_start_date))
          if str(Dict(dict_AniDB, 'originally_available_at')) in str(parsed_start_date): current_score += 1

        parsed_pictures = Dict(json, "pictures")
        if parsed_pictures and len(parsed_pictures) > 0:
          for picture_entry in parsed_pictures:
            poster_file_url = str(Dict(picture_entry, "medium"))
            poster_file_name = poster_file_url.split("/")[len(poster_file_url.split("/"))-1]
            poster_entry_value = ( os.path.join('MyAnimeList', 'poster', poster_file_name), poster_rank('MyAnimeList', 'posters'), None)
            SaveDict(poster_entry_value, parsed_response, 'posters', poster_file_url)
            Log.Debug("Cover: " + str(poster_file_name))
        
        parsed_studios = Dict(json, "studios")
        if parsed_studios:
          studio = ", ".join(str(Dict(x, "name")) for x in parsed_studios)
          SaveDict(str(studio), parsed_response, "studio")
          Log.Debug("Studios: " + str(studio))
        
        parsed_genres = Dict(json, "genres")
        for genre in parsed_genres if parsed_genres and len(parsed_genres) > 0 else []:
          genre_name = Dict(genre, "name")
          SaveDict([str(genre_name)], parsed_response, "genres")
          Log.Debug("Genres: " + str(genre_name))

        parsed_media_type = Dict(json, "media_type")
        if parsed_media_type:
          if str(parsed_media_type) == str(media_type): current_score += 2
          elif str(parsed_media_type) == str("ova"): current_score += 1
        
        ### Check the result of data compare to anidb and replace the selection if better result
        Log.Debug("Mal id: {}, Compare score: {}".format(myanimelistId, current_score))
        if current_score > best_score:
          best_score = current_score
          best_match = parsed_response

      ### In case there is multiple entries to fetch, Sleep between to prevent overload on mal api
      if len(season_mal_id_list) > 2: time.sleep(1)
    
    if Dict(best_match, "id"):
      ### Save best match data on season level
      SaveDict(Dict(best_match, 'summary'), return_result, 'seasons', season, 'summary')
      SaveDict(Dict(best_match, 'title'), return_result, 'seasons', season, 'title')
      SaveDict(Dict(best_match, 'posters'), return_result, 'seasons', season, 'posters')
      ### Save first found best match data on series level
      if not Dict(return_result, "id"):
        UpdateDict(return_result, best_match)
        MainMALid = Dict(best_match, 'id')
        Log.Debug("Selected MainMALid: '{}'".format(MainMALid))

  Log.Info("MyAnimeList_dict: {}".format(DictString(return_result, 4)))
  Log.Info("--- return ---".ljust(157, '-'))
  return return_result, MainMALid
