### AniBD ###

### Imports ###
import common
from common import GetElementText,     # Functions: SaveFile, LoadFile, metadata_download, WriteLogs, cleanse_title, getImagesFromASS
import os                            # Functions: 
import re                            # Functions: re.search, re.match, re.sub, re.IGNORECASE
import string                        # Functions: 
import datetime                      # Functions: 

### Variables ###
ANIDB_SERIE_URL    = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s' # AniDB link to the anime
ANIDB_PIC_BASE_URL = 'http://img7.anidb.net/pics/anime/'                                                                # AniDB picture directory

### Functions ###

# Anidb Movie collection
def GetAniDBTitlesDB():
  ANIDB_TITLES  = 'http://anidb.net/api/anime-titles.xml.gz'               # AniDB title database file contain all ids, all languages  #http://bakabt.info/anidb/animetitles.xml
  AniDBTitlesDB = common.LoadFile(filename=os.path.basename(ANIDB_TITLES), relativeDirectory="", url=ANIDB_TITLES, cache= CACHE_1HOUR * 24 * 14)  # AniDB title database loaded once every 2 weeks
  if not AniDBTitlesDB:  raise Exception("Failed to load core file '{url}'".format(url=os.path.splitext(os.path.basename(ANIDB_TITLES))[0]))
  return AniDBTitlesDB

#def Search_AniDB_Exact_Title():
def Search (results, media, lang, manual, movie, AniDBTitlesDB):
  Log.Info("=== Search - Begin - ================================================================================================")
  orig_title = ( media.title if movie else media.show )
  try:                    orig_title = orig_title.encode('utf-8')  # NEEDS UTF-8
  except Exception as e:  Log.Error("UTF-8 encode issue, Exception: '%s'" % e)
  if not orig_title:  return
  if orig_title.startswith("clear-cache"):   HTTP.ClearCache()  ### Clear Plex http cache manually by searching a serie named "clear-cache" ###
  Log.Info("Title: '%s', name: '%s', filename: '%s', manual: '%s', year: '%s'" % (orig_title, media.name, media.filename, str(manual), media.year))  #if media.filename is not None: filename = String.Unquote(media.filename) #auto match only
  
  ### Check if a guid is specified "Show name [anidb-id]" ###
  match = re.search("(?P<show>.*?)\[(?P<source>(anidb|anidb2|tvdb|tvdb2|tvdb3|tvdb4|tvdb5|tmdb|imdb))-(tt)?(?P<guid>[0-9]{1,7})\]", orig_title, re.IGNORECASE)
  if match:  ###metadata id provided
    source, guid, show = match.group('source').lower(), match.group('guid'), match.group('show')
    if source.startswith("anidb"):  show, mainTitle = getAniDBTitle(AniDBTitlesDB.xpath("/animetitles/anime[@aid='%s']/*" % guid))
    Log.Info("source: '%s', id: '%s', foldername show title: '%s', from title database id: '%s'" % (source, guid, orig_title, show) )
    results.Append(MetadataSearchResult(id="%s-%s" % (source, guid), name=show, year=media.year, lang=lang, score=100))
    return
  
  ### AniDB Local exact search ###
  cleansedTitle = common.cleanse_title(orig_title)
  if media.year is not None: orig_title = orig_title + " (" + str(media.year) + ")"  ### Year - if present (manual search or from scanner but not mine), include in title ###
  #Log.Info(orig_title)
  parent_element, show , score, maxi = None, "", 0, 0
  AniDBTitlesDB_elements = list(AniDBTitlesDB.iterdescendants()) if AniDBTitlesDB else []
  for element in AniDBTitlesDB_elements:
    if element.get('aid'):
      if score: #only when match found and it skipped to next serie in file, then add
        if score>maxi: maxi=score
        Log.Info("AniDB - score: '%3d', id: '%6s', title: '%s' " % (score, aid, show))
        langTitle, mainTitle = getAniDBTitle(parent_element)
        results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=lang, score=score))
        parent_element, show, score = None, "", 0
      aid = element.get('aid')
    elif element.get('type') in ('main', 'official', 'syn', 'short'):
      title = element.text
      if   title.lower()              == orig_title.lower() and 100                            > score:  parent_element, show , score = element.getparent(), title,         100; #Log.Info("AniDB - temp score: '%3d', id: '%6s', title: '%s' " % (100, aid, show))  #match = [element.getparent(), show,         100]
      elif common.cleanse_title (title) == cleansedTitle    and  99                            > score:  parent_element, show , score = element.getparent(), cleansedTitle,  99  #match = [element.getparent(), cleansedTitle, 99]
      elif orig_title in title                              and 100*len(orig_title)/len(title) > score:  parent_element, show , score = element.getparent(), orig_title,    100*len(orig_title)/len(title)  #match = [element.getparent(), show, 100*len(orig_title)/len(element.text)]
      else:  continue #no match 
  if score: #last serie detected, added on next serie OR here
    Log.Info("AniDB - score: '%3d', id: '%6s', title: '%s' " % (score, aid, show))
    langTitle, mainTitle = getAniDBTitle(parent_element)
    results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=lang, score=score))
  if len(results)>=1:  return  #results.Sort('score', descending=True)
  
  ### AniDB local keyword search ###
  matchedTitles, matchedWords, words  = [ ], { }, [ ]
  log_string     = "Keyword search - Matching '%s' with: " % orig_title
  temp = orig_title
  for i in common.SPLIT_CHARS:
    if i in temp:  temp = temp.replace(i, " ")
  for word in temp.split():
    word = common.cleanse_title (word)
    if word and word not in common.FILTER_SEARCH_WORDS and len(word) > 1:  words.append (word.encode('utf-8'));  log_string += "'%s', " % word
  Log.Info(log_string[:-2]) #remove last 2 chars  #if len(words)==0:
  SERIE_LANGUAGE_PRIORITY   = [ Prefs['SerieLanguage1'  ].encode('utf-8'), Prefs['SerieLanguage2'  ].encode('utf-8'), Prefs['SerieLanguage3'].encode('utf-8') ]  #override default language
  for title in AniDBTitlesDB_elements:
    if title.get('aid'): aid = title.get('aid')
    elif title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main':
      sample = common.cleanse_title (title.text).encode('utf-8')
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
  Log.Info(", ".join( key+"(%d)" % len(value) for key, value in matchedWords.iteritems() )) #list comprehention
  log_string = "similarity with '%s': " % orig_title
  for match in matchedTitles: ### calculate scores + Buid results ###
    scores = []
    for title in match[2]: # Calculate distance without space and characters
      a, b = common.cleanse_title(title), cleansedTitle
      scores.append( int(100 - (100*float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) )) )  #To-Do: LongestCommonSubstring(first, second). use that?
    bestScore  = max(scores)
    log_string = log_string + match[1] + " (%s%%), " % '{:>2}'.format(str(bestScore))
    results.Append(MetadataSearchResult(id="anidb-"+match[0], name=match[1]+" [anidb-%s]"  % match[0], year=media.year, lang=lang, score=bestScore))
  Log.Info(log_string) #results.Sort('score', descending=True)
  Log.Info("maxi: '%d'" % maxi)
  return maxi

### Extract the series/movie/Episode title from AniDB ########################################################################################################################
def getAniDBTitle(titles, lang=None):
  languages = lang if lang else [ Prefs['SerieLanguage1'], Prefs['SerieLanguage2'], Prefs['SerieLanguage3'] ]  #override default language
  if not 'main' in languages:  languages.append('main')                                      # Add main to the selection if not present in list (main nearly same as x-jat)
  type_priority = {'main':1, 'official':2, 'syn':3, 'synonym':4, 'short':5, None:6}          # lower = highter priority
  langLevel     = [9  for index in range(len(languages))]                                    # languages: title order including main title, then choosen title
  langTitles    = ["" for index in range(len(languages))]                                    # languages: title order including main title, then choosen title
  for title in titles:                                                                       # Loop through all languages listed in the anime XML
    type = title.get('type')
    lang = title.get('{http://www.w3.org/XML/1998/namespace}lang') # If Serie: Main, official, Synonym, short. If episode: None # Get the language, 'xml:lang' attribute need hack to read properly
    if lang in languages and (type and type_priority[type] < langLevel[languages.index(lang)] or not type):  langTitles[languages.index(lang)  ], langLevel [languages.index(lang)  ] = title.text, type_priority [ type ]
    if type=='main':                                                                                         langTitles[languages.index('main')], langLevel [languages.index('main')] = title.text, type_priority [ type ]
    if lang==languages[0] and type in ['main', ""]:  break
  Log.Info("getAniDBTitle - languages: '%s', langLevel: '%s', langTitles: '%s'" % (str(languages), str(langLevel), str(langTitles)))
  for title in langTitles:
    if title:  return title.replace("`", "'").encode("utf-8"), langTitles[languages.index('main')].replace("`", "'").encode("utf-8")
  else:  return '', ''

### ###
def GetMetadata(AniDBid):
  ANIDB_HTTP_API_URL      = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='          #
  ANNid, MALid,  = "", "", {}
  AniDBxml = common.LoadFile(filename=AniDBid+".xml", relativeDirectory="AniDB", url=ANIDB_HTTP_API_URL + AniDBid, cache=CACHE_1HOUR * 24 * 7)  # AniDB title database loaded once every 2 weeks
  if AniDBxml:
    ANNid = AniDBxml.xpath("/anime/resources/resource[@type='1']/externalentity/identifier")[0].text
    MALid = AniDBxml.xpath("/anime/resources/resource[@type='2']/externalentity/identifier")[0].text
    Log.Info("AniDB.get_metadata() - ANNid: '%s', MALid: '%s', xml loaded: '%s'" % (ANNid, MALid, str(AniDBxml is not None)))
    #AniDB_meta = {'title': "Title AniDB", 'summary': "Summary AniDB", "rating": "4.2"}
    #AniDBdict
  
  else: Log.Info("AniDB.get_metadata() - AniDB Serie XML: '%s', file: '%s" % (ANIDB_HTTP_API_URL + AniDBid, "AniDB/%s.xml" % AniDBid))
  return ANNid, MALid, AniDBxml

# AniDB Poster
def GetImages (metadata, AniDBxml, error_log, num=99):
  url = ANIDB_PIC_BASE_URL + GetElementText(AniDBxml, 'picture') if GetElementText(AniDBxml, 'picture') else ""
  Log.Info("AniDB.GetImages() - Poster url: '%s', AniDBxml: '%s'" % (url, "Present" if AniDBxml else ""))
  if Prefs['AniDB'] and GetPosters():
    if GetElementText(AniDBxml, 'picture'):  common.metadata_download(metadata, metadata.posters, url, num, "AniDB/%s" % GetElementText(AniDBxml, 'picture')) 
    else:                                    error_log['AniDB posters missing'].append("AniDBid: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid) + " | Title: '%s'" % metadata.title))

### AniDB collection mapping - complement AniDB movie collection file with related anime AND series sharing the same TVDBid ########################
def anidbCollectionMapping(metadata, media, AniDBxml, mappingList, AniDBMovieSets, TVDBid):
  AniDBid_source, AniDBid = metadata.id.split('-', 1)
  AniDBid_table                   = mappingList['poster_id_array'][TVDBid] if 'poster_id_array' in mappingList and TVDBid in mappingList['poster_id_array'] else []
  related_anime_list              = []
  for anime in AniDBMovieSets.iter("anime") if AniDBMovieSets else []:
    if TVDBid == anime.get('TVDBid'):  AniDBid_table.append( AniDBxml.get("anidbid") ) #collection gathering
  for relatedAnime in anime.xpath('/anime/relatedanime/anime'):  related_anime_list.append(relatedAnime.get('id'));
  metadata.collections.clear()
  for element in AniDBMovieSets.iter("anime") if AniDBMovieSets else []:
    if element.get('AniDBid') in related_anime_list + AniDBid_table + [AniDBid] and AniDBid_source == "anidb":
      set         = element.getparent()
      title, main = getAniDBTitle(set.xpath('titles')[0])
      metadata.collections.add(title) #metadata.collections.clear()
      Log.Info("AniDBid '%s' is part of movie collection: %s', related_anime_list: '%s', " % (AniDBid, title, str(related_anime_list)))
      break
  else:  Log.Info("AniDBid is not part of any collection, related_anime_list: '%s'" % str(related_anime_list)) 
  
  StreamTypes = {1: "video", 2: "audio", 3: "subtitle"}
  try:
    for season in media.seasons:
      for episode in media.seasons[season].episodes:
        for item in media.seasons[season].episodes[episode].items:
          for part in item.parts:
            for stream in part.streams:
              Log.Info("stream.type: '%s' ('%s'), stream.language: '%s'" % (stream.type, StreamTypes[stream.type], stream.language if hasattr(stream, 'language') else "N/A"))
            else:
              Log.Info("processed all streams")
              return
  except Exception as e:  Log.Info("streams - error: '%s'" % e)
 
### AniDB Creator data -  Aside from the animation studio, none of this maps to Series entries, so save it for episodes ###
def AniDB_creator_data(metadata, AniDBxml, movie, mapping_studio):
  roles     = { "Animation Work":"studio", "Direction":"directors", "Series Composition":"producers", "Original Work":"writers", "Script":"writers", "Screenplay":"writers" }
  role_list = {'directors': [],                 'producers': [],                 'writers': [],                 'studio': []}
  log_string = "AniDB Creator data: "
  for creator in AniDBxml.xpath('creators/name'):
    for role in roles: 
      if role in creator.get('type'):
        role_list [ roles[role] ].append(creator.text)
        log_string += "%s (%s), " % (creator.text, roles[role].rstrip('s') )
        break
  Log.Info(log_string)
  
  if movie:
    role_meta = {'directors': metadata.directors, 'producers': metadata.producers, 'writers': metadata.producers              }
    for role in role_list[:-1]:
      if cmp(role_meta[role], role_list[role]):  role_meta[role].clear(); [ role_meta[role].append(role2) for role2 in role_list[role] ]
      else:                                      Log.Info("Roles: '{role}': {name}'*".format(role=role, name= str([ role2 for role2 in role_list[role] ])))
  
  ### AniDB Cast - Get all the voice actors that voice main or secondary characters ###
  try:
    for role in metadata.roles:
      Log.Debug("metadata.roles.name: '%s'" % str(metadata.roles[role].name))
  except Exception as e:  Log.Error("role metadata: '%s'" % e)
  metadata.roles.clear()
  for character in AniDBxml.xpath("characters/character[(@type='secondary cast in') or (@type='main character in')]"):
    try:
      character_name = character.find('name').text
      seiyuu         = character.find('seiyuu')
      seiyuu_name    = seiyuu.text
      seiyuu_picture = ANIDB_PIC_BASE_URL + seiyuu.get('picture')
      Log.Debug("{seiyuu} voices {character} and has a profile picture at {url}".format(seiyuu=seiyuu_name, character=character_name, url=seiyuu_picture))
      #Log.Info("Prefs[{key:<{width}}] = {value}".format(key=key, width=max(map(len, DefaultPrefs)), value=Prefs[key]))
      role                             = metadata.roles.new()
      role.name, role.role, role.photo = seiyuu_name, character_name, seiyuu_picture
    except Exception as e:  Log.Error("Could not locate Seiyuu information for character ID {id}, Exception: {exception}".format(id=character.get('id'), exception=e))

  if metadata.studio       and mapping_studio and metadata.studio != mapping_studio: error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB has studio '%s' and anime-list has '%s' | "    % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, metadata.studio, mapping_studio) + common.WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(AniDBxml, encoding='utf8'))), "Submit bug report (need GIT account)"))
  if metadata.studio == "" and mapping_studio == "":                                 error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB and anime-list are both missing the studio" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title) )
  if metadata.studio == "" and mapping_studio:                                       metadata.studio = mapping_studio
  return role_list
 
### ###
def AniDB_content_rating(metadata, AniDBxml, movie, TVDBid, TheTVDBdict):
  c_source, c_rating, c_genre = 'None', 'None', 'No match'
  a_movie = True if (movie or AniDBxml.xpath('/anime/type')[0].text == "Movie" or TVDBid == 'movie' or 
                     "Complete Movie" in [titleText.text for titleText in AniDBxml.xpath('episodes/episode/title')]) else False
  if   'ContentRating' in TheTVDBdict: c_source, c_rating, c_genre = 'TVDB',    common.MOVIE_RATING_MAP[TheTVDBdict['ContentRating']] if a_movie else TheTVDBdict['ContentRating'], 'Rating flag'
  elif TVDBid=='hentai':              c_source, c_rating, c_genre = 'ScudLee', "X",                                                                                              'Hentai flag'
  else:
    anidb_genres = [GetElementText(tag, 'name').lower() for tag in AniDBxml.xpath('tags/tag')]
    result       = [(r, g) for r in common.RESTRICTED_GENRE for g in common.RESTRICTED_GENRE[r] if g in anidb_genres]  # List Comprehension: [word for sentence in text for word in sentence

### ###
def AniDB_summary(metadata, AniDBxml, error_log, tvdbOverview, AniDBid):
  try:                    description = re.sub(r'http://anidb\.net/[a-z]{1,2}[0-9]+ \[(.+?)\]', r'\1', GetElementText(AniDBxml, 'description')).replace("`", "'") # Remove wiki-style links to staff, characters etc
  except Exception as e:  description = ""; Log.Error("Exception: %s" % e)
  if not description:     error_log['AniDB summaries missing'].append("AniDBid: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid) + " | Title: '%s'" % metadata.title))
  if metadata.summary != description and description:  metadata.summary = description

### AniDB update meta information###
def UpdateMetadata(metadata, media, movie, AniDBxml, AniDBid, TVDBid, TheTVDBdict, mappingList, AniDBMovieSets, error_log, current_date):
  EPISODE_LANGUAGE_PRIORITY = [ Prefs['EpisodeLanguage1'], Prefs['EpisodeLanguage2'] ]                                           #override default language
  TVDB_IMAGES_URL = 'http://thetvdb.com/banners/'                                                                      # TVDB picture directory
  if AniDBxml:
    ### AniDB Title ###
    try:                    title, orig = getAniDBTitle(AniDBxml.xpath('/anime/titles/title'))
    except Exception as e:  Log.Error("AniDB Title: Exception raised, Exception: '%s'" % e)
    else:
      if title == str(metadata.title):  Log.Info("AniDB title: '%s', original title: '%s', metadata.title '%s'*" % (title, orig, metadata.title))
      elif title != "": #If title different but not empty [Failsafe]
        Log.Info("AniDB title: '%s', original title: '%s', metadata.title '%s'" % (title, orig, metadata.title))
        metadata.title = title
        if movie and orig != "" and orig != metadata.original_title: metadata.original_title = orig # If it's a movie, Update original title in metadata http://forums.plexapp.com/index.php/topic/25584-setting-metadata-original-title-and-sort-title-still-not-possible/
            
    ### AniDB Start Date ###
    if GetElementText(AniDBxml, 'startdate') == "":                                  Log.Info("AniDB Start Date: None")
    elif metadata.originally_available_at == GetElementText(AniDBxml, 'startdate'):  Log.Info("AniDB Start Date: '%s'*" % str(metadata.originally_available_at))
    else:
      metadata.originally_available_at = Datetime.ParseDate( GetElementText(AniDBxml, 'startdate') ).date()
      if movie: metadata.year          = metadata.originally_available_at.year
      Log.Info("AniDB Start Date: '%s'" % str(metadata.originally_available_at))
        
    ### AniDB Ratings ###
    misc = GetElementText(AniDBxml, 'ratings/permanent')
    if misc=="":                                         Log.Info("AniDB Ratings:    'None'")   
    elif '.' in misc and float(misc) == metadata.rating: Log.Info("AniDB Ratings:    '%s'*" % misc)
    else:                                                Log.Info("AniDB Ratings:    '%s'"  % misc);  metadata.rating = float( misc )
        
    ### AniDB Genres ###
    genres = {}
    for tag in AniDBxml.xpath('tags/tag'):
      this_tag = GetElementText(tag, 'name').lower()
      this_tag_caps = " ".join(string.capwords(tag_part, '-') for tag_part in this_tag.split())
      if int(tag.get('weight')) >= (400 if Prefs['MinimumWeight'] == None else int(Prefs['MinimumWeight'])): genres [ this_tag_caps ] = int(tag.get('weight'))
    sortedGenres = sorted(genres.items(), key=lambda x: x[1],  reverse=True)
    log_string, genres = "AniDB Genres (Weight): ", []
    for genre in sortedGenres: genres.append(genre[0].encode("utf-8") )
    if sorted(metadata.genres)==sorted(genres): Log.Info(log_string+str(sortedGenres)+"*") 
    else:
      Log.Info("genres: " + str(sortedGenres) + " " + str(genres))
      metadata.genres.clear()
      for genre in sortedGenres:
        metadata.genres.add(genre[0])
        log_string += "%s (%s) " % (genre[0], str(genre[1]))
      Log.Info(log_string)

    ### AniDB Content Rating ###
    AniDB_content_rating          (metadata, AniDBxml, movie, TVDBid, TheTVDBdict)
    anidbCollectionMapping        (metadata, media, AniDBxml, mappingList, AniDBMovieSets, TVDBid)
    plex_role = AniDB_creator_data(metadata, AniDBxml, movie, mappingList['mapping_studio'] if 'mapping_studio' in mappingList else "")
    AniDB_summary                 (metadata, AniDBxml, error_log, TheTVDBdict ['Overview'] if 'Overview' in TheTVDBdict and TheTVDBdict['Overview'] else "", AniDBid)
            
    ### AniDB Posters ###
    #Log.Info("AniDB Poster, url: '%s'" % (ANIDB_PIC_BASE_URL + GetElementText(AniDBxml, 'picture')))
    #if GetElementText(AniDBxml, 'picture') == "": error_log['AniDB posters missing'].append("AniDBid: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid) + " | Title: '%s'" % metadata.title))
    #elif Prefs['AniDB']:  common.metadata_download(metadata, metadata.posters, ANIDB_PIC_BASE_URL + GetElementText(AniDBxml, 'picture'), 99, "AniDB/%s" % GetElementText(AniDBxml, 'picture')) 

    if not movie: ### TV Serie specific #################################################################################################################
      numEpisodes, totalDuration, mapped_eps, missing_eps, missing_specials, ending_table, op_nb = 0, 0, [], [], [], {}, 0 
      specials = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
        
      for episode in AniDBxml.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################
        ep_title, main   = getAniDBTitle (episode.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
        epNum,    eid    = episode.xpath('epno')[0], episode.get('id')
        epNumType        = epNum.get('type')
        season, epNumVal = "1" if epNumType == "1" else "0", epNum.text if epNumType == "1" else str( specials[ epNum.text[0] ][0] + int(epNum.text[1:]))
        if epNumType=="3":
          if ep_title.startswith("Ending"):
            if op_nb==0: op_nb = int(epNum.text[1:])-1 #first type 3 is first ending so epNum.text[1:] -1 = nb openings
            epNumVal = str( int(epNumVal) +50-op_nb)   #shifted to 150 for 1st ending.  
          Log.Info("AniDB specials title - Season: '%s', epNum.text: '%s', epNumVal: '%s', ep_title: '%s'" % (season, epNum.text, epNumVal, ep_title) )
         
        if not (season in media.seasons and epNumVal in media.seasons[season].episodes):  #Log.Debug("Season: '%s', Episode: '%s' => '%s' not on disk" % (season, epNum.text, epNumVal) )
          current_air_date = GetElementText(episode, 'airdate').replace('-','')
          current_air_date = int(current_air_date) if current_air_date.isdigit() and int(current_air_date) > 10000000 else 99999999
          if current_date <= (current_air_date+1):  Log.Warn("Episode '%s' is missing in Plex but air date '%s+1' is either missing (99999999) or in the future" % (epNumVal, current_air_date)); continue
          if epNumType == "1"  : missing_eps.append(     "s" + season + "e" + epNumVal )
          elif epNumType == "2": missing_specials.append("s" + season + "e" + epNumVal ) 
          continue
        episodeObj = metadata.seasons[season].episodes[epNumVal]
        
        ### AniDB Get the correct episode title ###
        if episodeObj.title == ep_title:  Log.Info("AniDB episode title: '%s'*" % ep_title) 
        else:                             Log.Info("AniDB episode title: '%s'"  % ep_title); episodeObj.title = ep_title
        
        ### AniDBN turn the YYYY-MM-DD airdate in each episode into a Date ###
        airdate, originally_available_at = GetElementText(episode, 'airdate'), None
        if airdate:
          match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", airdate)
          if match:
            try:                   originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError, e:  Log.Error("AniDB parseAirDate - Date out of range: " + str(e))
        if originally_available_at == episodeObj.originally_available_at: Log.Info("AniDB AirDate '%s'*" % airdate)
        else:                                                             Log.Info("AniDB AirDate '%s'"  % airdate);  episodeObj.originally_available_at = originally_available_at
        
        ### AniDB Duration ###
        if GetElementText(episode, 'length'):
          duration = int(GetElementText(episode, 'length')) * 1000 * 60  # Plex save duration in millisecs, AniDB stores it in minutes
          if episodeObj.duration == duration:  Log.Info("AniDB duration: '%d'*" % duration)
          else:                                Log.Info("AniDB duration: '%d'"  % duration);  episodeObj.duration = duration;               
          if season == "1": numEpisodes, totalDuration = numEpisodes + 1, totalDuration + episodeObj.duration
        
        ### AniDB Writers, Producers, Directors ###  #Log.Debug("### AniDB Writers, Producers, Directors ### ")
        Log.Info("Processing writers and directors for Episode.")
        episodeObj.writers.clear()
        episodeObj.directors.clear()
        for role in plex_role:
          for person in plex_role[role]:
            # Note: Writer/Director metadata is only written when the show is refreshed, not the episode.
            if role=="writers":
              meta_writer = episodeObj.writers.new()
              Log.Debug("Adding new Writer {name}".format(name=person))
              meta_writer.name = person
            if role=="directors":
              meta_director = episodeObj.directors.new()
              Log.Debug("Adding new Director {name}".format(name=person))
              meta_director.name = person
        
        ### Rating ###
        rating = GetElementText(episode, 'rating') #if rating =="":  Log.Debug(metadata.id + " Episode rating: ''") #elif rating == episodeObj.rating:  Log.Debug(metadata.id + " update - Episode rating: '%s'*" % rating )
        if not rating =="" and re.match("^\d+?\.\d+?$", rating):  episodeObj.rating = float(rating) #try: float(element) except ValueError:     print "Not a float"
        
        ### TVDB mapping episode summary ###
        try:
          if TVDBid.isdigit():
            anidb_ep, tvdb_ep, summary= 's' + season + 'e' + epNumVal, "", "No summary in TheTVDB.com" #epNum
            if anidb_ep in mappingList and mappingList[anidb_ep] in TheTVDBdict:  tvdb_ep = mappingList [ anidb_ep ]
            elif 's'+season in mappingList and int(epNumVal) >= int (mappingList['s'+season][0]) and int(epNumVal) <= int(mappingList['s'+season][1]): tvdb_ep = str( int(mappingList['s'+season][2]) + int(epNumVal) )  # season offset + ep number
            elif mappingList['defaulttvdbseason']=="a" and epNumVal in TheTVDBdict:              tvdb_ep = str( int(epNumVal) + ( int(mappingList [ 'episodeoffset' ]) if 'episodeoffset' in mappingList and mappingList [ 'episodeoffset' ].isdigit() else 0 ) )
            elif season=="0":                                                    tvdb_ep = "s"+season+"e"+epNumVal
            else:                                                                tvdb_ep = "s"+mappingList['defaulttvdbseason']+"e"+ str(int(epNumVal) + ( int(mappingList[ 'episodeoffset' ]) if 'episodeoffset' in mappingList and mappingList [ 'episodeoffset' ].isdigit() else 0 ))

            summary = "TVDB summary missing" if tvdb_ep=="" or tvdb_ep not in TheTVDBdict else TheTVDBdict [tvdb_ep] ['Overview'].replace("`", "'")
            if re.match("^Episode [0-9]{1,4}$", episodeObj.title) and tvdb_ep in TheTVDBdict: 
              ep_title = TheTVDBdict [tvdb_ep] ['EpisodeName'];
              #episodeObj.title = ep_title
              Log.Warn("AniDB episode title is missing but TVDB has one availabe so using it.")
            mapped_eps.append( anidb_ep + ">" + tvdb_ep )
            Log.Info("TVDB mapping episode summary - anidb_ep: '%s', tvdb_ep: '%s', season: '%s', epNumVal: '%s', mappingList['defaulttvdbseason']: '%s', title: '%s', summary: '%s'" %(anidb_ep, tvdb_ep, season, epNumVal, mappingList['defaulttvdbseason'], ep_title, TheTVDBdict [tvdb_ep] ['Overview'][0:50].strip() if tvdb_ep in TheTVDBdict else "") )
            episodeObj.summary = summary           
        except Exception as e:
          Log.Error("Issue in 'TVDB mapping episode summary', epNumVal: '%s'", epNumVal)
          Log.Error("mappingList = %s" % mappingList)
          Log.Error("Exception: %s" % e)
      ## End of "for episode in AniDBxml.xpath('episodes/episode'):" ### Episode Specific ###########################################################################################
      
      ### AniDB Missing Episodes ###
      #Log.Debug("type: %s , ep1 title: %s" % (AniDBxml.xpath('/anime/type')[0].text, AniDBxml.xpath('episodes/episode/title')[0].text))
      if len(missing_eps)>0 and AniDBxml.xpath('/anime/type')[0].text == "Movie" and "Complete Movie" in [titleText.text for titleText in AniDBxml.xpath('episodes/episode/title')]:
        movie_ep_groups = [ {}, {}, {}, {}, {}, {}, {} ]
        for episode in AniDBxml.xpath('episodes/episode'):
          epNum     = episode.xpath('epno')[0]
          epTitle   = episode.xpath('title')[0]
          epNumType = epNum.get('type')
          season    = "1" if epNumType == "1" else "0"
          if season == "0": continue
          epNumVal  = "s%se%s" % (season, epNum.text)

          part_group = -1
          if epTitle.text == "Complete Movie": part_group = 0
          if epTitle.text.startswith("Part "): part_group = int(epTitle.text[-1]) if epTitle.text[-1].isdigit() else -1
          if part_group != -1: movie_ep_groups[part_group][epNumVal] = 'found'
          #Log.Debug("orig movie_ep_groups: " + str(movie_ep_groups))
          #Log.Debug("orig missing_eps: " + str(missing_eps))
        for missing_ep in missing_eps:
          for movie_ep_group in movie_ep_groups:
            if missing_ep in movie_ep_group.keys(): movie_ep_group[missing_ep] = 'missing'
        Log.Debug("movie_ep_groups: " + str(movie_ep_groups))
        missing_eps = []
        for movie_ep_group in movie_ep_groups:
          if 'found' in movie_ep_group.keys() and 'missing' in movie_ep_group.keys():
            for key in movie_ep_group.keys():
              if movie_ep_group[key] == 'missing': missing_eps.append(key)
        Log.Debug("new missing_eps: " + str(missing_eps))
          
      if len(missing_eps     )>0:
        missing_eps = sorted(missing_eps, key=lambda x: int("%d%04d" % (int(x.split('e')[0][1:]), int(x.split('e')[1]))))
        error_log['Missing Episodes'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, str(missing_eps)))
      if len(missing_specials)>0:
        missing_specials = sorted(missing_specials, key=lambda x: int("%d%04d" % (int(x.split('e')[0][1:]), int(x.split('e')[1]))))
        error_log['Missing Specials'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, str(missing_specials)))
      
      convert      = lambda text: int(text) if text.isdigit() else text
      alphanum_key = lambda key:  [ convert(c) for c in re.split('([0-9]+)', key) ]
      
      ### AniDB Final post-episode titles cleanup ###
      Log.Info("DURATION: %s, numEpisodes: %s" %(str(totalDuration), str(numEpisodes)) )
      if numEpisodes: metadata.duration = int(totalDuration) / int(numEpisodes) #if movie getting scrapped as episode number by scanner...
    ### End of if anime is not None: ###
  ### End of elif not metadata.title and tvdbtitle: ###
### elif AniDBid_source == "anidb": ###
