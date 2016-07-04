```
```
TSEMAGT | Metadata Model Classes | Description - Source: http://dev.plexapp.com/docs/agents/models.html 
------- | ---------------------- | --------------------------------- 
X...... | class TV.Show          | Represents a TV show, or the top -level of other episodic content.
.X..... | class Season           | Represents a season of a TV show.
..X.... | class Episode          | Represents an episode of a TV show or other episodic content. 
...X... | class Movie            | Represents a movie (e.g. a theatrical release, independent film, home movie, etc.)
....X.. | class Album            | Represents a music album.
.....X. | class Artist           | Represents an artist or group.
......X | Track                  | Represents an audio track (e.g. music, audiobook, podcast, etc.)   
------- | ---------------------- | --------------------------------------------------------------------------------------------------
X.XXXX. | title                  | A string specifying the title.
XXXXXX. | summary                | A string specifying the summary.
X.XXX.. | originally_available_at| A date object specifying the movie/episode’s original release date.
X.XXXX. | rating                 | A float between 0 and 10 specifying the movie/episode’s rating.
X..XX.. | studio                 | A string specifying the studio.
X..XX.. | countries              | A set of strings specifying the countries involved in the production of the movie.
X..X... | duration               | An integer specifying the duration of the movie, in milliseconds.
X..XXX. | genres                 | A set of strings specifying the movie’s genre.
X..XXX. | tags                   | A set of strings specifying the movie’s tags.
X..XXX. | collections            | A set of strings specifying the movie’s collections.
X..X... | content_rating         | A string specifying the movie’s content rating.
..X.... | absolute_index         | An integer specifying the absolute index of the episode within the entire series.
......X | name                   | A string specifying the track’s name.
.X..... | episodes               | A map of Episode objects.
....X.. | tracks                 | A map of Track objects.
------- | ---------------------- | ---------------------------------------------------------------------------------------------------
..XX... | writers                | A set of strings specifying the writers.
..XX... | directors              | A set of strings specifying the directors.
..XXX.. | producers              | A set of strings specifying the producers. 
------- | ---------------------- | ---------------------------------------------------------------------------------------------------
...X... | year                   | An integer specifying the movie’s release year.
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

```
