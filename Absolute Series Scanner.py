# -*- coding: utf-8 -*-
### Python library  ####### Functions and structures ###  #import Stack, VideoFiles, fnmatch ### Plex Media Server\Plug-ins\Scanners.bundle\Contents\Resources\Common ###
import sys                                              # getdefaultencoding, getfilesystemencoding, platform
import os                                               # path, listdir
import tempfile                                         # NamedTemporaryFile
import time                                             # strftime
import re                                               # match, compile, sub
from lxml import etree                                  # fromstring
import logging, logging.handlers                        #
import Utils                                            # SplitPath
import VideoFiles                                       # VideoFiles.Scan(path, files, mediaList, subdirs, None) # Scan for video files.
import Stack                                            # Scan
try:                 from urllib.request import urlopen # urlopen Python 3.0 and later
except ImportError:  from urllib2        import urlopen # urlopen Python 2.x #import urllib2 # urlopen

### Log variables, regex, skipped folders, words to remove, character maps ###  ### http://www.zytrax.com/tech/web/regex.htm  # http://regex101.com/#python
TVDB_HTTP_API_URL         = 'http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/en.xml'
ASS_MAPPING_URL           = 'http://rawgit.com/ZeroQI/Absolute-Series-Scanner/master/tvdb4.mapping.xml'
ANIDB_TVDB_MAPPING        = 'http://rawgit.com/ScudLee/anime-lists/master/anime-list-master.xml'
ANIDB_TVDB_MAPPING_MOD    = 'http://rawgit.com/Dingmatt/AMSA/master/Plug-in%20Support/Data/com.plexapp.agents.amsa/DataItems/anime-list-corrections.xml'
ANIDB_TVDB_MAPPING_CUSTOM = 'anime-list-custom.xml'                                                                            # custom local correction for ScudLee mapping file url
SOURCE_IDS                = ".*? ?\[(anidb|anidb2|tvdb|tvdb2|tvdb3|tvdb4|tvdb5|tmdb|tsdb|imdb)-(tt)?[0-9]{1,7}-?(s[0-9]{1,3})?(e[0-9]{1,3})?\]"
SOURCE_ID_FILES           = ["anidb.id", "anidb2.id", "tvdb.id", "tvdb2.id", "tvdb3.id", "tvdb4.id", "tvdb5.id", "tmdb.id", "tsdb.id", "imdb.id"]
TVDB_MODE_IDS             = ".*?\[tvdb(?P<mode>(2|3|4|5))-(tt)?(?P<guid>[0-9]{1,7})(-s[0-9]{1,3}(e[0-9]{1,3})?)?\]"
TVDB_MODE_ID_OFFSET       = ".*? ?\[(?P<source>(tvdb|tvdb2|tvdb3|tvdb4|tvdb5))-(tt)?[0-9]{1,7}-(?P<season>s[0-9]{1,3})?(?P<episode>e[0-9]{1,3})?\]"
ANIDB2_MODE               = ".*? ?\[anidb2-(?P<guid>[0-9]{1,7})\]"
SEASON_RX = [                                                                                                                                                           ### Seasons Folders 
 'Specials',                                                                                                                                                            # Specials (season 0)
 '(Season|Series|Book|Saison|Livre|S)[ _\-]*(?P<season>[0-9]{1,2}).*',                                                                                                  # Season ##, Series #Book ## Saison ##, Livre ##, S##, S ##
 '(?P<season>[0-9]{1,2})a? Stagione.*',                                                                                                                                 # ##a Stagione
 '(([Ss]tory )?[Aa]r[kc]|[Vv]ideo).*' ]                                                                                                                                 # Last entry in array, folder name droped but files kept: Story, Arc, Ark, Video                                                                          #
SERIES_RX = [                                                                                                                                                           ######### Series regex - "serie - xxx - title" ###
  '(^|(?P<show>.*?)[ _\.\-]+)(?P<season>[0-9]{1,2})[Xx](?P<ep>[0-9]{1,3})(([_\-Xx]|[_\-][0-9]{1,2}[Xx])(?P<ep2>[0-9]{1,3}))?([ _\.\-]+(?P<title>.*))?$',                       #  0 # 1x01
  '(^|(?P<show>.*?)[ _\.\-]+)s(?P<season>[0-9]{1,2})(e| e|ep| ep|-)(?P<ep>[0-9]{1,3})(([ _\.\-]|(e|ep)|[ _\.\-](e|ep))(?P<ep2>[0-9]{1,3}))?($|( | - |)(?P<title>.*?)$)',#  1 # s01e01-02 
  '(^|(?P<show>.*?)[ _\.\-]+)(?P<ep>[0-9]{1,3})[ _\.\-]?of[ _\.\-]?[0-9]{1,3}([ _\.\-]+(?P<title>.*?))?$',                                                              #  2 # 01 of 08 (no stacking for this one ?)
  '^(?P<show>.*?) - (E|e|Ep|ep|EP)?(?P<ep>[0-9]{1,3})(-(?P<ep2>[0-9]{1,3}))?( - )?(?P<title>.*)$',                                                                      #  3 # Serie - xx - title.ext | ep01-ep02 | e01-02
  '^(?P<show>.*?) \[(?P<season>[0-9]{1,2})\] \[(?P<ep>[0-9]{1,3})\] (?P<title>.*)$']                                                                                    #  4 # Serie [Sxx] [Exxx] title.ext                     
ANIDB_OFFSET = [0, 100, 150, 200, 400, 0, 0]; ANIDB_RX  = [                                                                                                             ######### AniDB Specials regex ### 
  '(^|(?P<show>.*?)[ _\.\-]+)(SP|SPECIAL|OAV) ?(?P<ep>\d{1,2})(-(?P<ep2>[0-9]{1,3}))? ?(?P<title>.*)$',                                                                 #  5 # 001-099 Specials
  '(^|(?P<show>.*?)[ _\.\-]+)(OP|NCOP|OPENING) ?(?P<ep>\d{1,2}[a-z]?)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                      #  6 # 100-149 Openings
  '(^|(?P<show>.*?)[ _\.\-]+)(ED|NCED|ENDING) ?(?P<ep>\d{1,2}[a-z]?)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                       #  7 # 150-199 Endings
  '(^|(?P<show>.*?)[ _\.\-]+)(TRAILER|PROMO|PV|T) ?(?P<ep>\d{1,2}) ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                          #  8 # 200-299 Trailer, Promo with a  number  '(^|(?P<show>.*?)[ _\.\-]+)((?<=E)P|PARODY|PARODIES?) ?(?P<ep>\d{1,2})? ?(v2|v3|v4|v5)?(?P<title>.*)$',                                                                        # 10 # 300-399 Parodies
  '(^|(?P<show>.*?)[ _\.\-]+)(O|OTHERS?)(?P<ep>\d{1,2}) ?(v2|v3|v4|v5)?[ _\.\-]+(?P<title>.*)$',                                                                        #  9 # 400-499 Others
  '(^|(?P<show>.*?)[ _\.\-]+)(e|ep|e |ep |e-|ep-)?(?P<ep>[0-9]{1,3})((e|ep|-e|-ep|-)(?P<ep2>[0-9]{1,3})|)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                  # 10 # E01 | E01-02| E01-E02 | E01E02                                                                                                                       # __ # look behind: (?<=S) < position < look forward: (?!S)
  '(^|(?P<show>.*?)[ _\.\-]+)S ?(?P<ep>\d{1,2}) ?(?P<title>.*)$']                                                                                                       # 11 # 001-099 Specials #'S' moved to the end to make sure season strings are not caught in prev regex
IGNORE_DIRS_RX  = [ '@Recycle', '.@__thumb', 'lost\+found', '.AppleDouble','$Recycle.Bin', 'System Volume Information', 'Temporary Items', 'Network Trash Folder', '@eaDir', 'Extras', 'Samples?', 'bonus', '.*bonus disc.*', 'trailers?', '.*_UNPACK_.*', '.*_FAILED_.*', 'misc', '_Misc'] #, "VIDEO_TS"]# Filters.py  removed '\..*',        
IGNORE_FILES_RX = ['[ _\.\-]sample', 'sample[ _\.\-]', '-Recap\.', 'OST', 'soundtrack', 'Thumbs.db', '\.plexignore', '\.xml$', '\.smi$']         #, '.*\.log$'                                               # Skipped files (samples, trailers)                                                          
VIDEO_EXTS      = [ '3g2', '3gp', 'asf', 'asx', 'avc', 'avi', 'avs', 'bin', 'bivx', 'divx', 'dv', 'dvr-ms', 'evo', 'fli', 'flv', 'img', 'iso', 'm2t', 'm2ts', 'm2v',    #
                    'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'mts', 'nrg', 'nsv', 'nuv', 'ogm', 'ogv', 'tp', 'pva', 'qt', 'rm', 'rmvb', 'sdp', 'swf', 'svq3', 'strm', #
                    'ts', 'ty', 'vdr', 'viv', 'vp3', 'wmv', 'wpl', 'wtv', 'xsp', 'xvid', 'webm', 'ifo']                                                                 # DVD: 'ifo', 'bup', 'vob'
FILTER_CHARS    = "\\/:*?<>|~;"  #_;.                                                                                                                                     # Windows file naming limitations + "~-,._" + ';' as plex cut title at this for the agent
WHACK_PRE_CLEAN = ["x264-FMD Release", "x264-h65", "x264-mSD", "x264-BAJSKORV", "x264-MgB", "x264-SYS", "x264-FQM", "x264-ASAP", "x264-QCF", "x264-W4F", 'x264-w4f', "x264-AAC", 
  'x264-2hd', "x264-ASAP", 'x264-bajskorv', 'x264-batv', "x264-BATV", "x264-EXCELLENCE", "x264-KILLERS", "x264-LOL", 'x264-MgB', 'x264-qcf', 'x264-SnowDoN', 'x264-xRed', 
  "H.264-iT00NZ", "H.264.iT00NZ", 'H264-PublicHD', "H.264-BS", 'REAL.HDTV', "WEB.DL", "H_264_iT00NZ", "www.crazy-torrent.com", "ReourceRG Kids Release",
  "By UniversalFreedom", "XviD-2HD", "XviD-AFG", "xvid-aldi", 'xvid-asap', "XviD-AXED", "XviD-BiA-mOt", 'xvid-fqm', "xvid-futv", 'xvid-killer', "XviD-LMAO", 'xvid-pfa',
  'xvid-saints', "XviD-T00NG0D", "XViD-ViCKY", "XviD-BiA", "XVID-FHW", "PROPER-LOL", "5Banime-koi_5d", "%5banime-koi%5d", "minitheatre.org", "mthd bd dual", "WEB_DL",
  "HDTV-AFG", "HDTV-LMAO", "ResourceRG Kids", "kris1986k_vs_htt91",   'web-dl', "-Pikanet128", "hdtv-lol", "REPACK-LOL", " - DDZ", "OAR XviD-BiA-mOt", "3xR", "(-Anf-)",
  "Anxious-He", "Coalgirls", "Commie", "DarkDream", "Doremi", "ExiledDestiny", "Exiled-Destiny", "Exiled Destiny", "FFF", "FFFpeeps", "Hatsuyuki", "HorribleSubs", 
  "joseole99", "(II Subs)", "OAR HDTV-BiA-mOt", "Shimeji", "(BD)", "(RS)", "Rizlim", "Subtidal", "Seto-Otaku", "OCZ", "_dn92__Coalgirls__", 
  "(BD 1920x1080 Hi10P, JPN+ENG)", "(BD 1280x720 Hi10P)", "(DVD_480p)", "(1080p_10bit)", "(1080p_10bit_DualAudio)", "(Tri.Audio)", "(Dual.Audio)", "(BD_720p_AAC)", "x264-RedBlade",
  "BD 1080p", "BD 960p", "BD 720p", "BD_720p", "TV 720p", "DVD 480p", "DVD 476p", "DVD 432p", "DVD 336p", "1080p.BluRay", "FLAC5.1", "x264-CTR",
  "1920x1080", "1280x720", "848x480", "952x720", "(DVD 720x480 h264 AC3)", "(720p_10bit)", "(1080p_10bit)", "(1080p_10bit", "(BD.1080p.AAC)",
  "H.264_AAC", "Hi10P", "Hi10", "x264", "BD 10-bit", "DXVA", "H.264", "(BD, 720p, FLAC)", "Blu-Ray", "Blu-ray",  "SD TV", "SD DVD", "HD TV",  "-dvdrip", "dvd-jap", "(DVD)", 
  "FLAC", "Dual Audio", "AC3", "AC3.5.1", "AC3-5.1", "AAC2.0", "AAC.2.0", "AAC2_0", "AAC", 'DD5.1', "5.1",'divx5.1', "DD5_1", "TV-1", "TV-2", "TV-3", "TV-4", "TV-5",
  "(Exiled_Destiny)", "1080p", "720p", "480p", "_BD", ".XVID", "(xvid)", "dub.sub_ja+.ru+", "dub.sub_en.ja", "dub_en",
  "-Cd 1", "-Cd 2", "Vol 1", "Vol 2", "Vol 3", "Vol 4", "Vol 5", "Vol.1", "Vol.2", "Vol.3", "Vol.4", "Vol.5",
  "%28", "%29", " (1)", "(Clean)"]                                                                                                                                      #include spaces, hyphens, dots, underscore, case insensitive
WHACK = [ #lowercase                                                                                                                                                    ### Tags to remove ###
  'x264', 'h264', 'dvxa', 'divx', 'xvid', 'divx51', 'mp4', "avi", '8bit', '8-bit', 'hi10', 'hi10p', '10bit', '10-bit', 'crf24', 'crf 24', 'hevc',                       # Video Codecs (color depth and encoding, Resolution)
  '480p', '576p', '720p', '1080p', '1080i',                                                                                                                             #       
  '24fps', '25fps', 'ntsc', 'pal', 'ntsc-u', 'ntsc-j',                                                                                                                  # Refresh rate, Format
  'mp3', 'ogg', 'ogm', 'vorbis', 'aac', 'dts', 'ac3', 'ac-3', '5.1ch', '5.1', '7.1ch',  'qaac',                                                                         # Audio Codecs, channels
  'dc', 'se', 'extended', 'unrated', 'multi', 'multisubs', 'dubbed', 'dub', 'subbed', 'sub', 'engsub', 'eng', 'french', 'fr', 'jap', "JPN+ENG",                         # edition (dc = directors cut, se = special edition), subs and dubs
  'custom', 'internal', 'repack', 'proper', 'rerip', "raw", "remastered", "uncensored", 'unc', 'cen',                                                                   # format
  'cd1', 'cd2', 'cd3', 'cd4', '1cd', '2cd', '3cd', '4cd', 'xxx', 'nfo', 'read.nfo', 'readnfo', 'nfofix', 'fragment', 'ps3avchd', 'remux', 'fs', 'ws', "- copy", "reenc", "hom",# misc
  'retail', 'webrip', 'web-dl', 'wp', 'workprint', "mkv",  "v1", "v2", "v3", "v4", "v5"                                                                                 # release type: retail, web, work print
  'bdrc', 'bdrip', 'bluray', 'bd', 'brrip', 'hdrip', 'hddvd', 'hddvdrip', 'wsrip',                                                                                      # Source: bluray
  'ddc', 'dvdrip', 'dvd', 'r1', 'r3', 'r5', "dvd", 'svcd', 'vcd', 'sd', 'hd', 'dvb', "release",                                                                         # DVD, VCD, S-VCD
  'dsr', 'dsrip', 'hdtv', 'pdtv', 'ppv', 'stv', 'tvrip', 'complete movie', "hiei", "metis", "norar",                                                                    # dtv, stv
  'cam', 'bdscr', 'dvdscr', 'dvdscreener', 'scr', 'screener', 'tc', 'telecine', 'ts', 'telesync', 'mp4',                                                                # screener
  "mthd", "thora", 'sickrage', 'brrip', "remastered", "yify", "tsr", "reidy", "gerdhanse",                                                                              #'limited', 
  'rikou', 'homЯ', "it00nz", "nn92", "mthd", "elysium", "encodebyjosh", "krissy", "reidy", "it00nz", "s4a"]                                                             #
CHARACTERS_MAP = {
  14844057:"'", 14844051:'-', 14844052:'-', 14844070:'...', 15711386:':', 14846080:'∀', 15711646:'~',                                                                   #['’' \xe2\x80\x99] ['–' \xe2\x80\x93] ['…' \xe2\x80\xa6] # '：' # 12770:'', # '∀ Gundam' no need #'´' ['\xc2', '\xb4']
  50048:'A' , 50050:'A' , 50052:'Ä' , 50080:'a' , 50082:'a' , 50084:'a' , 50305:'a' , 50308:'A' , 50309:'a' ,  50055:'C' , 50087:'c' , 50310:'C' , 50311:'c' ,          #'à' ['\xc3', '\xa0'] #'â' ['\xc3', '\xa2'] #'Ä' ['\xc3', '\x84'] #'ā' ['\xc4', '\x81'] #'À' ['\xc3', '\x80'] #'Â' ['\xc3', '\x82'] # 'Märchen Awakens Romance', 'Rozen Maiden Träumend' #'Ç' ['\xc3', '\x87'] #'ç' ['\xc3', '\xa7'] 
  50057:'E' , 50088:'e' , 50089:'e' , 50090:'e' , 50091:'e' , 50323:'e' , 50328:'E' , 50329:'e' ,                                                                       #'É' ['\xc3', '\x89'] #'è' ['\xc3', '\xa8'] #'é' ['\xc3', '\xa9'] #'ē' ['\xc4', '\x93'] #'ê' ['\xc3', '\xaa'] #'ë' ['\xc3', '\xab']
  50094:'i' , 50095:'i' , 50347:'i' , 50561:'L' , 50562:'l' , 50563:'N' , 50564:'n' , 50097:'n' ,                                                                       #'î' ['\xc3', '\xae'] #'ï' ['\xc3', '\xaf'] #'ī' ['\xc4', '\xab'] #'ñ' ['\xc3', '\xb1']
  50067:'O' , 50068:'Ô' , 50072:'O' , 50099:'o' , 50100:'o' , 50102:'o' , 50573:'o' , 50578:'OE', 50579:'oe',                                                           #'Ø' ['', '']         #'Ô' ['\xc3', '\x94'] #'ô' ['\xc3', '\xb4'] #'ō' ['\xc5', '\x8d'] #'Œ' ['\xc5', '\x92'] #'œ' ['\xc5', '\x93']
  53423:'Я' , 50586:'S' , 50587:'s' , 50079:'ss', 50105:'u' , 50107:'u' , 50108:'u' , 50071:'x' , 50617:'Z' , 50618:'z' , 50619:'Z' , 50620:'z' ,                       #'Я' ['\xd0', '\xaf'] #'ß' []               #'ù' ['\xc3', '\xb9'] #'û' ['\xc3', '\xbb'] #'ü' ['\xc3', '\xbc'] #'²' ['\xc2', '\xb2'] #'³' ['\xc2', '\xb3'] #'×' ['\xc3', '\x97'],
  49835:'«' , 49842:'²' , 49843:'³' , 49844:"'" , 49847:' ' , 49848:'¸',  49851:'»' , 49853:'½', 52352:'', 52353:''}                                                    #'«' ['\xc2', '\xab'] #'·' ['\xc2', '\xb7'] #'»' ['\xc2', '\xbb']# 'R/Ranma ½ Nettou Hen'  #'¸' ['\xc2', '\xb8'] #'̀' ['\xcc', '\x80'] #  ['\xcc', '\x81'] 

### Log + CACHE_PATH calculated once for all calls ###
handler = None
Log     = logging.getLogger('main')
Log.setLevel(logging.DEBUG)

def set_logging(instance, filename, backup_count=0, format='%(message)s', mode='w'):#%(asctime)-15s %(levelname)s - 
  global Log, handler
  if handler: Log.removeHandler(handler)
  if backup_count:  handler = logging.handlers.RotatingFileHandler(os.path.join(CACHE_PATH, filename), maxBytes=10*1024*1024, backupCount=backup_count)
  else:             handler = logging.FileHandler                 (os.path.join(CACHE_PATH, filename), mode=mode)
  handler.setFormatter(logging.Formatter(format))
  handler.setLevel(logging.DEBUG)
  Log.addHandler(handler)

### Check config files on boot up then create library variables ###    #platform = xxx if callable(getattr(sys,'platform')) else "" 
import inspect
PLEX_ROOT  = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "..", ".."))
if not os.path.isdir(PLEX_ROOT):
  path_location = { 'Windows': '%LOCALAPPDATA%\\Plex Media Server',
                    'MacOSX':  '$HOME/Library/Application Support/Plex Media Server',
                    'Linux':   '$PLEX_HOME/Library/Application Support/Plex Media Server' }
  PLEX_ROOT = os.path.expandvars(path_location[Platform.OS.lower()] if Platform.OS.lower() in path_location else '~')  # Platform.OS:  Windows, MacOSX, or Linux
CACHE_PATH = os.path.join(PLEX_ROOT, 'Plug-in Support', 'Data', 'com.plexapp.agents.hama', 'DataItems', '_Logs', 'Series')
if not os.path.exists(CACHE_PATH):  os.makedirs(CACHE_PATH)
set_logging("Root", os.path.join(CACHE_PATH, '_root_.log'), mode='w')
#set_logging("Root", os.path.join(PLEX_ROOT, 'Logs', '_root_0.log'))

### Plex Library XML ###
PLEX_LIBRARY, PLEX_LIBRARY_URL = {}, "http://127.0.0.1:32400/library/sections/"    # Allow to get the library name to get a log per library https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token
if os.path.isfile(os.path.join(PLEX_ROOT, "X-Plex-Token.id")):
  Log.info("'X-Plex-Token.id' file present")
  with open(os.path.join(PLEX_ROOT, "X-Plex-Token.id"), 'r') as token_file:  PLEX_LIBRARY_URL += "?X-Plex-Token=" + token_file.read().strip()
try:
  library_xml = etree.fromstring(urlopen(PLEX_LIBRARY_URL).read())
  for library in library_xml.iterchildren('Directory'):
    for path in library.iterchildren('Location'):
      PLEX_LIBRARY[path.get("path")] = library.get("title")
except:  Log.info("Place correct Plex token in X-Plex-Token.id file in logs folder or in PLEX_LIBRARY_URL variable to have a log per library - https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token")

### replace a string by another while retaining original string case ##############################################################################################
def replace_insensitive (ep, word, sep=" "):
  if ep.lower()==word.lower(): return ""
  position = ep.lower().find(word.lower())
  if position > -1 and len(ep)>len(word):  return (""  if position==0 else ep[:position].lstrip()) + (sep if len(ep) < position+len(word) else ep[position+len(word):].lstrip())

### Turn a string into a list of string and number chunks  "z23a" -> ["z", 23, "a"] ###############################################################################
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):  return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]

### Return number of bytes of Unicode characters ########################################################
def unicodeCharLen (char):                                           # count consecutive 1 bits since it represents the byte numbers-1, less than 1 consecutive bit (128) is 1 byte , less than 23 bytes is 1
  for x in range(1,6):                                           # start at 1, 6 times 
    if ord(char) < 256-pow(2, 7-x)+(2 if x==6 else 0): return x  # 256-2pow(x) with x(7->0) = 128 192 224 240 248 252 254 255 = 1 to 8 bits at 1 from the left, 256-2pow(7-x) starts form left
  #og.info("ord(char): '%d'" % ord(char))

def unicodeLen (string):                                           # count consecutive 1 bits since it represents the byte numbers-1, less than 1 consecutive bit (128) is 1 byte , less than 23 bytes is 1
  length=0
  for char in string:
    length += unicodeCharLen(char)
  return length
  
### Decode string back to Unicode ###   #Unicodize in utils?? #fixEncoding in unicodehelper
def encodeASCII(string, language=None): #from Unicodize and plex scanner and other sources
  import unicodedata                                      # normalize
  if string=="": return ""
  ranges = [ {"from": u"\u3300" , "to": u"\u33ff" },
             {"from": u"\ufe30" , "to": u"\ufe4f" },
             {"from": u"\uf900" , "to": u"\ufaff" }, # compatibility ideographs
             {"from": u"\u30a0" , "to": u"\u30ff" }, #cjk radicals supplement                 - Japanese Kana    
             {"from": u"\u2e80" , "to": u"\u2eff" }, #cjk radicals supplement                 - Japanese Kana    
             {"from": u"\u4e00" , "to": u"\u9fff" }, #CJK Unified Ideographs                  - Chinese Han Ideographs, Common
             {"from": u"\uF900" , "to": u"\uFAFF" }, #CJK Compatibility Ideographs            - Chinese Han Ideographs, Rare, historic
             {"from": u"\u3400" , "to": u"\u4DBF" }, #CJK Unified Ideographs Extension A      - Chinese Han Ideographs, Rare
             {"from": u"\u20000", "to": u"\u2A6DF"}, #CJK Unified Ideographs Extension B      - Chinese Han Ideographs, Rare, historic
             {"from": u"\u2A700", "to": u"\u2B73F"}, #CJK Unified Ideographs Extension C      - Chinese Han Ideographs, Rare, historic
             {"from": u"\u2B740", "to": u"\u2B81F"}, #CJK Unified Ideographs Extension D      - Chinese Han Ideographs, Uncommon, some in current use
             {"from": u"\u2B820", "to": u"\u2CEAF"}, #CJK Unified Ideographs Extension E      - Chinese Han Ideographs, Rare, historic
             {"from": u"\u2F800", "to": u"\u2FA1F"}] #CJK Compatibility Ideographs Supplement - Chinese Han Ideographs, Duplicates, unifiable variants, corporate characters
  encodings, encoding = ['iso8859-1', 'utf-16', 'utf-16be', 'utf-8'], ord(string[0])                                                                          #
  if 0 <= encoding < len(encodings):  string = string[1:].decode('cp949') if encoding == 0 and language == 'ko' else string[1:].decode(encodings[encoding])   # If we're dealing with a particular language, we might want to try another code page.
  if sys.getdefaultencoding() not in encodings:
    try:     string = string.decode(sys.getdefaultencoding())
    except:  pass
  if not sys.getfilesystemencoding()==sys.getdefaultencoding():
    try:     string = string.decode(sys.getfilesystemencoding())
    except:  pass
  string = string.strip('\0')
  try:       string = unicodedata.normalize('NFKD', string)    # Unicode  to ascii conversion to corect most characters automatically
  except:    pass
  try:       string = re.sub(RE_UNICODE_CONTROL, '', string)   # Strip control characters.
  except:    pass
  try:       string = string.encode('ascii', 'replace')        # Encode into Ascii
  except:    pass
  original_string, string, i = string, list(string), 0
  asian_language = False
  while i < len(string):                                       ### loop through unicode and replace special chars with spaces then map if found ###
    if ord(string[i])<128:  i = i+1
    else: #non ascii char
      char, char2, char_list, char_len = 0, "", [], unicodeCharLen(string[i])
      for x in range(0, char_len):
        char = 256*char + ord(string[i+x]); char2 += string[i+x]; char_list.append(string[i+x])
        if x:   string[i] += string[i+x]; string[i+x]=''
      try:
        asian_language = any([mapping["from"] <= x <= mapping["to"] for mapping in ranges for x in char_list])
        Log.info("str: '%s'" % str([mapping["from"] <= x <= mapping["to"] for mapping in ranges for x in char_list]))
      except: asian_language = False
      if char in CHARACTERS_MAP:  string[i]=CHARACTERS_MAP.get( char ); Log.info("*Character remapped in CHARACTERS_MAP: %d:'%s'  , #'%s' %s, string: '%s'" % (char, char2, char2, char_list, original_string))
      elif not asian_language:    Log.warning("*Character missing in CHARACTERS_MAP: %d:'%s'  , #'%s' %s, string: '%s'" % (char, char2, char2, char_list, original_string))
      i += char_len
  return original_string if asian_language else ''.join(string)

### Allow to display ints even if equal to None at times ################################################
def clean_string(string, no_parenthesis=False, no_whack=False, no_dash=False):
  if not string: return ""                                                                                                                                    # if empty return empty string
  if no_parenthesis:                                                                                                                                          # delete parts between parenthesis if needed
    while re.match(".*\([^\(\)]*?\).*", string):                 string = re.sub(r'\([^\(\)]*?\)', ' ', string)                                               #   support imbricated parrenthesis like: "Cyborg 009 - The Cyborg Soldier ((Cyborg) 009 (2001))"
  if re.search("(\[|\]|\{|\})", string):                         string = re.sub("(\[|\]|\{|\})", "", re.sub(r'[\[\{](?![0-9]{1,3}[\]\}]).*?[\]\}]', ' ', string))  # remove "[xxx]" groups but ep numbers inside brackets as Plex cleanup keep inside () but not inside [] #look behind: (?<=S) < position < look forward: (?!S)
  if not no_whack:
    for word in WHACK_PRE_CLEAN:                                 string = replace_insensitive(string, word) if word.lower() in string.lower() else string     # Remove words present in pre-clean list
  string = re.sub(r'(?P<a>[^0-9Ssv])(?P<b>[0-9]{1,3})\.(?P<c>[0-9]{1,2})(?P<d>[^0-9])', '\g<a>\g<b>DoNoTfIlTeR\g<c>\g<d>', string)                            # Used to create a non-filterable special ep number (EX: 13.5 -> 13DoNoTfIlTeR5) # Restricvted to max 999.99 # Does not start with a season/special char 'S|s' (s2.03) or a version char 'v' (v1.2)
  for char, subst in zip(list(FILTER_CHARS), [" " for x in range(len(FILTER_CHARS))]) + [("`", "'"), ("(", " ( "), (")", " ) ")]:                             # remove leftover parenthesis (work with code a bit above)
    if char in string:                                           string = string.replace(char, subst)                                                         # translate anidb apostrophes into normal ones #s = s.replace('&', 'and')
  string = string.replace("DoNoTfIlTeR", '.')                                                                                                                 # Replace 13DoNoTfIlTeR5 into 13.5 back
  if re.match(".*?[\(\[\{]?[0-9a-fA-F]{8}[\[\)\}]?.*", string):  string = re.sub('[0-9a-fA-F]{8}', ' ', string)                                               # CRCs removal
  if re.search("[0-9]{3,4} ?[Xx] ?[0-9]{3,4}", string):          string = re.sub('[0-9]{3,4} ?[Xx] ?[0-9]{3,4}', ' ', string)                                 # Video size ratio removal
  if string.endswith(", The"):                                   string = "The " + ''.join( string.split(", The", 1) )                                        # ", The" is rellocated in front
  if string.endswith(", A"  ):                                   string = "A "   + ''.join( string.split(", A"  , 1) )                                        # ", A"   is rellocated in front
  if not no_whack:                                               string = " ".join([word for word in filter(None, string.split()) if word.lower() not in WHACK]).strip()  # remove double spaces + words present in "WHACK" list #filter(None, string.split())
  if no_dash:                                                    string = re.sub("-", " ", string)                                                            # replace the dash '-'
  string = re.sub(r'\([-Xx]?\)', '', re.sub(r'\( *(?P<internal>[^\(\)]*?) *\)', '(\g<internal>)', string))                                                    # Remove internal spaces in parenthesis then remove empty parenthesis
  string = " ".join([word for word in filter(None, string.split())]).strip()                                                                                  # remove multiple spaces
  for rx in ("-"):                                               string = string[len(rx):   ].strip() if string.startswith(rx)       else string              # In python 2.2.3: string = string.strip(string, " -_") #if string.startswith(("-")): string=string[1:]
  for rx in ("-", "- copy"):                                     string = string[ :-len(rx) ].strip() if string.lower().endswith(rx) else string              # In python 2.2.3: string = string.strip(string, " -_")
  return string

### Add files into Plex database ########################################################################
def add_episode_into_plex(mediaList, file, root, path, show, season=1, ep=1, title="", year=None, ep2="", rx="", length=0, tvdb_mapping={}, unknown_series_length=False, offset_season=0, offset_episode=0, mappingList={}):
  import Media                                            # Episode
  # Mapping List 
  ep_orig, ep_orig_padded = "s%de%d%s" % (season, ep, "" if not ep2 or ep==ep2 else "-%s" % ep2), "s%02de%02d%s" % (season, ep, "" if not ep2 or ep==ep2 else "-%02d" % ep2)
  ep_orig_single          = "s%de%d"   % (season, ep)
  if ep_orig_single in mappingList:
    multi_ep   = 0 if ep_orig == ep_orig_single else ep2-ep
    season, ep = mappingList[ep_orig_single][1:].split("e")
    if '-' in ep or  '+' in ep:  ep, ep2 = ep.split("+"); ep2 = int(ep2) if ep2 and ep2.isdigit() else None
    season, ep, ep2 = int(season), int(ep), int(ep)+multi_ep if multi_ep else ep2
    
  elif 's%d' % season in mappingList and int(mappingList['s%d' % season][0])<=ep and ep<=int(mappingList['s%d' % season][1]):  ep, season = ep + int (mappingList['s%d' % season][2]), int(mappingList['s%d' % season][3])
  elif season > 0:  season, ep, ep2 = season+offset_season if offset_season >= 0 else 0, ep+offset_episode, ep2+offset_episode if ep2 else None
  
  if title==title.lower() or title==title.upper() and title.count(" ")>0: title           = title.title()       # capitalise if all caps or all lowercase and one space at least
  if ep==0:                                                               season, ep, ep2 = 0, 1, 1             # s01e00 and S00e00 => s00e01
  if not ep2 or ep > ep2:                                                 ep2             = ep                  #  make ep2 same as ep for loop and tests
  if tvdb_mapping and season > 0 :
    max_ep_num, season_buffer = max(tvdb_mapping.keys()), 0 if unknown_series_length else 1
    if   ep  in tvdb_mapping:               season, ep  = tvdb_mapping[ep ]
    elif ep  > max_ep_num and season == 1:  season      = tvdb_mapping[max_ep_num][0]+season_buffer
    if   ep2 in tvdb_mapping:               season, ep2 = tvdb_mapping[ep2]
    elif ep2 > max_ep_num and season == 1:  season      = tvdb_mapping[max_ep_num][0]+season_buffer
  ep_final = "s%de%d" % (season, ep)
  file=os.path.join(root,path,file)
  for epn in range(ep, ep2+1):
    if len(show) == 0: Log.warning("show: '%s', s%02de%03d-%03d, file: '%s' has show empty, report logs to dev ASAP" % (show, season, ep, ep2, file))
    else:
      tv_show, tv_show.display_offset = Media.Episode(show, season, epn, title, year), (epn-ep)*100/(ep2-ep+1)
      if os.path.basename(file).upper()=="VIDEO_TS.IFO":  
        for item in os.listdir(os.path.dirname(file)) if os.path.dirname(file) else []:
          if item.upper().startswith("VTS_01_") and not item.upper()=="VTS_01_2.VOB":  tv_show.parts.append(os.path.join(os.path.dirname(file), item))
      else:  tv_show.parts.append(file)
      mediaList.append(tv_show)   # at this level otherwise only one episode per multi-episode is showing despite log below correct
  index = str(SERIES_RX.index(rx)) if rx in SERIES_RX else str(ANIDB_RX.index(rx)+len(SERIES_RX)) if rx in ANIDB_RX else ""  # rank of the regex used from 0
  Log.info('"%s" s%04de%03d%s%s%s%s' % (show, season, ep, "" if ep==ep2 or not ep2 else "-%03d" % ep2, " (Orig: %s)" % ep_orig_padded if ep_orig!=ep_final else "", " \"%s\"" % index if index else "", ' "%s"' % title if clean_string(title).replace('_', '') else ""))
  
### Get the tvdbId from the AnimeId #######################################################################################################################
def anidbTvdbMapping(AniDB_TVDB_mapping_tree, anidbid):
  mappingList                  = {}
  for anime in AniDB_TVDB_mapping_tree.iter('anime') if AniDB_TVDB_mapping_tree else []:
    if anime.get("anidbid") == anidbid and anime.get('tvdbid').isdigit():
      mappingList['episodeoffset'] = anime.get('episodeoffset')
      try:
        for season in anime.iter('mapping'):
          if season.get("offset"):  mappingList[ 's'+season.get("anidbseason")] = [season.get("start"), season.get("end"), season.get("offset"), season.get("tvdbseason")]
          for string2 in filter(None, season.text.split(';')) if season.text else []:  mappingList[ 's'+season.get("anidbseason") + 'e' + string2.split('-')[0] ] = 's' + season.get("tvdbseason") + 'e' + string2.split('-')[1] 
      except: Log.error("anidbTvdbMapping() - mappingList creation exception, mappingList: '%s'" % (str(mappingList)))
      else:   Log.info("anidbTvdbMapping() - anidb: '%s', tvbdid: '%s', defaulttvdbseason: '%s', name: '%s', mappingList: '%s'" % (anidbid, anime.get('tvdbid'), anime.get('defaulttvdbseason'), anime.xpath("name")[0].text, str(mappingList)) )
      return anime.get('tvdbid'), anime.get('defaulttvdbseason'), mappingList
  Log.error("anidbTvdbMapping() - No valid tvbdbid: found for anidbid '%s'" % (anidbid))
  return "", "", {}

### Look for episodes ###################################################################################
def Scan(path, files, mediaList, subdirs, language=None, root=None, **kwargs): #get called for root and each root folder
  if root in path:  path = path.replace(root, "")[1:] #can only call sub-sub-folder fullpath
  set_logging("Main", os.path.join(CACHE_PATH, (path.split(os.sep, 1)[0] if os.sep in path else path or '_root_')+'.log'), mode='a')
  Log.info("Library: '%s', root: '%s', path: '%s', dirs: '%d', subdirs: '%s', files: '%d', Scan date: %s" % (PLEX_LIBRARY[root] if root in PLEX_LIBRARY else "no valid X-Plex-Token.id", root, path, len(subdirs or []), str(subdirs), len(files or []), time.strftime("%Y-%m-%d %H:%M:%S")))
  Log.info("".ljust(157, '='))  
  for subdir in subdirs or []:
    if root in subdir:
      subdir=subdir.replace(root, '')[1:]
      
    for rx in IGNORE_DIRS_RX:
      if re.match(rx, os.path.basename(subdir), re.IGNORECASE): subdirs.remove(subdir);  Log.info("\"%s\" match IGNORE_DIRS_RX: \"%s\"" % (subdir, rx));  break  #skip dirs to be ignored
  reverse_path, files_to_remove = list(reversed(Utils.SplitPath(path))), []
  for file in sorted(files or [], key=natural_sort_key):  #sorted create list copy allowing deleting in place
    ext = os.path.splitext(file)[1].lstrip('.').lower()
    if ext in VIDEO_EXTS:
      for rx in IGNORE_FILES_RX:  # Filter trailers and sample files
        if re.match(rx, file, re.IGNORECASE):
          Log.info("File:   '%s' match IGNORE_FILES_RX: '%s'" % (file, rx))
          files.remove(file)
          break
      else:  Log.info(file.replace(root, "").lstrip(os.sep)) 
    else:  files.remove(file)
  Log.info("".ljust(157, '-'))
  for subdir in subdirs or []:
    subdir_files=[]
    for item in os.listdir(subdir):  subdir_files.append(item)
    Scan(subdir, subdir_files, mediaList, [], language, root)
  if not files:  return  # If direct scanner call on folder (not root) then skip if no files as will be called on subfolders too
  
  ### bluray/DVD folder management ### # source: https://github.com/doublerebel/plex-series-scanner-bdmv/blob/master/Plex%20Series%20Scanner%20(with%20disc%20image%20support).py
  if len(reverse_path) >= 3 and reverse_path[0].lower() == 'stream' and reverse_path[1].lower() == 'bdmv' or "VIDEO_TS.IFO" in str(files).upper():
    for temp in ['stream', 'bdmv', 'video_ts']:
      if reverse_path[0].lower() == temp:  reverse_path.pop(0)
    ep, disc = clean_string(reverse_path[0], True), True
    if len(reverse_path)>1:  reverse_path.pop(0)
    Log.info("BluRay/DVD folder detected - using as equivalent to filename ep: '%s', show: '%s'" % (ep, reverse_path[0]))
  else: disc = False
  
  ### Extract season folder to reduce complexity and use folder as serie name ###
  folder_season =  None
  for last_folder in reverse_path[:-1]:                 # remove root folder from test, [:-1] Doesn't thow errors but gives an empty list if items don't exist, might not be what you want in other cases
    for rx in SEASON_RX :                               # in anime, more specials folders than season folders, so doing it first
      match = re.match(rx, last_folder, re.IGNORECASE)  #
      if match:                                         # get season number but Skip last entry in seasons (skipped folders)
        reverse_path.remove(last_folder)                # All ways to remove: reverse_path.pop(-1), reverse_path.remove(thing|array[0])
        if rx!=SEASON_RX[-1]:
          folder_season = int( match.group('season')) if match.groupdict().has_key('season') and match.group('season') else 0 
          break
        else:  continue
    if match and rx!=SEASON_RX[-1]:  break              # cascade break if not skipped folder since season number found
    if not match and len(reverse_path)>1 and path.count(os.sep) and not "[grouping]" in reverse_path[1] and not "[multi-releases]" in reverse_path[0]:         #if grouping folders, skip and add them as additionnal folders
      Log.warning("Grouping folder: '%s' skipped, need to be added as root folder if needed" % path)
      Log.info("".ljust(157, '-'))
      return
  folder_show = reverse_path[0] if reverse_path else ""
  
  ### Capture guid from folder name or id file in serie or serie/Extras folder ###
  guid=""
  if not re.search(SOURCE_IDS, folder_show, re.IGNORECASE):
    for file in SOURCE_ID_FILES:
      if os.path.isfile(os.path.join(root, os.sep.join(list(reversed(reverse_path))), file)):
        with open(os.path.join(root, os.sep.join(list(reversed(reverse_path))), file), 'r') as guid_file:
          guid = guid_file.read().strip()
          folder_show  = "%s [%s-%s]" % (clean_string(reverse_path[0]), os.path.splitext(file)[0], guid)
        Log.info("Forced ID file: '{}' with id '{}' in series folder".format(file, guid))
        break
    else:  folder_show = folder_show.replace(" - ", " ").split(" ", 2)[2] if folder_show.lower().startswith(("saison","season","series","Book","Livre")) and len(folder_show.split(" ", 2))==3 else clean_string(folder_show) # Dragon Ball/Saison 2 - Dragon Ball Z/Saison 8 => folder_show = "Dragon Ball Z"
  
  ### Forced id mode - Capture if absolute numbering should be applied for all episode numbers  ###
  tvdb_mode, tvdb_guid, tvdb_mapping, unknown_series_length, tvdb_mode_search = "", "", {}, False, re.search(TVDB_MODE_IDS, folder_show, re.IGNORECASE)
  mappingList, offset_season, offset_episode, offset_match = {}, 0, 0, re.search(TVDB_MODE_ID_OFFSET, folder_show, re.IGNORECASE)
  if tvdb_mode_search:
    tvdb_mode, tvdb_guid = tvdb_mode_search.group('mode').lower(), tvdb_mode_search.group('guid').lower();
    #Log.info("folder_show: '%s', folder_season: '%s', tvdb mode: '%s', tvdb id: '%s'" % (folder_show, folder_season, tvdb_mode, tvdb_guid)) # mode 1 normal, mode 2 season mode (ep reset to 1), mode 3 hybrid mode (ep stay in absolute numbering put put in seasons)
    if tvdb_mode in ("2", "3"): 
      tvdb_guid_url, ep_count, abs_manual_placement_info, number_set = TVDB_HTTP_API_URL % tvdb_guid, 0, [], False
      Log.info("TVDB season mode (%s) enabled, serie url: '%s'" % (tvdb_mode, tvdb_guid_url))
      try:
        tvdbanime = etree.fromstring( urlopen(tvdb_guid_url).read() )
        for episode in tvdbanime.xpath('Episode'):
          if episode.xpath('SeasonNumber')[0].text != '0':
            ep_count = ep_count + 1
            if not episode.xpath('absolute_number')[0].text:
              episode.xpath('absolute_number')[0].text, number_set = str(ep_count), True
              abs_manual_placement_info.append("s%se%s = abs %s" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text, episode.xpath('absolute_number')[0].text))
            elif not number_set:  ep_count = int(episode.xpath('absolute_number')[0].text)
            else:  Log.error("different abs number found on ep (s%se%s) after starting to manually place our own abs numbers. all episodes will be added as season 1." % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text) );  break
        else:
          Log.debug("abs_manual_placement_worked, abs_manual_placement_info: '%s'" % (str(abs_manual_placement_info)))
          for episode in tvdbanime.xpath('Episode'):
            SeasonNumber    = episode.xpath('SeasonNumber'   )[0].text if episode.xpath('SeasonNumber'   )[0].text else ''
            EpisodeNumber   = episode.xpath('EpisodeNumber'  )[0].text if episode.xpath('EpisodeNumber'  )[0].text else ''
            absolute_number = episode.xpath('absolute_number')[0].text if episode.xpath('absolute_number')[0].text else ''
            if absolute_number:  tvdb_mapping[int(absolute_number)] = (int(SeasonNumber), int(EpisodeNumber) if tvdb_mode=="2" else int(absolute_number))
      except Exception as e:  Log.error("xml loading issue, Exception: '%s''" % e)
      
    elif tvdb_mode=="4" and folder_season==None:  #1-folders nothing to do, 2-local, 3-online
      url = ASS_MAPPING_URL
      try:
        if   os.path.isfile(os.path.join(root, path, "tvdb4.mapping")):  tvdb4_mapping_content ,url = open(os.path.join(root, path, "tvdb4.mapping")).read().strip(), temp;        Log.info("TVDB4 local file missing: '%s'" % temp)
        else:
          url                   = ASS_MAPPING_URL
          tvdb4_anime           = etree.fromstring( urlopen(url).read().strip() )
          tvdb4_mapping_content = tvdb4_anime.xpath("/tvdb4entries/anime[@tvdbid='%s']" % tvdb_guid)[0].text.strip()
        Log.info("TVDB season mode (%s) enabled, tvdb4 mapping url: '%s'" % (tvdb_mode, url))
        for line in filter(None, tvdb4_mapping_content.replace("\r","\n").split("\n")):
          season = line.strip().split("|")
          for absolute_episode in range(int(season[1]), int(season[2])+1):  tvdb_mapping[absolute_episode] = (int(season[0]), int(absolute_episode)) 
          if "(unknown length)" in season[3].lower(): unknown_series_length = True
      except Exception as e:
        tvdb_mapping, tvdb4_mapping_content = {}, "" 
        if str(e) == "list index out of range":  Log.error("tvdbid: '%s' not found in online season mapping file" % tvdb_guid)
        else:                                    Log.error("Error opening remote tvdb4.mapping.xml, Exception: '%s'" % e)
      
    elif tvdb_mode=="5": ##Star wars: Clone attack chronological order#
      Log.info("TVDB season mode (%s) enabled, tvdb serie rl: '%s'" % (tvdb_mode, TVDB_HTTP_API_URL % tvdb_guid))
      tvdb_guid_url= TVDB_HTTP_API_URL % tvdb_guid
      try:
        tvdbanime = etree.fromstring( urlopen(tvdb_guid_url).read() )
        for episode in tvdbanime.xpath('Episode'):
          if episode.xpath('SeasonNumber')[0].text != '0' and episode.xpath('absolute_number')[0].text:
            mappingList['s%se%s'%(episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text)] = "s1e%s" % episode.xpath('absolute_number')[0].text
        Log.info("mappingList: '%s'" % str(mappingList))
      except Exception as e:  Log.error("xml loading issue, Exception: '%s''" % e)
    if tvdb_mapping:  Log.info("unknown_series_length: %s, tvdb_mapping: %s (showing changing seasons/episodes only)" % (unknown_series_length, str({x:tvdb_mapping[x] for x in tvdb_mapping if tvdb_mapping[x]!=(1,x)})))
  #[for x in tvdb_mapping if tvdb_mapping[x]!=(1,x)]
  ### Calculate offset for season or episode ###
  if offset_match:
    match_source, match_season, match_episode = offset_match.group('source'), "", ""
    if offset_match.groupdict().has_key('season' ) and offset_match.group('season' ):  match_season,  offset_season  = offset_match.group('season' ), int(offset_match.group('season' )[1:])-1
    if offset_match.groupdict().has_key('episode') and offset_match.group('episode'):  match_episode, offset_episode = offset_match.group('episode'), int(offset_match.group('episode')[1:])-1
    if tvdb_mapping and match_season!='s0': 
      season_ep1      = min([e[1] for e in tvdb_mapping.values() if e[0] == offset_season+1]) if match_source in ['tvdb3','tvdb4'] else 1
      offset_episode += list(tvdb_mapping.keys())[list(tvdb_mapping.values()).index((offset_season+1,season_ep1))] - 1
    folder_show = folder_show.replace("-"+match_season+match_episode+"]", "]")
    if offset_season+offset_episode:  Log.info("offset_season = %s, offset_episode = %s" % (offset_season, offset_episode))
    
  ### anidb2 mode (requires ScudLee's mapping xml file) ###
  anidb2_match = re.search(ANIDB2_MODE, folder_show, re.IGNORECASE)
  a2_tvdbid, a2_defaulttvdbseason, scudlee_mapping_content = "", "", None
  if anidb2_match:
    
    # Local custom mapping file
    anidb_id, dir = anidb2_match.group('guid').lower(), os.path.join(root, path)
    while dir and os.path.splitdrive(dir)[1] != os.sep:
      scudlee_filename_custom = os.path.join(dir, ANIDB_TVDB_MAPPING_CUSTOM)
      if os.path.exists( scudlee_filename_custom ):
        with open(scudlee_filename_custom, 'r') as scudlee_file:
          try:     scudlee_mapping_content = etree.fromstring( scudlee_file.read() )
          except:  Log.info("Invalid local custom mapping file content")
          else:
            Log.info("Loading local custom mapping - url: '%s'" % os.path.join(root, ANIDB_TVDB_MAPPING_CUSTOM))
            a2_tvdbid, a2_defaulttvdbseason, mappingList = anidbTvdbMapping(scudlee_mapping_content, anidb_id)
            break
      dir = os.path.dirname(dir)
      
    # Online mod mapping file = ANIDB_TVDB_MAPPING_MOD 
    if not a2_tvdbid:
      tmp_file         = tempfile.NamedTemporaryFile(delete=False); tmp_filename = tmp_file.name; tmp_file.close()
      scudlee_filename = tmp_filename.replace(os.path.basename(tmp_filename), 'anime-list-corrections.xml')
      try:
        if os.path.exists(scudlee_filename) and int(time.time() - os.path.getmtime(scudlee_filename)) <= 86400:
          Log.info("Use existing: '%s'" % scudlee_filename)
          del tmp_file
          with open(scudlee_filename, 'r') as scudlee_file:  scudlee_file_content = scudlee_file.read()
        else:
          Log.info("Updating: '%s' from '%s'" % (scudlee_filename, ANIDB_TVDB_MAPPING_MOD) if os.path.exists(scudlee_filename) else "Creating: "+ scudlee_filename)
          with open(tmp_filename, 'w') as scudlee_file:
            scudlee_file_content = urlopen(ANIDB_TVDB_MAPPING_MOD).read()
            scudlee_file.write( scudlee_file_content )
          if os.path.exists(scudlee_filename): os.remove(scudlee_filename)
          os.rename(tmp_filename, scudlee_filename)
      except Exception as e:  Log.error("Error downloading ScudLee's file mod from local/GitHub '%s', Exception: '%s'" % (ANIDB_TVDB_MAPPING_MOD, e)) 
      else:
        try:                    a2_tvdbid, a2_defaulttvdbseason, mappingList = anidbTvdbMapping(etree.fromstring( scudlee_file_content ), anidb_id)
        except Exception as e:  Log.error("Error parsing ScudLee's file mod content, Exception: '%s'" % e)
    
    #ANIDB_TVDB_MAPPING
    if not a2_tvdbid:
      tmp_file         = tempfile.NamedTemporaryFile(delete=False); tmp_filename = tmp_file.name; tmp_file.close()
      scudlee_filename = tmp_filename.replace(os.path.basename(tmp_filename), 'ASS-tmp-anime-list-master.xml')
      try:
        if os.path.exists(scudlee_filename) and int(time.time() - os.path.getmtime(scudlee_filename)) <= 86400:
          Log.info("Use existing: '%s'" % scudlee_filename)
          del tmp_file
          with open(scudlee_filename, 'r') as scudlee_file:  scudlee_file_content = scudlee_file.read()
        else:
          Log.info("Updating: '%s' from '%s'" % (scudlee_filename, ANIDB_TVDB_MAPPING) if os.path.exists(scudlee_filename) else "Creating: "+ scudlee_filename)
          with open(tmp_filename, 'w') as scudlee_file:
            scudlee_file_content = urlopen(ANIDB_TVDB_MAPPING).read()
            scudlee_file.write( scudlee_file_content )
          if os.path.exists(scudlee_filename): os.remove(scudlee_filename)
          os.rename(tmp_filename, scudlee_filename)
      except Exception as e:  Log.error("Error parsing ScudLee's file mod content, Exception: '%s'" % e)
      else:
        try:                    a2_tvdbid, a2_defaulttvdbseason, mappingList = anidbTvdbMapping(etree.fromstring(scudlee_file_content), anidb_id)
        except Exception as e:  Log.error("Error parsing ScudLee's file from local/url '%s', Exception: '%s'" % (ANIDB_TVDB_MAPPING, e))
    
    #Build AniDB2 Offsets
    if a2_tvdbid:
      folder_show    = clean_string(folder_show)+" [tvdb-%s]" % a2_tvdbid
      offset_season  = int(a2_defaulttvdbseason)-1 if a2_defaulttvdbseason and a2_defaulttvdbseason.isdigit() else 0
      if 'episodeoffset' in mappingList and mappingList['episodeoffset']:  offset_episode = 0-int(mappingList['episodeoffset'][1:]) if mappingList['episodeoffset'].startswith('-') else int(mappingList['episodeoffset'])
      else:                                                                offset_episode = 0
      
  if tvdb_mode_search or anidb2_match:  Log.info("".ljust(157, '-'))
  
  # Build misc variable to check numbers in titles
  misc, misc_words, misc_count = "|", (), {} # put all filenames in folder in a string to count if ep number valid or present in multiple files ###clean_string was true ###
  array = ()
  length=0
  files.sort(key=natural_sort_key)
  if folder_show:
    array = (folder_show, clean_string(folder_show), clean_string(folder_show, True), clean_string(folder_show, no_dash=True), clean_string(folder_show, True, no_dash=True))
    for file in files:     # build misc variable, to avoid numbers in titles if present in multiple filenames
      length2=len(os.path.basename(file))
      #http://stackoverflow.com/questions/29776299/aligning-japanese-characters-in-python
      if length<length2: length = length2 #max len longest - dirname(file)
      for prefix in array: # remove cleansed folder name from cleansed filename and remove potential space
        if prefix.lower() in file.lower():  misc+= clean_string(os.path.basename(file).lower().replace(prefix.lower(), " "), True)+"|"; break
      else:   misc+= clean_string(os.path.basename(file), True)+"|"
    for separator in [' ', '.', '-', '_']:  misc = misc.replace(separator, '|') 
    misc = "|".join([s for s in misc.split('|') if s])
    #Log.info("misc: '%s'" % misc)
    for item in misc.split('|'): 
      if item in misc_count:  misc_count[item] +=1
      else:                   misc_count[item] = 1
    for item in misc_count:
      if item and (misc_count[item] >= len(files) and len(files)>=6 or misc_count[item]== max(misc_count.values()) and max(misc_count.values())>3 ):
        misc_words = misc_words + (item,)
      misc = misc.replace("|%s|" % item, '|')
    #Log.info("misc_words: '%s', misc_count: '%s'" % (str(misc_words), str(misc_count)))
  
  ### File main loop ###
  for file in files:
    show, season, ep2, title, year = folder_show, folder_season if folder_season is not None else 1, None, "", ""
    
    #DVD/BluRay folders
    ext = file[1:] if file.count('.')==1 and file.startswith('.') else os.path.splitext(file)[1].lstrip('.').lower()  # Otherwise .plexignore file has extension ""
    if ext=="ifo" and not file.upper()=="VIDEO_TS.IFO":  continue
    if disc:  filename = ep
    else:
      filename = os.path.splitext(os.path.basename(file))[0]
      encodeASCII(filename)
    
    #remove cleansed folder name from cleansed filename or keywords otherwise
    if clean_string(filename, True,no_dash=True)==clean_string(folder_show, True, no_dash=True):  ep, title  = "01", folder_show                  ### If a file name matches the folder name, place as episode 1
    else:
      for prefix in array:
        if prefix.lower() in filename.lower():  filename = clean_string(filename.lower().replace(prefix.lower(), " "), True); break
      else:
        filename = clean_string(filename, True)
        for item in misc_words:  filename = filename.lower().replace(item, ' ', 1)
      ep = filename
    
    if not path and " - Complete Movie" in ep:                                                                ep, title, show = "01", ep.split(" - Complete Movie")[0], ep.split(" - Complete Movie")[0];   ### Movies ### If using WebAOM (anidb rename) and movie on root
    elif len(files)==1 and not folder_season:
      if   ("movie" in ep.lower()+folder_show.lower() or "gekijouban" in folder_show.lower()) or "-m" in folder_show.split():  ep, title,      = "01", folder_show                  ### Movies ### If only one file in the folder & contains '(movie|gekijouban)' in the file or folder name
    if folder_show and folder_season >= 1:                                                                                                                                         # 
      for prefix in ("s%d" % folder_season, "s%02d" % folder_season):                                                         #"%s %d " % (folder_show, folder_season), 
        if prefix in ep.lower() or prefix in misc_count and misc_count[prefix]>1:  ep = replace_insensitive(ep, prefix , "").lstrip()   # Series S2  like transformers (bad naming)  # Serie S2  in season folder, Anidb specials regex doesn't like
    if folder_show and ep.lower().startswith("special") or "omake" in ep.lower() or "picture drama" in ep.lower():  season, title = 0, ep.title()                        # If specials, season is 0 and if title empty use as title ### 
    
    # Word search for ep number in scrubbed title
    words, loop_completed = filter(None, ep.split()), False                                                                                                         #
    for word in words:                                                                                                                                              #
      ep=word.lower().strip()                                                                                                                                       # cannot use words[words.index(word)] otherwise# if word=='': continue filter prevent "" on double spaces
      for prefix in ["ep", "e", "act", "s"]:                                                                                                                        #
        if ep.startswith(prefix) and len(ep)>len(prefix) and re.match("^\d+(\.\d+)?$", ep[len(prefix):]):      ep, season = ep[len(prefix):], 0 if prefix=="s" else season  # E/EP/act before ep number ex: Trust and Betrayal OVA-act1 # to solve s00e002 "Code Geass Hangyaku no Lelouch S5 Picture Drama 02 'Stage 3.25'.mkv" "'Stage 3 25'"
      if ep.endswith(("v1", "v2", "v3", "v4", "v5")):                                                          ep=ep[:-2].rstrip('-')                               #
      if '-' in ep and len(filter(None, ep.split('-',1)))==2:                                                                                                       # If separator in string
        if re.match("^(?P<ep>[0-9]{1,3})-(?P<ep2>[0-9]{1,3})$", ep, re.IGNORECASE):                            ep, ep2 = ep.split('-'); break
        if re.match("^(ep?[ -]?)?(?P<ep>[0-9]{1,3})(-|ep?|-ep?)(?P<ep2>[0-9]{1,3})", ep, re.IGNORECASE):       ep="Skip"; break                                     # if multi ep: make it non digit and exit so regex takes care of it
        elif path and ( (misc.count(ep)==1 and len(files)>=2) or ep not in clean_string(folder_show, True).lower().split() ):
          ep = ep.split('-',1)[0] if ''.join(letter for letter in ep.split('-',1)[0] if letter.isdigit()) else ep.split('-',1)[1];                                  # otherwise all after separator becomes word#words.insert(words.index(word)+1, "-".join(ep.split("-",1)[1:])) #.insert(len(a), x) is equivalent to a.append(x). #???
        else:                                                                                                  continue
      if re.match("((t|o)[0-9]{1,3}$|(sp|special|oav|op|ncop|opening|ed|nced|ending|trailer|promo|pv|others?)($|[0-9]{1,3}$))", ep):  break                         # Specials go to regex # 's' is ignored as dealt with later in prefix processing # '(t|o)' require a number to make sure a word is not accidently matched
      if ''.join(letter for letter in ep if letter.isdigit())=="":                                             continue                                             # Continue if there are no numbers in the string
      if path and misc.count(ep)>=3:                                                                           continue                                             # Continue if not root folder and string found in in any other filename
      if ep in clean_string(folder_show, True).split() and clean_string(filename, True).split().count(ep)!=2:  continue                                             # Continue if string is in the folder name & string is not in the filename only twice
      if   ep.isdigit() and len(ep)==4 and (int(ep)< 1900 or folder_season and int(ep[0:2])==folder_season):   season, ep = int(ep[0:2]), ep[2:4]                   # 1206 could be season 12 episode 06  #Get assigned from left ot right
      elif ep.isdigit() and len(ep)==4:  filename = clean_string( " ".join(words).replace(ep, "(%s)" % ep));   continue                                             # take everything after supposed episode number
      if "." in ep and ep.split(".", 1)[0].isdigit() and ep.split(".")[1].isdigit():                           season, ep, title = 0, ep.split(".", 1)[0], "Special " + ep; break # ep 12.5 = "12" title "Special 12.5"
      if not path  and not " - Complete Movie" in file:  show = clean_string( " ".join(words[:words.index(word)]) if words.index(word)>0 else "No title", False)    # root folder and 
      title = clean_string( " ".join(words[words.index(word):])[" ".join(words[words.index(word):]).lower().index(ep)+len(ep):] )                                   # take everything after supposed episode number
      break
    else:  loop_completed = True
    if not loop_completed and ep.isdigit():  
      add_episode_into_plex(mediaList, file, root, path, show, season, int(ep), title, year, int(ep2) if ep2 and ep2.isdigit() else None, "None", length, tvdb_mapping, unknown_series_length, offset_season, offset_episode, mappingList);  continue

    ### Check for Regex: SERIES_RX + ANIDB_RX ###
    movie_list, AniDB_op, counter, ep = {}, {}, 500, filename
    for rx in SERIES_RX + ANIDB_RX:
      match = re.search(rx, ep, re.IGNORECASE)
      if match:
        if match.groupdict().has_key('show'  ) and match.group('show'  ) and not path:  show   = clean_string( match.group('show' ))  # Mainly if file at root or _ folder
        if match.groupdict().has_key('title' ) and match.group('title' ):               title  = clean_string( match.group('title'))
        if match.groupdict().has_key('season') and match.group('season'):               season = int(match.group('season'))
        if match.groupdict().has_key('ep2'   ) and match.group('ep2'   ):               ep2    = match.group('ep2') 
        if match.groupdict().has_key('ep'    ) and match.group('ep'    ):               ep     = match.group('ep')
        elif rx in ANIDB_RX[:-2] or rx == ANIDB_RX[-1]:                                 ep     = "01"
        else:                                                                                                                                                   #No ep number, anidb usefull ?????
          movie_list[season] = movie_list[season]+1 if season in movie_list else 1                                                                              # if no ep in regex and anidb special#add movies using year as season, starting at 1  # Year alone is season Year and ep incremented, good for series, bad for movies but cool for movies in series folder...
          ep                 = str(movie_list[season])
        if rx in ANIDB_RX[:-2] or rx == ANIDB_RX[-1]:                                                                                                           ### AniDB Specials ################################################################
          offset, season = ANIDB_OFFSET [ ANIDB_RX.index(rx) ], 0                                                                                               # offset = 100 for OP, 150 for ED, etc... #Log.info("ep: '%s', rx: '%s', file: '%s'" % (ep, rx, file))
          if not ep.isdigit() and len(ep)>1 and ep[:-1].isdigit():                                                                                              ### OP/ED with letter version Example: op2a
            AniDB_op [ offset + int(ep[:-1]) ] = ord( ep[-1:].lower() ) - ord('a')                                                                              # {101: 0 for op1a / 152: for ed2b} and the distance between a and the version we have hereep, offset                         = str( int( ep[:-1] ) ), offset + sum( AniDB_op.values() )                             # "if xxx isdigit() else 1" implied since OP1a for example... # get the offset (100, 150, 200, 300, 400) + the sum of all the mini offset caused by letter version (1b, 2b, 3c = 4 mini offset)
            ep, offset                         = int( ep[:-1] ), offset + sum( AniDB_op.values() )                                                       # "if xxx isdigit() else 1" implied since OP1a for example... # get the offset (100, 150, 200, 300, 400) + the sum of all the mini offset caused by letter version (1b, 2b, 3c = 4 mini offset)
          if offset == 100 and not(match.groupdict().has_key('title' ) and match.group('title' )):  title = "Opening " + str(int(ep))                           # Dingmatt fix for opening with just the ep number
          if offset == 150 and not(match.groupdict().has_key('title' ) and match.group('title' )):  title = "Ending "  + str(int(ep))                           # Dingmatt fix for ending  with just the ep number
          ep = offset + int(ep) 
        add_episode_into_plex(mediaList, file, root, path, show, season, int(ep), title, year, int(ep2) if ep2 and ep2.isdigit() else None, rx, length, tvdb_mapping, unknown_series_length, offset_season, offset_episode, mappingList); 
        break
    if match: continue  # next file iteration
    
    ### Ep not found, adding as season 0 episode 501+ ###
    if " - " in ep and len(ep.split(" - "))>1:  title = clean_string(" - ".join(ep.split(" - ")[1:]))
    counter = counter+1                                          #                    #
    add_episode_into_plex(mediaList, file, root, path , show, 0, counter, title.strip(), year, None, "", length)

  Stack.Scan(path, files, mediaList, subdirs) if "Stack" in sys.modules else Log.info("Stack.Scan() doesn't exists")
  Log.info("")
