### AniBD ###
# http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=6481

### Imports ###
# Python Modules #
import os
import re
import string
import datetime
import time
from lxml import etree
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict, GetXml # Direct import of heavily used functions
import AnimeLists

### Variables ###
ANIDB_TITLE_DOMAIN = 'https://anidb.net'
ANIDB_TITLES       = ANIDB_TITLE_DOMAIN + '/api/anime-titles.xml.gz'  # AniDB title database file contain all ids, all languages
AniDBTitlesDB      = None

ANIDB_API_DOMAIN   = 'http://api.anidb.net:9001'
ANIDB_HTTP_API_URL = ANIDB_API_DOMAIN + '/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='

ANIDB_IMAGE_DOMAIN  = 'https://cdn.anidb.net'
ANIDB_PIC_BASE_URL  = ANIDB_IMAGE_DOMAIN + '/images/main/'
ANIDB_PIC_THUMB_URL = ANIDB_IMAGE_DOMAIN + '/images/65x100/{name}.jpg-thumb.jpg'

AniDBBan = False

### Functions ###
# Define custom functions to be available in 'xpath' calls
ns = etree.FunctionNamespace(None)
ns['lower-case' ] = lambda context, s: s[0].lower()
ns['clean-title'] = lambda context, s: common.cleanse_title(s)

def Search(results, media, lang, manual, movie):
  ''' AniDB Search assign an anidbid to a series or movie
  '''
  Log.Info("=== AniDB.Search() ===".ljust(157, '='))
  FILTER_SEARCH_WORDS  = [ ### These are words which cause extra noise due to being uninteresting for doing searches on, Lowercase only ####################################
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime', 'ni', 'sekai',                                             # Jp
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', 'me',  'princess', 'theater', 'and', # En Continued
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses', 'world', 'in', 'another', 'this', 'story', 'life', 'name',                                                                                        # Fr
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi']                                                                    # Roman digits
  SPLIT_CHARS          = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations
  orig_title           = media.title if movie else media.show
  orig_title_cleansed  = common.cleanse_title(orig_title)
  Log.Info("orig_title: '{}', orig_title_cleansed: '{}'".format(orig_title, orig_title_cleansed))
  
  ### Full title search = 1.3s
  Log.Info("--- full title ---".ljust(157, '-'))
  best_aid, best_score, best_title, n = "", 0, "", 0
  start_time = time.time()
  Log.Info('len AniDBTitlesDB: {}'.format(len(AniDBTitlesDB)))
  for element in AniDBTitlesDB.xpath(u"/animetitles/anime/title[text()[contains(lower-case(.), '%s')]]" % orig_title.lower().replace("'", " ")):
    aid            = element.getparent().get('aid',  '')
    title          = element.text
    if aid==best_aid and best_score>=100:  continue
    if orig_title            == title                      :  title_cleansed, score = title,        100 
    elif orig_title.lower()  == title.lower()              :  title_cleansed, score = title.lower(), 99
    else: #contained in title
      title_cleansed = common.cleanse_title(title)
      score1 = 100*len(String.LongestCommonSubstring(orig_title_cleansed, title_cleansed))/max(len(title_cleansed), len(orig_title_cleansed))-n if max(len(title_cleansed), len(orig_title_cleansed)) else 0
      score2 = 100 - 100 * Util.LevenshteinDistance (orig_title_cleansed, title_cleansed) /max(len(title_cleansed), len(orig_title_cleansed))-n  if max(len(title_cleansed), len(orig_title_cleansed)) else 0
      score=max(score1, score2)
    if score>=100 and not aid==best_aid:  n+=1
    results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="%s [%s-%s]" % (title, "anidb", aid), year=media.year, lang=lang, score=score))
    Log.Info("[+] score: {:>3}, aid: {:>5}, title: '{}', title_cleansed: {}".format(score, aid, title, title_cleansed))
    if score > best_score:  best_score, best_title, best_aid = score, title, aid
  if best_score:  Log.Info("[=] best_score: {:>3}, best_aid: {:>5}, best_title: {}".format(best_score, best_aid, best_title))
  Log.Info("elapsed_time: {:.3f}".format(time.time() - start_time ))
  if best_score>=90:  return best_score, n
  
  ### Keyword match using Xpath
  Log.Info("--- keyword ---".ljust(157, '-'))
  words, words_skipped  = [], []
  for i in SPLIT_CHARS:  orig_title_cleansed = orig_title_cleansed.replace(i, " ")
  orig_title_cleansed = orig_title_cleansed.replace("'", '')
  for word in orig_title_cleansed.split():  (words_skipped if word in FILTER_SEARCH_WORDS or len(word) <= 3 else words).append(word)
  if not words:  words, words_skipped = orig_title_cleansed.split(), []  #Prevent CRITICAL Exception in the search function of agent named 'HamaTV', called with keyword arguments {'show': 'No 6', 'id': '20145', 'year': None} (most recent call last):
  Log.Info("Keyword Search - Words: {}, skipped: {}".format(str(words), str(words_skipped)))
  type_order=('main', 'official', 'syn', 'short', 'card', 'kana', '')
  best_score, best_title, best_aid, best_type, best_lang = 0, "", "", "", ""
  last_chance, best_score_entry=[], 0
  start_time = time.time()
  
  for element in AniDBTitlesDB.xpath(u"/animetitles/anime[title[{}]]".format(" or ".join(["contains(lower-case(text()), '{}')".format(x.lower()) for x in words]) )):
    aid = element.get('aid',  '')
    best_score_entry, best_title_entry, best_type_entry, best_lang_entry = 0, "", "", ""
    for element in element.xpath(u"title[%s]" % " or ".join(["contains(lower-case(text()), '%s')" % x.lower() for x in words]) ):
      title          = element.text
      Type           = element.get('type', '')
      Lang           = element.get('{http://www.w3.org/XML/1998/namespace}lang', '')
      title_cleansed = common.cleanse_title(title)
      if title_cleansed == orig_title_cleansed:  score =  98 if ';' not in title else 100
      else:                                      score = WordsScore(orig_title_cleansed.split(), title_cleansed)  # - type_order.index(Type)  #Movies can have same title
      if score>best_score_entry or score==best_score_entry and (not best_type_entry or type_order.index(Type)<type_order.index(best_type_entry)):
        best_score_entry, best_title_entry, best_type_entry, best_lang_entry, best_title_entry_cleansed = score, title, Type, Lang, title_cleansed
    if best_score_entry<25:  last_chance.append((best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid));  continue
    Log.Info('[-] score: {:>3}, aid: {:>5}, title: "{}"'.format(best_score_entry, aid, best_title_entry))
    #Log.Info("levenstein: {}".format(100 - 200 * Util.LevenshteinDistance(title_cleansed, orig_title_cleansed) / (len(title_cleansed) + len(orig_title_cleansed)) ))
    results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="{title} [{Type}({Lang})] [anidb-{aid}]".format(title=best_title_entry, aid=aid, Type=best_type_entry, Lang=best_lang_entry), year=media.year, lang=lang, score=best_score_entry))
    if best_score_entry > best_score:  best_score, best_title, best_type, best_lang, best_aid = best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid
  if best_score <50:  # Add back lower than 25 if nothin above 50
    for best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid in last_chance:
      Log.Info('[-] score: {:>3}, aid: {:>5}, title: "{}"'.format(best_score_entry, best_title_entry, aid))
      results.Append(MetadataSearchResult(id="%s-%s" % ("anidb", aid), name="{title} [{Type}({Lang}): {aid}]".format(title=best_title_entry, aid=aid, Type=best_type_entry, Lang=best_lang_entry), year=media.year, lang=lang, score=best_score_entry))
    if best_score_entry > best_score:  best_score, best_title, best_type, best_lang, best_aid = best_score_entry, best_title_entry, best_type_entry, best_lang_entry, aid
  #Log.Info('           ---       -----         ---------------------------------------------------')
  #Log.Info('[=] score: {:>3}, aid: {:>5}, title: "{}"'.format(best_score, best_aid, best_title))
  Log.Info("elapsed_time: {:.3f}".format(time.time() - start_time ))
  
  return best_score, n

def GetMetadata(media, movie, error_log, source, AniDBid, TVDBid, AniDBMovieSets, mappingList):
  ''' Download metadata to dict_AniDB, ANNid, MALids
  '''
  Log.Info("=== AniDB.GetMetadata() ===".ljust(157, '='))
  AniDB_dict, ANNid, MALids = {}, "", {}
  original                  = AniDBid
  anidb_numbering           = source=="anidb" and (movie or max(map(int, media.seasons.keys()))<=1)
  
  ### Build the list of anidbids for files present ####
  if source.startswith("tvdb") or source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))>1:  #multi anidbid required only for tvdb numbering
    full_array  = [ anidbid for season in Dict(mappingList, 'TVDB', default=[]) for anidbid in Dict(mappingList, 'TVDB', season) if season and 'e' not in season and anidbid.isdigit() ]
    AniDB_array = { AniDBid: [] } if Dict(mappingList, 'defaulttvdbseason')=='1' and source!='tvdb4' else {}
    for season in sorted(media.seasons, key=common.natural_sort_key) if not movie else []:  # For each season, media, then use metadata['season'][season]...
      for episode in sorted(media.seasons[season].episodes, key=common.natural_sort_key):
        if int(episode)>99:  continue  # AniDB non-normal special (op/ed/t/o) that is not mapable
        if   source=='tvdb3' and season!=0:  new_season, new_episode, anidbid = AnimeLists.anidb_ep(mappingList, season, Dict(mappingList, 'absolute_map', episode, default=(None, episode))[1])  # Pull absolute number then try to map
        elif source=='tvdb4' and season!=0:  new_season, new_episode          = Dict(mappingList, 'absolute_map', episode, default=(season, episode)); anidbid = 'UNKN'                             # Not TVDB mapping. Use custom ASS mapping to pull season/episode
        else:                                new_season, new_episode, anidbid = AnimeLists.anidb_ep(mappingList, season, episode)                                                                   # Try to map
        numbering = 's{}e{}'.format(season, episode) + ('(s{}e{})'.format(new_season, new_episode) if season!=new_season and episode!=new_episode else '')
        if anidbid and not (new_season=='0' and new_episode=='0'):  SaveDict([numbering], AniDB_array, anidbid)
      else:  continue
  elif source.startswith('anidb') and AniDBid != "":  full_array, AniDB_array = [AniDBid], {AniDBid:[]}
  else:                                               full_array, AniDB_array = [], {}
  
  active_array = full_array if Dict(mappingList, 'possible_anidb3') or source in ("tvdb4", "tvdb6") else AniDB_array.keys()  # anidb3(tvdb)/anidb4(tvdb6) for full relation_map data | tvdb4 bc the above will not be able to know the AniDBid
  Log.Info("Source: {}, AniDBid: {}, Full AniDBids list: {}, Active AniDBids list: {}".format(source, AniDBid, full_array, active_array))
  for anidbid in sorted(AniDB_array, key=common.natural_sort_key):
    Log.Info('[+] {:>5}: {}'.format(anidbid, AniDB_array[anidbid]))
  
  ### Build list_abs_eps for tvdb 3/4/5 ###
  list_abs_eps, list_sp_eps={}, []
  if source in ('tvdb3', 'tvdb4'):
    for s in media.seasons:
      for e in media.seasons[s].episodes:
          if s=='0':  list_sp_eps.append(e)
          else:       list_abs_eps[e]=s 
    Log.Info('Present abs eps: {}'.format(list_abs_eps))

  ### Load anidb xmls in tvdb numbering format if needed ###
  for AniDBid in sorted(active_array, key=common.natural_sort_key):
    is_primary_entry = AniDBid==original or len(active_array)==1

    Log.Info(("--- %s ---" % AniDBid).ljust(157, '-'))
    Log.Info('AniDBid: {}, IsPrimary: {}, url: {}'.format(AniDBid, is_primary_entry, ANIDB_HTTP_API_URL+AniDBid))
    Log.Info(("--- %s.series ---" % AniDBid).ljust(157, '-'))

    xml, cache = None, CACHE_1DAY*6
    xml_cache  = common.LoadFileCache(filename=AniDBid+".xml", relativeDirectory=os.path.join("AniDB", "xml"))[0]
    if isinstance(xml_cache, str):  xml_cache = ''
    if xml_cache:  # Pull the enddate and adjust max cache age based on series enddate in relation to now
      ed = GetXml(xml_cache, 'enddate') or datetime.datetime.now().strftime("%Y-%m-%d")
      enddate = datetime.datetime.strptime("{}-12-31".format(ed) if len(ed)==4 else "{}-{}".format(ed, ([30, 31] if int(ed[-2:])<=7 else [31, 30])[int(ed[-2:]) % 2] if ed[-2:]!='02' else 28) if len(ed)==7 else ed, '%Y-%m-%d')
      days_old = (datetime.datetime.now() - enddate).days
      if   days_old > 1825:  cache = CACHE_1DAY*365                  # enddate > 5 years ago => 1 year cache
      elif days_old >   30:  cache = (days_old*CACHE_1DAY*365)/1825  # enddate > 30 days ago => (days_old/5yrs ended = x/1yrs cache)
    if AniDBBan:  xml = xml_cache  # Ban has been hit in this process' life span (which is transient)
    else:         xml = common.LoadFile(filename=AniDBid+".xml", relativeDirectory=os.path.join("AniDB", "xml"), url=ANIDB_HTTP_API_URL+AniDBid, cache=cache, sleep=6, throttle=['AniDB', CACHE_1HOUR, 100])
    if isinstance(xml, str) and 'banned' in xml:  global AniDBBan; AniDBBan = True  # Set ban hit on process level
    if AniDBBan:  SaveDict(True, AniDB_dict, 'Banned')                              # Set ban hit on series level

    if not xml or isinstance(xml, str):
      title, original_title, language_rank = GetAniDBTitle(AniDBTitlesDB.xpath('/animetitles/anime[@aid="{}"]/title'.format(AniDBid)))
      if is_primary_entry:
        Log.Info("[ ] title: {}"         .format(SaveDict(title,          AniDB_dict, 'title'         )))
        Log.Info("[ ] original_title: {}".format(SaveDict(original_title, AniDB_dict, 'original_title')))
        Log.Info("[ ] language_rank: {}" .format(SaveDict(language_rank,  AniDB_dict, 'language_rank' )))

    elif xml:
      title, original_title, language_rank = GetAniDBTitle(xml.xpath('/anime/titles/title'))
      if is_primary_entry:  ### for each main anime AniDBid ###
        Log.Info("[ ] title: {}"         .format(SaveDict(title,          AniDB_dict, 'title'         )))
        Log.Info("[ ] original_title: {}".format(SaveDict(original_title, AniDB_dict, 'original_title')))
        Log.Info("[ ] language_rank: {}" .format(SaveDict(language_rank,  AniDB_dict, 'language_rank' )))
        if SaveDict( GetXml(xml, 'startdate'  ), AniDB_dict, 'originally_available_at'):  Log.Info("[ ] originally_available_at: '{}'".format(AniDB_dict['originally_available_at']))
        if SaveDict(summary_sanitizer(GetXml(xml, 'description')), AniDB_dict, 'summary') and not movie and not anidb_numbering and Dict(mappingList, 'defaulttvdbseason').isdigit() and mappingList['defaulttvdbseason'] in media.seasons:
          SaveDict(AniDB_dict['summary'], AniDB_dict, 'seasons', mappingList['defaulttvdbseason'], 'summary') 
            
        Log.Info("[ ] rating: '{}'".format(SaveDict( GetXml(xml, 'ratings/permanent'), AniDB_dict, 'rating')))
        
        ### Posters
        if GetXml(xml, 'picture'):
          AniDB_dict['posters'] = {ANIDB_PIC_BASE_URL + GetXml(xml, 'picture'): ( os.path.join('AniDB', 'poster', GetXml(xml, 'picture')), common.poster_rank('AniDB', 'posters'), None)}  # ANIDB_PIC_THUMB_URL.format(name=GetXml(xml, 'picture').split('.')[0])
        
        ### genre ###
        RESTRICTED_GENRE     = {"18 restricted": 'X', "pornography": 'X', "tv censoring": 'TV-MA', "borderline porn": 'TV-MA'}
        for tag in xml.xpath('tags/tag'):
          if Prefs['AnidbGenresAddWeights'] and ((int(tag.get('weight', '')) >= int(Prefs['MinimumWeight'])) or tag.get('infobox', '')) or not Prefs['AnidbGenresAddWeights'] and tag.get('infobox', ''):
            SaveDict( [string.capwords(GetXml(tag, 'name'), '-')], AniDB_dict, 'genres')
            if GetXml(tag, 'name').lower() in RESTRICTED_GENRE:  AniDB_dict['content_rating'] = RESTRICTED_GENRE[ GetXml(tag, 'name').lower() ]
        if Dict(AniDB_dict, 'genres'): AniDB_dict['genres'].sort()
        SaveDict( "Continuing" if GetXml(xml, 'Anime/enddate')=="1970-01-01" else "Ended", AniDB_dict, 'status')
        Log.Info("[ ] genres ({}/{} above {} weight): {}".format(len(Dict(AniDB_dict, 'genres')), len(xml.xpath('tags/tag')), int(Prefs['MinimumWeight'] or 200), Dict(AniDB_dict, 'genres')))
        for element in AniDBMovieSets.xpath("/anime-set-list/set/anime"):
          if element.get('anidbid') == AniDBid or element.get('anidbid') in full_array:
            node              = element.getparent()
            title, main, language_rank = GetAniDBTitle(node.xpath('titles')[0])
            if title not in Dict(AniDB_dict, 'collections', default=[]):
              Log.Info("[ ] title: {}, main: {}, language_rank: {}".format(title, main, language_rank))
              SaveDict([title], AniDB_dict, 'collections')
              Log.Info("[ ] collection: AniDBid '%s' is part of movie collection: '%s', related_anime_list: %s" % (AniDBid, title, str(full_array)))
        if not Dict(AniDB_dict, 'collections'):  Log.Info("[ ] collection: AniDBid '%s' is not part of any collection, related_anime_list: %s" % (AniDBid, str(full_array))) 
      
        #roles  ### NEW, NOT IN Plex FrameWork Documentation 2.1.1 ###
        Log.Info(("--- %s.actors ---" % AniDBid).ljust(157, '-'))
        for role in xml.xpath('characters/character[(@type="secondary cast in") or (@type="main character in")]'):
          try:
            if GetXml(role, 'seiyuu') and GetXml(role, 'name'):  
              role_dict = {'role': role.find('name').text, 'name': role.find('seiyuu').text, 'photo': ANIDB_PIC_BASE_URL + role.find('seiyuu').get('picture')}
              SaveDict([role_dict], AniDB_dict, 'roles')
              Log.Info('[ ] role: {:<20}, name: {:<20}, photo: {}'.format(role_dict['role'], role_dict['name'], role_dict['photo']))
          except Exception as e:  Log.Info("Seyiuu error: {}".format(e))
        
      ### Creators ###
      creator_tags = { "Animation Work":"studio", "Work":"studio", "Direction":"directors", "Series Composition":"producers", "Original Work":"writers", "Script":"writers", "Screenplay":"writers" }
      studios      = {}
      creators     = {}
      for creator in xml.xpath('creators/name'):
        for tag in creator_tags:
          if tag != creator.get('type'):  continue
          if creator_tags[tag]=="studio":  studios[tag] = creator.text
          else:                            SaveDict([creator.text], creators, creator_tags[tag])
      if is_primary_entry:
        Log.Info("[ ] studio: {}".format(SaveDict(Dict(studios, "Animation Work", default=Dict(studios, "Work")), AniDB_dict, 'studio')))

      Log.Info("[ ] movie: {}".format(SaveDict(GetXml(xml, 'type')=='Movie', AniDB_dict, 'movie')))
      ### Movie ###
      if  movie:
        Log.Info("[ ] year: '{}'".format(SaveDict(GetXml(xml, 'startdate')[0:4], AniDB_dict, 'year')))

        if is_primary_entry:
          for creator in creators:  Log.Info("[ ] {}: {}".format(creator, SaveDict(creators[creator], AniDB_dict, creator)))

        Log.Info(("--- %s.summary info ---" % AniDBid).ljust(157, '-'))
          
      ### Series ###
      else:
        ### Translate into season/episode mapping
        numEpisodes, totalDuration, mapped_eps, ending_table, op_nb = 0, 0, [], {}, 0 
        specials        = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
        movie_ep_groups = {}
        ending_offset   = 99
        missing         = {'0': [], '1':[]}
                
        ### Episodes (and specials) not always in right order ###
        Log.Info(("--- %s.episodes ---" % AniDBid).ljust(157, '-'))
        Log.Info("[ ] ep creators (creators tag): " +str(creators))
        for ep_obj in sorted(xml.xpath('episodes/episode'), key=lambda x: [int(x.xpath('epno')[0].get('type')), int(x.xpath('epno')[0].text if x.xpath('epno')[0].text.isdigit() else x.xpath('epno')[0].text[1:])]):
          
          ### Title, Season, Episode number, Specials
          title, main, language_rank = GetAniDBTitle (ep_obj.xpath('title'), [language.strip() for language in Prefs['EpisodeLanguagePriority'].split(',')])
          if not anidb_numbering and title=='Complete Movie':  title = ""  # For mapping use meanningful titles
          epNum     = ep_obj.xpath('epno')[0]
          epNumType = epNum.get('type')
          season    = "1" if epNumType == "1" else "0"
          if   epNumType=="3" and ep_obj.xpath('title')[0].text.startswith('Ending') and int(epNum.text[1:])-1<ending_offset:  ending_offset = int(epNum.text[1:])-1
          if   epNumType=="3" and int(epNum.text[1:])>ending_offset:  episode = str(int(epNum.text[1:])+150-ending_offset)  #shifted to 150 for 1st ending.  
          elif epNumType=="1":                                        episode = epNum.text
          else:                                                       episode = str( specials[ epNum.text[0] ][0] + int(epNum.text[1:]))
          numbering = "s{}e{:>3}".format(season, episode)
          
          #If tvdb numbering used, save anidb episode meta using tvdb numbering
          if source.startswith("tvdb") or source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))>1:
            season, episode = AnimeLists.tvdb_ep(mappingList, season, episode, AniDBid)
            
            # Get episode number to absolute number
            if source in ('tvdb3', 'tvdb4') and season not in ['-1', '0']:
              if source=='tvdb4' or season=='1':
                ms, usl = (season, True) if source=='tvdb3' else (Dict(mappingList, 'absolute_map', 'max_season'), Dict(mappingList, 'absolute_map', 'unknown_series_length'))
                if ms and usl:  season  = Dict(mappingList, 'absolute_map', episode, default=(ms if usl else str(int(ms)+1), None))[0]
              else:
                try:     episode = list(Dict(mappingList, 'absolute_map', default={}).keys())[list(Dict(mappingList, 'absolute_map', default={}).values()).index((season, episode))]
                except:  pass
            
            if not(season =='0' and episode in list_sp_eps) and \
               not(source in ('tvdb3', 'tvdb4') and episode in list_abs_eps) and \
               not(season in media.seasons and episode in media.seasons[season].episodes):
              Log.Info('[ ] {} => s{:>1}e{:>3} epNumType: {}'.format(numbering, season, episode, epNumType))
              continue
            
            ### Series poster as season poster
            if GetXml(xml, 'picture') and not Dict(AniDB_dict, 'seasons', season, 'posters', ANIDB_PIC_BASE_URL + GetXml(xml, 'picture')):
              SaveDict((os.path.join('AniDB', 'poster', GetXml(xml, 'picture')), common.poster_rank('AniDB', 'posters'), None), AniDB_dict, 'seasons', season, 'posters', ANIDB_PIC_BASE_URL + GetXml(xml, 'picture'))

          ### In AniDB numbering, Movie episode group, create key and create key in dict with empty list if doesn't exist ###
          else:  #if source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))<=1:
                     
            ### Movie episode group, create key and create key in dict with empty list if doesn't exist ###
            key = ''
            if epNumType=='1' and GetXml(xml, '/anime/episodecount')=='1' and GetXml(xml, '/anime/type') in ('Movie', 'OVA'):
              key = '1' if title in ('Complete Movie', 'OVA') else title[-1] if title.startswith('Part ') and title[-1].isdigit() else '' #'-1'
              if key:  SaveDict([], movie_ep_groups, key)
            
            #Episode missing from disk
            if not season in media.seasons or not episode in media.seasons[season].episodes:
              Log.Info('[ ] {} => s{:>1}e{:>3} air_date: {}'.format(numbering, season, episode, GetXml(ep_obj, 'airdate')))
              current_air_date = GetXml(ep_obj, 'airdate').replace('-','')
              current_air_date = int(current_air_date) if current_air_date.isdigit() and int(current_air_date) > 10000000 else 99999999
              if int(time.strftime("%Y%m%d")) > current_air_date+1:
                if   epNumType == '1' and key:  SaveDict([numbering], movie_ep_groups, key   )
                elif epNumType in ['1', '2']:   SaveDict([episode],   missing,         season)
              continue
                    
          ### Episodes
          SaveDict(language_rank, AniDB_dict, 'seasons', season, 'episodes', episode, 'language_rank')
          SaveDict(title,         AniDB_dict, 'seasons', season, 'episodes', episode, 'title'        )
          Log.Info('[X] {} => s{:>1}e{:>3} air_date: {} language_rank: {}, title: "{}"'.format(numbering, season, episode, GetXml(ep_obj, 'airdate'), language_rank, title))
          
          if GetXml(ep_obj, 'length').isdigit():
            SaveDict(int(GetXml(ep_obj, 'length'))*1000*60, AniDB_dict, 'seasons', season, 'episodes', episode, 'duration')  # AniDB stores it in minutes, Plex save duration in millisecs
            if season == "1":  numEpisodes, totalDuration = numEpisodes+1, totalDuration + int(GetXml(ep_obj, 'length'))
          
          SaveDict(GetXml(ep_obj, 'rating' ), AniDB_dict, 'seasons', season, 'episodes', episode, 'rating'                 )
          SaveDict(GetXml(ep_obj, 'airdate'), AniDB_dict, 'seasons', season, 'episodes', episode, 'originally_available_at')
          ep_summary = SaveDict(summary_sanitizer(GetXml(ep_obj, 'summary')), AniDB_dict, 'seasons', season, 'episodes', episode, 'summary')
          Log.Info(' - [ ] summary: {}'.format((ep_summary[:200]).replace("\n", "\\n").replace("\r", "\\r")+'..' if len(ep_summary)> 200 else ep_summary))
          for creator in creators:  SaveDict(",".join(creators[creator]), AniDB_dict, 'seasons', season, 'episodes', episode, creator)

          ### Related Mal IDs
          if not (season == "0") and not (Dict(MALids, 'seasons', season)):
            for mal_entity in xml.xpath("/anime/resources/resource[@type='2']/externalentity"):
              mal_id = GetXml(mal_entity, 'identifier')
              if len(mal_id) > 0: SaveDict([mal_id], MALids, 'seasons', season)
                  
        ### End of for ep_obj...
        Log.Info(("--- %s.summary info ---" % AniDBid).ljust(157, '-'))
        if SaveDict((int(totalDuration)/int(numEpisodes))*60*1000 if int(numEpisodes) else 0, AniDB_dict, 'duration'):
          Log.Info("Duration: {}, numEpisodes: {}, average duration: {}".format(str(totalDuration), str(numEpisodes), AniDB_dict['duration']))

        ### AniDB numbering Missing Episodes ###
        if source.startswith("anidb") and not movie and max(map(int, media.seasons.keys()))<=1:
          if movie_ep_groups:
            Log.Info("Movie/OVA Ep Groups: %s" % movie_ep_groups)  #movie_ep_groups: {'1': ['s1e1'], '3': ['s1e4', 's1e5', 's1e6'], '2': ['s1e3'], '-1': []}
            SaveDict([value for key in movie_ep_groups for value in movie_ep_groups[key] if 0 < len(movie_ep_groups[key]) < int(key)], missing, '1')
          for season in sorted(missing):
            missing_eps = sorted(missing[season], key=common.natural_sort_key)
            Log.Info('Season: {} Episodes: {} not on disk'.format(season, missing_eps))
            if missing_eps:  error_log['Missing Specials' if season=='0' else 'Missing Episodes'].append("AniDBid: %s | Title: '%s' | Missing Episodes: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid), AniDB_dict['title'], str(missing_eps)))

      ### End of if not movie ###
    
      # Generate relations_map for anidb3/4(tvdb1/6) modes
      for relatedAnime in xml.xpath('/anime/relatedanime/anime'):
        if relatedAnime.get('id') not in Dict(mappingList, 'relations_map', AniDBid, relatedAnime.get('type'), default=[]): SaveDict([relatedAnime.get('id')], mappingList, 'relations_map', AniDBid, relatedAnime.get('type'))

      # External IDs
      ANNid = GetXml(xml, "/anime/resources/resource[@type='1']/externalentity/identifier")
      #MALid = GetXml(xml, "/anime/resources/resource[@type='2']/externalentity/identifier")
      #ANFOid = GetXml(xml, "/anime/resources/resource[@type='3']/externalentity/identifier"), GetXml(xml, "/anime/resources/resource[@type='3']/externalentity/identifier")
    
      # Logs
      if not Dict(AniDB_dict, 'summary'):  error_log['AniDB summaries missing'].append("AniDBid: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid) + " | Title: '%s'" % Dict(AniDB_dict, 'title')))
      if not Dict(AniDB_dict, 'posters'):  error_log['AniDB posters missing'  ].append("AniDBid: %s" % (common.WEB_LINK % (common.ANIDB_SERIE_URL + AniDBid, AniDBid) + " | Title: '%s'" % Dict(AniDB_dict, 'title')))
      #if not Dict(AniDB_dict, 'studio' ):                                                                                          error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB has studio '%s' and anime-list has '%s' | "    % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, metadata.studio, mapping_studio) + common.WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(xml, encoding='utf8'))), "Submit bug report (need GIT account)"))
      #if metadata.studio       and 'studio' in AniDB_dict and AniDB_dict ['studio'] and AniDB_dict ['studio'] != metadata.studio:  error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB has studio '%s' and anime-list has '%s' | "    % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title, metadata.studio, mapping_studio) + common.WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:" + metadata.id + " " + title, String.StripTags( XML.StringFromElement(xml, encoding='utf8'))), "Submit bug report (need GIT account)"))
      #if metadata.studio == "" and 'studio' in AniDB_dict and AniDB_dict ['studio'] == "":                                         error_log['anime-list studio logos'].append("AniDBid: %s | Title: '%s' | AniDB and anime-list are both missing the studio" % (common.WEB_LINK % (ANIDB_SERIE_URL % AniDBid, AniDBid), title) )
    
      Log.Info("ANNid: '%s', MALids: '%s', xml loaded: '%s'" % (ANNid, MALids, str(xml is not None)))
  
  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("relations_map: {}".format(DictString(Dict(mappingList, 'relations_map', default={}), 1)))
  Log.Info("AniDB_dict: {}".format(DictString(AniDB_dict, 4)))
  return AniDB_dict, ANNid, MALids

def GetAniDBTitlesDB():
  ''' Get the AniDB title database
  '''
  global AniDBTitlesDB
  AniDBTitlesDB = common.LoadFile(filename='anime-titles.xml', relativeDirectory="AniDB", url=ANIDB_TITLES)  # AniDB title database loaded once every 2 weeks
  if AniDBTitlesDB is None:  raise Exception("Failed to load core file '{url}'".format(url=os.path.splitext(os.path.basename(ANIDB_TITLES))[0]))
  else: Log.Info("Entries loaded: {}, File: {}".format(len(AniDBTitlesDB), ANIDB_TITLES))

def GetAniDBTitle(titles, lang=None, title_sort=False):
  ''' Extract the series/movie/Episode title from AniDB
  '''
  languages = lang or [language.strip() for language in Prefs['SerieLanguagePriority'].split(',')] #[ Prefs['SerieLanguage1'], Prefs['SerieLanguage2'], Prefs['SerieLanguage3'] ]  #override default language
  if not 'main' in languages:  languages.append('main')                                      # Add main to the selection if not present in list (main nearly same as x-jat)
  type_priority = {'main':1, 'official':2, 'kana':3, 'kanareading':3, 'card':4, 'titlecard':4, 'syn':5, 'synonym':5, 'short':6, None:7} # lower = higher priority
  langLevel     = [20 for index in range(len(languages))]                                    # languages: title order including main title, then choosen title
  langTitles    = ["" for index in range(len(languages))]                                    # languages: title order including main title, then choosen title
  for title in titles:                                                                       # Loop through all languages listed in the anime XML
    lang, type = title.get('{http://www.w3.org/XML/1998/namespace}lang'), title.get('type')  # If Serie: Main, official, Synonym, short. If episode: None # Get the language, 'xml:lang' attribute need hack to read properly
    if title_sort:  title.text = common.SortTitle(title.text, lang)                          # clean up title
    if lang in languages and (type!='short' and type_priority[type] < langLevel[languages.index(lang)] or not type):  langTitles[languages.index(lang)  ], langLevel [languages.index(lang)  ] = title.text.replace("`", "'"), type_priority [ type ] if type else 6 + languages.index(lang)
    if type=='main':                                                                                                  langTitles[languages.index('main')], langLevel [languages.index('main')] = title.text.replace("`", "'").replace("&lt;", "<").replace("&gt;", ">"), type_priority [ type ]
    if lang==languages[0] and type in ['main', ""]:  break
    #Log.Info("GetAniDBTitle - lang: {} type: {} title: {}".format(lang, type, title.text))
    
  for index, item in enumerate(langTitles+[]):
    if item:  break
  #Log.Info("GetAniDBTitle - lang index: '{}', langTitles: '{}', langLevel: '{}'".format(languages.index(lang) if lang in languages else '', str(langTitles), str(langLevel)))
  return langTitles[index], langTitles[languages.index('main') if 'main' in languages else 1 if 1 in langTitles else 0], index

def summary_sanitizer(summary):
  summary = summary.replace("`", "'")                                                                # Replace backquote with single quote
  summary = re.sub(r'https?://anidb\.net/[a-z]{1,2}[0-9]+ \[(?P<text>.+?)\]', r'\g<text>', summary)  # Replace links
  summary = re.sub(r'https?://anidb\.net/[a-z]+/[0-9]+ \[(?P<text>.+?)\]', r'\g<text>', summary)     # Replace long-form links
  summary = re.sub(r'^(\*|--|~) .*',              "",      summary, flags=re.MULTILINE)              # Remove the line if it starts with ('* ' / '-- ' / '~ ')
  summary = re.sub(r'\n(Source|Note|Summary):.*', "",      summary, flags=re.DOTALL)                 # Remove all lines after this is seen
  summary = re.sub(r'\n\n+',                      r'\n\n', summary, flags=re.DOTALL)                 # Condense multiple empty lines
  return summary.strip(" \n")
  
def WordsScore(words, title_cleansed):
  ''' Score word compared to string in percents
  '''
  max_length = max(len("".join(words)), len(title_cleansed))
  score=0
  for word in words:  score+= 100*len(String.LongestCommonSubstring(word, title_cleansed))/max_length
  return score
 
### Notes ###
# [].count(True) replaces any() (not declared in Python 2.4, gives "NameError: global name 'any' is not defined")
