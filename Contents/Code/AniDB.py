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

# AniDB 
def GetAniDBTitlesDB():
  ANIDB_TITLES  = 'http://anidb.net/api/anime-titles.xml.gz'               # AniDB title database file contain all ids, all languages  #http://bakabt.info/anidb/animetitles.xml
  AniDBTitlesDB = common.LoadFile(filename=os.path.basename(ANIDB_TITLES), relativeDirectory="", url=ANIDB_TITLES, cache= CACHE_1HOUR * 24 * 14)  # AniDB title database loaded once every 2 weeks
  if not AniDBTitlesDB:  raise Exception("Failed to load core file '{url}'".format(url=os.path.splitext(os.path.basename(ANIDB_TITLES))[0]))
  return AniDBTitlesDB

#def Search_AniDB_Exact_Title():
def Search (results, media, lang, manual, movie, AniDBTitlesDB):
  Log.Info("--- AniDB.Search() - Begin --------------------------------------------------------------------------------------------------")
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
    if source.startswith("anidb"):  show, mainTitle = GetAniDBTitle(AniDBTitlesDB.xpath("/animetitles/anime[@aid='%s']/*" % guid))
    Log.Info("source: '%s', id: '%s', foldername show title: '%s', from title database id: '%s'" % (source, guid, orig_title, show) )
    results.Append(MetadataSearchResult(id="%s-%s" % (source, guid), name=show, year=media.year, lang=lang, score=100))
    Log.Info("".ljust(157, '-'))
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
        langTitle, mainTitle = GetAniDBTitle(parent_element)
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
    langTitle, mainTitle = GetAniDBTitle(parent_element)
    results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (langTitle, "anidb", aid), year=media.year, lang=lang, score=score))
  if len(results)>=1:  Log.Info("".ljust(157, '-')); return  #results.Sort('score', descending=True)
  
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
  Log.Info("".ljust(157, '-'))
  return maxi

### Extract the series/movie/Episode title from AniDB ########################################################################################################################
def GetAniDBTitle(titles, lang=None):
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
  #Log.Info("GetAniDBTitle() - languages: '%s', langLevel: '%s', langTitles: '%s'" % (str(languages), str(langLevel), str(langTitles)))
  for title in langTitles:
    if title:  return title.replace("`", "'").encode("utf-8"), langTitles[languages.index('main')].replace("`", "'").encode("utf-8")
  else:  return '', ''

### ###
def GetMetadata(metadata, media, movie, error_log, AniDBMovieSets, AniDBid, TVDBid, mappingList):
  ANIDB_HTTP_API_URL        = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='
  EPISODE_LANGUAGE_PRIORITY = [ Prefs['EpisodeLanguage1'], Prefs['EpisodeLanguage2'] ]
  RESTRICTED_GENRE          = {'X': ["18 restricted", "pornography"], 'TV-MA': ["tv censoring", "borderline porn"]}
  #http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=6481
    
  Log.Info("".ljust(157, '-'))
  Log.Info("AniDB.GetMetadata() - AniDB Serie XML: '%s', file: '%s" % (ANIDB_HTTP_API_URL + AniDBid, "AniDB/%s.xml" % AniDBid))
  ANNid, MALid, ANFOid, AniDB_dict = "", "", "", {}
  AniDBxml = common.LoadFile(filename=AniDBid+".xml", relativeDirectory="AniDB", url=ANIDB_HTTP_API_URL + AniDBid, cache=CACHE_1HOUR * 24 * 7)  # AniDB title database loaded once every 2 weeks
  if AniDBxml:
    
    ### Common to Movies and Series Libraries
    # 'title'
    # 'original_title'
    AniDB_dict['title'], AniDB_dict['original_title'] = GetAniDBTitle(AniDBxml.xpath('/anime/titles/title'))
    if AniDB_dict['title']==AniDB_dict['original_title']:  AniDB_dict.pop('original_title', None)
    
    # 'summary'
    AniDB_dict['summary'] = re.sub(r'http://anidb\.net/[a-z]{1,2}[0-9]+ \[(.+?)\]', r'\1', GetElementText(AniDBxml, 'description')).replace("`", "'") # Remove wiki-style links to staff, characters etc
    
    # 'originally_available_at'
    AniDB_dict['originally_available_at'] = Datetime.ParseDate( GetElementText(AniDBxml, 'startdate') ).date()
    
    # 'duration'
    ### not listed for serie but is for eps
    
    # 'studio'
    # 'writers'
    # 'directors'
    # 'producers'
    roles = { "Animation Work":"studio", "Direction":"directors", "Series Composition":"producers", "Original Work":"writers", "Script":"writers", "Screenplay":"writers" }
    ep_roles = {}
    for creator in AniDBxml.xpath('creators/name'):
      for role in roles: 
       if role in creator.get('type'):
        if roles[role] in ep_roles:  ep_roles [roles[role]].append(creator.text)
        else:                        ep_roles [roles[role]] = [creator.text] if not roles[role]=="studio" else creator.text
           
    #roles  ### NEW, NOT IN Plex FrameWork Documentation 2.1.1 ###
    for character in AniDBxml.xpath("characters/character[(@type='secondary cast in') or (@type='main character in')]"):
      try:
        seyuu_dict = {'role': character.find('name').text, 'name': character.find('seiyuu').text, 'photo': ANIDB_PIC_BASE_URL + character.find('seiyuu').get('picture')}
        if 'roles' in AniDB_dict:  AniDB_dict ['roles'].append(seyuu_dict)
        else:                     AniDB_dict ['roles'] = [seyuu_dict]
      except:  pass     #"characters/character[((@type='secondary cast in') or (@type='main character in')) and /seiyuu]
      
    # 'rating'
    AniDB_dict['rating'] = float(GetElementText(AniDBxml, 'ratings/permanent'))
    
    # 'content_rating'
    # 'genres'
    genres = []
    for tag in AniDBxml.xpath('tags/tag'):
      if int(tag.get('weight')) >= (int(Prefs['MinimumWeight'])):
        if 'genres' in AniDB_dict:  AniDB_dict ['genres'].append( string.capwords(GetElementText(tag, 'name').lower(), '-') )
        else:                      AniDB_dict ['genres'] = [     string.capwords(GetElementText(tag, 'name').lower(), '-') ]
        for content_rating_key in RESTRICTED_GENRE:
          if GetElementText(tag, 'name').lower() in RESTRICTED_GENRE[content_rating_key]:  AniDB_dict['content_rating'] = content_rating_key

    # 'tags'
    # 'collections'
    AniDBid_source, AniDBid = metadata.id.split('-', 1)
    AniDBid_table           = mappingList['poster_id_array'][TVDBid] if 'poster_id_array' in mappingList and TVDBid in mappingList['poster_id_array'] else []
    #for anime in AniDBMovieSets.iter("anime") if AniDBMovieSets else []:
    #  if TVDBid == anime.get('TVDBid'):  AniDBid_table.append( anime.get("anidbid") ) #collection gathering
    for relatedAnime in AniDBxml.xpath('/anime/relatedanime/anime'):
      if relatedAnime.get('id') not in AniDBid_table: AniDBid_table.append(relatedAnime.get('id'))
    
    for element in AniDBMovieSets.iter("anime") if AniDBMovieSets else []:
      if AniDBid == element.get('AniDBid') or element.get('AniDBid') in AniDBid_table:
        node        = element.getparent()
        title, main = GetAniDBTitle(node.xpath('titles')[0])
        if 'collection' in AniDB_dict:  AniDB_dict ['collection'].append(title)
        else:                           AniDB_dict ['collection'] = [title]
        Log.Info("AniDB.GetMetadata() - AniDBid '%s' is part of movie collection: %s', related_anime_list: '%s', " % (AniDBid, title, str(related_anime_list)))
        break
    #else:  Log.Info("AniDBid is not part of any collection, related_anime_list: '%s'" % str(AniDBid_table)) 
  
    StreamTypes = {1: "video", 2: "audio", 3: "subtitle"}
    dub = False
    sub = False
    try:
      for season in media.seasons:
        for episode in media.seasons[season].episodes:
          for item in media.seasons[season].episodes[episode].items:
            for part in item.parts:
              for stream in part.streams:
                Log.Info("stream.type: '%s' ('%s'), stream.language: '%s'" % (stream.type, StreamTypes[stream.type], stream.language if hasattr(stream, 'language') else "N/A"))
                if StreamTypes[stream.type] == "audio"    and hasattr(stream, 'language'): # and stream.language == "eng":
                  Log.Info("GetMetadata() - " + stream.language + " Dubbed")
                  if 'collection' in AniDB_dict:  AniDB_dict ['collection'].append( stream.language + " Dubbed" )
                  else:                          AniDB_dict ['collection'] =     [ stream.language + " Dubbed" ] 
                if StreamTypes[stream.type] == "audio"    and hasattr(stream, 'language') and stream.language == "jpn" and \
                   StreamTypes[stream.type] == "subtitle" and hasattr(stream, 'language') and stream.language == "eng":
                  Log.Info("GetMetadata() - " + stream.language + " Dubbed")
                  if 'collection' in AniDB_dict:  AniDB_dict ['collection'].append( stream.language + " Subbed" )
                  else:                          AniDB_dict ['collection'] =     [ stream.language + " Subbed" ] 
              #else:  Log.Info("processed all streams")
              break
            break
          break
        break
    except Exception as e:  Log.Info("streams - error: '%s'" % e)

    # 'art'
    # 'posters'
    # 'themes'
    if GetElementText(AniDBxml, 'picture'):  AniDB_dict['posters'] = {ANIDB_PIC_BASE_URL + GetElementText(AniDBxml, 'picture'): ( "AniDB/%s" % GetElementText(AniDBxml, 'picture'), 99, None)}
    
    # 'tagline'
    
    if movie:  #Movie Library
      
      # 'year'
      if AniDB_dict['originally_available_at']:  AniDB_dict['year'] = AniDB_dict['originally_available_at'].year
      
      # 'quotes'
      # 'trivia'
    
    else:  # TV Series Library
      # summary
      #AniDB_dict['season'] = re.sub(r'http://anidb\.net/[a-z]{1,2}[0-9]+ \[(.+?)\]', r'\1', GetElementText(AniDBxml, 'description')).replace("`", "'") # Remove wiki-style links to staff, characters etc
    
      # 'seasons'
      # 'countries'
      # 'banners'

      ### Seasons
      # 'summary'
      # 'posters'
      # 'banners'
      # 'episodes'
      
      ### Translate into season/episode mapping
      
      numEpisodes, totalDuration, mapped_eps, missing_eps, missing_specials, ending_table, op_nb = 0, 0, [], [], [], {}, 0 
      specials = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
      for ep_obj in AniDBxml.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################
        epNum,    eid    = ep_obj.xpath('epno')[0], ep_obj.get('id')
        epNumType        = epNum.get('type')
        season, episode = "1" if epNumType == "1" else "0", epNum.text if epNumType == "1" else str( specials[ epNum.text[0] ][0] + int(epNum.text[1:]))
        if epNumType=="3":
          if ep_title.startswith("Ending"):
            if op_nb==0: op_nb = int(epNum.text[1:])-1 #first type 3 is first ending so epNum.text[1:] -1 = nb openings
            episode = str( int(episode) +50-op_nb)     #shifted to 150 for 1st ending.  
          #Log.Info("AniDB specials title - Season: '%s', epNum.text: '%s', episode: '%s', ep_title: '%s'" % (season, epNum.text, episode, ep_title) )
        
        if not (season in media.seasons and episode in media.seasons[season].episodes):
          current_air_date = GetElementText(ep_obj, 'airdate').replace('-','')
          current_air_date = int(current_air_date) if current_air_date.isdigit() and int(current_air_date) > 10000000 else 99999999
          if int(time.strftime("%Y%m%d")) <= (current_air_date+1):  Log.Warn("AniDB.get_metadata() - Episode '%s' is missing in Plex but air date '%s+1' is either missing (99999999) or in the future" % (episode, current_air_date)); continue
          if   epNumType == "1": missing_eps.append(     "s" + season + "e" + episode )
          elif epNumType == "2": missing_specials.append("s" + season + "e" + episode ) 
          continue
        episode_obj = metadata.seasons[season].episodes[episode]
        
        ### Episodes
      
        # 'absolute_index'
        # 'title'
        ep_title, main   = GetAniDBTitle (ep_obj.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
        if not 'seasons'  in AniDB_dict:                                 AniDB_dict['seasons']                              = {}
        if not  season    in AniDB_dict['seasons']:                      AniDB_dict['seasons'][season]                      = {}
        if not 'episodes' in AniDB_dict['seasons'][season]:              AniDB_dict['seasons'][season]['episodes']          = {}
        if not  episode   in AniDB_dict['seasons'][season]['episodes']:  AniDB_dict['seasons'][season]['episodes'][episode] = {}
        AniDB_dict['seasons'][season]['episodes'][episode]['title'] = ep_title
        
        # 'originally_available_at'
        if GetElementText(ep_obj, 'airdate'):
          match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", GetElementText(ep_obj, 'airdate'))
          if match:
            try:                   AniDB_dict['seasons'][season]['episodes'][episode]['originally_available_at'] = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError, e:  Log.Error("AniDB parseAirDate - Date out of range: " + str(e))
        
        # 'duration'
        if GetElementText(ep_obj, 'length'):
          AniDB_dict['seasons'][season]['episodes'][episode]['duration'] = int(GetElementText(ep_obj, 'length')) * 1000 * 60  # AniDB stores it in minutes, Plex save duration in millisecs
          if season == "1": numEpisodes, totalDuration = numEpisodes + 1, totalDuration + episode_obj.duration
        
        # 'rating'
         #if rating =="":  Log.Debug(metadata.id + " Episode rating: ''") #elif rating == episode_obj.rating:  Log.Debug(metadata.id + " update - Episode rating: '%s'*" % rating )
        if GetElementText(ep_obj, 'rating') and re.match("^\d+?\.\d+?$", GetElementText(ep_obj, 'rating')):
          AniDB_dict['seasons'][season]['episodes'][episode]['rating'] = float(GetElementText(ep_obj, 'rating')) #try: float(element) except ValueError:     print "Not a float"
              
        # 'summary'
        # 'thumbs'
        # 'writers'
        # 'directors'
        # 'producers'

      ### AniDB Missing Episodes ###
      if len(missing_eps)>0 and AniDBxml.xpath('/anime/type')[0].text == "Movie" and "Complete Movie" in [titleText.text for titleText in AniDBxml.xpath('episodes/episode/title')]:
        movie_ep_groups = [ {}, {}, {}, {}, {}, {}, {} ]
        for episode in AniDBxml.xpath('episodes/episode'):
          epNum     = ep_obj.xpath('epno')[0]
          epTitle   = ep_obj.xpath('title')[0]
          epNumType = epNum.get('type')
          season    = "1" if epNumType == "1" else "0"
          if season == "0": continue
          episode  = "s%se%s" % (season, epNum.text)

          part_group = -1
          if epTitle.text == "Complete Movie": part_group = 0
          if epTitle.text.startswith("Part "): part_group = int(epTitle.text[-1]) if epTitle.text[-1].isdigit() else -1
          if part_group != -1: movie_ep_groups[part_group][episode] = 'found'
          #Log.Debug("orig movie_ep_groups: " + str(movie_ep_groups))
          #Log.Debug("orig missing_eps: " + str(missing_eps))
        for missing_ep in missing_eps:
          for movie_ep_group in movie_ep_groups:
            if missing_ep in movie_ep_group.keys(): movie_ep_group[missing_ep] = 'missing'
        Log.Debug("AniDB.get_metadata() - movie_ep_groups: " + str(movie_ep_groups))
        missing_eps = []
        for movie_ep_group in movie_ep_groups:
          if 'found' in movie_ep_group.keys() and 'missing' in movie_ep_group.keys():
            for key in movie_ep_group.keys():
              if movie_ep_group[key] == 'missing': missing_eps.append(key)
        Log.Debug("AniDB.get_metadata() - new missing_eps: " + str(missing_eps))
          
      if len(missing_eps     )>0:
        missing_eps = sorted(missing_eps, key=lambda x: int("%d%04d" % (int(x.split('e')[0][1:]), int(x.split('e')[1]))))
        error_log['Missing Episodes'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, str(missing_eps)))
      if len(missing_specials)>0:
        missing_specials = sorted(missing_specials, key=lambda x: int("%d%04d" % (int(x.split('e')[0][1:]), int(x.split('e')[1]))))
        error_log['Missing Specials'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, str(missing_specials)))
      
      convert      = lambda text: int(text) if text.isdigit() else text
      alphanum_key = lambda key:  [ convert(c) for c in re.split('([0-9]+)', key) ]
      
      ### AniDB Final post-episode titles cleanup ###
      Log.Info("AniDB.get_metadata() - DURATION: %s, numEpisodes: %s" %(str(totalDuration), str(numEpisodes)) )
      if numEpisodes: metadata.duration = int(totalDuration) / int(numEpisodes) #if movie getting scrapped as episode number by scanner...
      ### End of if anime is not None: ###
       
    # Logs
    if not AniDB_dict['summary']:  error_log['AniDB summaries missing'].append("AniDBid: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid) + " | Title: '%s'" % metadata.title))
    if not AniDB_dict['posters']:  error_log['AniDB posters missing  '].append("AniDBid: %s" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid) + " | Title: '%s'" % metadata.title))
    if metadata.studio       and 'studio' in AniDB_dict and AniDB_dict ['studio'] and AniDB_dict ['studio'] != metadata.studio:  error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB has studio '%s' and anime-list has '%s' | "    % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, metadata.studio, mapping_studio) + common.WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(AniDBxml, encoding='utf8'))), "Submit bug report (need GIT account)"))
    if metadata.studio == "" and 'studio' in AniDB_dict and AniDB_dict ['studio'] == "":                                        error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB and anime-list are both missing the studio" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title) )

    # ANNid, MALid
    ANNid  = AniDBxml.xpath("/anime/resources/resource[@type='1']/externalentity/identifier")[0].text
    MALid  = AniDBxml.xpath("/anime/resources/resource[@type='2']/externalentity/identifier")[0].text
    ANFOid = (AniDBxml.xpath("/anime/resources/resource[@type='3']/externalentity/identifier")[0].text, AniDBxml.xpath("/anime/resources/resource[@type='3']/externalentity/identifier")[1].text)
  Log.Info("AniDB.get_metadata() - ANNid: '%s', MALid: '%s', ANFOid: '%s', xml loaded: '%s'" % (ANNid, MALid, ANFOid, str(AniDBxml is not None)))
  return ANNid, MALid, AniDB_dict
