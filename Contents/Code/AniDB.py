# -*- coding: utf-8 -*-

### AniBD ###
#http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=6481

### Imports ###
import common    # Functions: SaveFile, LoadFile, metadata_download, WriteLogs, cleanse_title, getImagesFromASS
import os        # Functions: 
import re        # Functions: re.search, re.match, re.sub, re.IGNORECASE
import string    # Functions: 
import datetime  # Functions: 
import time      # Functions: 
import AnimeLists
from common import GetXml, Dict, SaveDict, natural_sort_key
from lxml import etree
ns = etree.FunctionNamespace(None)
ns['lower-case' ] = lambda context, s: s[0].lower()
ns['clean-title'] = lambda context, s: common.cleanse_title(s)
  
### Variables ###

### Functions ###

### ###
def GetMetadata(media, movie, error_log, source, AniDBid, TVDBid, AniDBMovieSets, mappingList):
  ANIDB_HTTP_API_URL       = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='
  ANIDB_PIC_BASE_URL       = 'http://img7.anidb.net/pics/anime/'                                                                # AniDB picture directory
  ANIDB_PIC_THUMB_URL      = 'http://img7.anidb.net/pics/anime/thumbs/150/{}.jpg-thumb.jpg' 
  AniDB_dict, ANNid, MALid = {}, "", ""
  original                 = AniDBid
  
  ### Build the list of anidbids for files present ####
  Log.Info("".ljust(157, '-'))
  if source.startswith("tvdb") or source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))>1:  #multi anidbid required only for tvdb numbering
    Log.Info(str(mappingList))  #{'defaulttvdbseason': '1', 'name': 'Sword Art Online', 'episodeoffset': '0'}
    full_array  = [ anidbid for season in Dict(mappingList, 'TVDB') or [] for anidbid in Dict(mappingList, 'TVDB', season) if season and 'e' not in season and anidbid.isdigit() ]
    AniDB_array = []
    for season in sorted(media.seasons, key=common.natural_sort_key) if not movie else []:  # For each season, media, then use metadata['season'][season]...
      
      #Season check
      if len(Dict(mappingList, 'TVDB', 's'+season))==1: #import anidbif if one instance of the defaulttvdbseason exist as it has files
        if AniDBid and AniDBid not in AniDB_array:  AniDB_array.append(AniDBid);  continue
      
      #Episode check if more than 1 anidnid for this season
      for episode in sorted(media.seasons[season].episodes, key=common.natural_sort_key):
        if len(AniDB_array)==len(full_array):  break  #if all anidbid needed stop looping
        new_season, new_episode, anidbid = AnimeLists.anidb_ep(mappingList, season, episode)
        #Log.Info("anidbid: {}, season: {}, episode: {}, new_season: {}, new_episode: {}".format(anidbid, season, episode, new_season, new_episode))
        if anidbid and anidbid not in AniDB_array:  AniDB_array.append(anidbid)
      else:  continue
      break  #cascade break
  else: full_array, AniDB_array = [AniDBid], [AniDBid]
  Log.Info("AniDB.GetMetadata() - AniDBid: {}, AniDBids list: {}, AniDBids present on disk: {}".format(AniDBid, full_array, AniDB_array))
  
  ### Load anidb xmls in tvdb numbering format if needed ###
  for AniDBid in AniDB_array:
    xml = common.LoadFile(filename=AniDBid+".xml", relativeDirectory=os.path.join("AniDB", "xml"), url=ANIDB_HTTP_API_URL+AniDBid)  # AniDB title database loaded once every 2 weeks
    if xml:
      title,      original_title, language_rank = GetAniDBTitle(xml.xpath('/anime/titles/title'))
      title_sort, _,              _             = GetAniDBTitle(xml.xpath('/anime/titles/title'), None, True)
      Log.Info("AniDB.GetMetadata() - AniDBid: {} ".format(AniDBid).ljust(157, '-'))
      Log.Info("AniDB.GetMetadata() - 'title': {}, 'title_sort': {}, original_title: {}".format(title, title_sort, original_title))
      if AniDBid==original or len(AniDB_array)==1: #Dict(mappingList, 'poster_id_array', TVDBid, AniDBid)[0]in ('1', 'a'):  ### for each main anime AniDBid ###
        AniDB_dict['title'], AniDB_dict['original_title'], AniDB_dict['title_sort'] = title, original_title, title_sort
        
        if SaveDict( GetXml(xml, 'startdate'  ), AniDB_dict, 'originally_available_at'):  Log.Info("AniDB.GetMetadata() - 'originally_available_at': '{}'".format(AniDB_dict['originally_available_at']))
        if SaveDict( re.sub(r'http://anidb\.net/[a-z]{1,2}[0-9]+ \[(.+?)\]', r'\1', GetXml(xml, 'description')).replace("`", "'"), AniDB_dict, 'summary'):
          Log.Info("AniDB.GetMetadata() - 'summary' empty: '{}'".format(not GetXml(xml, 'description')))
          if not movie and Dict(mappingList, 'defaulttvdbseason').isdigit() and mappingList['defaulttvdbseason'] in media.seasons:
            SaveDict(AniDB_dict['summary'], AniDB_dict, 'seasons', mappingList['defaulttvdbseason'], 'summary') 
            
        #roles  ### NEW, NOT IN Plex FrameWork Documentation 2.1.1 ###
        for role in xml.xpath("characters/character[(@type='secondary cast in') or (@type='main character in')]"):
          try:     SaveDict([{'role': role.find('name').text, 'name': role.find('seiyuu').text, 'photo': ANIDB_PIC_BASE_URL + role.find('seiyuu').get('picture')}], AniDB_dict, 'roles')
          except:  Log.Info("AniDB.GetMetadata() - 'roles' - Seyiuu error")
        
        if SaveDict( GetXml(xml, 'ratings/permanent'), AniDB_dict, 'rating'):  Log.Info("AniDB.GetMetadata() - 'rating': '{}'".format(AniDB_dict['rating']))
        
        ###
        if GetXml(xml, 'picture'):
          #thumbLocalPath = functions.ParseImage(bannerPath, constants.ANIDB_PIC_BASE_URL, os.path.join("AniDB", id, "season"), constants.ANIDB_PIC_THUMB_URL % os.path.splitext(bannerPath)[0]
          AniDB_dict['posters'] = {ANIDB_PIC_BASE_URL + GetXml(xml, 'picture'): ( os.path.join('AniDB', 'poster', GetXml(xml, 'picture')), 99, ANIDB_PIC_THUMB_URL.format(GetXml(xml, 'picture').split('.')[0]))}
        
        ### genre ###
        RESTRICTED_GENRE     = {"18 restricted": 'X', "pornography": 'X', "tv censoring": 'TV-MA', "borderline porn": 'TV-MA'}
        for tag in xml.xpath('tags/tag'):
          if GetXml(tag, 'name') and tag.get('weight', '').isdigit() and int(tag.get('weight', '') or '200') >= int(Prefs['MinimumWeight'] or '200'):
            SaveDict( [string.capwords(GetXml(tag, 'name'), '-')], AniDB_dict, 'genres')
            if GetXml(tag, 'name').lower() in RESTRICTED_GENRE:  AniDB_dict['content_rating'] = RESTRICTED_GENRE[ GetXml(tag, 'name').lower() ]
        SaveDict( "Continuing" if GetXml(xml, 'Anime/enddate')=="1970-01-01" else "Ended", AniDB_dict, 'status')
        ###
        Log.Info("AniDB.GetMetadata() - 'genre' ({}/{} above {} weight): {}".format(len(Dict(AniDB_dict, 'genres')), len(xml.xpath('tags/tag')), int(Prefs['MinimumWeight'] or 200), Dict(AniDB_dict, 'genres')))
        Log.Info("AniDB.GetMetadata() - collections")
        AniDBid_table = Dict(mappingList, 'TVDB') or {}
        for relatedAnime in xml.xpath('/anime/relatedanime/anime'):
          if relatedAnime.get('id') not in AniDBid_table:  AniDBid_table[relatedAnime.get('id')] = (0, "")
        for element in AniDBMovieSets.xpath("/anime-set-list/set/anime"):
          if element.get('anidbid').startswith('377'):  Log.Info(element.get('anidbid'))
          if element.get('anidbid') == AniDBid or element.get('anidbid') in AniDBid_table:
            node              = element.getparent()
            title, main, language_rank = GetAniDBTitle(node.xpath('titles')[0])
            SaveDict(language_rank, AniDB_dict, 'language_rank')
            SaveDict([title], AniDB_dict, 'collections')
            Log.Info("AniDB.GetMetadata() - AniDBid '%s' is part of movie collection: %s', related_anime_list: '%s', " % (AniDBid, title, str(AniDBid_table)))
            break
        else:  Log.Info("AniDBid is not part of any collection, related_anime_list: '%s'" % str(AniDBid_table)) 
      
        
      ### Capture for all concerned AniDBid ###
      if not movie:
        
        ### not listed for serie but is for eps
        Log.Info("AniDB.GetMetadata() - Roles:")
        roles    = { "Animation Work":"studio", "Direction":"directors", "Series Composition":"producers", "Original Work":"writers", "Script":"writers", "Screenplay":"writers" }
        ep_roles = {}
        for creator in xml.xpath('creators/name'):
          for role in roles: 
            if not role in creator.get('type'):  continue
            if roles[role]=="studio":  SaveDict(creator.text, AniDB_dict, 'studio')
            else:                      SaveDict([creator.text], ep_roles, roles[role])
        Log.Info("AniDB.GetMetadata() - creators tag: " +str(ep_roles))
        if     movie and SaveDict(GetXml(xml, 'startdate')[0:4], AniDB_dict, 'year'):  Log.Info("AniDB.GetMetadata() - 'year': '{}'".format(AniDB_dict['year']))
        if not movie and SaveDict(GetXml(xml, 'type')=='Movie', AniDB_dict, 'movie'):  Log.Info("AniDB.GetMetadata() - 'movie': '{}'".format(AniDB_dict['movie']))
      
        ### Translate into season/episode mapping
        numEpisodes, totalDuration, mapped_eps, missing_eps, missing_specials, ending_table, op_nb = 0, 0, [], [], [], {}, 0 
        specials = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
        movie_ep_groups = {}
        for ep_obj in xml.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################
          
          ### Episodes
          title, main, language_rank = GetAniDBTitle (ep_obj.xpath('title'), [language.strip() for language in Prefs['EpisodeLanguagePriority'].split(',')])
          epNum                      = ep_obj.xpath('epno')[0]
          epNumType                  = epNum.get('type')
          season                     = "1" if epNumType == "1" else "0"
          episode                    = epNum.text if epNumType == "1" else str( specials[ epNum.text[0] ][0] + int(epNum.text[1:]))
          #Log.Info("AniDB.GetMetadata() - s{:>1}e{:>3} language_rank: '{}', title: '{}'".format(season, episode, language_rank, title))
          if epNumType=="3" and title.startswith("Ending"):
            if op_nb==0: op_nb = int(epNum.text[1:])-1 #first type 3 is first ending so epNum.text[1:] -1 = nb openings
            episode = str( int(episode) +50 -op_nb)      #shifted to 150 for 1st ending.  
          numbering       = "s{}e{}".format(season, episode)
          
          #If tvdb numbering used, save anidb episode meta using tvdb numbering
          if source.startswith("tvdb") or source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))>1:  season, episode = AnimeLists.tvdb_ep(mappingList, season, episode, source)#;  Log.Info('numbering: {}, season: {}, episode: {}'.format(numbering, season, episode))
          
          if GetXml(ep_obj, 'length').isdigit():
            SaveDict(int(GetXml(ep_obj, 'length'))*1000*60, AniDB_dict, 'seasons', season, 'episodes', episode, 'duration')  # AniDB stores it in minutes, Plex save duration in millisecs
            if season == "1":  numEpisodes, totalDuration = numEpisodes+1, totalDuration + int(GetXml(ep_obj, 'length'))
          
          SaveDict(title,                     AniDB_dict, 'seasons', season, 'episodes', episode, 'title'                  )
          SaveDict(GetXml(ep_obj, 'rating' ), AniDB_dict, 'seasons', season, 'episodes', episode, 'rating'                 )
          SaveDict(GetXml(ep_obj, 'airdate'), AniDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at')
          SaveDict(GetXml(ep_obj, 'summary'), AniDB_dict, 'seasons', season, 'episodes', episode, 'summary'                )
          SaveDict(language_rank,             AniDB_dict, 'seasons', season, 'episodes', episode, 'language_rank'          )
          for role in ep_roles:
            SaveDict(",".join(ep_roles[role]), AniDB_dict, 'seasons', season, 'episodes', episode, role)
            #Log.Info("AniDB.GetMetadata() - role: '%s', value: %s " % (role, str(ep_roles[role])))
                  
          ### In AniDB numbering, Movie episode group, create key and create key in dict with empty list if doesn't exist ###
          if source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))==1:  # AniDB mode
            ### Movie episode group, create key and create key in dict with empty list if doesn't exist ###
            key =''
            if epNumType=='1' and GetXml(xml, '/anime/episodecount')=='1' and GetXml(xml, '/anime/type') in ('Movie', 'OVA'):
              key = '1' if title in ('Complete Movie', 'OVA') else title[-1] if title.startswith('Part ') and title[-1].isdigit() else '' #'-1'
              if not key in movie_ep_groups:  movie_ep_groups[key] = []
            
            if not season in media.seasons or not episode in media.seasons[season].episodes:  #Episode missing
              current_air_date = GetXml(ep_obj, 'airdate').replace('-','')
              current_air_date = int(current_air_date) if current_air_date.isdigit() and int(current_air_date) > 10000000 else 99999999
              if int(time.strftime("%Y%m%d")) <= current_air_date+1:  Log.Warn("[!] Episode: {:>3} not in Plex but air date is {} ({})".format(episode, 'missing' if current_air_date==99999999 else 'not aired yet', current_air_date))  #; continue
              elif epNumType == '2':  missing_specials.append(numbering)
              elif epNumType == '1':
                if key:  SaveDict([numbering], movie_ep_groups, key)
                else:    missing_eps.append(numbering)
              #Log.Info("[!] Episode: {:>3} missing, epNumType: {}".format(numbering, epNumType))
        ### End of for ep_obj...
        if SaveDict(int(totalDuration)/int(numEpisodes) if int(numEpisodes) else 0, AniDB_dict, 'duration'):
          Log.Info("AniDB.get_metadata() - Duration: {}, numEpisodes: {}, average duration: {}".format(str(totalDuration), str(numEpisodes), AniDB_dict['duration']))
        
        ### AniDB Missing Episodes ###
        if movie_ep_groups:
          Log.Info("AniDB.GetMetadata() - Movie/OVA Ep Groups: %s" % movie_ep_groups)  #AniDB.GetMetadata() - movie_ep_groups: {'1': ['s1e1'], '3': ['s1e4', 's1e5', 's1e6'], '2': ['s1e3'], '-1': []}
          missing_eps.extend([value for key in movie_ep_groups for value in movie_ep_groups[key] if 0 < len(movie_ep_groups[key]) < int(key)])
        if missing_eps:
          #missing_eps = sorted(missing_eps, key=lambda x: int("%d%04d" % (int(x.split('e')[0][1:]), int(x.split('e')[1]))))  # .sort(key=natural_sort_key #sorted(list, key=natural_sort_key)
          missing_eps = sorted(missing_eps, key=natural_sort_key)  # .sort(key=natural_sort_key #sorted(list, key=natural_sort_key)
          error_log['Missing Episodes'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid), AniDB_dict['title'], str(missing_eps)))
          Log.Info("AniDB.GetMetadata() - Missing eps: "+ str(missing_eps))
        if missing_specials:
          missing_specials = sorted(missing_specials, key=natural_sort_key)
          error_log['Missing Specials'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid), AniDB_dict['title'], str(missing_specials)))
      ### End of if not movie ###
    
      # External IDs
      ANNid = GetXml(xml, "/anime/resources/resource[@type='1']/externalentity/identifier")
      MALid = GetXml(xml, "/anime/resources/resource[@type='2']/externalentity/identifier")
      #ANFOid = GetXml(xml, "/anime/resources/resource[@type='3']/externalentity/identifier"), GetXml(xml, "/anime/resources/resource[@type='3']/externalentity/identifier")
    
      # Logs
      if not Dict(AniDB_dict, 'summary'):  error_log['AniDB summaries missing'].append("AniDBid: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid) + " | Title: '%s'" % Dict(AniDB_dict, 'title')))
      if not Dict(AniDB_dict, 'posters'):  error_log['AniDB posters missing'  ].append("AniDBid: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid) + " | Title: '%s'" % Dict(AniDB_dict, 'title')))
      #if not Dict(AniDB_dict, 'studio' ):  error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB has studio '%s' and anime-list has '%s' | "    % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, metadata.studio, mapping_studio) + common.WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(xml, encoding='utf8'))), "Submit bug report (need GIT account)"))
      #if metadata.studio       and 'studio' in AniDB_dict and AniDB_dict ['studio'] and AniDB_dict ['studio'] != metadata.studio:  error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB has studio '%s' and anime-list has '%s' | "    % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, metadata.studio, mapping_studio) + common.WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(xml, encoding='utf8'))), "Submit bug report (need GIT account)"))
      #if metadata.studio == "" and 'studio' in AniDB_dict and AniDB_dict ['studio'] == "":                                         error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB and anime-list are both missing the studio" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title) )
    
      Log.Info("AniDB.get_metadata() - ANNid: '%s', MALid: '%s', xml loaded: '%s'" % (ANNid, MALid, str(xml is not None)))
  #Log.Info(str(AniDB_dict))
  return AniDB_dict, ANNid, MALid

### Get the AniDB title database #############################################################################################################################################
def GetAniDBTitlesDB():
  ANIDB_TITLES  = 'http://anidb.net/api/anime-titles.xml.gz'               # AniDB title database file contain all ids, all languages  #http://bakabt.info/anidb/animetitles.xml
  AniDBTitlesDB = common.LoadFile(filename=os.path.basename(ANIDB_TITLES), relativeDirectory="AniDB", url=ANIDB_TITLES, cache= CACHE_1DAY * 30)  # AniDB title database loaded once every 2 weeks
  #AniDBTitlesDB_dict = {}
  if not AniDBTitlesDB:  raise Exception("Failed to load core file '{url}'".format(url=os.path.splitext(os.path.basename(ANIDB_TITLES))[0]))
  return AniDBTitlesDB

### Extract the series/movie/Episode title from AniDB ########################################################################################################################
def GetAniDBTitle(titles, lang=None, title_sort=False):
  languages = lang or [language.strip() for language in Prefs['SerieLanguagePriority'].split(',')] #[ Prefs['SerieLanguage1'], Prefs['SerieLanguage2'], Prefs['SerieLanguage3'] ]  #override default language
  if not 'main' in languages:  languages.append('main')                                      # Add main to the selection if not present in list (main nearly same as x-jat)
  type_priority = {'main':1, 'official':2, 'syn':3, 'synonym':4, 'short':5, None:6}          # lower = highter priority
  langLevel     = [20 for index in range(len(languages))]                                    # languages: title order including main title, then choosen title
  langTitles    = ["" for index in range(len(languages))]                                    # languages: title order including main title, then choosen title
  for title in titles:                                                                       # Loop through all languages listed in the anime XML
    lang, type = title.get('{http://www.w3.org/XML/1998/namespace}lang'), title.get('type')  # If Serie: Main, official, Synonym, short. If episode: None # Get the language, 'xml:lang' attribute need hack to read properly
    if title_sort:  title.text = common.SortTitle(title.text, lang)                          # clean up title
    #Log.Info("GetAniDBTitle - lang: {} type: {} title: {}".format(lang, type, title.text))
    if lang in languages and (type and type_priority[type] < langLevel[languages.index(lang)] or not type):  langTitles[languages.index(lang)  ], langLevel [languages.index(lang)  ] = title.text.replace("`", "'"), type_priority [ type ] if type else 6 + languages.index(lang)
    if type=='main':                                                                                         langTitles[languages.index('main')], langLevel [languages.index('main')] = title.text.replace("`", "'"), type_priority [ type ]
    if lang==languages[0] and type in ['main', ""]:  break
  for index, item in enumerate(langTitles+[]):
    if item:  break
  #Log.Info("GetAniDBTitle - lang index: '{}', langTitles: '{}', langLevel: '{}'".format(languages.index(lang) if lang in languages else '', str(langTitles), str(langLevel)))
  return langTitles[index], langTitles[languages.index('main') if 'main' in languages else 1 if 1 in langTitles else 0], index

### Score word compared to string ###
def WordsScore(words, title_cleansed):
  max_length = max(len("".join(words)), len(title_cleansed))
  score=0
  for word in words:  score+= 100*(len(String.LongestCommonSubstring(word, title_cleansed))+1)/ max_length
  return score
 
### AniDB Search #############################################################################################################################################################
def Search (results, media, lang, manual, movie):
  FILTER_SEARCH_WORDS  = [ ### These are words which cause extra noise due to being uninteresting for doing searches on, Lowercase only ####################################
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime', 'ni', 'sekai',                                             # Jp
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', 'me',  'princess', 'theater', 'and', # En Continued
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses', 'world', 'in', 'another', 'this', 'story', 'life', 'name',                                                                                        # Fr
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi']                                                                    # Roman digits
  SPLIT_CHARS          = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations
  orig_title           = media.title if movie else media.show
  orig_title_cleansed  = common.cleanse_title(orig_title)
  Log.Info("".ljust(157, '-'))
  Log.Info("AniDB.Search() - orig_title: '{}', orig_title_cleansed: '{}'".format(orig_title, orig_title_cleansed))
  
  ### Full title search = 1.3s
  best_aid, best_score, best_title, n = "", 0, "", 0
  start_time = time.time()
  #Log.Info( str(u"/animetitles/anime/title[text()[contains(lower-case(.), '%s')]]" % orig_title.lower()) )
  for element in AniDBTitlesDB.xpath(u"/animetitles/anime/title[text()[contains(lower-case(.), '%s')]]" % orig_title.lower().replace("'", " ")):
    aid            = element.getparent().get('aid',  '')
    title          = element.text
    if aid==best_aid and best_score>=100:  continue
    if orig_title            == title                      :  title_cleansed, score = title,        100 
    elif orig_title.lower()  == title.lower()              :  title_cleansed, score = title.lower(), 99
    else: #contained in title
      title_cleansed = common.cleanse_title(title)
      score1 = 98*len(String.LongestCommonSubstring(orig_title_cleansed, title_cleansed))/max(len(title_cleansed), len(orig_title_cleansed))-n if max(len(title_cleansed), len(orig_title_cleansed)) else 0
      score2 = 98 - 98 * Util.LevenshteinDistance (orig_title_cleansed, title_cleansed) /max(len(title_cleansed), len(orig_title_cleansed))-n  if max(len(title_cleansed), len(orig_title_cleansed)) else 0
      score=max(score1, score2)
    if score>=100 and not aid==best_aid:  n+=1
    results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (title, "anidb", aid), year=media.year, lang=lang, score=score))
    Log.Info("[+] score: {:>3}, aid: {:>5}, title: '{}', title_cleansed: {}".format(score, aid, title, title_cleansed))
    if score > best_score:  best_score, best_title, best_aid = score, title, aid
  if best_score:  Log.Info("[=] best_score: {:>3}, best_aid: {:>5}, best_title: {}".format(best_score, best_aid, best_title))
  Log.Info("elapsed_time: {:.3f}".format(time.time() - start_time ))
  if best_score>=90:  return best_score, n
  
  ### Keyword match using Xpath
  words, words_skipped  = [], []
  for i in SPLIT_CHARS:  orig_title_cleansed = orig_title_cleansed.replace(i, " ")
  orig_title_cleansed = orig_title_cleansed.replace("'", '')
  for word in orig_title_cleansed.split():  (words_skipped if word in FILTER_SEARCH_WORDS or len(word) <= 3 else words).append(word)
  if not words:  words, words_skipped = orig_title_cleansed.split(), []  #Prevent CRITICAL Exception in the search function of agent named 'HamaTV', called with keyword arguments {'show': 'No 6', 'id': '20145', 'year': None} (most recent call last):
  Log.Info("".ljust(157, '-'))
  Log.Info("Keyword Search - Words: {}, skipped: {}".format(str(words), str(words_skipped)))
  type_order=('main', 'official', 'syn', 'short', '')
  best_score, best_title, best_aid, best_type, best_lang = 0, "", "", "", ""
  last_chance, best_score_entry=[], 0
  start_time = time.time()
  
  #temp = " or ".join(["contains(lower-case(text()), '{}')".format(x.lower()) for x in words])
  #result = AniDBTitlesDB.xpath(u"""./anime/title[contains(clean-title(string(text())), "%s")]""" % temp)  
  #for element in AniDBTitlesDB.xpath(u"/animetitles/anime[title[{}]]".format(" or ".join(["contains(lower-case(text()), '{}')".format(x.lower()) for x in words]) )):
  for element in AniDBTitlesDB.xpath(u"/animetitles/anime[title[{}]]".format(" or ".join(["contains(lower-case(text()), '{}')".format(x.lower()) for x in words]) )):
    aid = element.get('aid',  '')
    best_score_entry, best_title_entry, best_type_entry, best_lang_entry = 0, "", "", ""
    for element in element.xpath(u"title[%s]" % " or ".join(["contains(lower-case(text()), '%s')" % x.lower() for x in words]) ):
      title          = element.text
      Type           = element.get('type', '')
      Lang           = element.get('{http://www.w3.org/XML/1998/namespace}lang', '')
      title_cleansed = common.cleanse_title(title)
      if title_cleansed == orig_title_cleansed:  score =  98
      else:                                      score = WordsScore(orig_title_cleansed.split(), title_cleansed)  # - type_order.index(Type)  #Movies can have same title
      if score>best_score_entry or score==best_score_entry and (not best_type_entry or type_order.index(Type)<type_order.index(best_type_entry)):
        best_score_entry, best_title_entry, best_type_entry, best_lang_entry, best_title_entry_cleansed = score, title, Type, Lang, title_cleansed
    if best_score_entry<25:  last_chance.append((best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid));  continue
    Log.Info("[-] score: {:>3}, aid: {:>5}, title: {}, title_cleansed: {}".format(best_score_entry, aid, best_title_entry, best_title_entry_cleansed))
    #Log.Info("levenstein: {}".format(100 - 200 * Util.LevenshteinDistance(title_cleansed, orig_title_cleansed) / (len(title_cleansed) + len(orig_title_cleansed)) ))
    results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="{title} [{Type}({Lang})] [anidb-{aid}]".format(title=best_title_entry, aid=aid, Type=best_type_entry, Lang=best_lang_entry), year=media.year, lang=lang, score=best_score_entry))
    if best_score_entry > best_score:  best_score, best_title, best_type, best_lang, best_aid = best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid
  if best_score <50:  # Add back lower than 25 if nothin above 50
    for best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid in last_chance:
      Log.Info("[-] score: '{}', title: '{}', aid: '{}'".format(best_score_entry, best_title_entry, aid))
      results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="{title} [{Type}({Lang}): {aid}]".format(title=best_title_entry, aid=aid, Type=best_type_entry, Lang=best_lang_entry), year=media.year, lang=lang, score=best_score_entry))
    if best_score_entry > best_score:  best_score, best_title, best_type, best_lang, best_aid = best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid
  Log.Info("[=] score: '{}', best_title: '{}', aid: '{}'".format(best_score, best_title, best_aid))
  Log.Info("elapsed_time: {:.3f}".format(time.time() - start_time ))
  
  return best_score, n
  
### Always on variables ###
AniDBTitlesDB = GetAniDBTitlesDB()

### Notes ###
# [].count(True) replaces any() (not declared in Python 2.4, gives "NameError: global name 'any' is not defined")
#for element in AniDBTitlesDB.xpath(u"/animetitles/anime[title[@type='official' or @type='main' or @type='syn' or @type='short']/text()[contains(.,'%s')]]" % str(orig_title) ):  #parent::node()
#score          = 100*len(String.LongestCommonSubstring(orig_title_cleansed, title_cleansed)) / max_length # - type_order.index(Type)  #Movies can have same title
#temp_score  = sum([len(String.LongestCommonSubstring(word, title)) for word in words]) / len(" ".join(words))
#Levenshtein = 100 - 200 * Util.LevenshteinDistance(title_cleansed, orig_title_cleansed) / (len(title_cleansed) + len(orig_title_cleansed) )
