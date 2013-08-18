######################################################################
# HTTP Anidb Metadata Agent (HAMA) v0.4 for plex By Atomicstrawberry #
# Forked+maintained from v0.5 by ZeroQI                              #
######################################################################

### Global initialisation ################################################################################################################################################
import os, os.path, re, time, datetime, string # Functions used per module: os (read), re (sub, match), time (sleep), datetim (datetime).
                                       # Unused modules:            urllib, types, hashlib , unicodedata, Stack, utils
SERIE_LANGUAGE_PRIORITY      = [ 'x-jat', 'en']
EPISODE_LANGUAGE_PRIORITY    = [ 'en', 'x-jat']
MINIMUM_WEIGHT               = 200

HTTP.CacheTime               = CACHE_1HOUR * 24 * 7
SECONDS_BETWEEN_REQUESTS     = 2

### AniDB and TVDB URL and path variable definition ####################################################################################################################
ANIDB_HTTP_API_URL           = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='
ANIDB_PIC_BASE_URL           = 'http://img7.anidb.net/pics/anime/'                             # AniDB picture directory
ANIDB_ANIME_TITLES_URL       = 'http://anidb.net/api/anime-titles.xml.gz'                      # AniDB title database file contain all ids, all languages
ANIDB_SERIE_URL              = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s'
ANIDB_EPISODE_URL            = 'http://anidb.net/perl-bin/animedb.pl?show=ep&eid=%s'

TVDB_API_KEY                 = 'A27AD9BE0DA63333'                                              # TVDB API key register URL: http://thetvdb.com/?tab=apiregister
TVDB_HTTP_API_URL            = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'                # TVDB Serie XML for episodes sumaries for now
TVDB_BANNERS_URL             = 'http://thetvdb.com/api/%s/series/%s/banners.xml'               # TVDB Serie pictures xml: fanarts, posters, banners   
TVDB_IMAGES_URL              = 'http://thetvdb.com/banners/'                                   # TVDB picture directory
TVDB_SERIE_URL               = 'http://thetvdb.com/?tab=series&id=%s'
TVDB_SEASON_URL              = 'http://thetvdb.com/?tab=season&seriesid=%s&seasonid=%s'
TVDB_EPISODE_URL             = 'http://thetvdb.com/?tab=episode&seriesid=%s&seasonid=%s&id=%s'
TVDB_SEARCH_URL              = 'http://thetvdb.com/?tab=listseries&function=Search&string=%s'

ANIDB_ANIME_TITLES           = 'anime-lists/animetitles.xml'                                   # AniDB title database decompressed in Hama.bundle\Contents\Resources
ANIDB_TVDB_MAPPING           = 'anime-lists/anime-list-master.xml'                             # ScudLee AniDB to TVDB XML mapping file
ANIDB_COLLECTION_MAPPING     = 'anime-lists/anime-movieset-list.xml'                           # ScudLee AniDB movies collections XML mapping file
ANIDB_TVDB_MAPPING_FEEDBACK  = 'https://github.com/ScudLee/anime-lists/issues/new?title=%s&body='

### List of AniDB category names useful as genre. 1st variable mark 18+ categories. The 2nd variable will actually cause a flag to appear in Plex ######################
RESTRICTED_GENRE_NAMES    = [ '18 Restricted', 'Pornography' ]
RESTRICTED_CONTENT_RATING = "NC-17"
GENRE_NAMES               = [
  ### Audience categories - all useful but not used often ############################################################################################################
  'Josei', 'Kodomo', 'Mina', 'Seinen', 'Shoujo', 'Shounen',
  
  ### Elements - many useful #########################################################################################################################################
  'Action', 'Martial Arts', 'Swordplay', 'Adventure', 'Angst', 'Anthropomorphism', 'Comedy', 'Parody', 'Slapstick', 'Super Deformed', 'Detective', 'Ecchi', 'Fantasy',
  'Contemporary Fantasy', 'Dark Fantasy', 'Ghost', 'High Fantasy', 'Magic', 'Vampire', 'Zombie', 'Harem', 'Reverse Harem', 'Henshin', 'Horror', 'Incest',
  'Mahou Shoujo', 'Pornography', 'Yaoi', 'Yuri', 'Romance', 'Love Polygon', 'Shoujo Ai', 'Shounen Ai', 'Sci-Fi', 'Alien', 'Mecha', 'Space Travel', 'Time Travel', 
  'Thriller', 'Western',                                             
      
  ### Fetishes. Leaving out most porn genres #########################################################################################################################
  'Futanari', 'Lolicon', 'Shotacon', 'Tentacle', 'Trap', 'Reverse Trap',
  
  ### Original Work - mainly useful ##################################################################################################################################
  'Game', 'Action Game', 'Dating Sim - Visual Novel', 'Erotic Game', 'RPG', 'Manga', '4-koma', 'Movie', 'Novel',
  
  ### Setting - most of the places aren't genres, some Time stuff is useful ##########################################################################################
  'Fantasy World', 'Parallel Universe', 'Virtual Reality', 'Hell', 'Space', 'Mars', 'Space Colony', 'Shipboard', 'Alternative Universe', 'Past', 'Present', 'Future',
  'Historical', '1920s', 'Bakumatsu - Meiji Period', 'Edo Period', 'Heian Period', 'Sengoku Period', 'Victorian Period', 'World War I', 'World War II',
  'Alternative Present',
  
  ### Themes - many useful ###########################################################################################################################################
  'Anti-War', 'Art', 'Music', 'Band', 'Idol', 'Photography', 'Christmas', 'Coming of Age', 'Conspiracy', 'Cooking', 'Cosplay', 'Cyberpunk', 'Daily Life', 'Earthquake',
  'Post-War', 'Post-apocalypse', 'War', 'Dystopia', 'Friendship', 'Law and Order', 'Cops', 'Special Squads', 'Military', 'Airforce', 'Feudal Warfare', 'Navy',
  'Politics', 'Proxy Battles', 'Racism', 'Religion', 'School Life', 'All-boys School', 'All-girls School', 'Art School', 'Clubs', 'College', 'Delinquents', 
  'Elementary School', 'High School', 'School Dormitory', 'Student Council', 'Transfer Student', 'Sports', 'Acrobatics', 'Archery', 'Badminton', 'Baseball', 
  'Basketball', 'Board Games', 'Chess', 'Go', 'Mahjong', 'Shougi', 'Combat', 'Boxing', 'Judo', 'Kendo', 'Muay Thai', 'Wrestling', 'Cycling', 'Dodgeball', 'Fishing',
  'Football', 'Golf', 'Gymnastics', 'Horse Riding', 'Ice Skating', 'Inline Skating', 'Motorsport', 'Formula Racing', 'Street Racing', 'Rugby', 'Swimming', 'Tennis',
  'Track and Field', 'Volleyball', 'Steampunk', 'Summer Festival', 'Tragedy', 'Underworld', 'Assassin', 'Bounty Hunter', 'Mafia', 'Yakuza', 'Pirate', 'Terrorist',
  'Thief'
]

### AniDB.net resources (external links) translation dictionnary ###
AniDB_Resources = { "1":["http://www.animenewsnetwork.com/encyclopedia/anime.php?id=%s", "ANN"                ], #
                    "2":["http://myanimelist.net/anime/%s"                             , "MAL"                ], #
                    "3":["http://www.animenfo.com/animetitle,%s,%s,a.html"             , "AnimeNfo"           ], #
                    "4":["%s"                                                          , "Official page (jp)" ], #
                    "5":["%s"                                                          , "Official page (en)" ], #
                    "6":["http://en.wikipedia.org/wiki/%s"                             , "Wiki (en)"          ], #
                    "7":["http://ja.wikipedia.org/wiki/%s"                             , "Wiki (jp)"          ], #
                    "8":["http://cal.syoboi.jp/tid/%s/time"                            , "Schedule"           ], #
                    "9":["http://www.allcinema.net/prog/show_c.php?num_c=%s"           , "Allcinema"          ], #
                   "10":["http://anison.info/data/program/%s.html"                     , "Anison"             ], #
                   "11":["http://lain.gr.jp/%s"                                        , ".lain"              ], #
                   "14":["http://vndb.org/v%s"                                         , "VNDB"               ], #
                   "15":["http://www.anime.marumegane.com/%s.html"                     , "Marumegane"         ], #
                   "19":["http://ko.wikipedia.org/wiki/%s"                             , "Wiki (ko)"          ], #
                   "20":["http://zh.wikipedia.org/wiki/%s"                             , "Wiki (zh)"          ], #
                   "xx":["%s"                                                          , " "                  ], #
      }
      
### TheTVDB.com language codes ###
THETVDB_LANGUAGES_CODE = { 'cs':'28', 'da':'10',
 'de':'14',
 'el':'20', 'en': '7', 'es':'16', 'fi':'11',
 'fr':'17', 'he':'24', 'hu':'19',
 'it':'15', 'ja':'25',

                           'ko':'32', 'nl':'13', 'no': '9',
 'pl':'18',
 'pt':'26', 'ru':'22',
 'sv': '8', 'tr':'21',
 'zh': '6'
}

### These are words which cause extra noise due to being uninteresting for doing searches on ###########################################################################
FILTER_SEARCH_WORDS          = [                                                                                                      # Lowercase only
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', # En 
  'princess', 'theater',                                                                                                              # En Continued
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime',                                                   # Jp 
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses'                                                                                 # Fr 
]
FILTER_CHARS                 = "\\/:*?<>|~- "
SPLIT_CHARS                  = [';', ',', '.', '~', '-' ] #Space is implied
WEB_LINK                     = "<A HREF='%s' target='_blank'>%s</A>"

### Global variables ###
networkLock                  = None
AniDB_title_tree             = None
AniDB_TVDB_mapping_tree      = None
AniDB_collection_tree        = None

### Pre-Defined Start function #########################################################################################################################################
def Start():
  Log.Debug('### HTTP Anidb Metadata Agent (HAMA) Started ##############################################################################################################')
  
  msgContainer = ValidatePrefs()
  if msgContainer.header == 'Error': 
    Log("ValidatePrefs - Error")
    return
  else:
    MessageContainer('Success', "HAMA started")

  global AniDB_title_tree, AniDB_TVDB_mapping_tree, AniDB_collection_tree
  
  AniDB_title_tree        = HamaCommonAgent().xmlElementFromFile(ANIDB_ANIME_TITLES)       # AniDB's:   anime-titles.xml
  AniDB_TVDB_mapping_tree = HamaCommonAgent().xmlElementFromFile(ANIDB_TVDB_MAPPING)       # ScudLee's: anime-list-master.xml 
  AniDB_collection_tree   = HamaCommonAgent().xmlElementFromFile(ANIDB_COLLECTION_MAPPING) #            anime-movieset-list.xml 

  global networkLock
  networkLock = Thread.Lock()

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info('HAMA - ValidatePrefs initialised')
  result     = 'Success'
  msg        = 'HAMA - Provided preference values are ok'
  log_string = ""
  settings   = ['GetTvdbFanart', 'GetTvdbPosters', 'GetTvdbBanners', 'PreferAnidbPoster', 'UseWebLinks', 'UseWarnings', 'Language1', 'Language2']
  for key in settings: #for key, value in enumerate(settings):
    try:
      temp = Prefs[key]
    except:
      result = 'Error'
      msg    = "Couldn't get values '%s', probably a missing/empty/outdated 'DefaultPrefs.json' so replace it" % key
      Log.Error(msg)
  if result=='Success':
    Log.Info(msg)
  return MessageContainer(result, msg)

### main metadata agent ################################################################################################################################################
class HamaCommonAgent:

  ### Local XML AniDB lookup ###
  def searchByName(self, results, lang, origTitle, year):
  
    Log.Debug("=== searchByName - Begin - ================================================================================================")
    Log("SearchByName (%s,%s,%s,%s)" % (results, lang, origTitle, str(year) ))
    global AniDB_title_tree                                                                   # Call global variable
    if not AniDB_title_tree:                                                                  # If not loaded yet
      AniDB_title_tree = self.xmlElementFromFile(ANIDB_ANIME_TITLES)  # Get the xml title file into a tree, #from lxml import etree #doc = etree.parse('content-sample.xml')
    
    ### aid:xxxxx Fetch the exact serie XML form AniDB.net (Caching it) from the anime-id ###
    if origTitle.startswith('aid:'):                                                          # If custom search starts with aid:
      animeId = str(origTitle[4:])                                                            #   Get string after "aid:" which is 4 characters
      langTitle, mainTitle = self.getMainTitle(AniDB_title_tree.xpath("/animetitles/anime[@aid='%s']/*" % animeId), SERIE_LANGUAGE_PRIORITY) # Extract titles from the Anime XML element tree directly
      Log.Debug( "SearchByName - aid: %s, Title: %s, Main title: %s" % (animeId, langTitle, mainTitle) )                   # Log aid, title found, main title
      results.Append(MetadataSearchResult(id=animeId, name=langTitle, year=None, lang=Locale.Language.English, score=100)) # Return array with result
      return 
    
    ### Local exact search ###
    cleansedTitle = self.cleanse_title (origTitle)                                            # Cleanse title for search
    elements      = list(AniDB_title_tree.iterdescendants())                                  # from lxml import etree; tree = etree.parse(ANIDB_ANIME_TITLES) folder missing?; #To-Do: Save to local (media OR cache-type folder) XML???  
    for title in elements:                                                                    # For each title in serie
      if title.get('aid'):                                                                    #   Is an anime tag (not title tag) in that case ###
        aid = title.get('aid')                                                                #   Get anime id
      else:                                                                                   # Else
        if title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main':
          sample = self.cleanse_title (title.text)                                            # Put cleanse title in sample
          if cleansedTitle == sample :                                                        # Should i add "origTitle.lower()==title.text.lower() or" ??
            Log.Debug("SearchByName: Local exact search for '%s' matched aid: %s %s" % (origTitle, aid,title.text))          # 
            langTitle, mainTitle = self.getMainTitle(title.getparent(), SERIE_LANGUAGE_PRIORITY)                             # Title according language order selection instead of main title
            results.Append(MetadataSearchResult(id=aid, name=langTitle, year=None, lang=Locale.Language.English, score=100)) # return
            return

    ### local keyword search ###
    matchedTitles  = [ ]                                                                      # 
    matchedWords   = { }                                                                      # 
    words          = [ ]                                                                      #
    log_string     = "SearchByName - Keyword search - Matching '%s' with: " % origTitle       #
    for word in self.splitByChars(origTitle, SPLIT_CHARS):                                    #
      word = self.cleanse_title (word)                                                        #
      if not word == "" and word not in FILTER_SEARCH_WORDS and len(word) > 1:                # Special characters scrubbed result in empty word matching all
        words.append (word)                                                                   #
        log_string += "'%s', " % word                                                         #
    Log.Debug(log_string)

    if len(words)==0 or len( self.splitByChars(origTitle, SPLIT_CHARS) )==1 :                 # Single work title so already tested
      return None                                                                             # No result found
    
    for title in elements:                                                                    # For each line in the XML case
      if title.get('aid'):                                                                    #   If it is an anime tag in that case
        aid = title.get('aid')                                                                #     Save the Animeid
      else:                                                                                   # Else
        if title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main': #
          sample = self.cleanse_title (title.text)                                            # Cleanse 
          for word in words:                                                                  # For each keyword
            if word in sample:                                                                #   if work in cleanse comparison title
              index  = len(matchedTitles)-1                                                   #     find the key of last elements
              if index >=0 and matchedTitles[index][0] == aid:                                #     if same serie id and at least an element (update array for same aid)
                if title.get('type') == 'main':                                               #       if main title
                  matchedTitles[index][1] = aid.zfill(5) + ' ' + title.text                   #         use main title as display title as it pass the match as well
                if not title.text in matchedTitles[index][2]:                                 #       if title not already added
                  matchedTitles[index][2].append(title.text)                                  #         append title to allTitles list
              else:                                                                           #     else
                matchedTitles.append([aid, aid.zfill(5) + ' ' + title.text, [title.text] ])   #       new insertion (not necessarily main title)
                if word in matchedWords:
                  matchedWords[word].append(sample)
                else:
                  matchedWords[word]= [sample]
    log_string="SearchByName - Keywords: "
    for key, value in matchedWords.iteritems():
      log_string += key + " (" + str(len(value)) + "), "
    Log.Debug(log_string)  
    if len(matchedTitles)==0:
      return None

    ### calculate scores + Buid results ###
    for match in matchedTitles:
      scores = []                                                                             
      for title in match[2]:                                                                  # Calculate distance without space and characters not allowed for files 
        a = self.cleanse_title(title)
        b = cleansedTitle
        score = int(100 - (100*float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) )) # (removed tilde when used WRONGLY as separator by MIKE)
        scores.append(score)              
      bestScore = max(scores)
      results.Append(MetadataSearchResult(id=match[0], name=match[1], year=None, lang=Locale.Language.English, score=bestScore))
      #Log.Debug("SearchByName - %s%% similarity with %s" % ('{:>2}'.format(str(bestScore)), match[1]) )
    results.Sort('score', descending=True)
    Log.Debug("=== searchByName - End - =================================================================================================")
	
  ### Parse the AniDB anime title XML ##################################################################################################################################
  def parseAniDBXml(self, metadata, media, force, movie):
   
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # TSEMAGT   Metadata Model Classes    Description - Source: http://dev.plexapp.com/docs/agents/models.html 
    # -------   -----------------------   --------------------------------- --------------------------------------------------------------------------------------------
    # X         class TV_Show             Represents a TV show, or the top -level of other episodic content.
    #  X        class Season              Represents a season of a TV show.
    #   X       class Episode             Represents an episode of a TV show or other episodic content. 
    #    X      class Movie               Represents a movie (e.g. a theatrical release, independent film, home movie, etc.)
    #     X     class Album               Represents a music album.
    #      X    class Artist              Represents an artist or group.
    #       X   Track                     Represents an audio track (e.g. music, audiobook, podcast, etc.)   
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X.XXXX.   title                     A string specifying the title.
    # XXXXXX.   summary                   A string specifying the summary.
    # X.XXX..   originally_available_at   A date object specifying the movie/episode’s original release date.
    # X..X...   duration                  An integer specifying the duration of the movie, in milliseconds.
    # ..X....   absolute_index            An integer specifying the absolute index of the episode within the entire series.
    # ...XX..   original_title            A string specifying the original title.
    # ...X...   tagline                   A string specifying the tagline.
    # ...X...   year                      An integer specifying the movie’s release year.
    # ......X   name                      A string specifying the track’s name.
    # .X.....   episodes                  A map of Episode objects.
    # ....X..   tracks                    A map of Track objects.
    #--------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X..XX..   studio                    A string specifying the studio.
    # X..XX..   countries                 A set of strings specifying the countries involved in the production of the movie.
    # ..XX...   writers                   A set of strings specifying the writers.
    # ..XX...   directors                 A set of strings specifying the directors.
    # ..XXX..   producers                 A set of strings specifying the producers. 
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X.XXXX.   rating                    A float between 0 and 10 specifying the movie/episode’s rating.
    # X..XXX.   genres                    A set of strings specifying the movie’s genre.
    # X..XXX.   tags                      A set of strings specifying the movie’s tags.
    # X..XXX.   collections               A set of strings specifying the movie’s genre.
    # X..X...   content_rating            A string specifying the movie’s content rating.
    # ...X...   content_rating_age        A string specifying the minumum age for viewers of the movie.
    # ...X...   trivia                    A string containing trivia about the movie.
    # ...X...   quotes                    A string containing memorable quotes from the movie.
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X..X.X.   art                       A container of proxy objects representing the movie’s background art. See below for information about proxy objects.
    # XX.XXX.   posters                   A container of proxy objects representing the movie’s posters. See below for information about proxy objects.
    # XX.....   banners                   A container of proxy objects representing the season’s banner images. See below for information about proxy objects.
    # ..X....   thumbs                    A container of proxy objects representing the episode’s thumbnail images. See below for information about proxy objects.
    # X..X.X.   themes                    A container of proxy objects representing the movie’s theme music. See below for information about proxy objects.
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
  
    getElementText    = lambda el, xp : el.xpath(xp)[0].text if el.xpath(xp) and el.xpath(xp)[0].text else ""  # helper for getting text from XML element
    PreferAnidbPoster = Prefs['PreferAnidbPoster']
    GetTvdbPosters    = Prefs['GetTvdbPosters'   ]
    GetTvdbFanart     = Prefs['GetTvdbFanart'    ]
    GetTvdbBanners    = Prefs['GetTvdbBanners'   ]
    UseWebLinks       = Prefs['UseWebLinks'      ]
    UseWarnings       = Prefs['UseWarnings'      ]
    global AniDB_title_tree, AniDB_TVDB_mapping_tree, AniDB_collection_tree                   # Keep XML loaded persistantly as global variable
    
    Log.Debug('--- parseAniDBXml - Begin -------------------------------------------------------------------------------------------')
    Log("parseAniDBXml (%s, %s, %s)" % (metadata, media, force) )

    ### AniDB Serie MXL ###
    Log.Debug("parseAniDBXml - AniDB.net - AniDB Serie MXL")
    try:
      anime = self.urlLoadXml( ANIDB_HTTP_API_URL + metadata.id ).xpath('/anime')[0]          # Put AniDB.net serie xml (cached if able) into 'anime'
    except:
      raise ValueError
    movie = (True if getElementText(anime, 'type')=='Movie' else False)                       # Read movie type from XML
    
    ### AniDB Title ###
    Log.Debug("parseAniDBXml - AniDB.net - Anime title")
    try:
      metadata.title, orig = self.getMainTitle(anime.xpath('/anime/titles/title'), SERIE_LANGUAGE_PRIORITY)
    except:
      raise ValueError                                                                        # No title found
    if movie:                                                                                 # If it's a movie
      metadata.original_title = orig                                                          #   Update original title in metadata http://forums.plexapp.com/index.php/topic/25584-setting-metadata-original-title-and-sort-title-still-not-possible/
    Log.Debug("parseAniDBXml - Title - Chosen title: '%s' original title: '%s'" % (metadata.title, metadata.original_title))

    ### AniDB Start Date ###
    Log.Debug("parseAniDBXml - AniDB.net - Anime Start Date")
    startdate  = getElementText(anime, 'startdate')                                           # get start date if any
    if startdate != "":                                                                       # If not empty
      metadata.originally_available_at = Datetime.ParseDate(startdate).date()                 #   Update metadata.originally_available_at
      if movie:                                                                               #   If it's a movie
        metadata.year = metadata.originally_available_at.year                                 #     Update year in metadata
    
    ### AniDB Ratings ###
    Log.Debug("parseAniDBXml - AniDB.net - AniDB Ratings")
    rating = getElementText(anime, 'ratings/permanent')                                       # Get 'ratings/permanent' attribute form 'anime' XML
    if not rating == "":                                                                                # If not empty
      metadata.rating = float(rating)                                                         #   Update rating in metadata
      
    ### AniDB Category -> Genre mapping ###
    Log.Debug("parseAniDBXml - AniDB.net - AniDB Category -> Genre mapping")
    genres = {}                                                                               #
    for category in anime.xpath('categories/category'):                                       # For each category in the serie
      weight = category.get('weight')                                                         #   Get the weight attribute from the category
      name   = getElementText(category, 'name')                                               #   Get the name   attribute from the category
      if name in GENRE_NAMES and weight >= MINIMUM_WEIGHT:                                    #   If genre name in whitelist
        genres [ name ] = int(weight)                                                         #     Build genre table with name as key and weight as value
      if name in RESTRICTED_GENRE_NAMES and \
         not metadata.content_rating == RESTRICTED_CONTENT_RATING:                            #   If genre name in adult blacklist and content not flagged restricted
        metadata.content_rating = RESTRICTED_CONTENT_RATING                                   #     Set content_rating in metadata
    sortedGenres = sorted(genres.items(), key=lambda x: x[1],  reverse=True)                  # sort genre list
    log_string = "parseAniDBXml - Categories - Genres (Weight): "                             #
    metadata.genres.clear()                                                                   #
    for genre in sortedGenres:                                                                #
      metadata.genres.add(genre[0])                                                           #
      log_string += "%s (%s) " % (genre[0], str(genre[1]))                                    #
    Log.Debug(log_string)                                                                     #

    ### AniDB Collections ###
    Log.Debug("parseAniDBXml - AniDB.net - AniDB Collections")
    self.anidbCollectionMapping(metadata, anime)                                              #   Group movies using anime-movieset-list.xml, XBMC support only collection for movies
    
    ### AniDB Creator data -  Aside from the animation studio, none of this maps to Series entries, so save it for episodes ###
    Log.Debug("parseAniDBXml - AniDB.net - AniDB Creator data")
    studio          = ""
    metadata.studio = ""                                                                      # Empty Studio string
    if movie:
      metadata.writers.clear()                                                                # Empty list of writers
      metadata.producers.clear()                                                              # Empty list of producers
      metadata.directors.clear()                                                              # Empty list of Directors
      ### tagline ###      ### duration ###      ### Countries ###
    else:                                                                                     # 
      writers   = []                                                                          # 
      directors = []                                                                          # 
      producers = []                                                                          # 
    log_string = "parseAniDBXml - Categories - Creator data: "                                #   
    for creator in anime.xpath('creators/name'):                                              #
      nameType = creator.get('type')                                                          #
      
      if nameType == "Animation Work":                                                        # Studio
        # Studio pic - XBOX: .png file, white-on-clear, sized 161px x 109px, Save it in 'skin.aeon.nox"/media/flags/studios/'
        #                               Already created ones: https://github.com/BigNoid/Aeon-Nox/tree/master/media/flags/studios
        #              Plex: 512x288px .png located in 'Plex/Library/Application Support/Plex Media Server/Plug-ins/Media-Flags.bundle/Contents/Resources/'
        metadata.studio = creator.text;                                                       # Set studio in metadata
        studio          = creator.text                                                        # 
        log_string     += "Studio: %s, " % creator.text                                       # 
    
      if "Direction" in nameType:                                                             # Direction, Animation Direction, Chief Animation Direction, Chief Direction
        if movie:                                                                             # if movie
          metadata.directors.add(director)                                                    #   Add director
        else:                                                                                 # else it's a serie
          directors.append(creator.text)                                                      #   add to directors[] for episodes
        log_string += "%s is director, " % creator.text
        
      if nameType == "Series Composition":                                                    # Series Composition is basically a producer role 
        if movie:                                                                             # if movie
          metadata.producers.add(producer)                                                    #   Add Producer
        else:                                                                                 # else it's a serie
          producers.append(creator.text)                                                      #   Add to producers[] for episodes
        log_string += "%s is producer, " % creator.text
        
      if nameType == "Original Work" or "Script" in nameType or "Screenplay" in nameType:     # Original mangaka => 'writers' is the best we can map to / Script writer
        if movie:                                                                             # if movie
          metadata.writers.add(writer)                                                        #   Add movie writer
        else:                                                                                 # else it's a serie
          writers.append(creator.text)                                                        #   Add to writers[] for episodes
        log_string += "%s is writer, " % creator.text
    Log.Debug(log_string)

    ### AniDB-TVDB mapping file + get mapped TVDB id + set serie warning list ###
    Log.Debug("parseAniDBXml - TVDB - AniDB-TVDB mapping file")                                         #
    AniDB_warnings = []                                                                         #
    TVDB_warnings  = []                                                                         #
    tvdbid, defaulttvdbseason, mappingList, mapping_studio = self.anidbTvdbMapping(metadata)  # Search for the TVDB ID from the animeId + update studio
    tvdbSummary   = {}                                                                         # Declare tvdbSummary as Dictionnary
    if tvdbid.isdigit():                                                                      # If a TV Serie so will have a tvdbid
      Log.Debug("parseAniDBXml - TVDB - id: " + tvdbid)                                         #
      
      ### TheTVDB.com - Fanart, Poster and Banner ###
      tvdbposternum = 0                                                                       # Put hte number of TVDB posters to 0
      if GetTvdbPosters or GetTvdbFanart or GetTvdbBanners:                                   # TVDB doesn't index movies, nor 18+ anime
        tvdbposternum = self.getImagesFromTVDB(metadata, media, tvdbid)                       # getImagesFromTVDB(self, metadata, tvdbSeriesId):self.getImagesFromTVDB(metadata, media, tvdbid)                                           # getImagesFromTVDB(self, metadata, tvdbSeriesId):
        if not tvdbposternum:                                                                 # If a TV Serie doesn't have english posters
          TVDB_warnings.append("No English poster")                                           #   Add warning to TVDB warning table
     
      ### TheTVDB.com - Load serie XML ###
      Log.Debug("parseAniDBXml - TheTVDB.com - Load serie XML")                               #
      try:
        tvdbanime = self.urlLoadXml( TVDB_HTTP_API_URL % (TVDB_API_KEY, tvdbid) ).xpath('/Data')[0] ### Pull down the XML cached if possible for a given anime ID
      except:
        tvdbanime = None
      else:
        tvdbtitle = getElementText(tvdbanime, 'Series/SeriesName')                            # Get TVDB serie title
        Log.Debug("parseAniDBXml - TVDB - loaded serie xml: " + tvdbid + " " + tvdbtitle)       
      
        ### TheTVDB.com - Build 'tvdbSummary' table ###
        Log.Debug("parseAniDBXml - TheTVDB.com - Build 'tvdbSummary' table")                               #
        summary_missing = []
        summary_present = []
        for episode in tvdbanime.xpath('Episode'):                         
          seasonid        = getElementText(episode, 'seasonid'       )
          SeasonNumber    = getElementText(episode, 'SeasonNumber'   )   
          EpisodeNumber   = getElementText(episode, 'EpisodeNumber'  )
          EpisodeName     = getElementText(episode, 'EpisodeName'    )
          Overview        = getElementText(episode, 'Overview'       )    
          absolute_number = getElementText(episode, 'absolute_number')
          id              = getElementText(episode, 'id'             )
          episodeWarning  = ""
          if Overview=="":                                                                      # If empty overview
            summary_missing.append(" s" + SeasonNumber + "e" + EpisodeNumber)                   #
            episodeWarning ="Episode Overview Empty\n"                                          #
          else:                                                                                 #
            summary_present.append(" s" + SeasonNumber + "e" + EpisodeNumber)
          if UseWebLinks:
           Overview = "TheTVDB.com: " + \
                       WEB_LINK % (TVDB_SERIE_URL  %(tvdbid              ),  tvdbtitle             ) + \
                       WEB_LINK % (TVDB_SEASON_URL %(tvdbid, seasonid    ), "Season "+SeasonNumber) + \
                       WEB_LINK % (TVDB_EPISODE_URL%(tvdbid, seasonid, id), "s"+SeasonNumber+"e"+EpisodeNumber) + episodeWarning + "\n" + Overview
          tvdbSummary [ "s"+SeasonNumber+"e"+(EpisodeNumber if absolute_number=="" else absolute_number) ] = Overview
        Log.Debug("parseAniDBXml - TheTVDB.com - Episode Summary table - Episodes with summary:    " + str(sorted(summary_present)) )
        Log.Debug("parseAniDBXml - TheTVDB.com - Episode Summary table - Episodes without Summary: " + str(sorted(summary_missing)) )
    else:                                                                                     #
      TVDB_warnings.append("TVDBid not in mapping file")                                      #  
      
    ### AniDB.net Posters ###
    Log.Debug("parseAniDBXml - AniDB.net - Posters")
    if getElementText(anime, 'picture') == "":
      AniDB_warnings.append("No poster present")
    elif PreferAnidbPoster or tvdbposternum == 0:                                             # If anidb poster and PreferAnidbPoster or no TVDB poster (prevent ban for dl poster that ultimately you will take from thetvdb)
      bannerRealUrl = ANIDB_PIC_BASE_URL + getElementText(anime, 'picture');                  #   Build banner RealUrl variable
      if not bannerRealUrl in metadata.posters:                                               #   If url not already there
        metadata.posters[ bannerRealUrl ] = Proxy.Media(HTTP.Request(bannerRealUrl).content, sort_order=(1 if PreferAnidbPoster else 99))

    ### AniDB Serie/Movie description + link ###
    Log.Debug("parseAniDBXml - AniDB.net - Serie/Movie description + link")
    if studio + mapping_studio == "":
      warnings = "AniDb and XML missing studio."                                          # add studio in xml
    elif not studio == "" and not mapping_studio == "":
      warnings = "AniDb have studio '%s'  but XML have '%s'" % (studio, mapping_studio)   # => remove studio in xml
    
    AniDB_warning = ""
    for temp in AniDB_warnings:
      AniDB_warning += temp + ", "
    AniDB_warning = ("" if len(AniDB_warnings) == 0 else AniDB_warning[:-2])

    TVDB_warning  = ""
    for temp in TVDB_warnings:
      TVDB_warning  += temp + ", "
    TVDB_warning  = ("" if len(TVDB_warnings) == 0 else TVDB_warning[:-2])
    
    if UseWebLinks:
      ### To Do: add ANN link
      description = "AniDB.net: "     +WEB_LINK % (ANIDB_SERIE_URL % metadata.id,   metadata.title) + " "+(AniDB_warning if UseWarnings else "")+"\n"
      if tvdbid.isdigit():                                                                      # If a TV Serie have a tvdbid in the mapping file
        description += "TheTVDB.com: "+WEB_LINK % (TVDB_SERIE_URL  % tvdbid,        metadata.title) +" "+(TVDB_warning if UseWarnings else "") +" <BR />\n"
      else: ### NO TVDB id ###
        description += "TheTVDB.com: "+WEB_LINK % ( TVDB_SEARCH_URL % (metadata.title,"Search title"), TVDB_warning) + " <BR />\n"
        # #%3B Semi-colon, %0A Line Feed, %09 Tab or ('	'), ```  code block # #xml.etree.ElementTree.tostring
        # TheTVBD.com: id not mapped. [search TVDB] [Submit bug report] (need GIT account) [file format]
        # SubmitBugReport = "<A href='%s'>%s</A>" % (ANIDB_TVDB_MAPPING_FEEDBACK % ("anidbid:%s '%s' matches tvdbid:xxxxxxx" % (metadata.id,metadata.title), body), str(warnings))
    elif UseWarnings:
      description = ("" if len(AniDB_warnings) == 0 else "AniDB.net: "   + AniDB_warning +       "\n")
      description+= ("" if len( TVDB_warnings) == 0 else "TheTVDB.com: " +  TVDB_warning + "<BR />\n")
    else:
      description = ""
    try:                                                                                      
      description += re.sub(r'http://anidb\.net/[a-z]{2}[0-9]+ \[(.+?)\]', r'\1', getElementText(anime, 'description'))       # Remove wiki-style links to staff, characters etc
      metadata.summary = description                                                          #
    except Exception, e:                                                                      #
      Log.Debug("Exception: " + str(e) )                                                      #
     
    if not movie: ### TV Serie specific #################################################################################################################
      numEpisodes   = 0
      totalDuration = 0
      mapped_eps    = []
      missing_eps   = []
      for episode in anime.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################

        eid         = episode.get('id')
        epNum       = episode.xpath('epno')[0]
        epNumType   = epNum.get('type')
        season      = ("0" if epNumType == "2" else "1" if epNumType == "1" else "")          # Normal episode
        epNumVal    = ( epNum.text[1:] if epNumType == "2" and epNumVal[0] == ['S'] else epNum.text )
        if epNumVal[0] in ['C', 'T', 'P', 'O']:                                               # Specials are prefixed with S(Specials 000-100), C(OPs, EDs 101-199),
          continue                                                                            #       T(Trailers 201-299), P(Parodies 301-399), O(Other    401-499)
        if not (season in media.seasons and epNumVal in media.seasons[season].episodes):      # Log missing episodes
          missing_eps.append(" s" + season + "e" + epNumVal )                                 #
          continue                                                                         
        episodeObj = metadata.seasons[season].episodes[epNumVal]                              # easier to manipulate, as it's going to be used a lot below
        
        ### Writers, etc... ###
        episodeObj.writers.clear()                                                            #
        for writer in writers:                                                                #
          episodeObj.writers.add(writer)                                                      #
          
        episodeObj.producers.clear()                                                          #
        for producer in producers:                                                            #
          episodeObj.producers.add(producer)                                                  #
        
        episodeObj.directors.clear()                                                          #
        for director in directors:                                                            #
          episodeObj.directors.add(director)                                                  #
          
        try:
          rating = getElementText(episode, 'rating')                                          # Get rating if present
          if rating != "":                                                                    # If rating not empty
            episodeObj.rating = float(rating)                                                 #   Update rating
        except:
          pass                                                                                # Continue, as rating is optional
      
        ### AniDBN turn the YYYY-MM-DD airdate in each episode into a Date ###
        airdate = getElementText(episode, 'airdate')
        if airdate != "":
          match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", airdate)
          if match:
            try:
              episodeObj.originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError, e:
              Log.Debug("parseAniDBXml - parseAirDate - Date out of range: " + str(e))

        ### AniDB Get the correct episode title ###
        episodeObj.title, main = self.getMainTitle (episode.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
        if episodeObj.title=="" :                                                             # if no title
          episodeObj.title = epNum.text                                                       #   use epNum.text as for specials it's still prefixed with S  
        
        ### TVDB mapping episode summary ###
        anidb_ep = 's' + season + 'e' + epNumVal                                              # Set anidb_ep episode number
        tvdb_ep  = ""                                                                         #
        summary  = ""
        if tvdbid.isdigit():                                                                  # Matching TVDB id found 
          if anidb_ep in mappingList and mappingList[anidb_ep] in tvdbSummary :               #   If ep in mapping list and mapped ep in the summary list
            tvdb_ep = mappingList [ anidb_ep ]                                                #     tvdb_ep correcponding episode is through the mapping list
          elif defaulttvdbseason=="a" and anidb_ep in tvdbSummary:                            #   else if tvdb have absolute listing and ep in summary list
            tvdb_ep = anidb_ep                                                                #     tvdb_ep in absolute numbering is the anidb id
          elif "s"+defaulttvdbseason+"e"+epNumVal in tvdbSummary:                             #   else mapped season ep exist (implies: and not defaulttvdbseason=="a")
            tvdb_ep = "s"+defaulttvdbseason+"e"+epNumVal                                      #     tvdb_ep used the mapped default season
          if tvdb_ep == "":                                                                   #   if tvdb_ep variable defines
            pass
            #Log.Debug("parseAniDBXml - Episode Summaries - AniDB episod '"+anidb_ep+"' could not be mapped - defaulttvdbseason: " + defaulttvdbseason)
          else:
            summary = ( tvdbSummary [ tvdb_ep ] if not tvdb_ep == None else "" )              #     update summary with tvdbSummary at 'tvdb_ep' key
            #if not tvdb_ep == anidb_ep:                                                      # Because if there is no mapping to be done, no point seeing the logs
            mapped_eps.append( anidb_ep + ">" + tvdb_ep )                                     #
        if UseWebLinks:
          summary = "AniDB.net: " + \
                    WEB_LINK % (ANIDB_SERIE_URL   % metadata.id, metadata.title         ) + \
                    WEB_LINK % (ANIDB_EPISODE_URL % eid,         "s"+season+"e"+epNumVal) + \
                    "\n" + summary
        episodeObj.summary = summary                                                          #

        ### AniDB Duration ###
        duration = getElementText(episode, 'length')
        if duration != "":                                                                    # If duration present
          episodeObj.duration = int(duration) * 1000 * 60                                     #   Save duration in millisecs, AniDB stores it in minutes
          if season == 1:                                                                     #    If it is a serie then
            numEpisodes   += 1                                                                #    One more episode for the average to come
            totalDuration += episodeObj.duration                                              #    Adding episode duration
            
      convert      = lambda text: int(text) if text.isdigit() else text 
      alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
  
      Log.Debug("parseAniDBXml - Episode Summaries - AniDB->TVDB mapped: %s"  %                               str( mapped_eps.sort(key=alphanum_key)) )
      Log.Debug("parseAniDBXml - Episode Summaries - %s %s - Missing eps: %s" % (metadata.id, metadata.title, str(missing_eps.sort(key=alphanum_key))))   

      ### AniDB Final post-episode titles cleanup ###
      if numEpisodes:                                                                         #if movie getting scrapped as episode number by scanner...
        metadata.duration = int(totalDuration) / int(numEpisodes)     

    Log.Debug('--- parseAniDBXml - end -------------------------------------------------------------------------------------------------')

  ### Pull down the XML (and cache it) for a given anime ID ############################################################################################################
  def urlLoadXml(self, url):
    Log('anidbLoadXml (%s)' % url)
    global lastRequestTime
    lastRequestTime = datetime.datetime.utcfromtimestamp(0);
    try:
      networkLock.acquire()
      tries = 2
      while tries:
        delta = datetime.datetime.utcnow() - lastRequestTime;
        if delta.seconds < SECONDS_BETWEEN_REQUESTS:                                         #On AniDB.net, requests closer than 2 secs apart will get you banned
          time.sleep(SECONDS_BETWEEN_REQUESTS - delta.seconds)
        result = None
        try:
          lastRequestTime = datetime.datetime.utcnow()
          result          = HTTP.Request(url, headers={'Accept-Encoding':''}, timeout=60)
        except urllib2.HTTPError, err:
          Log("HTTP Error: " + str(err))
        else:
          if result == "<error>Banned</error>":
            Log('urlLoadXml - You have been Banned by AniDB.net. more than a xml every 2s OR downloaded more than once the title database')
            return None
          else:
            return XML.ElementFromString(result)
        tries -= 1
    finally:
      try:
        networkLock.release()
      except:
        pass

  ### Get the tvdbId from the AnimeId #######################################################################################################################
  def anidbTvdbMapping(self, metadata ):
    
    # --------------------------------   -----------------   --------------------------------------------------------------------------------------------------------
    # ScudLee anime-list-full.xml Tags   attributes          Description
    # --------------------------------   -----------------   --------------------------------------------------------------------------------------------------------
    # anime-list 
    #   anime                            anidbid             AniDB.net   serie unique id
    #                                    tvdbid              TheTVDB.com serie unique id
    #                                    defaulttvdbseason   which season of TheTVDB.com the anidb eps maps to by default, overwritten by the mapping list
    #                                    imdbid              [optional] IMDB serie unique ID
    #                                    tmdbid              [optional] The Movie Database serie unique ID
    #     name                           [text]              Main Anime title                                      
    #     supplemental-info                                  [optional] contain only studio tag so far
    #       studio                       [text]              Animation studio, when absent from AniDB.net
    #     mapping-list                                       Contain mapping list when AniDB.net and TheTVDB.com episode numbers differs
    #       mapping                      anidbseason         AniDB.net season
    #                                    tvdbseason          TheTVDB.com season
    #                                    [text]              Episode mapping anidb_ep-tvdb_ep separated by ';', also present at the beginning & end of the string
    # --------------------------------   -----------------   --------------------------------------------------------------------------------------------------------
    
    mappingList             = {}                                                              # Episode mapping list
    mapping_studio          = ""                                                              # Studio from mapping file
    global AniDB_TVDB_mapping_tree, TVDB_warnings, AniDB_warnings                             # Global variables
    if not AniDB_TVDB_mapping_tree:                                                           # If XML mappile file not loaded
      AniDB_TVDB_mapping_tree = self.xmlElementFromFile(ANIDB_TVDB_MAPPING)                   # Load XML file

    for anime in AniDB_TVDB_mapping_tree.iterchildren('anime'):                               # For anime in matches.xpath('/anime-list/anime')
      if metadata.id == anime.get("anidbid"):                                                 # If it is the right anime id
        tvdbid            = anime.get('tvdbid')                                               #   Get tvdb id
        defaulttvdbseason = anime.get('defaulttvdbseason')                                    #   get default tvdb season
        #tmdbid           = anime.get('tmdbid')                                               #   Optional: TheMovieDatabase id
        #imdbid           = anime.get('imdbid')                                               #   optional: IMDB id
        
        try: ### Studio ###
          studio2 = anime.xpath("supplemental-info/studio")[0].text                           # Try to get Anime studio if present 
        except:                                                                               # But if not there
          studio2 = ""                                                                        # Make the variable empty
        else:                                                                                 # 
          if metadata.studio == "":                                                           # Need to be after "elf.anidbTvdbMapping(metadata)"
            metadata.studio = studio2                                                         #
          else:
            AniDB_warnings.append("Studio in both AniDB and mapping file")                     # studio in mapping file but is in AniDB  
            pass                                                                              #
        if not tvdbid.isdigit():                                                              #   If the xml mapping file possibly needs updating, log it
            Log("[Lanime-list-full.xml] Missing tvdbid for anidbid %s" % metadata.id);       #
            AniDB_warnings.append("studio AniDB '%s', anime-list: '%s'" % (studio, studio2))   #
        else:                                                                                 # Else if Anime id valid
          try:
            for season in anime.iterchildren('mapping-list'):                                 # For each season mapping line in mapping list
              for string in season.text.split(';'):                                           #   Split the sting between semi-colon
                if string=="":                                                                #   If empty
                  continue                                                                    #   Just skip it
                eps = string.split('-')                                                       #   Split it into AniDB and theTVDB episodes
                Log.Debug( 's' + season.get("anidbseason") + 'e' + eps[0] + ' = s'+ season.get("tvdbseason") + 'e' + eps[1])
                mappingList [ 's' + season.get("anidbseason") + 'e' + eps[0] ] = 's' + season.get("tvdbseason") + 'e' + eps[1]   #save mapping in the format s1e123
          except:                                                                             # But if failed
            mappingList = {}                                                                  # Leave it empty
            pass         
        Log("gettvdbId(%s) tvbdid: %s studio: %s defaullttvdbseason: %s" % (metadata.id, tvdbid, studio2, str(defaulttvdbseason)) )
        return tvdbid, defaulttvdbseason, mappingList, studio2

    Log.Debug('anidbTvdbMapping('+metadata.id+') found no matching anidbid...')
    return "", "",[], ""

  ### [banners.xml] Attempt to get the TVDB's image data ###############################################################################################################
  def getImagesFromTVDB(self, metadata, media, tvdbSeriesId):

    # ----------------------------------   -------   ------------   -------------------------------------------------------------------------------------------------------
    # theTVDB.com banners.xml Tags         Used by   Values         Description
    # ----------------------------------   -------   ------------   -------------------------------------------------------------------------------------------------------
    # Banners
    #   Banner
    #     id                               ALL                      TVDB serie ID
    #     BannerPath                       ALL       path           Can be appended to <mirrorpath>/banners/ to determine the actual location of the artwork.
    #     BannerType                       ALL       fanart         ...  
    #                                                poster         ...  
    #                                                series         ...  
    #                                                season         ...     
    #     BannerType2                      fanart    1280x720       ...
    #                                                1920x1080      ...
    #                                      poster    680x1000       ...
    #                                      series    blank          will leave the title and show logo off the banner
    #                                                text           will show the series name as plain text in an Arial font
    #                                                graphical      will show the series name in the show's official font or will display the actual logo for the show
    #                                      season    season         will be the same dimensions as standard DVD cover format
    #                                                seasonwide     will be the same dimensions as the series banners
    #     Colors                           fanart    Null/rx|gx|bx  These are colors the artist picked that go well with the image.
    #                                                               In order they are Light Accent Color, Dark Accent Color and Neutral Midtone Color. 
    #                                                               It's meant to be used if you want to write something over the image, it gives you a good idea of what colors may work and show up well.
    #     Language                         ALL       en, ...        Some banners list the series name in a foreign language. The language abbreviation will be listed here.
    #     Season                           ?         season         If the banner is for a specific season, that season number will be listed here.
    #     Rating                           ALL                      Returns either null or a decimal with four decimal places. The rating the banner currently has on the site.
    #     RatingCount                      ALL       unsigned int   Number of people who have rated the image.
    #     SeriesName                       fanart    Bolean         Indicates if the seriesname is included in the image or not.
    #     ThumbnailPath                    fanart    path           Path to the thumbnail pic, diplayed if fanart only
    #     VignettePath                     fanart    path           Used exactly the same way as BannerPath, only shows if BannerType is fanart.
    # ----------------------------------   -------   ------------   -------------------------------------------------------------------------------------------------------
    
    PreferAnidbPoster = Prefs['PreferAnidbPoster'];
    GetTvdbPosters    = Prefs['GetTvdbPosters'   ];
    GetTvdbFanart     = Prefs['GetTvdbFanart'    ];
    GetTvdbBanners    = Prefs['GetTvdbBanners'   ];
    
    try:
      bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbSeriesId), cacheTime=(CACHE_1HOUR * 720)) # don't bother with the full zip, all we need is the banners 
    except:
      return 0

    Log('getImagesFromTVDB([METADATA],%s) GetTvdbPosters: %s, GetTvdbFanart: %s, GetTvdbBanners: %s, PreferAnidbPoster: %s' %(tvdbSeriesId, GetTvdbPosters, GetTvdbFanart, GetTvdbBanners, PreferAnidbPoster))
    num       = 0
    posternum = 0
    for banner in bannersXml.xpath('Banner'):                                                 # For each picture reference in the banner file
      num += 1                                                                                # Increase their count
      if banner.xpath('Language')[0].text != 'en':                                            # Skipping non-english images as AniDB/theTVDB english mainly as is this metadata agent
        continue
      
      bannerType     = banner.xpath('BannerType' )[0].text                                    #
      bannerType2    = banner.xpath('BannerType2')[0].text                                    #
      bannerPath     = banner.xpath('BannerPath' )[0].text                                    #
      rating         =(banner.xpath('Rating'     )[0].text if banner.xpath('Rating') else "") #
      season         =(banner.xpath('Season'     )[0].text if banner.xpath('season') else "") #Season if it is a season poster
      proxyFunc      =(Proxy.Preview if bannerType=='fanart' else Proxy.Media)                # Manage preview for if pic is a fanart
      bannerRealUrl  = TVDB_IMAGES_URL + bannerPath
      bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
      metaType       = (metadata.art                     if bannerType=='fanart' else \
                        metadata.posters                 if bannerType=='poster' else \
                        metadata.banners                 if bannerType=='series' or  bannerType2=='seasonwide' else \
                        metadata.seasons[season].posters if bannerType=='season' and bannerType2=='season'     else None)
                          
      if GetTvdbFanart  and   bannerType == 'fanart' or \
         GetTvdbPosters and ( bannerType == 'poster' or bannerType2 == 'season'    ) or \
         GetTvdbBanners and ( bannerType == 'series' or bannerType2 == 'seasonwide'):
        if not bannerRealUrl in [metadata.art, metadata.posters, metadata.banners, metadata.seasons[season].posters]: 
          try:
            metaType[bannerRealUrl] = proxyFunc(HTTP.Request(bannerThumbUrl).content, sort_order=(num+1 if PreferAnidbPoster else num))  #why 
            Log.Debug('getImagesFromTVDB - Downloading url1: %s, url2: %s, sort_order: %s' % (bannerRealUrl, bannerThumbUrl, num))
          except:
            Log.Debug('getImagesFromTVDB - error downloading banner url1: %s, url2: %s' % (bannerRealUrl, bannerThumbUrl))
      if bannerType == 'poster':
        posternum += 1
      return posternum

  ### AniDB collection mapping #######################################################################################################################
  def anidbCollectionMapping(self, metadata, anime ):
  
    # AniDB.net telated anime tag in the serie XML
    # --------------------------------------------
    # <relatedanime>
    #   <relatedanime>
    #     <anime id="4"    type="Sequel" >Seikai no Senki               </anime>               # Type= Same Setting, Alternative Setting, Sequel, Prequel, Side Story, Other
    #     <anime id="6"    type="Prequel">Seikai no Danshou             </anime>
    #     <anime id="1623" type="Summary">Seikai no Monshou Tokubetsuhen</anime>
    #</relatedanime>
    #
    # --------------------------------   ----------   -------------------------------------------------------------------------------------------------------
    # ScudLee anime-movieset-list Tags   Attributes   Description
    # --------------------------------   ----------   -------------------------------------------------------------------------------------------------------
    # anime-set-list
    #   set
    #     anime                          anidbid      AniDB.net unique anime id
    #                                    [text]       Main title
    #     titles
    #       title                        type         main, official, syn, short
    #                                    xml:lang     AniDB.net language
    #                                    [text]
    
    global AniDB_collection_tree
    if not AniDB_collection_tree:
      AniDB_collection_tree = self.xmlElementFromFile(ANIDB_COLLECTION_MAPPING)

    ### AniDB related anime List creation ###
    related_anime_list = [ ]
    for relatedAnime in anime.xpath('/anime/relatedanime/anime'):                              #
      id    = relatedAnime.get('id')                                                           # 
      #type  = relatedAnime.get('type')                                                        # 
      #title = relatedAnime.text                                                               # 
      related_anime_list.append(id)                                                            # 

    ### AniDB search in collection XML ###
    for element in AniDB_collection_tree.iterfind("anime"):
      anidbid = element.get('anidbid')                                                         # 
      title   = element.text                                                                   #  
      if anidbid in related_anime_list:                                                        #
        set = element.getparent()                                                              # 
        title, main = self.getMainTitle(set.xpath('titles')[0], SERIE_LANGUAGE_PRIORITY)       #
        metadata.collections.clear()                                                           # Empty collection
        metadata.collections.add(title)                                                        # 
        Log.Debug('anidbCollectionMapping - anidbid is part of collection: %s' % (metadata.id, title) )
        return True
      
    Log("anidbCollectionMapping([metadata], %s) - %s is not part of any collection" % (metadata.id, metadata.id.zfill(5)) )
    return False
    # #Dict.Reset()
    # Dict[key] = name
    # if key in Dict:
    #   x = Dict[key]
    #   Dict.Save()
    
  ### Import XML file from 'Resources' folder into an XML element ######################################################################################################
  def xmlElementFromFile (self, filename, url=None):
    Log('xmlElementFromFile (%s, %s) %s' % (filename, url, R(filename) ) )
    try:
      element = XML.ElementFromString( Resource.Load(filename) )
    except:
      Log.Debug("xmlElementFromFile - Loading XML file from Resources folder failed:" + filename)
      try:
        element = XML.ElementFromString( XML.ElementFromURL(url, cacheTime=CACHE_1HOUR * 24 * 7 * 2) ) # String = XML.ElementFromString( Archive.GzipDecompress( HTTP.Request(subUrl, headers={'Accept-Encoding':''}).content ) )
      except:
        Log("xmlElementFromFile - Loading XML from url failed: " + url)
      else:
        Log("xmlElementFromFile - Loading XML from url worked: " + url)
    else:
      Log.Debug("xmlElementFromFile - Loading XML file from Resources folder worked: " + filename)
      return element

  ### Get the Levenshtein distance score in percent between two strings ################################################################################################
  #def getScore(self, a, b):
  #  return int(100 - (100 * float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) ))   #To-Do: LongestCommonSubstring(first, second). use that?

  ### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
  def cleanse_title(self, title):
    return title.replace("'", "`").translate(string.maketrans('', ''), FILTER_CHARS).lower() # None in the translate call was giving an error of 'TypeError: expected a character buffer object'. So, we construct a blank translation table instead.

  ### Split a string per list of chars #################################################################################################################################
  def splitByChars(self, string, separators=SPLIT_CHARS):
    for i in separators:
      string.replace(" ", i)
    return string.split()

  ### extract the series/movie/Episode title #################################################################################################################################
  def getMainTitle(self, titles, LANGUAGE_PRIORITY):
    
    langTitles = ["" for index in range(len(LANGUAGE_PRIORITY)+2)]                            # LANGUAGE_PRIORITY title order, original title, then choosen title
    for title in titles:                                                                      # For each of the possible titles given
      lang = title.get('{http://www.w3.org/XML/1998/namespace}lang')                          #   Get the language, 'xml:lang' attribute need hack to read properly
      type = title.get('type')                                                                #   Get the type (main, official, syn, short)
                                                                                              
      if type == 'main' or type == None and langTitles[ len(LANGUAGE_PRIORITY) ] == "":       # If main title or default episode title empty
          langTitles [ len(LANGUAGE_PRIORITY)        ] = title.text                           #   save main title or episode first result as original title
      if type in ['official', 'main', None]  and lang in LANGUAGE_PRIORITY:                   # If title in the languages order (include main title)
          langTitles [ LANGUAGE_PRIORITY.index(lang) ] = title.text                           #   save it in the right language slot
                                                                                              
      for index in range( len(LANGUAGE_PRIORITY)+1 ):                                         # Loop all saved language and main titles in the priority order
        if not langTitles [ index ] == '' :                                                   #   If the title for language was filled
          langTitles [len(LANGUAGE_PRIORITY)+1] = langTitles [ index ]                        #     set as language title
          break                                                                               #     Break the loop if found the title
                                                                                               
    if not type== None:
      Log.Debug("getMainTitle (%d titles) Title: %s  Main title: %s" % (len(titles), langTitles[len(LANGUAGE_PRIORITY)], langTitles[len(LANGUAGE_PRIORITY)+1] ))
    return langTitles[len(LANGUAGE_PRIORITY)+1], langTitles[len(LANGUAGE_PRIORITY)]

### TV Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows, HamaCommonAgent):
  name             = 'HamaTV'
  languages        = [ Locale.Language.English, ]
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles']
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
 
  def search(self, results, media, lang, manual):
    self.searchByName(results, lang, media.show, media.year)

  def update(self, metadata, media, lang, force):
    self.parseAniDBXml(metadata, media, force, False)

### Movie Agent declaration ############################################################################################################################################
class HamaMovieAgent(Agent.Movies, HamaCommonAgent):
  name             = 'HamaMovies'
  languages        = [ Locale.Language.English, ]
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles']
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None

  def search(self, results, media, lang, manual):
    self.searchByName(results, lang, media.name, media.year)
 
  def update(self, metadata, media, lang, force):
    self.parseAniDBXml(metadata, media, force, True)
