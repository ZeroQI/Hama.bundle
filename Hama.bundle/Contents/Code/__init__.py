# -*- coding: utf-8 -*-
### HTTP Anidb Metadata Agent (HAMA) By ZeroQI, Forked from Atomicstrawberry after v0.4

import os, re, time, datetime, string, thread, threading, urllib # Functions used per module: os (read), re (sub, match), time (sleep), datetim (datetime).
### AniDB, TVDB, AniDB mod agent for XBMC XML's, and Plex URL and path variable definition ###########################################################################
ANIDB_TVDB_MAPPING           = 'anime-list-master.xml'                                                                        # ScudLee mapping file local
ANIDB_TVDB_MAPPING_URL       = 'http://rawgithub.com/ScudLee/anime-lists/master/anime-list-master.xml'                        # ScudLee mapping file url
ANIDB_TVDB_MAPPING_FEEDBACK  = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'                            # ScudLee mapping file git feedback url
ANIDB_COLLECTION_MAPPING     = 'anime-movieset-list.xml'                                                                      # ScudLee AniDB movies collections XML mapping file
ANIDB_COLLECTION_MAPPING_URL = 'http://rawgithub.com/ScudLee/anime-lists/master/anime-movieset-list.xml'                      # ScudLee collection mapping file
ANIDB_ANIME_TITLES           = 'anime-titles.xml'                                                                             # AniDB title database decompressed in Hama.bundle\Contents\Resources
ANIDB_ANIME_TITLES_URL       = 'http://anidb.net/api/anime-titles.xml.gz'                                                     # AniDB title database file contain all ids, all languages
ANIDB_HTTP_API_URL           = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='
ANIDB_PIC_BASE_URL           = 'http://img7.anidb.net/pics/anime/'                                                            # AniDB picture directory
ANIDB_SERIE_URL              = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s'                                       # AniDB link to the anime
ANIDB_SERIE_CACHE            = 'AniDB'                                                                                        # AniDB link to the anime

TVDB_API_KEY                 = 'A27AD9BE0DA63333'                                                                             # TVDB API key register URL: http://thetvdb.com/?tab=apiregister
TVDB_HTTP_API_URL            = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'                                               # TVDB Serie XML for episodes sumaries for now
TVDB_BANNERS_URL             = 'http://thetvdb.com/api/%s/series/%s/banners.xml'                                              # TVDB Serie pictures xml: fanarts, posters, banners
TVDB_SERIE_SEARCH            = 'http://thetvdb.com/api/GetSeries.php?seriesname='
TVDB_IMAGES_URL              = 'http://thetvdb.com/banners/'                                                                  # TVDB picture directory
TVDB_SERIE_URL               = 'http://thetvdb.com/?tab=series&id=%s'                                                         #
TVDB_SERIE_CACHE             = 'TVDB'                                                                                         #

TMDB_BASE_URL                = 'https://api.tmdb.org/3/'
TMDB_CONFIG_URL              = TMDB_BASE_URL + 'configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
TMDB_IMAGES_URL              = TMDB_BASE_URL + 'movie/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
TMDB_SEARCH_URL_BY_IMDBID    = TMDB_BASE_URL + 'find/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id'
TMDB_ARTWORK_ITEM_LIMIT      = 15
TMDB_SCORE_RATIO             = .3   # How much weight to give ratings vs. vote counts when picking best posters/backdrop. 0 means use only ratings.

OMDB_HTTP_API_URL            = "http://www.omdbapi.com/?i="
THEME_URL                    = 'http://tvthemes.plexapp.com/%s.mp3'                                                           # Plex TV Theme url

### List of AniDB category names useful as genre. 1st variable mark 18+ categories. The 2nd variable will actually cause a flag to appear in Plex ####################
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
  'Historical', '1920s', 'Bakumatsu - Meiji Period', 'Edo Period', 'Heian Period', 'Sengoku Period', 'Victorian Period', 'World War I', 'World War II', 'Alternative Present',

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

### These are words which cause extra noise due to being uninteresting for doing searches on ###########################################################################
FILTER_SEARCH_WORDS          = [                                                                                                      # Lowercase only
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', # En
  'princess', 'theater',                                                                                                              # En Continued
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime',                                                   # Jp
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses',                                                                                # Fr
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi'                                # Roman digits
]

### Global variables ###
networkLock, lastRequestTime, AniDB_title_tree, AniDB_collection_tree, AniDB_TVDB_mapping_tree = Thread.Lock(), None, None, None, None  #ValueError if in Start()
SERIE_LANGUAGE_PRIORITY   = [ Prefs['SerieLanguage1'].encode('utf-8'),   Prefs['SerieLanguage2'].encode('utf-8'), Prefs['SerieLanguage3'].encode('utf-8') ] #override default language
EPISODE_LANGUAGE_PRIORITY = [ Prefs['EpisodeLanguage1'].encode('utf-8'), Prefs['EpisodeLanguage2'].encode('utf-8') ] #override default language

### Language Priorities ###
SECONDS_BETWEEN_REQUESTS     = 2                                                    #Ban after 160 series if too short
SPLIT_CHARS                  = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations
FILTER_CHARS                 = "\\/:*?<>|~-; "
WEB_LINK                     = "<a href='%s' target='_blank'>%s</a>"

### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info('HAMA - ValidatePrefs initialised')
  result, msg = ('Success', 'HAMA - Provided preference values are ok')
  for key in ['GetTvdbFanart', 'GetTvdbPosters', 'GetTvdbBanners', 'GetAnidbPoster', 'MinimumWeight', 'SerieLanguage1', 'SerieLanguage2', 'SerieLanguage3', 'EpisodeLanguage1', 'EpisodeLanguage2']: #for key, value in enumerate(settings):
    try:    temp = Prefs[key]
    except: result, msg = ('Error', "Couldn't get values '%s', probably a missing/empty/outdated 'DefaultPrefs.json' so replace it" % key)
  if result=='Error':  Log.Error(msg)
  return MessageContainer(result, msg)
   
### test all values of list against another, only defined in Python 2.5+ ##################################################################################
def all(iterable):
  for element in iterable:
    if not element: return False
  return True

### Pre-Defined Start function #########################################################################################################################################
def Start():
  Log.Debug('### HTTP Anidb Metadata Agent (HAMA) Started ##############################################################################################################'+ANIDB_ANIME_TITLES)
  msgContainer = ValidatePrefs()
  Log.Debug("getMainTitle - LANGUAGE_PRIORITY: " + str(SERIE_LANGUAGE_PRIORITY))
  global AniDB_title_tree, AniDB_TVDB_mapping_tree, AniDB_collection_tree                                            # only this one to make search after start faster
  HTTP.CacheTime                   = CACHE_1HOUR * 24 * 7                                                            # Cache time for Plex XML and html pages
  AniDB_title_tree                 = HamaCommonAgent().xmlElementFromFile(ANIDB_ANIME_TITLES_URL,       ANIDB_ANIME_TITLES,       True,  CACHE_1HOUR * 24 * 7) # AniDB's:   anime-titles.xml
  AniDB_TVDB_mapping_tree          = HamaCommonAgent().xmlElementFromFile(ANIDB_TVDB_MAPPING_URL,       ANIDB_TVDB_MAPPING,       False, CACHE_1HOUR * 24 * 7) # ScudLee's: anime-list-master.xml
  AniDB_collection_tree            = HamaCommonAgent().xmlElementFromFile(ANIDB_COLLECTION_MAPPING_URL, ANIDB_COLLECTION_MAPPING, False, CACHE_1HOUR * 24 * 7) # ScudLee's: anime-movieset-list.xml
  Log.Debug('### HTTP Anidb Metadata Agent (HAMA) Ended ################################################################################################################')
  time.strptime("30 Nov 00", "%d %b %y")                                                                            # Avoid "AttributeError: _strptime" on first call [http://bugs.python.org/issue7980]
  
### Common metadata agent ################################################################################################################################################
class HamaCommonAgent:
  
  ### Serie search ###
  def search2(self, results, media, lang, manual, movie):
    global SERIE_LANGUAGE_PRIORITY
    Log.Debug(str(SERIE_LANGUAGE_PRIORITY))
    Log.Debug("=== Search - Begin - ================================================================================================")
    Log.Info("search() - Title: '%s', name: '%s', filename: '%s', manual:'%s'" % (media.title if movie else media.show, media.name, media.filename, str(manual)))      #if media.filename is not None: filename = String.Unquote(media.filename) #auto match only
    orig_title = ( media.title if movie else media.show ).encode('utf-8')  # NEEDS UTF-8
    if not orig_title:  return  #Log.Debug("=== Search - End - Empty ================================================================================================")

    ### Clear Plex http cache manually by searching a serei named "clear-cache" ###
    if orig_title.startswith("clear-cache"):   HTTP.ClearCache()
    
    ### Check if a guid is specified "Show name [anidb-id]" ###
    match = re.search("(?P<show>.*?) ?\[(?P<source>(anidb|tvdb|tmdb|imdb))-(tt)?(?P<guid>[0-9]{1,7})\]", orig_title, re.IGNORECASE)
    if match:  ###metadata id provided
      source, guid, show = match.group('source').lower(), match.group('guid'), match.group('show')
      if source=="anidb":  show, mainTitle = self.getMainTitle(AniDB_title_tree.xpath("/animetitles/anime[@aid='%s']/*" % guid), SERIE_LANGUAGE_PRIORITY) #global AniDB_title_tree, SERIE_LANGUAGE_PRIORITY;
      Log.Debug( "search - source: '%s', id: '%s', show from id: '%s' provided in foldername: '%s'" % (source, guid, show, orig_title) )
      results.Append(MetadataSearchResult(id="%s-%s" % (source, guid), name=show, year=media.year, lang=Locale.Language.English, score=100))
      Log.Debug("=== Search - End - =================================================================================================")
      return
  
    ### AniDB Local exact search ###
    cleansedTitle = self.cleanse_title (orig_title).encode('utf-8')
    if media.year is not None: orig_title = orig_title + " (" + str(media.year) + ")"  ### Year - if present (manual search or from scanner but not mine), include in title ###
    parent_element, show , score, maxi = None, "", 0, 0
    AniDB_title_tree_elements = list(AniDB_title_tree.iterdescendants())
    for element in AniDB_title_tree_elements: #list(AniDB_title_tree.iterdescendants())
      if element.get('aid'): #or </animetitles>
        if score: #only when match found and it skipped to next serie in file, then add
          if score>maxi: maxi=score
          Log.Debug("search() - AniDB - score: '%3d', id: '%6s', title: '%s' " % (score, aid, show))
          langTitle, mainTitle = self.getMainTitle(parent_element, SERIE_LANGUAGE_PRIORITY)
          results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=Locale.Language.English, score=score))
          parent_element, show , score = None, "", 0
        aid = element.get('aid')
      elif element.get('type') in ('main', 'official', 'syn', 'short'): #element.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or element.get('type') == 'main'):
        title = element.text.encode('utf-8')
        if   title.lower()              == orig_title.lower() and 100                            > score:  parent_element, show , score = element.getparent(), title,         100; Log.Debug("search() - AniDB - temp score: '%3d', id: '%6s', title: '%s' " % (100, aid, show))  #match = [element.getparent(), show,         100]
        elif self.cleanse_title (title) == cleansedTitle      and  99                            > score:  parent_element, show , score = element.getparent(), cleansedTitle,  99  #match = [element.getparent(), cleansedTitle, 99]
        elif orig_title in title                              and 100*len(orig_title)/len(title) > score:  parent_element, show , score = element.getparent(), orig_title,    100*len(orig_title)/len(title)  #match = [element.getparent(), show, 100*len(orig_title)/len(element.text)]
        else:  continue #no match 
    if score: #last serie detected, added on next serie OR here
      Log.Debug("search() - AniDB - score: '%3d', id: '%6s', title: '%s' " % (score, aid, show))
      langTitle, mainTitle = self.getMainTitle(parent_element, SERIE_LANGUAGE_PRIORITY)
      results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=Locale.Language.English, score=score))
    
    ### TVDB serie search ###
    Log.Debug("maxi: '%d'" % maxi)
    if maxi<50:
      try:  TVDBsearchXml = XML.ElementFromURL( TVDB_SERIE_SEARCH + orig_title.replace(" ", "%20"), cacheTime=CACHE_1HOUR * 24 * 7)
      except:  Log.Debug("search() - TVDB Loading search XML failed: ")
      else:
        for serie in TVDBsearchXml.xpath('Series'):
          a, b = orig_title, serie.xpath('SeriesName')[0].text.encode('utf-8') #a, b  = cleansedTitle, self.cleanse_title (serie.xpath('SeriesName')[0].text)
          score = 100 - 100*Util.LevenshteinDistance(a,b) / max(len(a),len(b)) if a!=b else 100
          Log.Debug( "search() - TVDB  - score: '%3d', id: '%6s', title: '%s'" % (score, serie.xpath('seriesid')[0].text, serie.xpath('SeriesName')[0].text) )
          results.Append(MetadataSearchResult(id="%s-%s" % ("tvdb", serie.xpath('seriesid')[0].text), name="%s [%s-%s]" % (serie.xpath('SeriesName')[0].text, "tvdb", serie.xpath('seriesid')[0].text), year=None, lang=Locale.Language.English, score=score) )
    if len(results)>=1:      #results.Sort('score', descending=True)
      Log.Debug("=== Search - End - =================================================================================================")
      return

    ### AniDB local keyword search ###
    matchedTitles, matchedWords, words  = [ ], { }, [ ]
    log_string     = "search - Keyword search - Matching '%s' with: " % orig_title
    for word in self.splitByChars(orig_title, SPLIT_CHARS):
      word = self.cleanse_title (word)
      if word and word not in FILTER_SEARCH_WORDS and len(word) > 1:  words.append (word.encode('utf-8'));  log_string += "'%s', " % word
    Log.Debug(log_string[:-2]) #remove last 2 chars
    if len(words)==0: # or len( self.splitByChars(orig_title, SPLIT_CHARS) )<=1:
      Log.Debug("search: Local exact search - NO KEYWORD: title: '%s'" % (orig_title))
      Log.Debug("=== Search - End - =================================================================================================")
      return None # No result found

    for title in AniDB_title_tree_elements:
      if title.get('aid'): aid = "anidb-"+title.get('aid')
      elif title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main':
        sample = self.cleanse_title (title.text).encode('utf-8')
        for word in words:
          if word in sample:
            index  = len(matchedTitles)-1
            if index >=0 and matchedTitles[index][0] == "anidb-"+aid:
              if title.get('type') == 'main':               matchedTitles[index][1] = title.text #aid.zfill(5) + ' ' + title.text
              if not title.text in matchedTitles[index][2]: matchedTitles[index][2].append(title.text)
            else:
              matchedTitles.append([aid, title.text, [title.text] ]) #aid.zfill(5) + ' ' + title.text
              if word in matchedWords: matchedWords[word].append(sample) ##### remove str
              else:                    matchedWords[word]=[sample]       ##### remove str
    log_string="search - Keywords: "
    for key, value in matchedWords.iteritems(): log_string += key + " (" + str(len(value)) + "), "
    Log.Debug(log_string)
    if len(matchedTitles)==0: Log.Debug("=== Search - End - ================================================================================================="); return None
    
    ### calculate scores + Buid results ###
    log_string = "Search - similarity with '%s': " % orig_title
    for match in matchedTitles:
      scores = []
      for title in match[2]: # Calculate distance without space and characters
        a, b = self.cleanse_title(title), cleansedTitle
        scores.append( int(100 - (100*float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) )) )  #To-Do: LongestCommonSubstring(first, second). use that?
      bestScore = max(scores)
      results.Append(MetadataSearchResult(id=match[0], name=match[1], year=media.year, lang=Locale.Language.English, score=bestScore))
      log_string += match[1] + " (%s%%), " % '{:>2}'.format(str(bestScore))
    Log.Debug(log_string)
    results.Sort('score', descending=True)
    Log.Debug("=== Search - End - =================================================================================================")
    return

  ### Parse the AniDB anime title XML ##################################################################################################################################
  def update2(self, metadata, media, lang, force, movie):

    global SERIE_LANGUAGE_PRIORITY, EPISODE_LANGUAGE_PRIORITY
    error_log = { 'anime-list anidbid missing': [], 'anime-list tvdbid missing': [], 'anime-list studio logos': [], 'Missing episodes'    : [], 'Plex themes missing'    : [],
                  'AniDB summaries missing'   : [], 'AniDB posters missing'    : [], 'TVDB summaries missing' : [], 'TVDB posters missing': []}
    getElementText = lambda el, xp: el.xpath(xp)[0].text if el is not None and el.xpath(xp) and el.xpath(xp)[0].text else ""  # helper for getting text from XML element
    
    Log.Debug('--- Update Begin -------------------------------------------------------------------------------------------')
    Log.Debug("update2 - metadata ID: '%s', Title: '%s',(%s, %s, %s)" % (metadata.id, metadata.title, "[...]", "[...]", force) )

    ### Get tvdbid, tmdbid, imdbid (+etc...) through mapping file ###
    tvdbid, tmdbid, imdbid, defaulttvdbseason, mapping_studio, poster_id, mappingList, anidbid_table = "", "", "", "", "", "", {}, []
    tvdbposternumber, tvdb_table, tvdbtitle, tvdbOverview, tvdbNetwork, tvdbFirstAired = 0, {}, "", "", "", ""
    if   metadata.id.startswith("tvdb"):  tvdbid = metadata.id [len("tvdb-"):]
    elif metadata.id.startswith("anidb"):
      anidbid=metadata.id[len("anidb-"):]
      tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio, anidbid_table, poster_id = self.anidbTvdbMapping(metadata, anidbid, error_log)  # Log.Debug("mappingList: '%s'" % str(mappingList))

    if tvdbid.isdigit(): ### TVDB ID exists ####

      ### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###
      if THEME_URL % tvdbid in metadata.themes:  Log.Debug("update2 - Theme song - already added")
      else:                                      self.metadata_download (metadata.themes, THEME_URL % tvdbid, 1, "Plex/"+metadata.id+".mp3")
      
      ### TVDB - Load serie XML ###
      Log.Debug("update2 - TVDB - loading serie xml: " + tvdbid)
      try:
        url = TVDB_HTTP_API_URL % (TVDB_API_KEY, tvdbid)
        if self.http_status_code(url) != 200:
          Log.Debug("update2 - metadata_download failed, url: '%s'" % url)
          error_log['anime-list tvdbid missing'].append(url + " - xml not downloadable so serie probably a duplicate deleted from thetvdb")
          tvdbanime = None
        else:  tvdbanime = self.xmlElementFromFile ( url, TVDB_SERIE_CACHE+"/"+tvdbid+".xml", False, CACHE_1HOUR * 24 * 7).xpath('/Data')[0]
      except:  tvdbanime = None
      tvdbtitle, tvdbNetwork        = getElementText(tvdbanime, 'Series/SeriesName'), getElementText(tvdbanime, 'Series/Network')
      tvdbOverview, tvdbFirstAired  = getElementText(tvdbanime, 'Series/Overview'  ), getElementText(tvdbanime, 'Series/FirstAired')
      tvdbContentRating, tvdbRating = getElementText(tvdbanime, 'Series/ContentRating'), float(getElementText(tvdbanime, 'Series/Rating'))
      tvdbGenre                     = filter(None, getElementText(tvdbanime, 'Series/Genre').split("|"))
      Log.Debug(tvdbGenre)
      if imdbid is None or imdbid =="" and getElementText(tvdbanime, 'Series/IMDB_ID'):  imdbid = getElementText(tvdbanime, 'Series/IMDB_ID');  Log.Debug("IMDB ID was empty, loaded through tvdb serie xml, IMDBID: '%s'" % imdbid)
      Log.Debug("update2 - TVDB - loaded serie xml: " + tvdbid + " " + tvdbtitle)

      ### TVDB - Build 'tvdb_table' ###
      Log.Debug("### TVDB - Build 'tvdb_table' ###")
      summary_missing, summary_present = [], []
      if tvdbanime is not None:
        for episode in tvdbanime.xpath('Episode'):  # Combined_episodenumber, Combined_season, DVD(_chapter, _discid, _episodenumber, _season), Director, EpImgFlag, EpisodeName, EpisodeNumber, FirstAired, GuestStars, IMDB_ID #seasonid, imdbd
          numbering, Overview = getElementText(episode, 'absolute_number') if defaulttvdbseason=="a" else "s" + getElementText(episode, 'SeasonNumber') + "e" + getElementText(episode, 'EpisodeNumber'), getElementText(episode, 'Overview')
          if Overview=="":  summary_missing.append(numbering)
          else:             summary_present.append(numbering)
          tvdb_table [numbering] = { 'EpisodeName': getElementText(episode, 'EpisodeName'), 'FirstAired':  getElementText(episode, 'FirstAired' ),
                                     'Rating':      getElementText(episode, 'Rating'),      'filename':    getElementText(episode, 'filename'), # filename = episode.xpath('filename')[0].text
                                     'Overview':    Overview }              
      Log.Debug("update2 - TVDB - tvdb_table: "               + str(sorted(summary_present)) )
      Log.Debug("update2 - TVDB - Episodes without Summary: " + str(sorted(summary_missing)) )

      ### TVDB - Fanart, Poster and Banner ###
      if Prefs['GetTvdbPosters'] or Prefs['GetTvdbFanart' ] or Prefs['GetTvdbBanners']:
        tvdbposternumber = self.getImagesFromTVDB(metadata, media, tvdbid, movie, poster_id, force)
        if tvdbposternumber == 0:  error_log['TVDB posters missing'].append(WEB_LINK % (TVDB_SERIE_URL % tvdbid, tvdbid))
    ### End of "if tvdbid.isdigit():" ###
  
    ### Movie posters including imdb from TVDB - Load serie XML ###
    if imdbid.isalnum():
      self.getImagesFromTMDB                      (metadata, imdbid, 97)  #The Movie Database is least prefered by the mapping file, only when imdbid missing
      self.getImagesFromOMDB                      (metadata, imdbid, 98)  #return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
    elif tmdbid.isdigit():  self.getImagesFromTMDB(metadata, tmdbid, 97)  #The Movie Database is least prefered by the mapping file, only when imdbid missing
 
    ### TVDB mode when a season 2 or more exist ############################################################################################################
    if not movie and (len(media.seasons)>2 or max(map(int, media.seasons.keys()))>1 or metadata.id.startswith("tvdb-")):
      Log.Debug("using TVDB numbering mode (seasons)" )
      metadata.title, metadata.summary, metadata.studio, metadata.rating  = tvdbtitle, tvdbOverview, tvdbNetwork, tvdbRating
      metadata.originally_available_at, metadata.content_rating = Datetime.ParseDate( tvdbFirstAired ).date(), tvdbContentRating
      for genre in tvdbGenre: metadata.genres.add(genre)
      list_eps = ""
      for media_season in media.seasons:
        metadata.seasons[media_season].summary, metadata.seasons[media_season].title, metadata.seasons[media_season].show,metadata.seasons[media_season].source_title = "#" + tvdbOverview, "#" + tvdbtitle, "#" + tvdbtitle, "#" + tvdbNetwork
        for media_episode in media.seasons[media_season].episodes:
          ep, episode_count = "s%se%s" % (media_season, media_episode), 0
          if ep in tvdb_table:
            if 'Overview'    in tvdb_table[ep]:
              try:     metadata.seasons[media_season].episodes[media_episode].summary = tvdb_table [ep] ['Overview']
              except:  Log.Debug("Error adding summary - ep: '%s', media_season: '%s', media_episode: '%s', summary:'%s'" % (ep, media_season, media_episode, tvdb_table [ep] ['Overview']))                  
            if 'EpisodeName' in tvdb_table[ep]: metadata.seasons[media_season].episodes[media_episode].title   = tvdb_table [ep] ['EpisodeName']
            if 'Rating'      in tvdb_table[ep]:
              try:     metadata.seasons[media_season].episodes[media_episode].rating  = float(tvdb_table [ep] ['Rating'])
              except:  Log.Debug("float issue: '%s'" % tvdb_table [ep] ['Rating']) #ValueError
            if 'FirstAired'  in tvdb_table[ep] and tvdb_table [ep] ['FirstAired'] != "":
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
      Log.Debug("MODE AniDB DETECTED")
      ### AniDB Serie XML ##################################################################################################################################
      Log.Debug("update - AniDB Serie XML: " + ANIDB_HTTP_API_URL + metadata.id[len("anidb-"):] + ", " + ANIDB_SERIE_CACHE +"/"+metadata.id[len("anidb-"):]+".xml" )
      try:    anime = self.xmlElementFromFile ( ANIDB_HTTP_API_URL + metadata.id[len("anidb-"):], ANIDB_SERIE_CACHE +"/"+metadata.id[len("anidb-"):]+".xml", True, CACHE_1HOUR * 24 * 7).xpath('/anime')[0]          # Put AniDB serie xml (cached if able) into 'anime'
      except:
        Log.Error("update - AniDB Serie XML: Exception raised, probably no return in xmlElementFromFile")
        anime = None         #return #if banned return ?

      if anime is not None:  #if getElementText(anime, 'type')=='Movie' usefull for something in the future ??

        ### AniDB Title ###
        try:
          title, orig = self.getMainTitle(anime.xpath('/anime/titles/title'), SERIE_LANGUAGE_PRIORITY)
          title, orig = title.replace("`", "'"), orig.replace("`", "'")
        except:  Log.Debug("update - AniDB Title: Exception raised" )
        else:
          title, orig = title.encode("utf-8").replace("`", "'"), orig.encode("utf-8").replace("`", "'")
          if title == str(metadata.title):  Log.Debug("update - AniDB title need no change: '%s' original title: '%s' metadata.title '%s'" % (title, orig, metadata.title) )
          elif title != "": #If title diffeerent but not empty [Failsafe]
            Log.Debug("update - AniDB title changed: '%s' original title: '%s'" % (title, orig) )
            metadata.title = title
            if movie and orig != "" and orig != metadata.original_title: metadata.original_title = orig # If it's a movie, Update original title in metadata http://forums.plexapp.com/index.php/topic/25584-setting-metadata-original-title-and-sort-title-still-not-possible/

        ### AniDB Start Date ###
        if getElementText(anime, 'startdate') == "":                                  Log.Debug("update - AniDB Start Date: None")
        elif metadata.originally_available_at == getElementText(anime, 'startdate'):  Log.Debug("update - AniDB Start Date: " + str(metadata.originally_available_at) + "*")
        else:
          metadata.originally_available_at = Datetime.ParseDate( getElementText(anime, 'startdate') ).date()
          if movie: metadata.year          = metadata.originally_available_at.year
          Log.Debug("update - AniDB Start Date: " + str(metadata.originally_available_at))

        ### AniDB Ratings ###
        misc = getElementText(anime, 'ratings/permanent')
        if misc=="":                         Log.Debug("update - AniDB Ratings: None")   
        elif float(misc) == metadata.rating: Log.Debug("update - AniDB Ratings: " + misc + "*")
        else:                                Log.Debug("update - AniDB Ratings: " + misc);  metadata.rating = float( misc )
        
        ### AniDB Genres ###
        genres = {}
        for category in anime.xpath('categories/category'):
          if getElementText(category, 'name') in GENRE_NAMES and category.get('weight') >= Prefs['MinimumWeight']:                genres [ getElementText(category, 'name') ] = int(category.get('weight')) # Remove genre whitelist
          if getElementText(category, 'name') in RESTRICTED_GENRE_NAMES and metadata.content_rating != RESTRICTED_CONTENT_RATING: metadata.content_rating = RESTRICTED_CONTENT_RATING
        sortedGenres = sorted(genres.items(), key=lambda x: x[1],  reverse=True)
        log_string, genres = "AniDB Genres (Weight): ", []
        for genre in sortedGenres: genres.append(genre[0].encode("utf-8") )
        if all(x in metadata.genres for x in genres): Log.Debug(log_string+str(sortedGenres)+"*") #set(sortedGenres).issubset(set(metadata.genres)):
        else:
          Log.Debug("update - genres: " + str( sortedGenres) + " " + str(genres))
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
          metadata.writers.clear()
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

        ### AniDB Serie/Movie description + link ###
        Log.Debug("update - AniDB description + link")
        description = ""
        try:     description = re.sub(r'http://anidb\.net/[a-z]{2}[0-9]+ \[(.+?)\]', r'\1', getElementText(anime, 'description')).replace("`", "'") + "\n" # Remove wiki-style links to staff, characters etc
        except:  Log.Debug("Exception ")
      
        if description == "":                  error_log['AniDB summaries missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id[len("anidb-"):], metadata.id[len("anidb-"):]) + " " + metadata.title)
        elif metadata.summary != description and description:  metadata.summary = description.replace("`", "'")

        ### AniDB Posters ###
        Log.Debug("update - AniDB Poster, url: '%s'" % (ANIDB_PIC_BASE_URL + getElementText(anime, 'picture')))
        if getElementText(anime, 'picture') == "": error_log['AniDB posters missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id[len("anidb-"):], metadata.id[len("anidb-"):]) + "" + metadata.title)
        elif Prefs['GetAnidbPoster']:  self.metadata_download (metadata.posters, ANIDB_PIC_BASE_URL + getElementText(anime, 'picture'), 99, "AniDB/%s" % getElementText(anime, 'picture')) 

        if not movie: ### TV Serie specific #################################################################################################################
          numEpisodes, totalDuration, mapped_eps, missing_eps, ending_table, op_nb = 0, 0, [], [], {}, 0 
          specials      = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
          #Log.Debug("### AniDB mappingList: '%s'" % str(mappingList))  #Log.Debug("### AniDB tvdb_table:  '%s'" % str(tvdb_table))   
          
          for episode in anime.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################
            ep_title, main   = self.getMainTitle (episode.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
            ep_title, main   = ep_title.replace("`", "'"), main.replace("`", "'")
            epNum,    eid    = episode.xpath('epno')[0], episode.get('id')
            epNumType        = epNum.get('type')
            season, epNumVal = "1" if epNumType == "1" else "0", epNum.text if epNumType == "1" else str( specials[ epNum.text[0] ][0] + int(epNum.text[1:]))
            if epNumType=="3":
              if ep_title.startswith("Ending"):
                if op_nb==0: op_nb = int(epNum.text[1:])-1                                      #first type 3 is first ending so epNum.text[1:] -1 = nb openings
                epNumVal = str( int(epNumVal) +50-op_nb)   #shifted to 150 for 1st ending.  
              Log.Debug("AniDB specials title - Season: '%s', epNum.text: '%s', epNumVal: '%s', ep_title: '%s'" % (season, epNum.text, epNumVal, ep_title) )
             
            if not (season in media.seasons and epNumVal in media.seasons[season].episodes):  #Log.Debug("update - Season: '%s', Episode: '%s' => '%s' not on disk" % (season, epNum.text, epNumVal) )
              if epNumType == "1": missing_eps.append(" s" + season + "e" + epNumVal )
              continue
            episodeObj = metadata.seasons[season].episodes[epNumVal]
            
            ### AniDB Get the correct episode title ###            #Log.Debug("AniDB correct episode title")  #if ep_title == "":                    episodeObj.title = specials[ epNum.text[0] ][1] + ' ' + epNum.text[1:] #make title from first letter of type            #elif
            if episodeObj.title != ep_title:  episodeObj.title = ep_title
            
            ### AniDBN turn the YYYY-MM-DD airdate in each episode into a Date ###
            airdate = getElementText(episode, 'airdate')
            if airdate != "":
              match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", airdate)
              if match: ### error int here
                try:                   episodeObj.originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
                except ValueError, e:  Log.Debug("update - AniDB parseAirDate - Date out of range: " + str(e))
            
            ### AniDB Duration ###
            duration = getElementText(episode, 'length')
            if duration != "":
              episodeObj.duration = int(duration) * 1000 * 60 # Plex save duration in millisecs, AniDB stores it in minutes
              if season == "1":   numEpisodes, totalDuration = numEpisodes + 1, totalDuration + episodeObj.duration
            
            ### AniDB Writers, Producers, Directors ###  #Log.Debug("### AniDB Writers, Producers, Directors ### ")
            for role in plex_role:
              for person in plex_role[role]:
                if role=="writers":    episodeObj.writers.add  (person)
                if role=="producers":  episodeObj.producers.add(person)
                if role=="directors":  episodeObj.directors.add(person)
              
            ### Rating ###
            rating = getElementText(episode, 'rating') #if rating =="":  Log.Debug(metadata.id + " Episode rating: ''") #elif rating == episodeObj.rating:  Log.Debug(metadata.id + " update - Episode rating: '%s'*" % rating )
            if not rating =="" and not rating == episodeObj.rating: #else:        #Log.Debug(metadata.id + " update - Episode rating: '%s'" % rating )
                episodeObj.rating = float(rating)
            
            ### TVDB mapping episode summary ###
            anidb_ep, tvdb_ep, summary= 's' + season + 'e' + epNumVal, "", "No summary in TheTVDB.com" #epNum
            if tvdbid.isdigit():
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
          if len(missing_eps)>0:  error_log['Missing episodes'].append("anidbid: %s, Title: '%s', Missing Episodes: %s" % (metadata.id.zfill(5), title, missing_eps))
          convert      = lambda text: int(text) if text.isdigit() else text
          alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]

          ### AniDB Final post-episode titles cleanup ###
          Log.Debug("update - DURATION: %s, numEpisodes: %s" %(str(totalDuration), str(numEpisodes)) )
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
    global AniDB_TVDB_mapping_tree    #if not AniDB_TVDB_mapping_tree: AniDB_TVDB_mapping_tree = self.xmlElementFromFile(ANIDB_TVDB_MAPPING_URL, ANIDB_TVDB_MAPPING, False, CACHE_1HOUR * 24 * 7) # Load XML file
    poster_id_array, mappingList, mapping_studio = {}, {}, ""
    for anime in AniDB_TVDB_mapping_tree.iter('anime'):
      anidbid, tvdbid  = anime.get("anidbid"), anime.get('tvdbid')
      if tvdbid.isdigit():  poster_id_array [tvdbid] = poster_id_array [tvdbid] + 1 if tvdbid in poster_id_array else 0
      if anidb_id == anidbid: #manage all formats latter
        name = anime.xpath("name")[0].text
        if tvdbid.isdigit():
          try: ### mapping list ###
            for season in anime.iter('mapping'):
              for string in filter(None, season.text.split(';')):  mappingList [ 's' + season.get("anidbseason") + 'e' + string.split('-')[0] ] = 's' + season.get("tvdbseason") + 'e' + string.split('-')[1]
          except: Log.Debug("exception") #mappingList = {}
        else:
          if anime.get('tvdbid')=="" or anime.get('tvdbid')=="unknown":
            error_log ['anime-list tvdbid missing'].append("anidbid: %s title: '%s' has no matching tvdbid ('%s') in mapping file" % (anidb_id.zfill(5), name, anime.get('tvdbid')) + WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; tvdbid:" % (anidb_id, name), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report"))
            Log.Debug("anidbTvdbMapping - Missing tvdbid for anidbid %s" % anidb_id)  # Semi-colon, %0A Line Feed, %09 Tab or ('	'), ```  code block # #xml.etree.ElementTree.tostring  #dict = {';':"%3B", '\n':"%0A", '	':"%09"} for item in dict: temp.replace(item, list[item]) description += temp
        try:    mapping_studio  = anime.xpath("supplemental-info/studio")[0].text
        except: mapping_studio  = ""
        Log.Debug("anidbTvdbMapping - AniDB-TVDB Mapping - anidb:%s tvbdid: %s studio: %s defaulttvdbseason: %s" % (anidb_id, anime.get('tvdbid'), mapping_studio, str(anime.get('defaulttvdbseason'))) )
        break
    else:
      error_log['anime-list anidbid missing'].append("anidbid: " + anidb_id.zfill(5))
      Log.Debug('anidbTvdbMapping('+anidb_id+') found no matching anidbid...')
      return "", "", "", "", [], "", [], "0"

    anidbid_table = []
    for anime2 in AniDB_collection_tree.iter("anime"):
      if anime.get('tvdbid') == anime2.get('tvdbid'):  anidbid_table.append( anime2.get("anidbid") )
    return tvdbid, anime.get('tmdbid'), anime.get("imdbid"), anime.get('defaulttvdbseason'), mappingList, mapping_studio, anidbid_table, poster_id_array [tvdbid] if tvdbid in poster_id_array else {}
    
  ### AniDB collection mapping - complement AniDB movie collection file with related anime AND series sharing the same tvdbid ########################
  def anidbCollectionMapping(self, metadata, anime, anidbid_table=[]):
    related_anime_list = []
    for relatedAnime in anime.xpath('/anime/relatedanime/anime'): related_anime_list.append(relatedAnime.get('id'))
    global AniDB_collection_tree, SERIE_LANGUAGE_PRIORITY # if not AniDB_collection_tree: AniDB_collection_tree = self.xmlElementFromFile(ANIDB_COLLECTION_MAPPING_URL, ANIDB_COLLECTION_MAPPING, False, CACHE_1HOUR * 24 * 7)
    for element in AniDB_collection_tree.iter("anime"):
      if element.get('anidbid') == metadata.id or element.get('anidbid') in related_anime_list + anidbid_table:
        set         = element.getparent()
        title, main = self.getMainTitle(set.xpath('titles')[0], SERIE_LANGUAGE_PRIORITY)
        metadata.collections.add(title) #metadata.collections.clear()
        Log.Debug("anidbCollectionMapping - anidbid (%s) is part of collection: %s', related_anime_list: '%s', " % (metadata.id, title, str(related_anime_list)))
        return
    Log.Debug("anidbCollectionMapping - anidbid is not part of any collection, related_anime_list: '%s'" % str(related_anime_list)) 

  ### [banners.xml] Attempt to get the TVDB's image data ###############################################################################################################
  def getImagesFromTVDB(self, metadata, media, tvdbid, movie, poster_id=1, force=False):
    locked, posternum, num, poster_total = networkLock.acquire(), 0, 0, 0
    try:     bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbid), cacheTime=CACHE_1HOUR * 24 * 7) # don't bother with the full zip, all we need is the banners
    except:  Log.Debug("getImagesFromTVDB - Loading picture XML failed: " + TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbid));  return
    else:    Log.Debug("getImagesFromTVDB - Loading picture XML: " + TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbid))
    for banner in bannersXml.xpath('Banner'):
      if banner.xpath('BannerType')[0].text=="poster":  poster_total +=1
    for banner in bannersXml.xpath('Banner'):
      num, bannerType, bannerType2, bannerPath  = num+1, banner.xpath('BannerType' )[0].text, banner.xpath('BannerType2')[0].text, banner.xpath('BannerPath' )[0].text  #rating         =(banner.xpath('Rating'     )[0].text if banner.xpath('Rating') else "")
      season = banner.xpath('Season'     )[0].text if banner.xpath('Season') else ""                                                                                    #Language       = banner.xpath('Language'   )[0].text #if Language not in ['en', 'jp']: continue                                        # id             = banner.xpath('id'         )[0].text
      if bannerType == 'poster':  posternum += 1
      if movie and not bannerType in ('fanart', 'poster') or season!="" and season not in media.seasons:  continue                                          # or and not defaulttvdbseason == season #skipping banner as it's a movie and not fanart or poster, skipping season poster as not defaulttvdbseason so wrong season
      if Prefs['GetTvdbPosters'] and ( bannerType == 'poster' or bannerType2 == 'season' and not movie ) or \
         Prefs['GetTvdbFanart' ] and   bannerType == 'fanart' or Prefs['GetTvdbBanners'] and not movie and ( bannerType == 'series' or bannerType2 == 'seasonwide'):
        metatype     = (metadata.art if bannerType=='fanart' else metadata.posters if bannerType=='poster' else metadata.banners if bannerType=='series' or  bannerType2=='seasonwide' \
                        else metadata.seasons[season].posters if bannerType=='season' and bannerType2=='season' else None)
        if metatype == metadata.posters:  rank = 1 if poster_id and poster_total and posternum == divmod(poster_id, poster_total)[1] + 1 else posternum+1 #fmod #Why '%' not working #rank = 1 if posternum == divmod(poster_id, poster_total)[1] + 1 else poster_id if posternum==1 else posternum
        else:                             rank = num
        bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
        self.metadata_download (metatype, TVDB_IMAGES_URL + bannerPath, rank, "TVDB/"+bannerPath, bannerThumbUrl)
    if locked:  networkLock.release() 
    return posternum

  ### Download TMDB poster and background through IMDB or TMDB ID ##########################################################################################
  def  getImagesFromTMDB(self, metadata, id, num=90):
    config_dict = self.get_json(TMDB_CONFIG_URL, cache_time=CACHE_1WEEK * 2)
    images={}
    if id.startswith("tt"):
      Log.Debug("getImagesFromTMDB - by IMDBID - url: " + TMDB_SEARCH_URL_BY_IMDBID % id)
      tmdb_json   = self.get_json(TMDB_SEARCH_URL_BY_IMDBID %id, cache_time=CACHE_1WEEK * 2) # Log.Debug("getImagesFromTMDB - by IMDBID - tmdb_json: '%s'" % str(tmdb_json))
      for type in ['movie_results', 'tv_results']:
        if tmdb_json is not None and type in tmdb_json:
          for index, poster in enumerate(tmdb_json[type]):
            if 'poster_path'   in tmdb_json[type][index] and tmdb_json[type][index]['poster_path'  ]!="null":  images[ tmdb_json[type][index]['poster_path'  ]] = metadata.posters
            if 'backdrop_path' in tmdb_json[type][index] and tmdb_json[type][index]['backdrop_path']!="null":  images[ tmdb_json[type][index]['backdrop_path']] = metadata.art
      rank=90
    else:
      Log.Debug("getImagesFromTMDB - by TMDBID - url: " + TMDB_IMAGES_URL % id)
      tmdb_json = self.get_json(url=TMDB_IMAGES_URL % id, cache_time=CACHE_1WEEK * 2) # Log.Debug("getImagesFromTMDB - by IMDBID - tmdb_json: '%s'" % str(tmdb_json))
      if tmdb_json is not None and 'poster'    in tmdb_json and len(tmdb_json['posters'  ]):
        for index, poster in enumerate(tmdb_json['posters']):
          if 'file_path' in tmdb_json['posters'][index] and tmdb_json['posters'][index]['file_path']!="null":  images[ tmdb_json['posters'  ][index]['file_path']] = metadata.posters
      if tmdb_json is not None and 'backdrops' in tmdb_json and len(tmdb_json['backdrops']):
        for index, poster in enumerate(tmdb_json['backdrops']):
          if 'file_path' in tmdb_json['backdrops'][index] and tmdb_json['backdrops'][index]['file_path']!="null":  images[ tmdb_json['backdrops'][index]['file_path']] = metadata.art
      rank=95  # Log.Debug("getImagesFromTMDB - images: '%s'" % str(images))
    if len(images):
      for filename in images.keys():
         if filename is None:  Log.Debug("Filename: 'None'" )
         else:
           image_url, thumb_url = config_dict['images']['base_url'] + 'original' + filename, config_dict['images']['base_url'] + 'w300'     + filename
           self.metadata_download (images[filename], image_url, rank, "TMDB/%s.jpg" % id, thumb_url) 
   
  ### Fetch the IMDB poster using OMDB HTTP API ###########################################################################################################
  def getImagesFromOMDB(self, metadata, imdbid, num=99):
    Log.Debug("getImagesFromOMDB - imdbid: '%s', url: '%s', filename: '%s'" % (imdbid, OMDB_HTTP_API_URL + imdbid, "OMDB/%s.jpg" % imdbid))
    try:
      OMDB = self.get_json(OMDB_HTTP_API_URL + imdbid, cache_time=CACHE_1WEEK * 56)
      if 'Poster' in OMDB and OMDB['Poster']!="N/A":  self.metadata_download (metadata.posters, OMDB['Poster'], num, "OMDB/%s.jpg" % imdbid)
      else:                                           Log.Debug("getImagesFromOMDB - No poster to download")
    except: Log.Debug("getImagesFromOMDB - issue - OMDB: '%s' " % OMDB)

  #########################################################################################################################################################
  def metadata_download (self, metatype, url, num=99, filename="", url_thumbnail=None):  #if url in metatype:#  Log.Debug("metadata_download - url: '%s', num: '%s', filename: '%s'*" % (url, str(num), filename)) # Log.Debug(str(metatype))   #  return
    Log.Debug("metadata_download - url: '%s', num: '%d', filename: '%s'" % (url, num, filename))
    file = None #if filename empty no local save
    if filename and Data.Exists(filename):  ### if stored locally load it# Log.Debug("media_download - url: '%s', num: '%s', filename: '%s' was in Hama local disk cache" % (url, str(num), filename))
      try:     file = Data.Load(filename)
      except:  Log.Debug("media_download - could not load file present in cache")
    if file == None: ### if not loaded locally download it
      try:
        #if self.http_status_code(url) != 200:  Log.Debug("metadata_download - metadata_download failed, url: '%s', num: '%d', filename: %s" % (url, num, filename));  return
        file = HTTP.Request(url_thumbnail if url_thumbnail else url, cacheTime=None).content
      except:  Log.Debug("metadata_download - error downloading"); return
      else:  ### if downloaded, try saving in cache but folders need to exist
        if not filename == "" and not filename.endswith("/"):
          try:     Data.Save(filename, file)
          except:  Log.Debug("metadata_download - Plugin Data Folder not created for filename '%s', no local cache, or download failed ##########" % (filename))
    try:
      proxy_item = Proxy.Preview(file, sort_order=num) if url_thumbnail is None else Proxy.Media(file, sort_order=num)
      if url not in metatype or metatype[ url ] != proxy_item:  metatype[ url ] = proxy_item
    except: Log.Debug("metadata_download - issue adding picture to plex - url downloaded: '%s', filename: '%s'" % (url_thumbnail if url_thumbnail else url, filename))
    #metatype.validate_keys( url_thumbnail if url_thumbnail else url ) remove many posters, to avoid
      
  ### get_json file, TMDB API supports only JSON now ######################################################################################################
  def get_json(self, url, cache_time=CACHE_1MONTH):
    try:     tmdb_dict = JSON.ObjectFromURL(url, sleep=2.0, cacheTime=cache_time)
    except:  Log('get_json - Error fetching JSON page')
    else:    return tmdb_dict

  ### Pull down the XML from web and cache it or from local cache for a given anime ID ####################################################################
  def xmlElementFromFile (self, url, filename="", delay=True, cache=None):
    locked = False
    global lastRequestTime
    if delay:
      locked, now = networkLock.acquire(), datetime.datetime.utcnow()
      if lastRequestTime is not None:
        delta = now - lastRequestTime
        if delta.seconds < SECONDS_BETWEEN_REQUESTS: time.sleep(SECONDS_BETWEEN_REQUESTS - delta.seconds)
      lastRequestTime = now
    try:
      result = ""
      try:     result = HTTP.Request(url, headers={'Accept-Encoding':''}, timeout=60, cacheTime=cache )  #
      except:  Log("xmlElementFromFile - XML issue, result: '%s', url: '%s'" %(result, url) )
      except URLError as e:
        if   hasattr(e, 'reason'):  Log("xmlElementFromFile - We failed to reach a server: " + e.reason)
        elif hasattr(e, 'code'  ):  Log("xmlElementFromFile - The server couldn't fulfill the request: " + e.code)      
      if len(result)<1024:  # http issue or worked but returned banned string
        Log("xmlElementFromFile - XML issue, result: '%s', url: '%s'" %(result, url) )
        if Data.Exists(filename):
          Log.Debug("xmlElementFromFile - Loading locally since banned (result page <1024 bytes)")
          try:     return XML.ElementFromString(Data.Load(filename))
          except:  Log("xmlElementFromFile - Error loading - url: '%s', filename: '%s'" % (url, filename))
      else:
        if filename!="":  #and Prefs['TVDB-Local-cache']==true:
          try:     Data.Save(filename, result)
          except:  Log.Debug("xmlElementFromFile - Serie XML could not be saved locally")  #Catch ALL #else:    Log.Debug("xmlElementFromFile - Serie XML saved locally successfully") 
      Log.Debug ("xmlElementFromFile - Serie XML url: %s, Data filename: %s" % (url, filename))
      try:     return XML.ElementFromString(result)
      except:  Log.Error("result: " + result)

    except:   
      Log.Debug ("xmlElementFromFile - main loop except - url: %s, filename: %s" % (url, filename))
      if Data.Exists(filename):
        Log.Debug("xmlElementFromFile - Loading locally")
        try:     return XML.ElementFromString(Data.Load(filename))
        except:  Log("xmlElementFromFile - Error loading - url: '%s', filename: '%s'" % (url, filename))
      
    finally:
      if delay and locked: networkLock.release()

  ### http_code retrieves the http status code of a url by requesting header data only from the hos##########################################################
  def http_status_code(self, url):
    a=urllib.urlopen(url)
    if a is not None: return a.getcode()

  ### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
  def cleanse_title(self, title):
    try:    title=title.encode('utf-8')
    except: pass
    return  title.replace("`", "'").translate(string.maketrans('', ''), FILTER_CHARS).lower() # None in the translate call was giving an error of 'TypeError: expected a character buffer object'. So, we construct a blank translation table instead.

  ### Split a string per list of chars #################################################################################################################################
  def splitByChars(self, string, separators=SPLIT_CHARS):
    for i in separators: string.replace(" ", i)
    return string.split()

  ### extract the series/movie/Episode title #################################################################################################################################
  def getMainTitle(self, titles, languages):
    if not 'main' in languages:  languages.append('main')                                        # Add main to the selection if not present
    langTitles = ["" for index in range(len(languages)+1)]                                       # languages: title order including main title, then choosen title
    for title in titles:                                                                         # Loop through all languages listed in the anime XML
      type, lang = title.get('type'), title.get('{http://www.w3.org/XML/1998/namespace}lang')    # IF Serie: Main, official, Synonym, short. If episode: None # Get the language, 'xml:lang' attribute need hack to read properly
      if type == 'main' or type == None and langTitles[ languages.index('main') ] == "":  langTitles [ languages.index('main') ] = title.text  # type==none is for mapping episode language
      if lang in languages and type in ['main', 'official', 'syn', 'synonym', None]:      langTitles [ languages.index( lang ) ] = title.text  #Applede Korean synonym fix
    for index in range( len(languages) ):
      if langTitles[index] != '':         langTitles[len(languages)] = langTitles[index];  break #Log.Debug("getMainTitle - LANGUAGE titles: " + str(langTitles))  #else: Log.Debug("getMainTitle - Languages: '%s', langTitles: '%s'" % (str(languages), str(langTitles)))
    if langTitles[len(languages)] == "":  langTitles[len(languages)] = langTitles[languages.index('main')]
    return langTitles[len(languages)], langTitles[languages.index('main')]
    
### Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows, HamaCommonAgent):
  name, primary_provider, fallback_agent, contributes_to, languages, accepts_from = ('HamaTV', True, False, None, [Locale.Language.English,], ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles'] )
  def search(self, results,  media, lang, manual): self.search2(results,  media, lang, manual, False )
  def update(self, metadata, media, lang, force ): self.update2(metadata, media, lang, force,  False )

class HamaMovieAgent(Agent.Movies, HamaCommonAgent):
  name, primary_provider, fallback_agent, contributes_to, languages, accepts_from = ('HamaMovies', True, False, None, [Locale.Language.English,], ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles'] )
  def search(self, results,  media, lang, manual): self.search2(results,  media, lang, manual, True )
  def update(self, metadata, media, lang, force ): self.update2(metadata, media, lang, force,  True )
