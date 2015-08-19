# -*- coding: utf-8 -*-
### HTTP Anidb Metadata Agent (HAMA) By ZeroQI (Forked from Atomicstrawberry's v0.4 - AniDB, TVDB, AniDB mod agent for XBMC XML's, and Plex URL and path variable definition ###
ANIDB_TITLES                 = 'http://anidb.net/api/anime-titles.xml.gz'                                                         # AniDB title database file contain all ids, all languages
ANIDB_TVDB_MAPPING           = 'http://rawgithub.com/ScudLee/anime-lists/master/anime-list-master.xml'                            # ScudLee mapping file url
ANIDB_TVDB_MAPPING_CUSTOM    = 'anime-list-custom.xml'                                                                            # custom local correction for ScudLee mapping file url
ANIDB_COLLECTION             = 'http://rawgithub.com/ScudLee/anime-lists/master/anime-movieset-list.xml'                          # ScudLee collection mapping file
ANIDB_HTTP_API_URL           = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='          #
ANIDB_PIC_BASE_URL           = 'http://img7.anidb.net/pics/anime/'                                                                # AniDB picture directory
ANIDB_SERIE_URL              = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s'                                           # AniDB link to the anime
ANIDB_TVDB_MAPPING_FEEDBACK  = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'                                # ScudLee mapping file git feedback url
TVDB_HTTP_API_URL            = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/en.xml'                                     # TVDB Serie XML for episodes sumaries for now
TVDB_BANNERS_URL             = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/banners.xml'                                    # TVDB Serie pictures xml: fanarts, posters, banners
TVDB_SERIE_SEARCH            = 'http://thetvdb.com/api/GetSeries.php?seriesname='                                                 #
TVDB_IMAGES_URL              = 'http://thetvdb.com/banners/'                                                                      # TVDB picture directory
TVDB_SERIE_URL               = 'http://thetvdb.com/?tab=series&id=%s'                                                             #
TMDB_MOVIE_SEARCH            = 'http://api.tmdb.org/3/search/movie?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&query=%s&year=&language=en&include_adult=true'
TMDB_MOVIE_SEARCH_BY_TMDBID  = 'http://api.tmdb.org/3/movie/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=releases,credits&language=en'
TMDB_SEARCH_URL_BY_IMDBID    = 'https://api.tmdb.org/3/find/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id'  #
TMDB_CONFIG_URL              = 'https://api.tmdb.org/3/configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'                    #
TMDB_IMAGES_URL              = 'https://api.tmdb.org/3/movie/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'                  #
OMDB_HTTP_API_URL            = "http://www.omdbapi.com/?i="                                                                       #
THEME_URL                    = 'http://tvthemes.plexapp.com/%s.mp3'                                                               # Plex TV Theme url
RESTRICTED_CONTENT_RATING    = "NC-17"
RESTRICTED_GENRE_NAMES       = [ '18 Restricted', 'Pornography' ]
FILTER_CHARS                 = "\\/:*?<>|~-; "
SPLIT_CHARS                  = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations
WEB_LINK                     = "<a href='%s' target='_blank'>%s</a>"
GENRE_NAMES                  = [  ### List of AniDB category names useful as genre. 1st variable mark 18+ categories. The 2nd variable will actually cause a flag to appear in Plex ####################
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
  'Historical', '1920s', 'Bakumatsu - Meiji Period', 'Edo Period', 'Heian Period', 'Sengoku Period', 'Victorian Period', 'World War I', 'World War II', 'Alternative Present',
  ### Themes - many useful ###########################################################################################################################################
  'Anti-War', 'Art', 'Music', 'Band', 'Idol', 'Photography', 'Christmas', 'Coming of Age', 'Conspiracy', 'Cooking', 'Cosplay', 'Cyberpunk', 'Daily Life', 'Earthquake',
  'Post-War', 'Post-apocalypse', 'War', 'Dystopia', 'Friendship', 'Law and Order', 'Cops', 'Special Squads', 'Military', 'Airforce', 'Feudal Warfare', 'Navy',
  'Politics', 'Proxy Battles', 'Racism', 'Religion', 'School Life', 'All-boys School', 'All-girls School', 'Art School', 'Clubs', 'College', 'Delinquents',
  'Elementary School', 'High School', 'School Dormitory', 'Student Council', 'Transfer Student', 'Sports', 'Acrobatics', 'Archery', 'Badminton', 'Baseball',
  'Basketball', 'Board Games', 'Chess', 'Go', 'Mahjong', 'Shougi', 'Combat', 'Boxing', 'Judo', 'Kendo', 'Muay Thai', 'Wrestling', 'Cycling', 'Dodgeball', 'Fishing',
  'Football', 'Golf', 'Gymnastics', 'Horse Riding', 'Ice Skating', 'Inline Skating', 'Motorsport', 'Formula Racing', 'Street Racing', 'Rugby', 'Swimming', 'Tennis',
  'Track and Field', 'Volleyball', 'Steampunk', 'Summer Festival', 'Tragedy', 'Underworld', 'Assassin', 'Bounty Hunter', 'Mafia', 'Yakuza', 'Pirate', 'Terrorist',
  'Thief']
FILTER_SEARCH_WORDS = [ ### These are words which cause extra noise due to being uninteresting for doing searches on, Lowercase only #############################################################
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime', 'ni', 'sekai',                                             # Jp
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', 'me',  'princess', 'theater',  # En Continued
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses',                                                                                                               # Fr
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi']                                                              # Roman digits

import os, re, time, datetime, string, thread, threading, urllib # Functions used per module: os (read), re (sub, match), time (sleep), datetim (datetime).
AniDB_title_tree, AniDB_collection_tree, AniDB_TVDB_mapping_tree = None, None, None  #ValueError if in Start()
SERIE_LANGUAGE_PRIORITY   = [ Prefs['SerieLanguage1'  ].encode('utf-8'), Prefs['SerieLanguage2'  ].encode('utf-8'), Prefs['SerieLanguage3'].encode('utf-8') ]  #override default language
EPISODE_LANGUAGE_PRIORITY = [ Prefs['EpisodeLanguage1'].encode('utf-8'), Prefs['EpisodeLanguage2'].encode('utf-8') ]                                           #override default language

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs(): #     a = sum(getattr(t, name, 0) for name in "xyz")
  DefaultPrefs = ("GetTvdbFanart", "GetTvdbPosters", "GetTvdbBanners", "GetAnidbPoster", "GetTmdbFanart", "GetTmdbPoster", "localart", "adult", 
                  "GetPlexThemes", "MinimumWeight", "SerieLanguage1", "SerieLanguage2", "SerieLanguage3", "EpisodeLanguage1", "EpisodeLanguage2")
  try:  [Prefs[key] for key in DefaultPrefs]
  except:  Log.Error("DefaultPrefs.json invalid" );  return MessageContainer ('Error', "Value '%s' missing from 'DefaultPrefs.json', update it" % key)
  else:    Log.Info ("DefaultPrefs.json is valid");  return MessageContainer ('Success', 'HAMA - Provided preference values are ok')
  
### Pre-Defined Start function #########################################################################################################################################
def Start():
  msgContainer = ValidatePrefs();
  if msgContainer.header == 'Error': return
  Log.Debug('### HTTP Anidb Metadata Agent (HAMA) Started ##############################################################################################################')
  global AniDB_title_tree, AniDB_TVDB_mapping_tree, AniDB_collection_tree  # only this one to make search after start faster
  AniDB_title_tree        = HamaCommonAgent().xmlElementFromFile(ANIDB_TITLES, os.path.splitext(os.path.basename(ANIDB_TITLES))[0]  , True,  CACHE_1HOUR * 24 * 2)
  AniDB_TVDB_mapping_tree = HamaCommonAgent().xmlElementFromFile(ANIDB_TVDB_MAPPING,            os.path.basename(ANIDB_TVDB_MAPPING), False, CACHE_1HOUR * 24 * 2)
  AniDB_collection_tree   = HamaCommonAgent().xmlElementFromFile(ANIDB_COLLECTION,              os.path.basename(ANIDB_COLLECTION  ), False, CACHE_1HOUR * 24 * 2)
  HTTP.CacheTime          = CACHE_1HOUR * 24
  
class HamaCommonAgent:
  
  ### Serie search ######################################################################################################################################################
  def Search(self, results, media, lang, manual, movie):
    Log.Debug("=== Search - Begin - ================================================================================================")
    orig_title = ( media.title if movie else media.show ).encode('utf-8')  # NEEDS UTF-8
    if not orig_title:  return
    if orig_title.startswith("clear-cache"):   HTTP.ClearCache()  ### Clear Plex http cache manually by searching a serie named "clear-cache" ###
    Log.Info("search() - Title: '%s', name: '%s', filename: '%s', manual:'%s'" % (orig_title, media.name, media.filename, str(manual)))  #if media.filename is not None: filename = String.Unquote(media.filename) #auto match only
    
    ### Check if a guid is specified "Show name [anidb-id]" ###
    global SERIE_LANGUAGE_PRIORITY
    match = re.search("(?P<show>.*?) ?\[(?P<source>(anidb|tvdb|tmdb|imdb))-(tt)?(?P<guid>[0-9]{1,7})\]", orig_title, re.IGNORECASE)
    if match:  ###metadata id provided
      source, guid, show = match.group('source').lower(), match.group('guid'), match.group('show')
      if source=="anidb":  show, mainTitle = self.getAniDBTitle(AniDB_title_tree.xpath("/animetitles/anime[@aid='%s']/*" % guid), SERIE_LANGUAGE_PRIORITY) #global AniDB_title_tree, SERIE_LANGUAGE_PRIORITY;
      Log.Debug( "search - source: '%s', id: '%s', show from id: '%s' provided in foldername: '%s'" % (source, guid, show, orig_title) )
      results.Append(MetadataSearchResult(id="%s-%s" % (source, guid), name=show, year=media.year, lang=Locale.Language.English, score=100))
      return
  
    ### AniDB Local exact search ###
    cleansedTitle = self.cleanse_title (orig_title).encode('utf-8')
    if media.year is not None: orig_title = orig_title + " (" + str(media.year) + ")"  ### Year - if present (manual search or from scanner but not mine), include in title ###
    parent_element, show , score, maxi = None, "", 0, 0
    AniDB_title_tree_elements = list(AniDB_title_tree.iterdescendants()) if AniDB_title_tree else []
    for element in AniDB_title_tree_elements:
      if element.get('aid'):
        if score: #only when match found and it skipped to next serie in file, then add
          if score>maxi: maxi=score
          Log.Debug("search() - AniDB - score: '%3d', id: '%6s', title: '%s' " % (score, aid, show))
          langTitle, mainTitle = self.getAniDBTitle(parent_element, SERIE_LANGUAGE_PRIORITY)
          results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=Locale.Language.English, score=score))
          parent_element, show , score = None, "", 0
        aid = element.get('aid')
      elif element.get('type') in ('main', 'official', 'syn', 'short'):
        title = element.text
        if   title.lower()              == orig_title.lower() and 100                            > score:  parent_element, show , score = element.getparent(), title,         100; Log.Debug("search() - AniDB - temp score: '%3d', id: '%6s', title: '%s' " % (100, aid, show))  #match = [element.getparent(), show,         100]
        elif self.cleanse_title (title) == cleansedTitle      and  99                            > score:  parent_element, show , score = element.getparent(), cleansedTitle,  99  #match = [element.getparent(), cleansedTitle, 99]
        elif orig_title in title                              and 100*len(orig_title)/len(title) > score:  parent_element, show , score = element.getparent(), orig_title,    100*len(orig_title)/len(title)  #match = [element.getparent(), show, 100*len(orig_title)/len(element.text)]
        else:  continue #no match 
    if score: #last serie detected, added on next serie OR here
      Log.Debug("search() - AniDB - score: '%3d', id: '%6s', title: '%s' " % (score, aid, show))
      langTitle, mainTitle = self.getAniDBTitle(parent_element, SERIE_LANGUAGE_PRIORITY)
      results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=Locale.Language.English, score=score))
    if len(results)>=1:  return  #results.Sort('score', descending=True)

    ### AniDB local keyword search ###
    matchedTitles, matchedWords, words  = [ ], { }, [ ]
    log_string     = "search() - Keyword search - Matching '%s' with: " % orig_title
    for word in self.splitByChars(orig_title, SPLIT_CHARS):
      word = self.cleanse_title (word)
      if word and word not in FILTER_SEARCH_WORDS and len(word) > 1:  words.append (word.encode('utf-8'));  log_string += "'%s', " % word
    Log.Debug(log_string[:-2]) #remove last 2 chars  #if len(words)==0:
    for title in AniDB_title_tree_elements:
      if title.get('aid'): aid = title.get('aid')
      elif title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main':
        sample = self.cleanse_title (title.text).encode('utf-8')
        for word in words:
          if word in sample:
            index  = len(matchedTitles)-1
            if index >=0 and matchedTitles[index][0] == aid:
              if title.get('type') == 'main':               matchedTitles[index][1] = title.text
              if not title.text in matchedTitles[index][2]: matchedTitles[index][2].append(title.text)
            else:
              matchedTitles.append([aid, title.text, [title.text] ])
              if word in matchedWords: matchedWords[word].append(sample) ## a[len(a):] = [x]
              else:                    matchedWords[word]=[sample]       ## 
    Log.Debug(", ".join( key+"(%d)" % len(value) for key, value in matchedWords.iteritems() )) #list comprehention
    log_string = "Search - similarity with '%s': " % orig_title
    for match in matchedTitles: ### calculate scores + Buid results ###
      scores = []
      for title in match[2]: # Calculate distance without space and characters
        a, b = self.cleanse_title(title), cleansedTitle
        scores.append( int(100 - (100*float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) )) )  #To-Do: LongestCommonSubstring(first, second). use that?
      bestScore  = max(scores)
      log_string = log_string + match[1] + " (%s%%), " % '{:>2}'.format(str(bestScore))
      results.Append(MetadataSearchResult(id="anidb-"+match[0], name=match[1]+" [anidb-%s]"  % match[0], year=media.year, lang=Locale.Language.English, score=bestScore))
    Log.Debug(log_string)    #results.Sort('score', descending=True)
    return

    ### TVDB serie search ###
    Log.Debug("maxi: '%d'" % maxi)
    if maxi<50:
      try:  TVDBsearchXml = XML.ElementFromURL( TVDB_SERIE_SEARCH + orig_title.replace(" ", "%20"), cacheTime=CACHE_1HOUR * 24)
      except:  Log.Debug("search() - TVDB Loading search XML failed: ")
      else:
        for serie in TVDBsearchXml.xpath('Series'):
          a, b = orig_title, serie.xpath('SeriesName')[0].text.encode('utf-8') #a, b  = cleansedTitle, self.cleanse_title (serie.xpath('SeriesName')[0].text)
          score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
          Log.Debug( "search() - TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, serie.xpath('seriesid')[0].text, serie.xpath('SeriesName')[0].text) )
          results.Append(MetadataSearchResult(id="%s-%s" % ("tvdb", serie.xpath('seriesid')[0].text), name="%s [%s-%s]" % (serie.xpath('SeriesName')[0].text, "tvdb", serie.xpath('seriesid')[0].text), year=None, lang=Locale.Language.English, score=score) )
    if len(results)>=1:  return

    ### TMDB movie search ###
    Log.Debug("search() - TMDB  - url: " + TMDB_MOVIE_SEARCH % orig_title)  #config_dict = self.get_json(TMDB_CONFIG_URL, cache_time=CACHE_1WEEK * 2)
    try:     tmdb_json = JSON.ObjectFromURL(TMDB_MOVIE_SEARCH % orig_title.replace(" ", "%20"), sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1WEEK * 2)
    except:  Log('get_json - Error fetching JSON page ' + TMDB_MOVIE_SEARCH % orig_title) # tmdb_json   = self.get_json(TMDB_MOVIE_SEARCH % orig_title, cache_time=CACHE_1WEEK * 2)
    else:
      if isinstance(tmdb_json, dict) and 'results' in tmdb_json:
        for i, movie in enumerate(tmdb_json['results']):
          a, b = orig_title, movie['title'].encode('utf-8')
          score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
          id = movie['id']
          Log.Debug( "search() - TMDB  - score: '%3d', id: '%6s', title: '%s'" % (score, movie['id'],  movie['title']) )
          results.Append(MetadataSearchResult(id="%s-%s" % ("tmdb", movie['id']), name="%s [%s-%s]" % (movie['title'], "tmdb", movie['id']), year=None, lang=Locale.Language.English, score=score) )
          if '' in movie and movie['adult']!="null":  Log.Debug( "adult: '%s'" % movie['adult'])
          # genre_ids, original_language, id, original_language, original_title, overview, release_date, poster_path, popularity, video, vote_average, vote_count, adult, backdrop_path

  ### Parse the AniDB anime title XML ##################################################################################################################################
  def Update(self, metadata, media, lang, force, movie):

    Log.Debug('--- Update Begin -------------------------------------------------------------------------------------------')
    if not "-" in metadata.id:  metadata.id = "anidb-" + metadata.id  # Old metadata from when the id was only the anidbid
    Log.Debug("Update - metadata source: '%s', id: '%s', Title: '%s',(%s, %s, %s)" % (metadata.id.split('-')[0], metadata.id.split('-')[1], metadata.title, "[...]", "[...]", force) )
    global SERIE_LANGUAGE_PRIORITY, EPISODE_LANGUAGE_PRIORITY
    error_log = { 'anime-list anidbid missing': [], 'anime-list tvdbid missing': [], 'anime-list studio logos': [], 'Missing episodes'    : [], 'Plex themes missing'    : [],
                  'AniDB summaries missing'   : [], 'AniDB posters missing'    : [], 'TVDB summaries missing' : [], 'TVDB posters missing': []}
    getElementText = lambda el, xp: el.xpath(xp)[0].text if el is not None and el.xpath(xp) and el.xpath(xp)[0].text else ""  # helper for getting text from XML element

    ### Get tvdbid, tmdbid, imdbid (+etc...) through mapping file ###
    tvdbid, tmdbid, imdbid, defaulttvdbseason, mapping_studio, poster_id, mappingList, anidbid_table = "", "", "", "", "", "", {}, []
    tvdbposternumber, tvdb_table, tvdbtitle, tvdbOverview, tvdbNetwork, tvdbFirstAired, tvdbRating, tvdbContentRating, tvdbgenre = 0, {}, "", "", "", "", None, None, ()
    if   metadata.id.startswith("tvdb-"):  tvdbid = metadata.id [len("tvdb-"):]
    elif metadata.id.startswith("anidb-"):
      anidbid=metadata.id[len("anidb-"):]
      tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio, anidbid_table, poster_id = self.anidbTvdbMapping(metadata, anidbid, error_log)
    elif metadata.id.startswith("tmdb-"):
      tmdbid = metadata.id [len("tmdb-"):]
      Log.Debug("Update() - TMDB  - url: " + TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid)
      try:     tmdb_json = JSON.ObjectFromURL(TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid, sleep=2.0, headers={'Accept': 'application/json'}, cacheTime=CACHE_1DAY)
      except:  Log('Update() - get_json - Error fetching JSON page ' + TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid)
      else:
        Log('Update() - get_json - worked: ' + TMDB_MOVIE_SEARCH_BY_TMDBID % tmdbid)
        if 'vote_average' in tmdb_json and isinstance(tmdb_json['vote_average'], float):  metadata.rating                  = tmdb_json['vote_average']  # if not ep.isdigit() and "." in ep and ep.split(".", 1)[0].isdigit() and ep.split(".")[1].isdigit():  
        if 'runtime'      in tmdb_json and isinstance(tmdb_json['runtime'     ], int):    metadata.duration                = int(tmdb_json['runtime']) * 60 * 1000
        if 'title'        in tmdb_json and tmdb_json['title']:                            metadata.title                   = tmdb_json['title']
        if 'overview'     in tmdb_json and tmdb_json['overview']:                         metadata.summary                 = tmdb_json['overview']
        if 'release_date' in tmdb_json and tmdb_json['release_date']:                     metadata.originally_available_at = Datetime.ParseDate(tmdb_json['release_date']).date()
        if 'imdb_id'      in tmdb_json and tmdb_json['imdb_id'] and not imdbid:           imdbid                           = tmdb_json['imdb_id']
        if 'vote_average' in tmdb_json and tmdb_json['vote_average'] and 'vote_count' in tmdb_json and tmdb_json['vote_count'] > 3: metadata.rating = tmdb_json['vote_average']
        if 'genres'       in tmdb_json and tmdb_json['genres']!=[]:
          for genre in tmdb_json['genres']: metadata.genres.add(genre['name'].strip()) #metadata.genres = tmdb_json['genres'] ???
        if 'production_companies' in tmdb_json and len(tmdb_json['production_companies']) > 0:  # Studio.
          index, company = tmdb_json['production_companies'][0]['id'],""
          for studio in tmdb_json['production_companies']:
            if studio['id'] <= index:  index, company = studio['id'], studio['name'].strip()
          metadata.studio = company
        if 'belongs_to_collection' in tmdb_json and tmdb_json['belongs_to_collection']:  metadata.collections.add(tmdb_json['belongs_to_collection']['name'].replace(' Collection',''))
        if movie:
          if tmdb_json['tagline']:  metadata.tagline = tmdb_json['tagline']
          #if metadata.year = metadata.originally_available_at.year

    if tvdbid.isdigit(): ### TVDB ID exists ####

      ### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###
      if THEME_URL % tvdbid in metadata.themes:  Log.Debug("Update() - Theme song - already added")
      else:                                      self.metadata_download (metadata.themes, THEME_URL % tvdbid, 1, "Plex/"+metadata.id+".mp3")  #if local, load it ?
      
      ### TVDB - Load serie XML ###
      tvdbanime, summary_missing, summary_present = None, [], []
      Log.Debug("Update() - TVDB - tvdbid: '%s', url: '%s'" %(tvdbid, TVDB_HTTP_API_URL % tvdbid))
      tvdbanime=self.xmlElementFromFile ( TVDB_HTTP_API_URL % tvdbid, "TVDB/"+tvdbid+".xml", False, CACHE_1HOUR * 24)
      if tvdbanime:
        tvdbanime = tvdbanime.xpath('/Data')[0]
        tvdbtitle, tvdbNetwork, tvdbOverview, tvdbFirstAired = getElementText(tvdbanime, 'Series/SeriesName'), getElementText(tvdbanime, 'Series/Network'), getElementText(tvdbanime, 'Series/Overview'  ), getElementText(tvdbanime, 'Series/FirstAired')
        tvdbContentRating = getElementText(tvdbanime, 'Series/ContentRating')
        tvdbGenre         = filter(None, getElementText(tvdbanime, 'Series/Genre').split("|"))
        if '.' in getElementText(tvdbanime, 'Series/Rating'): ###tvdbRating   # isinstance(tmdb_json['vote_average'], float)
          try:    tvdbRating = float(getElementText(tvdbanime, 'Series/Rating'))
          except: tvdbRating = None 
        else: tvdbRating = None
        if imdbid is None or imdbid =="" and getElementText(tvdbanime, 'Series/IMDB_ID'):  imdbid = getElementText(tvdbanime, 'Series/IMDB_ID');  Log.Debug("Update() - IMDB ID was empty, loaded through tvdb serie xml, IMDBID: '%s'" % imdbid)
      
        ### TVDB - Build 'tvdb_table' ###
        for episode in tvdbanime.xpath('Episode'):  # Combined_episodenumber, Combined_season, DVD(_chapter, _discid, _episodenumber, _season), Director, EpImgFlag, EpisodeName, EpisodeNumber, FirstAired, GuestStars, IMDB_ID #seasonid, imdbd
          numbering = getElementText(episode, 'absolute_number') if defaulttvdbseason=="a" else "s" + getElementText(episode, 'SeasonNumber') + "e" + getElementText(episode, 'EpisodeNumber')
          tvdb_table [numbering] = { 'EpisodeName': getElementText(episode, 'EpisodeName'), 'FirstAired':  getElementText(episode, 'FirstAired' ),
                                     'filename':    getElementText(episode, 'filename'   ), 'Overview':    getElementText(episode, 'Overview'   ), 
                                     'Rating':      getElementText(episode, 'Rating'     ) if '.' in getElementText(episode, 'Rating') else None }              
          if getElementText(episode, 'Overview'):  summary_present.append(numbering)
          else:                                    summary_missing.append(numbering)
      else:
        Log.Debug("'anime-list tvdbid missing.htm' log added as tvdb serie deleted: '%s', modify in custom mapping file to circumvent but please submit feedback to ScumLee's mapping file using html log link" % url)
        error_log['anime-list tvdbid missing'].append(TVDB_HTTP_API_URL % tvdbid + " - xml not downloadable so serie deleted from thetvdb")
      Log.Debug("Update() - TVDB - tvdb_table: "               + str(sorted(summary_present)) )
      Log.Debug("Update() - TVDB - Episodes without Summary: " + str(sorted(summary_missing)) )

      ### TVDB - Fanart, Poster and Banner ###
      if Prefs['GetTvdbPosters'] or Prefs['GetTvdbFanart' ] or Prefs['GetTvdbBanners']:
        tvdbposternumber = self.getImagesFromTVDB(metadata, media, tvdbid, movie, poster_id, force)
        if tvdbposternumber == 0:
          error_log['TVDB posters missing'].append(WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid))
          Log.Debug("Update() - TVDB - No poster, check logs in ../../Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB posters missing.htm to update Metadata Source")
  
    ### Movie posters including imdb from TVDB - Load serie XML ###
    if imdbid.isalnum():
      self.getImagesFromTMDB                      (metadata, imdbid, 97)  #The Movie Database is least prefered by the mapping file, only when imdbid missing
      self.getImagesFromOMDB                      (metadata, imdbid, 98)  #return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
    elif tmdbid.isdigit():  self.getImagesFromTMDB(metadata, tmdbid, 97)  #The Movie Database is least prefered by the mapping file, only when imdbid missing
 
    ### TVDB mode when a season 2 or more exist ############################################################################################################
    if not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1 or metadata.id.startswith("tvdb-")):
      Log.Debug("using TVDB numbering mode (seasons)" )
      if tvdbtitle:          metadata.title                   = tvdbtitle
      if tvdbRating:         metadata.rating                  = tvdbRating
      if tvdbOverview:       metadata.summary                 = tvdbOverview
      if tvdbNetwork:        metadata.studio                  = tvdbNetwork
      if tvdbContentRating:  metadata.content_rating          = tvdbContentRating 
      if tvdbFirstAired:     metadata.originally_available_at = Datetime.ParseDate( tvdbFirstAired ).date()
      if tvdbGenre:
        for genre in tvdbGenre: metadata.genres.add(genre)
        Log.Debug("Update() - TVDB - tvdbGenre: '%s'" % str(tvdbgenre))
      list_eps = ""
      for media_season in media.seasons:
        metadata.seasons[media_season].summary, metadata.seasons[media_season].title, metadata.seasons[media_season].show,metadata.seasons[media_season].source_title = "#" + tvdbOverview, "#" + tvdbtitle, "#" + tvdbtitle, "#" + tvdbNetwork
        for media_episode in media.seasons[media_season].episodes:
          ep, episode_count = "s%se%s" % (media_season, media_episode), 0
          if ep in tvdb_table:
            if 'Overview'    in tvdb_table[ep] and tvdb_table[ep]['Overview']: 
              try:     metadata.seasons[media_season].episodes[media_episode].summary = tvdb_table [ep] ['Overview']
              except:  Log.Debug("Error adding summary - ep: '%s', media_season: '%s', media_episode: '%s', summary:'%s'" % (ep, media_season, media_episode, tvdb_table [ep] ['Overview']))                  
            if 'EpisodeName' in tvdb_table[ep] and tvdb_table [ep] ['EpisodeName']: metadata.seasons[media_season].episodes[media_episode].title   = tvdb_table [ep] ['EpisodeName']
            if 'Rating'      in tvdb_table[ep] and tvdb_table [ep] ['Rating']:
              try:     metadata.seasons[media_season].episodes[media_episode].rating  = float(tvdb_table [ep] ['Rating'])
              except:  Log.Debug("float issue: '%s'" % tvdb_table [ep] ['Rating']) #ValueError
            if 'FirstAired'  in tvdb_table[ep] and tvdb_table [ep] ['FirstAired']:
              match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", tvdb_table [ep] ['FirstAired'])
              if match:
                try:   metadata.seasons[media_season].episodes[media_episode].originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
                except ValueError, e: Log.Debug("update - TVDB parseAirDate - Date out of range: " + str(e))
          for media_item in media.seasons[media_season].episodes[media_episode].items:
            for item_part in media_item.parts:  Log("File: '%s'" % item_part.file)
          episode_count, list_eps = episode_count + 1, list_eps + ep + ", "
        metadata.seasons[media_season].episode_count = episode_count #An integer specifying the number of episodes in the season.
      if list_eps !="":  Log.Debug("List_eps: " + list_eps)    
      Log.Debug("TVDB table: '%s'" % str(tvdb_table))   
      
    elif metadata.id.startswith("anidb-"): 
      ### AniDB Serie XML ##################################################################################################################################
      Log.Debug("Update() - AniDB mode - AniDB Serie XML: " + ANIDB_HTTP_API_URL + metadata.id[len("anidb-"):] + ", " + "AniDB/"+metadata.id[len("anidb-"):]+".xml" )
      anime = None         #return #if banned return ?
      try:     anime = self.xmlElementFromFile ( ANIDB_HTTP_API_URL + metadata.id[len("anidb-"):], "AniDB/"+metadata.id[len("anidb-"):]+".xml", True, CACHE_1HOUR * 24).xpath('/anime')[0]          # Put AniDB serie xml (cached if able) into 'anime'
      except: Log.Error("Update() - AniDB Serie XML: Exception raised, probably no return in xmlElementFromFile")
      if anime:
        
        ### AniDB Title ###
        try:     title, orig = self.getAniDBTitle(anime.xpath('/anime/titles/title'), SERIE_LANGUAGE_PRIORITY)
        except:  Log.Debug("Update() - AniDB Title: Exception raised" )
        else:  # title, orig = title.encode("utf-8").replace("`", "'"), orig.encode("utf-8").replace("`", "'")
          if title == str(metadata.title):  Log.Debug("Update() - AniDB title: '%s', original title: '%s', metadata.title '%s'*" % (title, orig, metadata.title))
          elif title != "": #If title different but not empty [Failsafe]
            Log.Debug("Update() - AniDB title: '%s', original title: '%s', metadata.title '%s'" % (title, orig, metadata.title))
            metadata.title = title
            if movie and orig != "" and orig != metadata.original_title: metadata.original_title = orig # If it's a movie, Update original title in metadata http://forums.plexapp.com/index.php/topic/25584-setting-metadata-original-title-and-sort-title-still-not-possible/
            
        ### AniDB Start Date ###
        if getElementText(anime, 'startdate') == "":                                  Log.Debug("Update() - AniDB Start Date: None")
        elif metadata.originally_available_at == getElementText(anime, 'startdate'):  Log.Debug("Update() - AniDB Start Date: '%s'*" % str(metadata.originally_available_at))
        else:
          metadata.originally_available_at = Datetime.ParseDate( getElementText(anime, 'startdate') ).date()
          if movie: metadata.year          = metadata.originally_available_at.year
          Log.Debug("Update() - AniDB Start Date: '%s'" % str(metadata.originally_available_at))
        
        ### AniDB Ratings ###
        misc = getElementText(anime, 'ratings/permanent')
        if misc=="":                                         Log.Debug("update() - AniDB Ratings:    'None'")   
        elif '.' in misc and float(misc) == metadata.rating: Log.Debug("update() - AniDB Ratings:    '%s'*" % misc)
        else:                                                Log.Debug("update() - AniDB Ratings:    '%s'"  % misc);  metadata.rating = float( misc )
        
        ### AniDB Genres ###
        genres = {}
        for category in anime.xpath('categories/category'):
          if getElementText(category, 'name') in GENRE_NAMES and category.get('weight') >= Prefs['MinimumWeight']:                 genres [ getElementText(category, 'name') ] = int(category.get('weight')) # Remove genre whitelist
          if getElementText(category, 'name') in RESTRICTED_GENRE_NAMES and metadata.content_rating != RESTRICTED_CONTENT_RATING:  metadata.content_rating = RESTRICTED_CONTENT_RATING
        sortedGenres = sorted(genres.items(), key=lambda x: x[1],  reverse=True)
        log_string, genres = "AniDB Genres (Weight): ", []
        for genre in sortedGenres: genres.append(genre[0].encode("utf-8") )
        if sorted(metadata.genres)==sorted(genres): Log.Debug(log_string+str(sortedGenres)+"*") 
        else:
          Log.Debug("Update() - genres: " + str(sortedGenres) + " " + str(genres))
          metadata.genres.clear()
          for genre in sortedGenres:
            metadata.genres.add(genre[0])
            log_string += "%s (%s) " % (genre[0], str(genre[1]))
          Log.Debug(log_string)
        
        ### AniDB Collections ###
        self.anidbCollectionMapping(metadata, anime, anidbid_table)
        
        ### AniDB Creator data -  Aside from the animation studio, none of this maps to Series entries, so save it for episodes ###
        log_string, metadata.studio, plex_role = "AniDB Creator data: ", "", {'directors': [], 'producers': [], 'writers': []}
        roles = { "Animation Work": ["studio",  'studio' , "studio"], "Direction": ["directors", 'directors', "director"], "Series Composition": ["producers", 'producers', "producer"],
                  "Original Work" : ["writers", 'writers', "writer"], "Script"   : ["writers",   'writers'  , "writer"  ], "Screenplay"        : ["writers",   'writers'  , "writer"  ] }
        if movie: ###github for role in roles [1:3]: roles[role][0].clear()
          metadata.writers.clear #   a = sum(getattr(t, name, 0) for name in "xyz")
          metadata.producers.clear()
          metadata.directors.clear()          #Log.Debug("before for") #test = {"directors", 'producers', 'writers'} #for role in test:  metadata.test[role].clear() #for role in ["directors", 'producers', 'writers']:  metadata.role.clear() #role2[role].clear() #TypeError: unhashable type
        log_string = "AniDB Creator data: "
        for creator in anime.xpath('creators/name'):
          for role in roles: 
            if role in creator.get('type'):
              if roles[ role ][1]=='studio':  metadata.studio = creator.text
              elif     movie:
                if   roles[ role ][1]=='directors':  metadata.directors.add(creator.text)
                elif roles[ role ][1]=='writers':    metadata.writers.add(creator.text)
              else:                                  plex_role [ roles[role][1] ].append(creator.text) #not movie #for episodes
              log_string += "%s is a %s, " % (creator.text, roles[role][2] )
        if metadata.studio == "" and mapping_studio != "":  metadata.studio = mapping_studio
        if metadata.studio != "" and mapping_studio != "":  error_log['anime-list studio logos'].append("Aid: %s AniDB have studio '%s' and XML have '%s'"         % (metadata.id[len("anidb-"):].zfill(5), metadata.studio, mapping_studio) + WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(anime, encoding='utf8'))), "Submit bug report (need GIT account)"))
        if metadata.studio == "" and mapping_studio == "":  error_log['anime-list studio logos'].append("Aid: %s AniDB and anime-list are both missing the studio" % (metadata.id[len("anidb-"):].zfill(5)) )
        Log.Debug(log_string)

        ### AniDB Serie/Movie description ###
        try:     description = re.sub(r'http://anidb\.net/[a-z]{2}[0-9]+ \[(.+?)\]', r'\1', getElementText(anime, 'description')).replace("`", "'") # Remove wiki-style links to staff, characters etc
        except:  description = ""; Log.Debug("Exception ")
        if description == "":  error_log['AniDB summaries missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id[len("anidb-"):], metadata.id[len("anidb-"):]) + " " + metadata.title)
        if metadata.summary != description and description:  metadata.summary = description.replace("`", "'")
        
        ### AniDB Posters ###
        Log.Debug("Update() - AniDB Poster, url: '%s'" % (ANIDB_PIC_BASE_URL + getElementText(anime, 'picture')))
        if getElementText(anime, 'picture') == "": error_log['AniDB posters missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id[len("anidb-"):], metadata.id[len("anidb-"):]) + "" + metadata.title)
        elif Prefs['GetAnidbPoster']:  self.metadata_download (metadata.posters, ANIDB_PIC_BASE_URL + getElementText(anime, 'picture'), 99, "AniDB/%s" % getElementText(anime, 'picture')) 

        if not movie: ### TV Serie specific #################################################################################################################
          numEpisodes, totalDuration, mapped_eps, missing_eps, ending_table, op_nb = 0, 0, [], [], {}, 0 
          specials = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
          
          for episode in anime.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################
            ep_title, main   = self.getAniDBTitle (episode.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
            epNum,    eid    = episode.xpath('epno')[0], episode.get('id')
            epNumType        = epNum.get('type')
            season, epNumVal = "1" if epNumType == "1" else "0", epNum.text if epNumType == "1" else str( specials[ epNum.text[0] ][0] + int(epNum.text[1:]))
            if epNumType=="3":
              if ep_title.startswith("Ending"):
                if op_nb==0: op_nb = int(epNum.text[1:])-1 #first type 3 is first ending so epNum.text[1:] -1 = nb openings
                epNumVal = str( int(epNumVal) +50-op_nb)   #shifted to 150 for 1st ending.  
              Log.Debug("Update() - AniDB specials title - Season: '%s', epNum.text: '%s', epNumVal: '%s', ep_title: '%s'" % (season, epNum.text, epNumVal, ep_title) )
             
            if not (season in media.seasons and epNumVal in media.seasons[season].episodes):  #Log.Debug("update - Season: '%s', Episode: '%s' => '%s' not on disk" % (season, epNum.text, epNumVal) )
              if epNumType == "1": missing_eps.append(" s" + season + "e" + epNumVal )
              continue
            episodeObj = metadata.seasons[season].episodes[epNumVal]
            
            ### AniDB Get the correct episode title ###
            if episodeObj.title == ep_title:  Log.Debug("Update() - AniDB episode title: '%s'*" % ep_title) 
            else:                             Log.Debug("Update() - AniDB episode title: '%s'"  % ep_title); episodeObj.title = ep_title
            
            ### AniDBN turn the YYYY-MM-DD airdate in each episode into a Date ###
            airdate, originally_available_at = getElementText(episode, 'airdate'), None
            if airdate:
              match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", airdate)
              if match:
                try:                   originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
                except ValueError, e:  Log.Debug("Update() - AniDB parseAirDate - Date out of range: " + str(e))
            if originally_available_at == episodeObj.originally_available_at: Log.Debug("Update() - AniDB AirDate '%s'*" % airdate)
            else:                                                             Log.Debug("Update() - AniDB AirDate '%s'"  % airdate);  episodeObj.originally_available_at = originally_available_at
            
            ### AniDB Duration ###
            if getElementText(episode, 'length'):
              duration = int(getElementText(episode, 'length')) * 1000 * 60  # Plex save duration in millisecs, AniDB stores it in minutes
              if episodeObj.duration == duration:  Log.Debug("Update() - AniDB duration: '%d'*" % duration)
              else:                                Log.Debug("Update() - AniDB duration: '%d'"  % duration);  episodeObj.duration = duration;               
              if season == "1": numEpisodes, totalDuration = numEpisodes + 1, totalDuration + episodeObj.duration
            
            ### AniDB Writers, Producers, Directors ###  #Log.Debug("### AniDB Writers, Producers, Directors ### ")
            for role in plex_role:
              for person in plex_role[role]:
                if role=="writers":    episodeObj.writers.add  (person)
                if role=="producers":  episodeObj.producers.add(person)
                if role=="directors":  episodeObj.directors.add(person)
            
            ### Rating ###
            rating = getElementText(episode, 'rating') #if rating =="":  Log.Debug(metadata.id + " Episode rating: ''") #elif rating == episodeObj.rating:  Log.Debug(metadata.id + " update - Episode rating: '%s'*" % rating )
            if not rating =="" and re.match("^\d+?\.\d+?$", rating):  episodeObj.rating = float(rating) #try: float(element) except ValueError:     print "Not a float"
            
            ### TVDB mapping episode summary ###
            if tvdbid.isdigit():
              anidb_ep, tvdb_ep, summary= 's' + season + 'e' + epNumVal, "", "No summary in TheTVDB.com" #epNum
              if anidb_ep in mappingList  and mappingList[anidb_ep] in tvdb_table:  tvdb_ep = mappingList [ anidb_ep ]
              elif defaulttvdbseason=="a" and              epNumVal in tvdb_table:  tvdb_ep = epNumVal
              elif season=="0":                                                     tvdb_ep = "s"+season+"e"+epNumVal
              else:                                                                 tvdb_ep = "s"+defaulttvdbseason+"e"+epNumVal
              summary = "TVDB summary missing" if tvdb_ep=="" or tvdb_ep not in tvdb_table else tvdb_table [tvdb_ep] ['Overview'].replace("`", "'")
              mapped_eps.append( anidb_ep + ">" + tvdb_ep )
              if tvdb_ep in tvdb_table and 'filename' in tvdb_table[tvdb_ep] and tvdb_table[tvdb_ep]['filename']!="":  self.metadata_download (episodeObj.thumbs, TVDB_IMAGES_URL + tvdb_table[tvdb_ep]['filename'], 1, "TVDB/episodes/"+ os.path.basename(tvdb_table[tvdb_ep]['filename']))            
              Log.Debug("TVDB mapping episode summary - anidb_ep: '%s', tvdb_ep: '%s', season: '%s', epNumVal: '%s', defaulttvdbseason: '%s', title: '%s', summary: '%s'" %(anidb_ep, tvdb_ep, season, epNumVal, defaulttvdbseason, ep_title, tvdb_table [tvdb_ep] ['Overview'][0:50].strip() if tvdb_ep in tvdb_table else "") )
              episodeObj.summary = summary.replace("`", "'")            
          ## End of "for episode in anime.xpath('episodes/episode'):" ### Episode Specific ###########################################################################################

          ### AniDB Missing Episodes ###
          if len(missing_eps)>0:  error_log['Missing episodes'].append("anidbid: %s, Title: '%s', Missing Episodes: %s" % (metadata.id.split("-")[1].zfill(5), title, missing_eps))
          convert      = lambda text: int(text) if text.isdigit() else text
          alphanum_key = lambda key:  [ convert(c) for c in re.split('([0-9]+)', key) ]

          ### AniDB Final post-episode titles cleanup ###
          Log.Debug("Update() - DURATION: %s, numEpisodes: %s" %(str(totalDuration), str(numEpisodes)) )
          if numEpisodes: metadata.duration = int(totalDuration) / int(numEpisodes) #if movie getting scrapped as episode number by scanner...
        ### End of if anime is not None: ###

    ### HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems ###
    for log in error_log:
      if error_log[log] != []:
        if Data.Exists(log+".htm"):  string = Data.Load(log+".htm")
        else:
          string=""
          if log == 'TVDB posters missing': string = WEB_LINK % ("http://thetvdb.com/wiki/index.php/Posters",              "Restrictions") + "<br />\n"
          if log == 'Plex themes missing':  string = WEB_LINK % ("https://plexapp.zendesk.com/hc/en-us/articles/201572843","Restrictions") + "<br />\n"
        for entry in error_log[log]:
          if entry not in string:  Data.Save(log+".htm", string + entry + "<br />\r\n")
    Log.Debug('--- Update end -------------------------------------------------------------------------------------------------')
        
  ### Get the tvdbId from the AnimeId #######################################################################################################################
  def anidbTvdbMapping(self, metadata, anidb_id, error_log):
    global AniDB_TVDB_mapping_tree    #if not AniDB_TVDB_mapping_tree: AniDB_TVDB_mapping_tree = self.xmlElementFromFile(ANIDB_TVDB_MAPPING, ANIDB_TVDB_MAPPING, False, CACHE_1HOUR * 24) # Load XML file
    poster_id_array, mappingList = {}, {}  #AniDB_TVDB_mapping_misc = xmlElementFromFile(ANIDB_TVDB_MAPPING, os.path.basename(ANIDB_TVDB_MAPPING), False, CACHE_1HOUR * 24)
    for anime in AniDB_TVDB_mapping_tree.iter('anime') if AniDB_TVDB_mapping_tree else []:
      anidbid, tvdbid, tmdbid, imdbid, defaulttvdbseason = anime.get("anidbid"), anime.get('tvdbid'), anime.get('tmdbid'), anime.get('imdbid'), anime.get('defaulttvdbseason')
      if tvdbid.isdigit():  poster_id_array [tvdbid] = poster_id_array [tvdbid] + 1 if tvdbid in poster_id_array else 0  # Count posters to have a unique poster per anidbid
      if anidbid == anidb_id: #manage all formats latter
        name = anime.xpath("name")[0].text 
        if tvdbid.isdigit():
          try: ### mapping list ###
            for season in anime.iter('mapping'):
              for string in filter(None, season.text.split(';')):  mappingList [ 's' + season.get("anidbseason") + 'e' + string.split('-')[0] ] = 's' + season.get("tvdbseason") + 'e' + string.split('-')[1]
          except: Log.Debug("anidbTvdbMapping() - mappingList creation exception")
        elif tvdbid in ("", "unknown"):  error_log ['anime-list tvdbid missing'].append("anidbid: %s title: '%s' has no matching tvdbid ('%s') in mapping file" % (anidb_id.zfill(5), name, tvdbid) + WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; tvdbid:" % (anidb_id, name), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
        try:    mapping_studio  = anime.xpath("supplemental-info/studio")[0].text
        except: mapping_studio  = ""
        Log.Debug("anidbTvdbMapping() - anidb: '%s', tvbdid: '%s', tmdbid: '%s', imbdid: '%s', studio: '%s', defaulttvdbseason: '%s', name: '%s'" % (anidbid, tvdbid, tmdbid, imdbid, mapping_studio, defaulttvdbseason, name) )
        anidbid_table = []
        for anime2 in AniDB_collection_tree.iter("anime"):
          if tvdbid == anime2.get('tvdbid'):  anidbid_table.append( anime2.get("anidbid") ) #collection gathering
        return tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio, anidbid_table, poster_id_array [tvdbid] if tvdbid in poster_id_array else {}
    else:
      Log.Debug("anidbTvdbMapping() - anidbid '%s' not found in file" % anidb_id)
      error_log['anime-list anidbid missing'].append("anidbid: " + anidb_id.zfill(5))
      return "", "", "", "", [], "", [], "0"
    
  ### AniDB collection mapping - complement AniDB movie collection file with related anime AND series sharing the same tvdbid ########################
  def anidbCollectionMapping(self, metadata, anime, anidbid_table=[]):
    global AniDB_collection_tree, SERIE_LANGUAGE_PRIORITY
    related_anime_list = []
    for relatedAnime in anime.xpath('/anime/relatedanime/anime'):  related_anime_list.append(relatedAnime.get('id'));
    for element in AniDB_collection_tree.iter("anime"):
      if element.get('anidbid') in related_anime_list + anidbid_table + [metadata.id.split('-')[1]] :
        set         = element.getparent()
        title, main = self.getAniDBTitle(set.xpath('titles')[0], SERIE_LANGUAGE_PRIORITY)
        metadata.collections.add(title) #metadata.collections.clear()
        Log.Debug("anidbCollectionMapping() - anidbid '%s' is part of movie collection: %s', related_anime_list: '%s', " % (metadata.id.split('-')[1], title, str(related_anime_list)))
        return
    Log.Debug("anidbCollectionMapping() - anidbid is not part of any collection, related_anime_list: '%s'" % str(related_anime_list)) 

  ### [banners.xml] Attempt to get the TVDB's image data ###############################################################################################################
  def getImagesFromTVDB(self, metadata, media, tvdbid, movie, poster_id=1, force=False):
    posternum, num, poster_total = 0, 0, 0
    try:     bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % tvdbid, cacheTime=CACHE_1HOUR * 24) # don't bother with the full zip, all we need is the banners
    except:  Log.Debug("getImagesFromTVDB() - Loading picture XML failed: " + TVDB_BANNERS_URL % tvdbid);  return
    else:    Log.Debug("getImagesFromTVDB() - Loaded picture XML: '%s'" % (TVDB_BANNERS_URL % tvdbid))
    for banner in bannersXml.xpath('Banner'): 
      if banner.xpath('BannerType')[0].text=="poster":  poster_total +=1
    for banner in bannersXml.xpath('Banner'): #rating   = banner.xpath('Rating'     )[0].text if banner.xpath('Rating') else ""  #Language = banner.xpath('Language'   )[0].text #if Language not in ['en', 'jp']: continue  #id       = banner.xpath('id'         )[0].text
      num, bannerType, bannerType2, bannerPath  = num+1, banner.xpath('BannerType' )[0].text, banner.xpath('BannerType2')[0].text, banner.xpath('BannerPath' )[0].text
      if bannerType == 'poster':  posternum += 1
      season = banner.xpath('Season')[0].text if banner.xpath('Season') else ""
      if movie and not bannerType in ('fanart', 'poster') or season and season not in media.seasons:  continue
      if Prefs['GetTvdbPosters'] and                  ( bannerType == 'poster' or bannerType2 == 'season' and not movie ) or \
         Prefs['GetTvdbFanart' ] and                    bannerType == 'fanart' or \
         Prefs['GetTvdbBanners'] and not movie and    ( bannerType == 'series' or bannerType2 == 'seasonwide'):
        metatype = (metadata.art                     if bannerType == 'fanart' else \
                    metadata.posters                 if bannerType == 'poster' else \
                    metadata.banners                 if bannerType == 'series' or bannerType2=='seasonwide' else \
                    metadata.seasons[season].posters if bannerType == 'season' and bannerType2=='season' else None)
        if metatype == metadata.posters:  rank = 1 if poster_id and poster_total and posternum == divmod(poster_id, poster_total)[1] + 1 else posternum+1
        else:                             rank = num
        bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
        self.metadata_download (metatype, TVDB_IMAGES_URL + bannerPath, rank, "TVDB/"+bannerPath, bannerThumbUrl)
    return posternum

  ### Download TMDB poster and background through IMDB or TMDB ID ##########################################################################################
  def  getImagesFromTMDB(self, metadata, id, num=90):
    config_dict, images = self.get_json(TMDB_CONFIG_URL, cache_time=CACHE_1WEEK * 2), {}
    if id.startswith("tt"):
      Log.Debug("getImagesFromTMDB() - using IMDBID url: " + TMDB_SEARCH_URL_BY_IMDBID % id)
      tmdb_json = self.get_json(TMDB_SEARCH_URL_BY_IMDBID %id, cache_time=CACHE_1WEEK * 2) # Log.Debug("getImagesFromTMDB - by IMDBID - tmdb_json: '%s'" % str(tmdb_json))
      for type in ['movie_results', 'tv_results']:
        if tmdb_json is not None and type in tmdb_json:
          for index, poster in enumerate(tmdb_json[type]):
            if 'poster_path'   in tmdb_json[type][index] and tmdb_json[type][index]['poster_path'  ] not in (None, "", "null"):  images[ tmdb_json[type][index]['poster_path'  ]] = metadata.posters
            if 'backdrop_path' in tmdb_json[type][index] and tmdb_json[type][index]['backdrop_path'] not in (None, "", "null"):  images[ tmdb_json[type][index]['backdrop_path']] = metadata.art
      rank=90
    else:
      Log.Debug("getImagesFromTMDB() - using TMDBID  url: " + TMDB_IMAGES_URL % id)
      tmdb_json = self.get_json(url=TMDB_IMAGES_URL % id, cache_time=CACHE_1WEEK * 2)
      if tmdb_json and 'posters'    in tmdb_json and len(tmdb_json['posters'  ]):
        for index, poster in enumerate(tmdb_json['posters']):
          if 'file_path' in tmdb_json['posters'][index] and tmdb_json['posters'][index]['file_path'] not in (None, "", "null"):  images[ tmdb_json['posters'  ][index]['file_path']] = metadata.posters
      if tmdb_json is not None and 'backdrops' in tmdb_json and len(tmdb_json['backdrops']):
        for index, poster in enumerate(tmdb_json['backdrops']):
          if 'file_path' in tmdb_json['backdrops'][index] and tmdb_json['backdrops'][index]['file_path'] not in (None, "", "null"):  images[ tmdb_json['backdrops'][index]['file_path']] = metadata.art
      rank=95
    if len(images):
      for filename in images.keys():
        if filename:
          image_url, thumb_url = config_dict['images']['base_url'] + 'original' + filename, config_dict['images']['base_url'] + 'w300'     + filename
          self.metadata_download (images[filename], image_url, rank, "TMDB/%s%s.jpg" % (id, "" if images[filename]==metadata.posters else "-art"), thumb_url) 
        
  ### Fetch the IMDB poster using OMDB HTTP API ###########################################################################################################
  def getImagesFromOMDB(self, metadata, imdbid, num=99):
    Log.Debug("getImagesFromOMDB() - imdbid: '%s', url: '%s', filename: '%s'" % (imdbid, OMDB_HTTP_API_URL + imdbid, "OMDB/%s.jpg" % imdbid))
    try:    OMDB = self.get_json(OMDB_HTTP_API_URL + imdbid, cache_time=CACHE_1WEEK * 56)
    except: Log.Debug("getImagesFromOMDB() - Exception - imdbid: '%s', url: '%s', filename: '%s'" % (imdbid, OMDB_HTTP_API_URL + imdbid, "OMDB/%s.jpg" % imdbid))
    else:
      if OMDB and 'Poster' in OMDB and OMDB['Poster'] not in ("N/A", "", None):  self.metadata_download (metadata.posters, OMDB['Poster'], num, "OMDB/%s.jpg" % imdbid)
      else:                                                                      Log.Debug("getImagesFromOMDB() - No poster to download - " + OMDB_HTTP_API_URL + imdbid)
    
  #########################################################################################################################################################
  def metadata_download (self, metatype, url, num=99, filename="", url_thumbnail=None):  #if url in metatype:#  Log.Debug("metadata_download - url: '%s', num: '%s', filename: '%s'*" % (url, str(num), filename)) # Log.Debug(str(metatype))   #  return
    if url not in metatype:
      file = None
      if filename and Data.Exists(filename):  ### if stored locally load it
        try:     file = Data.Load(filename)
        except:  Log.Debug("metadata_download() - media_download - could not load file '%s' present in cache" % filename)
      if file == None: ### if not loaded locally download it
        try:     file = HTTP.Request(url_thumbnail if url_thumbnail else url, cacheTime=None).content
        except:  Log.Debug("metadata_download() - metadata_download - error downloading"); return
        else:  ### if downloaded, try saving in cache but folders need to exist
          if filename and not filename.endswith("/"):
            try:     Data.Save(filename, file)
            except:  Log.Debug("metadata_download() - metadata_download - could not write filename '%s' in Plugin Data Folder" % (filename)); return
      if file:
        try:    metatype[ url ] = Proxy.Preview(file, sort_order=num) if url_thumbnail else Proxy.Media(file, sort_order=num) # or metatype[ url ] != proxy_item # proxy_item = 
        except: Log.Debug("metadata_download() - metadata_download - issue adding picture to plex - url downloaded: '%s', filename: '%s'" % (url_thumbnail if url_thumbnail else url, filename))  #metatype.validate_keys( url_thumbnail if url_thumbnail else url ) # remove many posters, to avoid
        else:   Log.Debug("metadata_download() - url: '%s', num: '%d', filename: '%s'" % (url, num, filename))
    else:  Log.Debug("metadata_download() - url: '%s', num: '%d', filename: '%s'*" % (url, num, filename))

  ### get_json file, TMDB API supports only JSON now ######################################################################################################
  def get_json(self, url, cache_time=CACHE_1MONTH):
    try:     return JSON.ObjectFromURL(url, sleep=2.0, cacheTime=cache_time)
    except:  Log("get_json() - Error fetching JSON url: '%s'" % url )

  ### Pull down the XML from web and cache it or from local cache for a given anime ID ####################################################################
  def xmlElementFromFile (self, url, filename="", delay=True, cache=None):
    Log.Debug("xmlElementFromFile() - url: '%s', filename: '%s'" % (url, filename))
    if delay:  time.sleep(4) #2s between anidb requests but 2 threads                                                                                                   # Ban after 160 series if too short, ban also if same serie xml downloaded repetitively, delay for AniDB only for now     e #try:    a = urllib.urlopen(url)#if a is not None and a.getcode()==200:
    try:     result = str(HTTP.Request(url, headers={'Accept-Encoding':'gzip', 'content-type':'charset=utf8'}, timeout=20, cacheTime=cache))  # Loaded with Plex cache, str prevent AttributeError: 'HTTPRequest' object has no attribute 'find'
    except:  result = None #Log.Debug("xmlElementFromFile() - XML issue loading url: '%s'" % url )                                                      # issue loading, but not AniDB banned as it returns "<error>Banned</error>"
    
    if result and len(result)>1024 and filename:  # if loaded OK save else load from last saved file
      try:     Data.Save(filename, result)
      except:  Log.Debug("xmlElementFromFile() - url: '%s', filename: '%s' saving failed, probably missing folder" % (url, filename))
    elif filename and Data.Exists(filename):  # Loading locally if backup exists
      Log.Debug("xmlElementFromFile() - Loading locally since banned or empty file (result page <1024 bytes)")
      try:     result = Data.Load(filename)
      except:  Log.Debug("xmlElementFromFile() - Loading locally failed but data present - url: '%s', filename: '%s'" % (url, filename)); return
      
    if url==ANIDB_TVDB_MAPPING and Data.Exists(ANIDB_TVDB_MAPPING_CUSTOM):  # Special case: if importing anidb tvdb mapping, load custom mapping entries first
      Log.Debug("xmlElementFromFile() - Loading local custom mapping - url: '%s'" % ANIDB_TVDB_MAPPING_CUSTOM)
      result_custom = Data.Load(ANIDB_TVDB_MAPPING_CUSTOM)
      result        = result_custom[:result_custom.rfind("</anime-list>")-1] + result[result.find("<anime-list>")+len("<anime-list>")+1:] #cut both fiels together removing ending and starting tags to do so
    
    if result:
      element = XML.ElementFromString(result)
      if str(element).startswith("<Element error at "):  Log.Debug("xmlElementFromFile() - Not an XML file, AniDB banned possibly, result: '%s'" % result)
      else:                                              return element
    
  ### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
  def cleanse_title(self, title):
    try:    title=title.encode('utf-8')
    except: pass
    title = " ".join(self.splitByChars(title))
    return  title.replace("`", "'").lower() # None in the translate call was giving an error of 'TypeError: expected a character buffer object'. So, we construct a blank translation table instead.

  ### Split a string per list of chars #################################################################################################################################
  def splitByChars(self, string, separators=SPLIT_CHARS): #AttributeError: 'generator' object has no attribute 'split'  #return (string.replace(" ", i) for i in separators if i in string).split()
    for i in separators:
      if i in string:  string = string.replace(i, " ")
    return filter(None, string.split())
    
  ### Extract the series/movie/Episode title from AniDB ########################################################################################################################
  def getAniDBTitle(self, titles, languages):
    if not 'main' in languages:  languages.append('main')                                                                                      # Add main to the selection if not present
    langTitles = ["" for index in range(len(languages)+1)]                                                                                     # languages: title order including main title, then choosen title
    for title in titles:                                                                                                                       # Loop through all languages listed in the anime XML
      type, lang = title.get('type'), title.get('{http://www.w3.org/XML/1998/namespace}lang')                                                  # If Serie: Main, official, Synonym, short. If episode: None # Get the language, 'xml:lang' attribute need hack to read properly
      if type == 'main' or type == None and langTitles[ languages.index('main') ] == "":  langTitles [ languages.index('main') ] = title.text  # type==none is for mapping episode language
      if lang in languages and type in ['main', 'official', 'syn', 'synonym', None]:      langTitles [ languages.index( lang ) ] = title.text  # 'Applede' Korean synonym fix
    for index in range( len(languages) ):                                                                                                      # Loop through title result array
      if langTitles[index]:  langTitles[len(languages)] = langTitles[index];  break                                               # If title present we're done
    else: langTitles[len(languages)] = langTitles[languages.index('main')]                                     # Fallback on main title
    return langTitles[len(languages)].replace("`", "'").encode("utf-8"), langTitles[languages.index('main')].replace("`", "'").encode("utf-8") #
    
### Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows, HamaCommonAgent):
  name, primary_provider, fallback_agent, contributes_to, languages, accepts_from = ('HamaTV', True, False, None, [Locale.Language.English,], ['com.plexapp.agents.localmedia'] ) #, 'com.plexapp.agents.opensubtitles'
  def search(self, results,  media, lang, manual): self.Search(results,  media, lang, manual, False )
  def update(self, metadata, media, lang, force ): self.Update(metadata, media, lang, force,  False )

class HamaMovieAgent(Agent.Movies, HamaCommonAgent):
  name, primary_provider, fallback_agent, contributes_to, languages, accepts_from = ('HamaMovies', True, False, None, [Locale.Language.English,], ['com.plexapp.agents.localmedia'] ) #, 'com.plexapp.agents.opensubtitles'
  def search(self, results,  media, lang, manual): self.Search(results,  media, lang, manual, True )
  def update(self, metadata, media, lang, force ): self.Update(metadata, media, lang, force,  True )
