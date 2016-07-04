```
TSEMAGT | Metadata Model Classes | Description - Source: http://dev.plexapp.com/docs/agents/models.html 
------- | ---------------------- | --------------------------------- 
X______ | class TV_Show          | Represents a TV show, or the top -level of other episodic content.
_X_____ | class Season           | Represents a season of a TV show.
__X____ | class Episode          | Represents an episode of a TV show or other episodic content. 
___X___ | class Movie            | Represents a movie (e.g. a theatrical release, independent film, home movie, etc.)
____X__ | class Album            | Represents a music album.
_____X_ | class Artist           | Represents an artist or group.
______X | Track                  | Represents an audio track (e.g. music, audiobook, podcast, etc.)   
------- | ---------------------- | --------------------------------------------------------------------------------------------------
X_XXXX_ | title                  | A string specifying the title.
XXXXXX_ | summary                | A string specifying the summary.
X_XXX__ | originally_available_at| A date object specifying the movie/episode’s original release date.
X_XXXX_ | rating                 | A float between 0 and 10 specifying the movie/episode’s rating.
X__XX__ | studio                 | A string specifying the studio.
X__XX__ | countries              | A set of strings specifying the countries involved in the production of the movie.
X__X___ | duration               | An integer specifying the duration of the movie, in milliseconds.
X__XXX_ | genres                 | A set of strings specifying the movie’s genre.
X__XXX_ | tags                   | A set of strings specifying the movie’s tags.
X__XXX_ | collections            | A set of strings specifying the movie’s collections.
X__X___ | content_rating         | A string specifying the movie’s content rating.
__X____ | absolute_index         | An integer specifying the absolute index of the episode within the entire series.
______X | name                   | A string specifying the track’s name.
_X_____ | episodes               | A map of Episode objects.
____X__ | tracks                 | A map of Track objects.
------- | ---------------------- | ---------------------------------------------------------------------------------------------------
__XX___ | writers                | A set of strings specifying the writers.
__XX___ | directors              | A set of strings specifying the directors.
__XXX__ | producers              | A set of strings specifying the producers. 
------- | ---------------------- | ---------------------------------------------------------------------------------------------------
___X___ | year                   | An integer specifying the movie’s release year.
# ...X...   content_rating_age        A string specifying the minumum age for viewers of the movie.
# ...X...   trivia                    A string containing trivia about the movie.
# ...X...   quotes                    A string containing memorable quotes from the movie.
# ...XX..   original_title            A string specifying the original title.
# ...X...   tagline                   A string specifying the tagline.
# -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
# X..X.X.   art                       A container of proxy objects representing the movie’s background art. See below for information about proxy objects.
# XX.XXX.   posters                   A container of proxy objects representing the movie’s posters. See below for information about proxy objects.
# XX.....   banners                   A container of proxy objects representing the season’s banner images. See below for information about proxy objects.
# X..X.X.   themes                    A container of proxy objects representing the movie’s theme music. See below for information about proxy objects.
# ..X....   thumbs                    A container of proxy objects representing the episode’s thumbnail images. See below for information about proxy objects.
# -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    
---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|--------------------------------
Metadata source                             | AniDB.net                | TheTVDB.com               | TheMovieDB.net           | OBDbAPI.com                    | Plex tvdb Themes               | Scudlee's mapping file
--------------------------------------------|--------------------------|---------------------------|--------------------------|--------------------------------|--------------------------------|--------------------------------
Metadata Hama tags                          | anidb                    | tvdb, tvdb2, tvdb3, tvdb4 | tmdb, tsdb               | imdb                           | N/A                            | N/A
---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|--------------------------------
TV_Show - Serie   - title                   | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - summary                 | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - originally_available_at | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - rating                  | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - studio                  | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - countries               | ?                        | ?                         |                          |                        |                          | 
TV_Show - Serie   - duration                | No                       | No                        |                          |                        |                          | 
TV_Show - Serie   - genres                  | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - tags                    | ?                        | ?                         |                          |                        |                          | 
TV_Show - Serie   - collections             | Yes (related_anime)      | ?                         |                          |                        |                          | Movie collection
TV_Show - Serie   - content_rating          | Yes                      | Yes                       |                          |                        |                          | 
TV_Show - Serie   - art                     | No                       | Yes                       | Yes                      |                        |                          | 
TV_Show - Serie   - posters                 | Yes (variable low res)   | Yes                       | Yes                      |                        |                          | 
TV_Show - Serie   - banners                 | No                       | Yes                       | No                       |                        |                          | 
TV_Show - Serie   - themes                  | No                       | No                        |                          |                        |                          | 
TV_Show - Season  - summary                 | No                       | Yes                       |                          |                        |                          | 
TV_Show - Season  - posters                 | No                       | Yes                       |                          | 
TV_Show - Season  - banners                 | No                       | Yes                       |                          | 
TV_Show - Episode - title                   | Yes                      | Yes                       |                          | 
TV_Show - Episode - summary                 | No                       | Yes                       |                          | 
TV_Show - Episode - originally_available_at | Yes                      | Yes                       |                          | 
TV_Show - Episode - rating                  | No                       | Yes                       |                          | 
TV_Show - Episode - absolute_index          | Yes                      | Yes (on some series)      |                          | 
TV_Show - Episode - writers                 | Yes                      | Yes                       |                          | 
TV_Show - Episode - directors               | Yes                      | Yes                       |                          | 
TV_Show - Episode - producers               | Yes                      | Yes                       |                          | 
TV_Show - Episode - thumbs                  | No                       | Yes                       |                          | 
```
