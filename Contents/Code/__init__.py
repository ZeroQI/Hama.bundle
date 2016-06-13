# -*- coding: utf-8 -*-
### Python library  ####### Functions and structures ###  #import Stack, VideoFiles, fnmatch ### Plex Media Server\Plug-ins\Scanners.bundle\Contents\Resources\Common ###
import sys             # getdefaultencoding, getfilesystemencoding, platform
import os              # path, listdir
import time            # strftime
import re              # match, compile, sub
import unicodedata     # normalize
import urllib2         # urlopen
from lxml import etree # fromstring
import Utils           # SplitPath
import Media           # Episode
import Stack           # Scan

### Log variables, regex, skipped folders, words to remove, character maps ###  ### http://www.zytrax.com/tech/web/regex.htm  # http://regex101.com/#python
season_rx = [                                                                                                                                                           ### Seasons Folders 
 'Specials',                                                                                                                                                            # Specials (season 0)
 '(Season|Series|Book|Saison|Livre|S)[ _\-]*(?P<season>[0-9]{1,2}).*',                                                                                                  # Season ##, Series #Book ## Saison ##, Livre ##, S##, S ##
 '(?P<season>[0-9]{1,2})a? Stagione.*',                                                                                                                                 # ##a Stagione
 '(([Ss]tory )?[Aa]r[kc]|[Vv]ideo).*' ]                                                                                                                                 # Last entry in array, folder name droped but files kept: Story, Arc, Ark, Video                                                                          #
series_rx = [                                                                                                                                                           ######### Series regex - "serie - xxx - title" ###
  '(^|(?P<show>.*?)[ _\.\-]+)(?P<season>[0-9]{1,2})[Xx](?P<ep>[0-9]{1,3})((|[_\-][0-9]{1,2})[Xx](?P<ep2>[0-9]{1,3}))?([ _\.\-]+(?P<title>.*))?$',                       #  0 # 1x01
  '(^|(?P<show>.*?)[ _\.\-]+)s(?P<season>[0-9]{1,2})(e| e|ep| ep|-)(?P<ep>[0-9]{1,3})(([ _\.\-]|(e|ep)|[ _\.\-](e|ep))(?P<ep2>[0-9]{1,3}))?($|( | - |)(?P<title>.*?)$)',#  1 # s01e01-02 | ep01-ep02 | e01-02
  '(^|(?P<show>.*?)[ _\.\-]+)(?P<ep>[0-9]{1,3})[ _\.\-]?of[ _\.\-]?[0-9]{1,3}([ _\.\-]+(?P<title>.*?))?$',                                                              #  3 # 01 of 08 (no stacking for this one ?)
  '^(?P<show>.*?) - (?P<ep>[0-9]{1,3}) - (?P<title>.*)$',                                                                                                               #  4 # Serie - xx - title.ext
  '[(]?(?P<season>(19|20)[0-9]{2})[)]?[ _\.\-]+(?P<title>.*?)$',                                                                                                        #  2 # (1932) title.ext
  '(?P<title>.*?) [(]?(?P<season>(19|20)[0-9]{2})[)]$']                                                                                                                 #  5 # title (1932).ext
AniDBOffset = [0, 100, 150, 200, 400, 0, 0]; anidb_rx  = [                                                                                                              ######### AniDB Specials regex ### 
  '(^|(?P<show>.*?)[ _\.\-]+)(SP|SPECIAL|OAV) ?(?P<ep>\d{1,2}) ?(?P<title>.*)$',                                                                                        #  6 # 001-099 Specials
  '(^|(?P<show>.*?)[ _\.\-]+)(OP|NCOP|OPENING) ?(?P<ep>\d{1,2}[a-z]?)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                      #  7 # 100-149 Openings
  '(^|(?P<show>.*?)[ _\.\-]+)(ED|NCED|ENDING) ?(?P<ep>\d{1,2}[a-z]?)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                       #  8 # 150-199 Endings
  '(^|(?P<show>.*?)[ _\.\-]+)(TRAILER|PROMO|PV|T) ?(?P<ep>\d{1,2}) ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                          #  9 # 200-299 Trailer, Promo with a  number  '(^|(?P<show>.*?)[ _\.\-]+)((?<=E)P|PARODY|PARODIES?) ?(?P<ep>\d{1,2})? ?(v2|v3|v4|v5)?(?P<title>.*)$',                                                                        # 10 # 300-399 Parodies
  '(^|(?P<show>.*?)[ _\.\-]+)(O|OTHERS?)(?P<ep>\d{1,2}) ?(v2|v3|v4|v5)?[ _\.\-]+(?P<title>.*)$',                                                                        # 10 # 400-499 Others
  '(^|(?P<show>.*?)[ _\.\-]+)(e|ep|e |ep |e-|ep-)?(?P<ep>[0-9]{1,3})((e|ep|-e|-ep|-)(?P<ep2>[0-9]{1,3})|)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                  # 11 # E01 | E01-02| E01-E02 | E01E02                                                                                                                       # __ # look behind: (?<=S) < position < look forward: (?!S)
  '(^|(?P<show>.*?)[ _\.\-]+)S ?(?P<ep>\d{1,2}) ?(?P<title>.*)$']                                                                                                       # 12 # 001-099 Specials #'S' moved to the end to make sure season strings are not caught in prev regex
ignore_dirs_rx  = [ '@Recycle', '.@__thumb', 'lost\+found', '.AppleDouble','$Recycle.Bin', 'System Volume Information', 'Temporary Items', 'Network Trash Folder', '@eaDir', 'Extras', 'Samples?', 'bonus', '.*bonus disc.*', 'trailers?', '.*_UNPACK_.*', '.*_FAILED_.*', 'misc', '_Misc'] #, "VIDEO_TS"]# Filters.py  removed '\..*',        
ignore_files_rx = ['[-\._ ]sample', 'sample[-\._ ]', '-Recap\.', 'OST', 'soundtrack', 'Thumbs.db', '.plexignore']                                                       # Skipped files (samples, trailers)                                                          
video_exts      = [ '3g2', '3gp', 'asf', 'asx', 'avc', 'avi', 'avs', 'bin', 'bivx', 'divx', 'dv', 'dvr-ms', 'evo', 'fli', 'flv', 'img', 'iso', 'm2t', 'm2ts', 'm2v',    #
                    'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'mts', 'nrg', 'nsv', 'nuv', 'ogm', 'ogv', 'tp', 'pva', 'qt', 'rm', 'rmvb', 'sdp', 'swf', 'svq3', 'strm', #
                    'ts', 'ty', 'vdr', 'viv', 'vp3', 'wmv', 'wpl', 'wtv', 'xsp', 'xvid', 'webm', 'ifo']                                                                 # DVD: 'ifo', 'bup', 'vob'
FILTER_CHARS    = "\\/:*?<>|~;_."                                                                                                                                       # Windows file naming limitations + "~-,._" + ';' as plex cut title at this for the agent
whack_pre_clean = ["x264-FMD Release", "x264-h65", "x264-mSD", "x264-BAJSKORV", "x264-MgB", "x264-SYS", "x264-FQM", "x264-ASAP", "x264-QCF", "x264-W4F", 'x264-w4f', "x264-AAC", 
  'x264-2hd', "x264-ASAP", 'x264-bajskorv', 'x264-batv', "x264-BATV", "x264-EXCELLENCE", "x264-KILLERS", "x264-LOL", 'x264-MgB', 'x264-qcf', 'x264-SnowDoN', 'x264-xRed', 
  "H.264-iT00NZ", "H.264.iT00NZ", 'H264-PublicHD', "H.264-BS", 'REAL.HDTV', "WEB.DL", "H_264_iT00NZ", "www.crazy-torrent.com", "ReourceRG Kids Release",
  "By UniversalFreedom", "XviD-2HD", "XviD-AFG", "xvid-aldi", 'xvid-asap', "XviD-AXED", "XviD-BiA-mOt", 'xvid-fqm', "xvid-futv", 'xvid-killer', "XviD-LMAO", 'xvid-pfa',
  'xvid-saints', "XviD-T00NG0D", "XViD-ViCKY", "XviD-BiA", "XVID-FHW", "PROPER-LOL", "5Banime-koi_5d", "%5banime-koi%5d", "minitheatre.org", "mthd bd dual", "WEB_DL",
  "HDTV-AFG", "HDTV-LMAO", "ResourceRG Kids", "kris1986k_vs_htt91",   'web-dl', "-Pikanet128", "hdtv-lol", "REPACK-LOL", " - DDZ", "OAR XviD-BiA-mOt", "3xR", "(-Anf-)",
  "Anxious-He", "Coalgirls", "Commie", "DarkDream", "Doremi", "ExiledDestiny", "Exiled-Destiny", "Exiled Destiny", "FFF", "FFFpeeps", "Hatsuyuki", "HorribleSubs", 
  "joseole99", "(II Subs)", "OAR HDTV-BiA-mOt", "Shimeji", "(BD)", "(RS)", "Rizlim", "Subtidal", "Seto-Otaku", "OCZ", "_dn92__Coalgirls__", 
  "(BD 1280x720 Hi10P)", "(DVD_480p)", "(1080p_10bit)", "(1080p_10bit_DualAudio)", "(Tri.Audio)", "(Dual.Audio)", "(BD_720p_AAC)", "x264-RedBlade",
  "BD 1080p", "BD 960p", "BD 720p", "BD_720p", "TV 720p", "DVD 480p", "DVD 476p", "DVD 432p", "DVD 336p", "1080p.BluRay",
  "1920x1080", "1280x720", "848x480", "952x720", "(DVD 720x480 h264 AC3)", "(720p_10bit)", "(1080p_10bit)", "(1080p_10bit", "(BD.1080p.AAC)",
  "H.264_AAC", "Hi10P", "Hi10", "x264", "BD 10-bit", "DXVA", "H.264", "(BD, 720p, FLAC)", "Blu-Ray", "Blu-ray",  "SD TV", "SD DVD", "HD TV",  "-dvdrip", "dvd-jap", "(DVD)", 
  "FLAC", "Dual Audio", "AC3", "AC3.5.1", "AC3-5.1", "AAC2.0", "AAC.2.0", "AAC2_0", "AAC", 'DD5.1', "5.1",'divx5.1', "DD5_1", "TV-1", "TV-2", "TV-3", "TV-4", "TV-5",
  "(Exiled_Destiny)", "1080p", "720p", "480p", "_BD", ".XVID", "(xvid)", "dub.sub_ja+.ru+", "dub.sub_en.ja", "dub_en",
  "-Cd 1", "-Cd 2", "Vol 1", "Vol 2", "Vol 3", "Vol 4", "Vol 5", "Vol.1", "Vol.2", "Vol.3", "Vol.4", "Vol.5",
  "%28", "%29", " (1)", "(Clean)"]                                                                                                                                      #include spaces, hyphens, dots, underscore, case insensitive
whack = [ #lowercase                                                                                                                                                    ### Tags to remove ###
  'x264', 'h264', 'dvxa', 'divx', 'xvid', 'divx51', 'mp4', "avi", '8bit', '8-bit', 'hi10', 'hi10p', '10bit', '10-bit', 'crf24', 'crf 24', 'hevc',                       # Video Codecs (color depth and encoding, Resolution)
  '480p', '576p', '720p', '1080p', '1080i',                                                                                                                             #       
  '24fps', '25fps', 'ntsc', 'pal', 'ntsc-u', 'ntsc-j',                                                                                                                  # Refresh rate, Format
  'mp3', 'ogg', 'ogm', 'vorbis', 'aac', 'dts', 'ac3', 'ac-3', '5.1ch', '5.1', '7.1ch',  'qaac',                                                                         # Audio Codecs, channels
  'dc', 'se', 'extended', 'unrated', 'multi', 'multisubs', 'dubbed', 'dub', 'subbed', 'sub', 'engsub', 'eng', 'french', 'fr', 'jap',                                    # edition (dc = directors cut, se = special edition), subs and dubs
  'custom', 'internal', 'repack', 'proper', 'rerip', "raw", "remastered", "uncensored", 'unc', 'cen',                                                                   # format
  'cd1', 'cd2', 'cd3', 'cd4', '1cd', '2cd', '3cd', '4cd', 'xxx', 'nfo', 'read.nfo', 'readnfo', 'nfofix', 'fragment', 'ps3avchd', 'remux', 'fs', 'ws', "- copy", "reenc", "hom",# misc
  'retail', 'webrip', 'web-dl', 'wp', 'workprint', "mkv",  "v1", "v2", "v3", "v4",                                                                                      # release type: retail, web, work print
  'bdrc', 'bdrip', 'bluray', 'bd', 'brrip', 'hdrip', 'hddvd', 'hddvdrip', 'wsrip',                                                                                      # Source: bluray
  'ddc', 'dvdrip', 'dvd', 'r1', 'r3', 'r5', "dvd", 'svcd', 'vcd', 'sd', 'hd', 'dvb', "release",                                                                         # DVD, VCD, S-VCD
  'dsr', 'dsrip', 'hdtv', 'pdtv', 'ppv', 'stv', 'tvrip', 'complete movie', "hiei", "metis", "norar",                                                                    # dtv, stv
  'cam', 'bdscr', 'dvdscr', 'dvdscreener', 'scr', 'screener', 'tc', 'telecine', 'ts', 'telesync', 'mp4',                                                                # screener
  "mthd", "thora", 'sickrage', 'brrip', "remastered", "yify", "tsr", "reidy", "gerdhanse",                                                                              #'limited', 
  'rikou', 'homЯ', "it00nz", "nn92", "mthd", "elysium", "encodebyjosh", "krissy", "reidy", "it00nz", "s4a"]                                                             #
CHARACTERS_MAP = {
  14844057:"'", 14844051:'-', 14844070:'...', 15711386:':', 14846080:'∀',                                                                                               #['’' \xe2\x80\x99] ['–' \xe2\x80\x93] ['…' \xe2\x80\xa6] # '：' # 12770:'', # '∀ Gundam' no need #'´' ['\xc2', '\xb4']
  50048:'A' , 50050:'A' , 50052:'Ä' , 50080:'a' , 50082:'a' , 50084:'a' , 50305:'a' , 50308:'A' , 50309:'a' ,  50055:'C' , 50087:'c' , 50310:'C' , 50311:'c' ,          #'à' ['\xc3', '\xa0'] #'â' ['\xc3', '\xa2'] #'Ä' ['\xc3', '\x84'] #'ā' ['\xc4', '\x81'] #'À' ['\xc3', '\x80'] #'Â' ['\xc3', '\x82'] # 'Märchen Awakens Romance', 'Rozen Maiden Träumend' #'Ç' ['\xc3', '\x87'] #'ç' ['\xc3', '\xa7'] 
  50057:'E' , 50088:'e' , 50089:'e' , 50090:'e' , 50091:'e' , 50323:'e' , 50328:'E' , 50329:'e' ,                                                                       #'É' ['\xc3', '\x89'] #'è' ['\xc3', '\xa8'] #'é' ['\xc3', '\xa9'] #'ē' ['\xc4', '\x93'] #'ê' ['\xc3', '\xaa'] #'ë' ['\xc3', '\xab']
  50094:'i' , 50095:'i' , 50347:'i' , 50561:'L' , 50562:'l' , 50563:'N' , 50564:'n' , 50097:'n' ,                                                                       #'î' ['\xc3', '\xae'] #'ï' ['\xc3', '\xaf'] #'ī' ['\xc4', '\xab'] #'ñ' ['\xc3', '\xb1']
  50067:'O' , 50068:'Ô' , 50072:'O' , 50099:'o' , 50100:'o' , 50102:'o' , 50573:'o' , 50578:'OE', 50579:'oe',                                                           #'Ø' ['', '']         #'Ô' ['\xc3', '\x94'] #'ô' ['\xc3', '\xb4'] #'ō' ['\xc5', '\x8d'] #'Œ' ['\xc5', '\x92'] #'œ' ['\xc5', '\x93']
  53423:'Я' , 50586:'S' , 50587:'s' , 50079:'ss', 50105:'u' , 50107:'u' , 50108:'u' , 50071:'x' , 50617:'Z' , 50618:'z' , 50619:'Z' , 50620:'z' ,                       #'Я' ['\xd0', '\xaf'] #'ß' []               #'ù' ['\xc3', '\xb9'] #'û' ['\xc3', '\xbb'] #'ü' ['\xc3', '\xbc'] #'²' ['\xc2', '\xb2'] #'³' ['\xc2', '\xb3'] #'×' ['\xc3', '\x97'],
  49835:'«' , 49842:'²' , 49843:'³' , 49844:"'" , 49847:' ' , 49848:'¸',  49851:'»' , 49853:'½', 52352:'', 52353:''}                                                    #'«' ['\xc2', '\xab'] #'·' ['\xc2', '\xb7'] #'»' ['\xc2', '\xbb']# 'R/Ranma ½ Nettou Hen'  #'¸' ['\xc2', '\xb8'] #'̀' ['\xcc', '\x80'] #  ['\xcc', '\x81'] 

### Log + LOG_PATH calculated once for all calls ###
LOG_PATHS = { 'win32':  [ '%LOCALAPPDATA%\\Plex Media Server\\Logs',                                       # Windows Vista/7/8
                          '%USERPROFILE%\\Local Settings\\Application Data\\Plex Media Server\\Logs' ],    # Windows XP, 2003, Home Server
              'darwin': [ '$HOME/Library/Application Support/Plex Media Server/Logs' ],                    # LINE_FEED = "\r"
              'linux':  [ '$PLEX_HOME/Library/Application Support/Plex Media Server/Logs',                 # Linux
                          '$PLEX_MEDIA_SERVER_APPLICATION_SUPPORT_DIR/Plex Media Server/Logs',             # Slack, Ubuntu/Fedora, Synology
                          '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Logs',            #  Ubuntu/Fedor
                          '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Logs',            # QNAP
                          '/volume1/Plex/Library/Application Support/Plex Media Server/Logs',                # Synology, Asustor
                          '/c/.plex/Library/Application Support/Plex Media Server/Logs',                     # ReadyNAS
                          '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs',     # Debian, Fedora, CentOS, Ubuntu
                          '/usr/local/plexdata/Plex Media Server/Logs',                                    # FreeBSD
                          '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/Logs',                # FreeNAS
                          '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/Logs/',                          # FreeNAS
                          '/share/CACHEDEV1_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Logs',    # QNAP
                          '/volume2/Plex/Library/Application Support/Plex Media Server/Logs',              # Synology, if migrated a second raid volume as unique volume in new box         
                          '/raid0/data/module/Plex/sys/Plex Media Server/Logs',                            # Thecus
                          '/raid0/data/PLEX_CONFIG/Plex Media Server/Logs',                                # Thecus Plex community version
                          '/config/Library/Application Support/Plex Media Server/Logs'] }                  # Docker linuxserver/plex

### Log message in log file #######################################################################################################################################
def Log(entry, filename=None): 
  with open(os.path.join(LOG_PATH, filename if filename else LOG_FILE_LIBRARY), 'a') as file:
    file.write(("" if no_timestamp else time.strftime("%Y-%m-%d %H:%M:%S") + " ") + entry + "\n")

### Check config files on boot up then create library variables ###    #platform = xxx if callable(getattr(sys,'platform')) else "" 
platform = sys.platform.lower() if "platform" in dir(sys) and not sys.platform.lower().startswith("linux") else "linux" if "platform" in dir(sys) else Platform.OS.lower()
for LOG_PATH in LOG_PATHS[platform] if platform in LOG_PATHS else [ os.path.join(os.getcwd(),"Logs"), '$HOME']:
  if '%' in LOG_PATH or '$' in LOG_PATH:  LOG_PATH = os.path.expandvars(LOG_PATH)  # % on win only, $ on linux
  if os.path.isdir(LOG_PATH):             break                                    # os.path.exists(LOG_PATH)
else: LOG_PATH = os.path.expanduser('~')                                           # logging.basicConfig(), logging.basicConfig(filename=os.path.join(absolute_path, 'Plex Media Scanner (custom ASS).log'), level=logging.INFO) #logging.error('Failed on {}'.format(filename))
LOG_FILE_LIBRARY     = LOG_FILE = 'Plex Media Scanner (custom ASS).log'            # Log filename library will include the library name, LOG_FILE not and serve as reference
no_timestamp         = os.path.isfile(os.path.join(LOG_PATH, "no_timestamp"        ))
keep_zero_size_files = os.path.isfile(os.path.join(LOG_PATH, "keep_zero_size_files"))
season_from_folder   = os.path.isfile(os.path.join(LOG_PATH, "season_from_folder"  ))

PLEX_LIBRARY, PLEX_LIBRARY_URL = {}, "http://127.0.0.1:32400/library/sections/"  # Allow to get the library name to get a log per library https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token
if os.path.isfile(os.path.join(LOG_PATH, "X-Plex-Token.id")):                                                    #Log("'X-Plex-Token.id' file present")
  with open(os.path.join(LOG_PATH, "X-Plex-Token.id"), 'r') as token_file:  PLEX_LIBRARY_URL += "?X-Plex-Token=" + token_file.read().strip()  #Log("PLEX_LIBRARY_URL: '%s', token: '%s'" % (PLEX_LIBRARY_URL, token))
try:
  library_xml = etree.fromstring(urllib2.urlopen(PLEX_LIBRARY_URL).read())
  for library in library_xml.iterchildren('Directory'):
    for path in library.iterchildren('Location'):  PLEX_LIBRARY[path.get("path")] = library.get("title")
except:  Log("Place correct Plex token in X-Plex-Token.id file in logs folder or in PLEX_LIBRARY_URL variable to have a log per library - https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token")

### replace a string by another while retaining original string case ##############################################################################################
def replace_insensitive (ep, word, sep=" "):
  if ep.lower()==word.lower(): return ""
  position = ep.lower().find(word.lower())
  if position > -1 and len(ep)>len(word):  return (""  if position==0 else ep[:position].lstrip()) + (sep if len(ep) < position+len(word) else ep[position+len(word):].lstrip())

### Turn a string into a list of string and number chunks  "z23a" -> ["z", 23, "a"] ###############################################################################
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):  return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]

### Return number of bytes of Unicode characters ########################################################
def unicodeLen (char):                                           # count consecutive 1 bits since it represents the byte numbers-1, less than 1 consecutive bit (128) is 1 byte , less than 23 bytes is 1
  for x in range(1,6):                                           # start at 1, 6 times 
    if ord(char) < 256-pow(2, 7-x)+(2 if x==6 else 0): return x  # 256-2pow(x) with x(7->0) = 128 192 224 240 248 252 254 255 = 1 to 8 bits at 1 from the left, 256-2pow(7-x) starts form left

### Decode string back to Unicode ###   #Unicodize in utils?? #fixEncoding in unicodehelper
def encodeASCII(string, language=None): #from Unicodize and plex scanner and other sources
  if string=="": return ""
  ranges = [ {"from": ord(u"\u3300"), "to": ord(u"\u33ff")}, {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")}, {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},  # compatibility ideographs
             {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")}, {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},                                                  # Japanese Kana    # cjk radicals supplement
             {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")}, {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")}]                                                  # windows: TypeError: ord() expected a character, but string of length 2 found #{"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")}, #{"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")}, #{"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")}, #{"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}, # included as of Unicode 8.0                             #{"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}  # compatibility ideographs
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
  while i < len(string):                                       ### loop through unicode and replace special chars with spaces then map if found ###
    if ord(string[i])<128:  i = i+1
    else: #non ascii char
      char, char2, char3, char_len = 0, "", [], unicodeLen(string[i])
      for x in range(0, char_len):
        char = 256*char + ord(string[i+x]); char2 += string[i+x]; char3.append(string[i+x])
        if not x==0: string[i] += string[i+x]; string[i+x]=''
      try:    asian_language = any([mapping["from"] <= ord("".join(char3).decode('utf8')) <= mapping["to"] for mapping in ranges])
      except: asian_language = False
      if char in CHARACTERS_MAP:  string[i]=CHARACTERS_MAP.get( char )
      elif not asian_language:    Log("*Character missing in CHARACTERS_MAP: %d:'%s'  , #'%s' %s, string: '%s'" % (char, char2, char2, char3, original_string))
      i += char_len
  return ''.join(string)

### Allow to display ints even if equal to None at times ################################################
def clean_string(string, no_parenthesis=False, no_whack=False, no_dash=False):
  if not string: return ""                                                                                                                                    # if empty return empty string
  if no_parenthesis:                                                                                                                                          # delete parts between parenthesis if needed
    while re.match(".*\([^\(\)]*?\).*", string):                 string = re.sub(r'\([^\(\)]*?\)', ' ', string)                                               #   support imbricated parrenthesis like: "Cyborg 009 - The Cyborg Soldier ((Cyborg) 009 (2001))"
  if re.search("(\[|\]|\{|\})", string):                         string = re.sub("(\[|\]|\{|\})", "", re.sub(r'[\[\{](?![0-9]{1,3}[\]\}]).*?[\]\}]', ' ', string))  # remove "[xxx]" groups but ep numbers inside brackets as Plex cleanup keep inside () but not inside [] #look behind: (?<=S) < position < look forward: (?!S)
  string = encodeASCII(string)                                                                                                                                # Translate them
  if not no_whack:
    for word in whack_pre_clean:                                 string = replace_insensitive(string, word) if word.lower() in string.lower() else string     # Remove words present in pre-clean list
  string = re.sub(r'(?P<a>[^0-9Ssv])(?P<b>[0-9]{1,3})\.(?P<c>[0-9]{1,2})(?P<d>[^0-9])', '\g<a>\g<b>DoNoTfIlTeR\g<c>\g<d>', string)                            # Used to create a non-filterable special ep number (EX: 13.5 -> 13DoNoTfIlTeR5) # Restricvted to max 999.99 # Does not start with a season/special char 'S|s' (s2.03) or a version char 'v' (v1.2)
  for char, subst in zip(list(FILTER_CHARS), [" " for x in range(len(FILTER_CHARS))]) + [("`", "'"), ("(", " ( "), (")", " ) ")]:                             # remove leftover parenthesis (work with code a bit above)
    if char in string:                                           string = string.replace(char, subst)                                                         # translate anidb apostrophes into normal ones #s = s.replace('&', 'and')
  string = string.replace("DoNoTfIlTeR", '.')                                                                                                                 # Replace 13DoNoTfIlTeR5 into 13.5 back
  if re.match(".*?[\(\[\{]?[0-9a-fA-F]{8}[\[\)\}]?.*", string):  string = re.sub('[0-9a-fA-F]{8}', ' ', string)                                               # CRCs removal
  if re.search("[0-9]{3,4} ?[Xx] ?[0-9]{3,4}", string):          string = re.sub('[0-9]{3,4} ?[Xx] ?[0-9]{3,4}', ' ', string)                                 # Video size ratio removal
  if string.endswith(", The"):                                   string = "The " + ''.join( string.split(", The", 1) )                                        # ", The" is rellocated in front
  if string.endswith(", A"  ):                                   string = "A "   + ''.join( string.split(", A"  , 1) )                                        # ", A"   is rellocated in front
  if not no_whack:                                               string = " ".join([word for word in filter(None, string.split()) if word.lower() not in whack]).strip()  # remove double spaces + words present in "whack" list #filter(None, string.split())
  if no_dash:                                                    string = re.sub("-", " ", string)                                                            # replace the dash '-'
  string = re.sub(r'\([-Xx]?\)', '', re.sub(r'\( *(?P<internal>[^\(\)]*?) *\)', '(\g<internal>)', string))                                                    # Remove internal spaces in parenthesis then remove empty parenthesis
  string = " ".join([word for word in filter(None, string.split())]).strip()                                                                                  # remove multiple spaces
  for rx in ("-"):                                               string = string[len(rx):   ].strip() if string.startswith(rx)       else string              # In python 2.2.3: string = string.strip(string, " -_") #if string.startswith(("-")): string=string[1:]
  for rx in ("-", "- copy"):                                     string = string[ :-len(rx) ].strip() if string.lower().endswith(rx) else string              # In python 2.2.3: string = string.strip(string, " -_")
  return string

### Add files into Plex database ########################################################################
def add_episode_into_plex(mediaList, file, root, path, show, season=1, ep=1, title="", year=None, ep2="", rx="", tvdb_mapping={}):
  file=os.path.join(root,path,file);                                                                                   #
  if not keep_zero_size_files and str(os.path.getsize(file))=="0":         return                                      # do not keep dummy files by default unless this file present in Logs folder
  #if os.path.isfile(os.path.join(LOG_PATH,"dummy.mp4")):                   file = os.path.join(LOG_PATH,"dummy.mp4")  # with dummy.mp4(not empy file) in Logs folder to get rid of Plex Media Scanner.log exceptions, it will remove most eps with size 0 which oculd remove series
  if title==title.lower() or title==title.upper() and title.count(" ")>0:  title = title.title()                       # capitalise if all caps or all lowercase and one space at least
  if ep==0:                                                                season, ep, ep2       = 0, 1, 1             # s01e00 and S00e00 => s00e01
  if not ep2 or ep > ep2:                                                  ep2                   = ep                  #  make ep2 same as ep for loop and tests
  if tvdb_mapping and ep  in tvdb_mapping and season != 0:                 season, ep  = tvdb_mapping[ep ]
  if tvdb_mapping and ep2 in tvdb_mapping and season != 0:                 season, ep2 = tvdb_mapping[ep2]
  for epn in range(ep, ep2+1):
    if len(show) == 0: Log("Warning - show: '%s', s%02de%03d-%03d, file: '%s' has show empty, report logs to dev ASAP" % (show, season, ep, ep2, file))
    else:
      tv_show, tv_show.display_offset = Media.Episode(show, season, epn, title, year), (epn-ep)*100/(ep2-ep+1)
      if os.path.basename(file).upper()=="VIDEO_TS.IFO":  
        for item in os.listdir(os.path.dirname(file)) if os.path.dirname(file) else []:
          if item.upper().startswith("VTS_01_") and not item.upper()=="VTS_01_2.VOB":  tv_show.parts.append(os.path.join(os.path.dirname(file), item))
      else:  tv_show.parts.append(file)
      mediaList.append(tv_show)   # at this level otherwise only one episode per multi-episode is showing despite log below correct
  index = str(series_rx.index(rx)) if rx in series_rx else str(anidb_rx.index(rx)+len(series_rx)) if rx in anidb_rx else ""  # rank of the regex used from 0
  Log("\"%s\" s%04de%03d%s \"%s\"%s%s" % (show, season, ep, "" if ep==ep2 else "-%03d" % ep2, os.path.basename(file), " \"%s\"" % index if index else "", " \"%s\" " % title if title else ""))

### Look for episodes ###################################################################################
def Scan(path, files, mediaList, subdirs, language=None, root=None, **kwargs): #get called for root and each root folder

  global LOG_FILE_LIBRARY;
  LOG_FILE_LIBRARY = LOG_FILE[:-4] + " - " + PLEX_LIBRARY[root] + LOG_FILE[-4:] if root in PLEX_LIBRARY else LOG_FILE  ### Rename log file with library name if XML file can be accessed or token file present in log folder. LOG_FILE stays un-touched, and is used to custom update LOG_FILE_LIBRARY with the library name
  FILELIST = LOG_FILE_LIBRARY[:-4] + " - filelist " + os.path.basename(root) + LOG_FILE_LIBRARY[-4:]                   # custom log file per library root folder
  if not path:  open(os.path.join(LOG_PATH, FILELIST), 'w').close                                                      #Empty file for root folder call
  if path == "" :
    Log(("=== Library \"%s\", Root: \"%s\",  Launched: '%s'" % (PLEX_LIBRARY[root] if root in PLEX_LIBRARY else "X-Plex-Token.id missing", root, time.strftime("%Y-%m-%d %H:%M:%S"))).ljust(157, '='))
    Log("keep_zero_size_files: '%s'" % str(keep_zero_size_files))
    Log("no_timestamp:         '%s'" % str(no_timestamp        ))
    Log("season_from_folder:   '%s'" % str(season_from_folder  ))
    Log("".ljust(157, '='))
  Log("Scanner call - root: '%s', path: '%s', dirs: '%d', files: '%d'" % (root, path, len(subdirs), len(files)));  Log("".ljust(157, '='))  # Exit every other iteration than the root scan
  for subdir in subdirs:                                                    #
    for rx in ignore_dirs_rx:                                               # if initial scan and root folder
      if re.match(rx, os.path.basename(subdir), re.IGNORECASE): subdirs.remove(subdir);  Log("\"%s\" match ignore_dirs_rx: \"%s\"" % (subdir, rx));  break  #skip dirs to be ignored
  reverse_path = list(reversed(Utils.SplitPath(path)))
  files_to_remove = []
  for file in files:
    ext = os.path.splitext(file)[1].lstrip('.').lower()
    if ext in video_exts:
      for rx in ignore_files_rx:                                                                                        # Filter trailers and sample files
        if re.match(rx, file, re.IGNORECASE):  Log("File:   '%s' match ignore_files_rx: '%s'" % (file, rx)); files_to_remove.append(file);  break
      else:  
        with open(os.path.join(LOG_PATH, FILELIST), 'a') as log_file:  log_file.write(file + "\n")  #add to filelist
    else:  Log("file: '%s', ext: '%s' not in video_ext" % (file, ext));  files_to_remove.append(file);  continue
  for file in files_to_remove:  files.remove(file)
  if len(files)==0:  return  # If direct scanner call on folder (not root) then skip if no files as will be called on subfolders too
  
  ### bluray/DVD folder management ### # source: https://github.com/doublerebel/plex-series-scanner-bdmv/blob/master/Plex%20Series%20Scanner%20(with%20disc%20image%20support).py
  if len(reverse_path) >= 3 and reverse_path[0].lower() == 'stream' and reverse_path[1].lower() == 'bdmv' or "VIDEO_TS.IFO" in str(files).upper():
    for temp in ['stream', 'bdmv', 'video_ts']:
      if reverse_path[0].lower() == temp:  reverse_path.pop(0)
    ep, disc = clean_string(reverse_path[0], True), True
    if len(reverse_path)>1:  reverse_path.pop(0)
    Log("BluRay/DVD folder detected - using as equivalent to filename ep: '%s', show: '%s'" % (ep, reverse_path[0]))
  else: disc = False
  
  ### Extract season folder to reduce complexity and use folder as serie name ###
  folder_season =  None
  for last_folder in reverse_path[:-1]:                 # remove root folder from test, [:-1] Doesn't thow errors but gives an empty list if items don't exist, might not be what you want in other cases
    for rx in season_rx :                               # in anime, more specials folders than season folders, so doing it first
      match = re.match(rx, last_folder, re.IGNORECASE)  #
      if match:
        if rx!=season_rx[-1]:  folder_season = int( match.group('season')) if match.groupdict().has_key('season') and match.group('season') else 0 #get season number but Skip last entry in seasons (skipped folders)
        reverse_path.remove(last_folder);  break        # All ways to remove: reverse_path.pop(-1), reverse_path.remove(thing|array[0])
    if match and rx!=season_rx[-1]:  break              # cascade break if not skipped folder since season number found
    Log("len rev path: '%s', path count /: '%s'" % (len(reverse_path), path.count("/")))
    if len(reverse_path)>1 and path.count("/"):         #if grouping folders, skip and add them as additionnal folders
      Log("Grouping folder: '%s' skipped, need to be added as root folder if needed" % path)
      Log("".ljust(157, '-'))
      return
  folder_show = reverse_path[0] if reverse_path else ""
  
  ### Capture guid from folder name or id file in serie or serie/Extras folder ###
  guid = ""
  if not re.search(".*? ?\[(anidb|tvdb|tvdb2|tvdb3|tvdb4|tmdb|imdb)-(tt)?[0-9]{1,7}\]", folder_show, re.IGNORECASE):
    for file in ("anidb.id", "Extras/anidb.id", "tvdb.id", "Extras/tvdb.id", "tvdb2.id", "Extras/tvdb2.id", "tvdb3.id", "Extras/tvdb3.id", "tvdb4.id", "Extras/tvdb4.id", "tmdb.id", "Extras/tmdb.id", "tsdb.id", "Extras/tsdb.id", "imdb.id", "Extras/imdb.id"):
      if os.path.isfile(os.path.join(root, "/".join(reversed(reverse_path)), file)):
        with open(os.path.join(root, "/".join(reversed(reverse_path)), file), 'r') as guid_file:
          guid        = guid_file.read().strip()
          folder_show = "%s [%s-%s]" % (clean_string(reverse_path[0]), os.path.splitext(os.path.basename(file))[0], guid)
        break
    else:  folder_show = folder_show.replace(" - ", " ").split(" ", 2)[2] if folder_show.lower().startswith(("saison","season","series")) and len(folder_show.split(" ", 2))==3 else clean_string(folder_show) # Dragon Ball/Saison 2 - Dragon Ball Z/Saison 8 => folder_show = "Dragon Ball Z"
        
  ### Capture if absolute numbering should be applied for all episode numbers  ###
  guid, tvdb_mode, tvdb_mapping = "", "", {}
  if re.search(".*? ?\[(tvdb2|tvdb3)-(tt)?[0-9]{1,7}\]", folder_show, re.IGNORECASE): 
    tvdb_mode = "3" if "[tvdb3-" in folder_show else "2" if "[tvdb2-" in folder_show else "1" if "[tvdb-" in folder_show else "0"  # mode 1 normal, mode 2 season mode (ep reset to 1), mode 3 hybrid mode (ep stay in absolute numbering put put in seasons)
    guid = folder_show.split("[tvdb")[1].split("-")[1].split("]")[0]
    Log("folder_show: '%s', tvdb id: '%s'" % (folder_show, guid))
    
    try:
      Log("TVDB season mode (%s) enabled, serie url: 'https://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/en.xml'" % (tvdb_mode, guid))
      tvdbanime =  etree.fromstring( urllib2.urlopen('https://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/en.xml' % guid).read() )
      ep_count, abs_manual_placement_info, abs_manual_placement_worked, number_set = 0, [], True, False
      for episode in tvdbanime.xpath('Episode'):
        if episode.xpath('SeasonNumber')[0].text != '0':
          ep_count = ep_count + 1
          if not episode.xpath('absolute_number')[0].text:
            episode.xpath('absolute_number')[0].text, number_set = str(ep_count), True
            abs_manual_placement_info.append("s%se%s = abs %s" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text, episode.xpath('absolute_number')[0].text))
          elif not number_set:  ep_count = int(episode.xpath('absolute_number')[0].text)
          else:
            Log("An abs number has been found on ep (s%se%s) after starting to manually place our own abs numbers" % (episode.xpath('SeasonNumber')[0].text, episode.xpath('EpisodeNumber')[0].text) )
            abs_manual_placement_worked = False
            break
      Log("abs_manual_placement_worked: '%s', abs_manual_placement_info: '%s'" % (str(abs_manual_placement_worked), str(abs_manual_placement_info)))
      if abs_manual_placement_worked:
        for episode in tvdbanime.xpath('Episode'):
          SeasonNumber    = episode.xpath('SeasonNumber'   )[0].text if episode.xpath('SeasonNumber'   )[0].text else ''
          EpisodeNumber   = episode.xpath('EpisodeNumber'  )[0].text if episode.xpath('EpisodeNumber'  )[0].text else ''
          absolute_number = episode.xpath('absolute_number')[0].text if episode.xpath('absolute_number')[0].text else ''
          if absolute_number:  tvdb_mapping[int(absolute_number)] = (int(SeasonNumber), int(EpisodeNumber) if tvdb_mode=="2" else int(absolute_number))
    except Exception as e:  Log("xml loading issue"); Log(e)
        
  ### File main loop ###
  movie_list, AniDB_op, counter = {}, {}, 500;  files.sort(key=natural_sort_key)
  for file in files:
    ext = file[1:] if file.count('.')==1 and file.startswith('.') else os.path.splitext(file)[1].lstrip('.').lower()  # Otherwise .plexignore file has extension ""
    if ext=="ifo" and not file.upper()=="VIDEO_TS.IFO":  continue
    
    filename, year                           = os.path.splitext(os.path.basename(file))[0] if not disc else ep, ""
    show, season, ep, ep2, title, folder_use = folder_show, folder_season if folder_season else 1, clean_string(filename, False), None, "", False
    #Log("Initial: show '%s', season '%s', ep '%s', filename '%s'" % (show, season, ep, filename))
    if not path and " - Complete Movie" in ep:                                                                 ep, title, show = "01", ep.split(" - Complete Movie")[0], ep.split(" - Complete Movie")[0];   ### Movies ### If using WebAOM (anidb rename) and movie on root
    elif clean_string(filename, True, no_dash=True)==clean_string(folder_show, True, no_dash=True):            ep, title,      = "01", folder_show                  ### If a file name matches the folder name, place as episode 1
    elif len(files)==1:
      if   ("movie" in ep.lower()+folder_show.lower() or "gekijouban" in folder_show.lower()):                 ep, title,      = "01", folder_show                  ### Movies ### If only one file in the folder & contains '(movie|gekijouban)' in the file or folder name
      elif "-m" in clean_string(folder_show).split():                                                          ep, title,      = "01", folder_show                  ### Movies ### If only one file in the folder & contains '-m' in the folder name denoting a movie folder
      elif not re.search("\d+(\.\d+)?", clean_string(filename, True)):                                         ep, title,      = "01", folder_show                  ### Movies/Single Ep Shows ### If only one file in the folder & it has no numbers in it (as would otherwise force it to a 500+ special)
    elif folder_show:                                                                                                                                               # if not at root and containing folder exist and has name different from "_" (scrubed to "")
      for prefix in (folder_show, clean_string(folder_show, True), clean_string(folder_show, no_dash=True), clean_string(folder_show, True, no_dash=True)):         # remove cleansed folder name from cleansed filename and remove potential space
        if ep.lower().startswith(prefix.lower()):                                                              ep, folder_use = ep[len(prefix):].lstrip('- '), True; break
      if folder_season > 1:                                                                                                                                         # 
        for prefix in ("%s s%d" % (folder_show, folder_season), "%s s%02d" % (folder_show, folder_season)):                                                         #"%s %d " % (folder_show, folder_season), 
          if ep.lower().startswith(prefix.lower()):                                                            ep = replace_insensitive(ep, prefix , "").lstrip()   # Series S2  like transformers (bad naming)  # Serie S2  in season folder, Anidb specials regex doesn't like
      if ep.lower().startswith("special") or "omake" in ep.lower() or "picture drama" in ep.lower():           season, title = 0, ep.title()                        # If specials, season is 0 and if title empty use as title ### 
    #Log("Second Initial: show '%s', season '%s', ep '%s'" % (show, season, ep))
    words, misc = filter(None, ep.split()), filter(None, " ".join( [clean_string(os.path.basename(x), True) for x in files]).lower().split())                       # put all filenames in folder in a string to count if ep number valid or present in multiple files ###clean_string was true ###
    for word in words:                                                                                                                                              #
      ep=word.lower().strip()                                                                                                                                       # cannot use words[words.index(word)] otherwise# if word=='': continue filter prevent "" on double spaces
      if "(" in ep and len(ep)==6 and ep[0]=='(' and ep[5]==')' and ep[1:5].isdigit():                         ep = ep [1:5]                                        # remove parenthesis from year in parenthesis
      if '-' in ep and len(filter(None, ep.split('-',1)))==2:                                                                                                       # If separator in string
        if re.match("^(ep?[ -]?)?(?P<ep>[0-9]{1,3})(-|ep?|-ep?)(?P<ep2>[0-9]{1,3})", ep, re.IGNORECASE):       ep="Skip"; break                                     # if multi ep: make it non digit and exit so regex takes care of it
        elif path and ( (misc.count(ep)==1 and len(files)>=2) or ep not in clean_string(folder_show, True).lower().split() ):
          ep = ep.split('-',1)[0] if ''.join(letter for letter in ep.split('-',1)[0] if letter.isdigit()) else ep.split('-',1)[1];                                  # otherwise all after separator becomes word#words.insert(words.index(word)+1, "-".join(ep.split("-",1)[1:])) #.insert(len(a), x) is equivalent to a.append(x). #???
        else:                                                                                                  continue
      if ep.endswith(("v1", "v2", "v3", "v4")):                                                                ep=ep[:-2].rstrip('-')                               #
      if re.match("((t|o)[0-9]{1,3}$|(sp|special|oav|op|ncop|opening|ed|nced|ending|trailer|promo|pv|others?)($|[0-9]{1,3}$))", ep):  break                         # Specials go to regex # 's' is ignored as dealt with later in prefix processing # '(t|o)' require a number to make sure a word is not accidently matched
      if ep in ("", "-"):                                                                                      continue                                             #
      if ''.join(letter for letter in ep if letter.isdigit())=="":                                             continue                                             # Continue if there are no numbers in the string
      if path and misc.count(ep)>=2:                                                                           continue                                             # Continue if not root folder and string found in in any other filename
      if ep in clean_string(folder_show, True).split() and clean_string(filename, True).split().count(ep)!=2:  continue                                             # Continue if string is in the folder name & string is not in the filename only twice
      if   ep.isdigit() and len(ep)==4 and (int(ep)< 1900 or folder_season and int(ep[0:2])==folder_season):   season, ep = int(ep[0:2]), ep[2:4]                   # 1206 could be season 12 episode 06  #Get assigned from left ot right
      elif ep.isdigit() and len(ep)==4:  filename = clean_string( " ".join(words).replace(ep, "(%s)" % ep));   continue                                             # take everything after supposed episode number
      for prefix in ["ep", "e", "act", "s"]:                                                                                                                        #
        if ep.startswith(prefix) and len(ep)>len(prefix) and re.match("^\d+(\.\d+)?$", ep[len(prefix):]):      ep, season = ep[len(prefix):], 0 if prefix=="s" else season  # E/EP/act before ep number ex: Trust and Betrayal OVA-act1 # to solve s00e002 "Code Geass Hangyaku no Lelouch S5 Picture Drama 02 'Stage 3.25'.mkv" "'Stage 3 25'"
      if "." in ep and ep.split(".", 1)[0].isdigit() and ep.split(".")[1].isdigit():                           season, ep, title = 0, ep.split(".", 1)[0], "Special " + ep; break # ep 12.5 = "12" title "Special 12.5"
      if not path  and not " - Complete Movie" in file:  show = clean_string( " ".join(words[:words.index(word)]) if words.index(word)>0 else "No title", False)  # root folder and 
      title = clean_string( " ".join(words[ words.index(word)+1:]) if len(words)-words.index(word)>1 else "")                                                              # take everything after supposed episode number
      break
    #Log("Words: " + str(words) + " : Loop broken on: '%s'" % ep)
    if ep.isdigit():  add_episode_into_plex(mediaList, file, root, path , show, season, int(ep), title, year, int(ep2) if ep2 and ep2.isdigit() else None, "None", tvdb_mapping);  continue
  
    ### Check for Regex: series_rx + anidb_rx ###
    ep = clean_string(filename, False)  # restart matching from filename
    for rx in series_rx + anidb_rx:
      match = re.search(rx, ep, re.IGNORECASE)
      if match:
        if match.groupdict().has_key('show'  ) and match.group('show'  ) and not path:                show   = clean_string( match.group('show' ))  # Mainly if file at root or _ folder
        if match.groupdict().has_key('title' ) and match.group('title' ):                             title  = clean_string( match.group('title'))
        if match.groupdict().has_key('season') and match.group('season') and not season_from_folder:  season = int(match.group('season'))
        if match.groupdict().has_key('ep2'   ) and match.group('ep2'   ):                             ep2    = match.group('ep2') 
        if match.groupdict().has_key('ep'    ) and match.group('ep'    ):                             ep     = match.group('ep')
        elif rx in anidb_rx[:-2] or rx == anidb_rx[-1]:                                               ep     = "01"
        else:                                                                                                                                                      #No ep number, anidb usefull ?????
          movie_list[season] = movie_list[season]+1 if season in movie_list else 1  # if no ep in regex and anidb special#add movies using year as season, starting at 1  # Year alone is season Year and ep incremented, good for series, bad for movies but cool for movies in series folder...
          ep                 = str(movie_list[season])
        if rx in anidb_rx[:-2] or rx == anidb_rx[-1]:                                                                                 ### AniDB Specials ################################################################
          offset, season = AniDBOffset [ anidb_rx.index(rx) ], 0                                                                      # offset = 100 for OP, 150 for ED, etc... #Log("ep: '%s', rx: '%s', file: '%s'" % (ep, rx, file))
          if not ep.isdigit() and len(ep)>1 and ep[:-1].isdigit():                                                                    ### OP/ED with letter version Example: op2a
            AniDB_op [ offset + int(ep[:-1]) ] = ord( ep[-1:].lower() ) - ord('a')                                                    # {101: 0 for op1a / 152: for ed2b} and the distance between a and the version we have hereep, offset                         = str( int( ep[:-1] ) ), offset + sum( AniDB_op.values() )                             # "if xxx isdigit() else 1" implied since OP1a for example... # get the offset (100, 150, 200, 300, 400) + the sum of all the mini offset caused by letter version (1b, 2b, 3c = 4 mini offset)
            ep, offset                         = str( int( ep[:-1] ) ), offset + sum( AniDB_op.values() )                             # "if xxx isdigit() else 1" implied since OP1a for example... # get the offset (100, 150, 200, 300, 400) + the sum of all the mini offset caused by letter version (1b, 2b, 3c = 4 mini offset)
          ep = str( offset + int(ep))                                                                                                 # Add episode number to the offset, 01 by default from the match group above
        add_episode_into_plex(mediaList, file, root, path , show, season, int(ep), title, year, int(ep2) if ep2 and ep2.isdigit() else None, rx, tvdb_mapping); 
        break
    if match: continue  # next file iteration
    
    ### Ep not found, adding as season 0 episode 501+ ###
    if " - " in ep and len(ep.split(" - "))>1:  title = clean_string(" - ".join(ep.split(" - ")[1:]))  #for word in ep.split(" "): # if word in folder_show:  ep = replace_insensitive (ep, word, sep=" ")         # title.replace(word, "", 1)
    counter = counter+1                                          #                    #
    add_episode_into_plex(mediaList, file, root, path , show, 0, counter, title.strip(), year, None, "")
  Log("".ljust(157, '-'))
  Log("")
  Stack.Scan(path, files, mediaList, subdirs) if "Stack" in sys.modules else Log("Stack.Scan() doesn't exists")
