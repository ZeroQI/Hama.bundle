# -*- coding: utf-8 -*-
### Log variables, regex, skipped folders, words to remove, character maps ###
import sys, os, time, re, fnmatch, unicodedata, urllib2, Utils, VideoFiles, Media #import Stack ### Plex Media Server\Plug-ins\Scanners.bundle\Contents\Resources\Common ###
from lxml import etree
season_rx = [                                                                                                                                                           ### Seasons folder + skipped folders ### #http://www.zytrax.com/tech/web/regex.htm  # http://regex101.com/#python
  'Specials',                                                                                                                                                           # Specials (season 0)
  '(Season|Series|Book|Saison|Livre)[ _\-]*(?P<season>[0-9]{1,2}).*',                                                                                                   # Season|Series|Book|Saison|Livre xx
  '(?P<season>[0-9]{1,2})a? Stagione.*',                                                                                                                                # 1a Stagione
  '(([Ss]tory )?[Aa]r[kc]|[Vv]ideo).*']                                                                                                                                 # Arc|Story arc ...   #The last line matches are dropped
series_rx = [                                                                                                                                                           ######### Series regex - "serie - xxx - title" ###
  '(^|(?P<show>.*?)[ _\.\-]+)(?P<season>[0-9]{1,2})[Xx](?P<ep>[0-9]{1,3})((|[-_][0-9]{1,2})[Xx](?P<ep2>[0-9]{1,3}))?([ _\.\-]+(?P<title>.*))?$',                        #  0 # 1x01
  '(^|(?P<show>.*?)[ _\.\-]+)s(?P<season>[0-9]{1,2})(e| e|ep| ep|-)(?P<ep>[0-9]{1,3})(([ _\.\-]|(e|ep)|[ _\.\-](e|ep))(?P<ep2>[0-9]{1,3}))?($|( | - |)(?P<title>.*?)$)',#  1 # s01e01-02 | ep01-ep02 | e01-02
  '(?P<title>.*?) [\(]?(?P<season>(19|20)[0-9]{2})[\)]$',                                                                                                               #  2 # title (1932).ext
  '(^|(?P<show>.*?)[ _\.\-]+)(?P<ep>[0-9]{1,3})[ _\.\-]?of[ _\.\-]?[0-9]{1,3}([ _\.\-]+(?P<title>.*?))?$',                                                              #  3 # 01 of 08 (no stacking for this one ?)
  '^(?P<show>.*?) - (?P<ep>[0-9]{1,3}) - (?P<title>.*)$']                                                                                                               #  4 # Serie - xx - title.ext
#   . Add year-month-day   = '(?P<year>[0-9]{4})[^0-9a-zA-Z]+(?P<month>[0-9]{2})[^0-9a-zA-Z]+(?P<day>[0-9]{2})([^0-9]|$)',                                              #    # 2009-02-10 #   . Add day-month-year   = '(?P<month>[0-9]{2})[^0-9a-zA-Z]+(?P<day>[0-9]{2})[^0-9a-zA-Z(]+(?P<year>[0-9]{4})([^0-9a-zA-Z]|$)',    # 02-10-2009
AniDBOffset = [0, 100, 150, 200, 300, 400, 0]; anidb_rx  = [                                                                                                            ######### AniDB Specials regex ### 
  '(^|(?P<show>.*?)[ _\.\-]+)(S|SP|SPECIAL|OAV) ?(?P<ep>\d{1,2}) ?(?P<title>.*)$',                                                                                      #  5 # 001-099 Specials
  '(^|(?P<show>.*?)[ _\.\-]+)(OP|NCOP|OPENING) ?(?P<ep>\d{1,2}[a-z]?)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                      #  6 # 100-149 Openings
  '(^|(?P<show>.*?)[ _\.\-]+)(ED|NCED|ENDING) ?(?P<ep>\d{1,2}[a-z]?)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                       #  7 # 150-199 Endings
  '(^|(?P<show>.*?)[ _\.\-]+)(TRAILER|PROMO|PV|T) ?(?P<ep>\d{1,2}) ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*))?$',                                                          #  8 # 200-299 Trailer, Promo with a  number  '(^|(?P<show>.*?)[ _\.\-]+)((?<=E)P|PARODY|PARODIES?) ?(?P<ep>\d{1,2})? ?(v2|v3|v4|v5)?(?P<title>.*)$',                                                                        # 10 # 300-399 Parodies
  '(^|(?P<show>.*?)[ _\.\-]+)(O|OTHERS?)(?P<ep>\d{1,2}) ?(v2|v3|v4|v5)?[ _\.\-]+(?P<title>.*)$',                                                                        # 09 # 400-499 Others
  '(^|(?P<show>.*?)[ _\.\-]+)(e|ep|e |ep |e-|ep-)?(?P<ep>[0-9]{1,3})((e|ep|-e|-ep|-)(?P<ep2>[0-9]{1,3})|)? ?(v2|v3|v4|v5)?([ _\.\-]+(?P<title>.*?))?$']                 # 10 # E01 | E01-02| E01-E02 | E01E02 
#roman_rx  = [".*? (L?X{0,3})(IX|IV|V?I{0,3})$"]                                                                                                                        # __ # look behind: (?<=S) < position < look forward: (?!S)
ignore_dirs_rx  = [ 'lost\+found', '.AppleDouble','$Recycle.Bin', 'System Volume Information', 'Temporary Items', 'Network Trash Folder', '@eaDir', 'Extras', 'Samples?', 'bonus', '.*bonus disc.*', 'trailers?', '.*_UNPACK_.*', '.*_FAILED_.*', "VIDEO_TS"]# Filters.py  removed '\..*',        
ignore_files_rx = ['[-\._ ]sample', 'sample[-\._ ]', '-Recap\.', 'OST', 'soundtrack', 'Thumbs.db']                                                                                                            # Skipped files (samples, trailers)                                                          
ignore_exts     = ['plexignore', 'ssa', 'srt', 'ass', 'jpg', 'png', 'gif', 'mp3', 'wav', 'flac', 'pdf', 'db', 'nfo', 'ds_store', 'txt', 'zip', 'ini', "dvdmedia", "log", "bat", 'idx', 'sub']    # extensions dropped no warning (skipped list would be too long if showed)
video_exts      = [ '3g2', '3gp', 'asf', 'asx', 'avc', 'avi', 'avs', 'bin', 'bivx', 'divx', 'dv', 'dvr-ms', 'evo', 'fli', 'flv', 'img', 'iso', 'm2t', 'm2ts', 'm2v', 'm4v', 'mkv', 'mov', 'mp4', # DVD: 'ifo', 'bup', 'vob'
  'mpeg', 'mpg', 'mts', 'nrg', 'nsv', 'nuv', 'ogm', 'ogv', 'tp', 'pva', 'qt', 'rm', 'rmvb', 'sdp', 'swf', 'svq3', 'strm', 'ts', 'ty', 'vdr', 'viv', 'vp3', 'wmv', 'wpl', 'wtv', 'xsp', 'xvid', 'webm']
FILTER_CHARS    = "\\/:*?<>|~;_." #.                                                                             # Windows file naming limitations + "~-,._" + ';' as plex cut title at this for the agent
whack_pre_clean = ["x264-FMD Release", "x264-h65", "x264-mSD", "x264-BAJSKORV", "x264-MgB", "x264-SYS", "x264-FQM", "x264-ASAP", "x264-QCF", "x264-W4F", 'x264-w4f', 
  'x264-2hd', "x264-ASAP", 'x264-bajskorv', 'x264-batv', "x264-BATV", "x264-EXCELLENCE", "x264-KILLERS", "x264-LOL", 'x264-MgB', 'x264-qcf', 'x264-SnowDoN', 'x264-xRed', 
  "H.264-iT00NZ", "H.264.iT00NZ", 'H264-PublicHD', "H.264-BS", 'REAL.HDTV', "WEB.DL", "H_264_iT00NZ", "www.crazy-torrent.com", "ReourceRG Kids Release", "By UniversalFreedom", 
  "XviD-2HD", "XviD-AFG", "xvid-aldi", 'xvid-asap', "XviD-AXED", "XviD-BiA-mOt", 'xvid-fqm', "xvid-futv", 'xvid-killer', "XviD-LMAO", 'xvid-pfa',
  'xvid-saints', "XviD-T00NG0D", "XViD-ViCKY", "XviD-BiA", "XVID-FHW", "PROPER-LOL", "5Banime-koi_5d", "%5banime-koi%5d", "minitheatre.org", "mthd bd dual", "WEB_DL",
  "HDTV-AFG", "HDTV-LMAO", "ResourceRG Kids", "kris1986k_vs_htt91",   'web-dl', "-Pikanet128", "hdtv-lol", "REPACK-LOL", " - DDZ", "OAR XviD-BiA-mOt", "3xR", "(-Anf-)",
  "Anxious-He", "Coalgirls", "Commie", "DarkDream", "Doremi", "ExiledDestiny", "Exiled-Destiny", "Exiled Destiny", "FFF", "FFFpeeps", "Hatsuyuki", "HorribleSubs", 
  "joseole99", "(II Subs)", "OAR HDTV-BiA-mOt", "Shimeji", "(BD)", "(RS)", "Rizlim", "Subtidal", "Seto-Otaku", "OCZ", "_dn92__Coalgirls__", 
  "(BD 1280x720 Hi10P)", "(DVD_480p)","(1080p_10bit)", "(1080p_10bit_DualAudio)", "(Tri.Audio)", "(Dual.Audio)", "(BD_720p_AAC)", 
  "BD 1080p", "BD 960p", "BD 720p", "BD_720p", "TV 720p", "DVD 480p", "DVD 476p", "DVD 432p", "DVD 336p",
  "1920x1080", "1280x720", "848x480", "952x720", "(DVD 720x480 h264 AC3)", "(720p_10bit)", "(1080p_10bit)", "(1080p_10bit", "(BD.1080p.AAC)",
  "H.264_AAC", "Hi10P", "Hi10", "x264", "BD 10-bit", "DXVA", "H.264", "(BD, 720p, FLAC)", "Blu-Ray", "Blu-ray",  "SD TV","SD DVD", "HD TV",  "-dvdrip", "dvd-jap", "(DVD)", 
  "FLAC", "Dual Audio", "AC3", "AC3.5.1", "AC3-5.1", "AAC2.0", "AAC.2.0", "AAC2_0",  "AAC", 'DD5.1', "5.1",'divx5.1', "DD5_1", "TV-1", "TV-2", "TV-3", "TV-4", "TV-5", "(Exiled_Destiny)",
  "1080p", "720p", "480p", "_BD", ".XVID", "(xvid)", 
  "-Cd 1", "-Cd 2", "Vol 1", "Vol 2", "Vol 3", "Vol 4", "Vol 5", "Vol.1", "Vol.2", "Vol.3", "Vol.4", "Vol.5", "( )", "(  )", "(   )", "(    )", "(     )", "(_)", "%28", "%29", " (1)"] #include spaces, hyphens, dots, underscore, case insensitive
whack = [ #lowercase                                                                                          ### Tags to remove ###
  'x264', 'h264', 'dvxa', 'divx', 'xvid', 'divx51', 'mp4', "avi",                                             # Video Codecs
  'hi10', 'hi10p', '10bit', 'crf24', 'crf 24',                                                                #       color depth and encoding
  '480p', '576p', '720p', '1080p', '1080i', '1920x1080','1280x720',                                           #       Resolution
  '24fps', '25fps', 'ntsc','pal', 'ntsc-u', 'ntsc-j',                                                         # Refresh rate, Format
  'mp3', 'ogg','ogm', 'vorbis','aac','dts', 'ac3', '5.1ch','5.1', '7.1ch',  'qaac',                           # Audio Codecs, channels
  'dc', 'se', 'extended', 'unrated', 'multi','multisubs', 'dubbed','subbed', "french", "fr", "dub",           # edition (dc = directors cut, se = special edition), subs and dubs
  'custom', 'internal', 'repack', 'proper', 'rerip', "raw", "remastered", "uncensored",                       # format
  'cd1', 'cd2', 'cd3', 'cd4', '1cd', '2cd', '3cd', '4cd', 'xxx', 'nfo', 'read.nfo', 'readnfo', 'nfofix',      # misc 1
  'fragment','ps3avchd','remux','fs','ws', "- copy", "reenc", "hom",                                          # misc 2
  'retail', 'webrip','web-dl', 'wp','workprint', "mkv",  "v1", "v2", "v3", "v4",                              # release type: retail, web, work print
  'bdrc','bdrip','bluray','bd','brrip','hdrip','hddvd','hddvdrip', 'wsrip',                                   # Source: bluray
  'ddc','dvdrip','dvd','r1','r3','r5',"dvd",'svcd','vcd', 'sd', 'hd', 'dvb', "release",                       # DVD, VCD, S-VCD
  'dsr','dsrip','hdtv','pdtv','ppv','stv','tvrip','complete movie',"Hiei", "Metis", "NoRar",                  # dtv, stv
  'cam','bdscr','dvdscr','dvdscreener','scr','screener','tc','telecine','ts','telesync', 'mp4',               # screener
  "mthd", "thora", 'sickrage', 'brrip', 'ac3', "remastered", "yify", "tsr", "reidy", "(1280x720)", "(gerdhanse)", "(720p)", "(Commie)", #'limited', 
  'rikou', 'HOMЯ', "iT00NZ", "nn92", "mthd", "elysium", "encodebyjosh", "krissy", "reidy", "it00nz", "s4a", "()", "(", ")", "(", ")", "[", "]", "{", "}"]   #
CHARACTERS_MAP = { 14844057:"'", 14844051:'-', 14844070:'...', 15711386:':', 14846080:'∀',                   #['’' \xe2\x80\x99] ['–' \xe2\x80\x93] ['…' \xe2\x80\xa6] # '：' # 12770:'', # '∀ Gundam' no need #'´' ['\xc2', '\xb4']
  50048:'A' , 50050:'A' , 50052:'Ä' , 50080:'a' , 50082:'a' , 50084:'a' , 50305:'a' , 50308:'A' , 50309:'a' , #'à' ['\xc3', '\xa0'] #'â' ['\xc3', '\xa2'] #'Ä' ['\xc3', '\x84'] #'ā' ['\xc4', '\x81'] #'À' ['\xc3', '\x80'] #'Â' ['\xc3', '\x82'] # 'Märchen Awakens Romance', 'Rozen Maiden Träumend'
  50055:'C' , 50087:'c' , 50310:'C' , 50311:'c' ,                                                             #'Ç' ['\xc3', '\x87'] #'ç' ['\xc3', '\xa7'] 
  50057:'E' , 50088:'e' , 50089:'e' , 50090:'e' , 50091:'e' , 50323:'e' , 50328:'E' , 50329:'e' ,             #'É' ['\xc3', '\x89'] #'è' ['\xc3', '\xa8'] #'é' ['\xc3', '\xa9'] #'ē' ['\xc4', '\x93'] #'ê' ['\xc3', '\xaa'] #'ë' ['\xc3', '\xab']
  50094:'i' , 50095:'i' , 50347:'i' , 50561:'L' , 50562:'l' , 50563:'N' , 50564:'n' , 50097:'n' ,             #'î' ['\xc3', '\xae'] #'ï' ['\xc3', '\xaf'] #'ī' ['\xc4', '\xab'] #'ñ' ['\xc3', '\xb1']
  50067:'O' , 50068:'Ô' , 50072:'O' , 50100:'o' , 50099:'o' , 50573:'o' , 50578:'OE', 50579:'oe',             #'Ø' ['', '']         #'Ô' ['\xc3', '\x94'] #'ô' ['\xc3', '\xb4'] #'ō' ['\xc5', '\x8d'] #'Œ' ['\xc5', '\x92'] #'œ' ['\xc5', '\x93']
  53423:'Я' , 50586:'S' , 50587:'s' , 50079:'ss', 50105:'u' , 50107:'u' , 50108:'u' ,                         #'Я' ['\xd0', '\xaf'] #'ß' []               #'ù' ['\xc3', '\xb9'] #'û' ['\xc3', '\xbb'] #'ü' ['\xc3', '\xbc'] #'²' ['\xc2', '\xb2'] #'³' ['\xc2', '\xb3']
  50071:'x' , #'×' ['\xc3', '\x97'],
  50617:'Z' , 50618:'z' , 50619:'Z' , 50620:'z' ,                                                             #
  49835:'«' , 49842:'²' , 49843:'³' , 49844:"'" , 49848:'¸',  49851:'»' , 49853:'½'}                          #'«' ['\xc2', '\xab'] #'»' ['\xc2', '\xbb']# 'R/Ranma ½ Nettou Hen'                                                                                                 #'¸' ['\xc2', '\xb8']  

### LOG_PATH calculated once for all calls ####################################################################                        #platform = sys.platform.lower() if "platform" in dir(sys) and callable(getattr(sys,'platform')) else "" 
LOG_PATHS = { 'win32':  [ '%LOCALAPPDATA%\\Plex Media Server\\Logs',                                       #
                          '%USERPROFILE%\\Local Settings\\Application Data\\Plex Media Server\\Logs' ],    #
              'darwin': [ '$HOME/Library/Application Support/Plex Media Server/Logs' ],                    # LINE_FEED = "\r"
              'linux':  [ '$PLEX_HOME/Library/Application Support/Plex Media Server/Logs',                 # Linux
                          '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs',   # Debian, Fedora, CentOS, Ubuntu
                          '/usr/local/plexdata/Plex Media Server/Logs',                                    # FreeBSD
                          '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/Logs',                # FreeNAS
                          '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/Logs/',                          # FreeNAS
                          '/c/.plex/Library/Application Support/Plex Media Server/Logs',                   # ReadyNAS
                          '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Logs',          # QNAP
                          '/volume1/Plex/Library/Application Support/Plex Media Server/Logs',              # Synology, Asustor
                          '/volume2/Plex/Library/Application Support/Plex Media Server/Logs',              # Synology, if migrated a second raid volume as unique volume in new box         
                          '/raid0/data/module/Plex/sys/Plex Media Server/Logs',                            # Thecus
                          '/raid0/data/PLEX_CONFIG/Plex Media Server/Logs' ]}                              # Thecus Plex community version
platform = sys.platform.lower() if "platform" in dir(sys) and not sys.platform.lower().startswith("linux") else "linux" if "platform" in dir(sys) else Platform.OS.lower()
for LOG_PATH in LOG_PATHS[platform] if platform in LOG_PATHS else [ os.path.join(os.getcwd(),"Logs"), '$HOME']:
  if '%' in LOG_PATH or '$' in LOG_PATH:  LOG_PATH = os.path.expandvars(LOG_PATH)  # % on win only, $ on linux
  if os.path.isdir(LOG_PATH):             break                                    # os.path.exists(LOG_PATH)
else: LOG_PATH = os.path.expanduser('~')                                           # logging.basicConfig(), logging.basicConfig(filename=os.path.join(path, 'Plex Media Scanner (custom ASS).log'), level=logging.INFO) #logging.error('Failed on {}'.format(filename))
keep_zero_size_files = os.path.isfile(os.path.join(LOG_PATH, "keep_zero_size_files"))
no_timestamp         = os.path.isfile(os.path.join(LOG_PATH, "no_timestamp"        ))

### Allow to log to the same folder Plex writes its logs in #############################################
global LOG_FILE_LIBRARY
LOG_FILE_LIBRARY = LOG_FILE = 'Plex Media Scanner (custom ASS).log'  # Log filename library will include the library name, LOG_FILE not and serve as reference
def Log(entry, filename=None): 
  global LOG_FILE_LIBRARY
  with open(os.path.join(LOG_PATH, filename if filename else LOG_FILE_LIBRARY), 'a') as file:
    file.write(("" if no_timestamp else time.strftime("%Y-%m-%d %H:%M:%S") + " ") + entry + "\n")
    print entry  # when ran from console ### Allow to display ints even if equal to None at times ### def xint(s):   return str(s) if s is not None and not s=="" else "None"

### import Plex token to have a library list to put hte library name on the log filename ###
PLEX_LIBRARY, PLEX_LIBRARY_URL = {}, "http://127.0.0.1:32400/library/sections/?X-Plex-Token=ACCOUNT_TOKEN_HERE"  # Allow to get the library name to get a log per library https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token
if os.path.isfile(os.path.join(LOG_PATH, "X-Plex-Token.id")):                                                    #Log("'X-Plex-Token.id' file present")
  with open(os.path.join(LOG_PATH, "X-Plex-Token.id"), 'r') as token_file:  PLEX_LIBRARY_URL = PLEX_LIBRARY_URL.replace("ACCOUNT_TOKEN_HERE", token_file.read().strip())  #Log("PLEX_LIBRARY_URL: '%s', token: '%s'" % (PLEX_LIBRARY_URL, token))
try:
  library_xml = etree.fromstring(urllib2.urlopen(PLEX_LIBRARY_URL).read())
  for library in library_xml.iterchildren('Directory'):
    for path in library.iterchildren('Location'):  PLEX_LIBRARY[path.get("path")] = library.get("title")
except:  Log("Place correct Plex token in X-Plex-Token.id file in logs folder or in PLEX_LIBRARY_URL variable to have a log per library - https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token")

### xxxxxxxxxxxxxxxx ###
def roman_to_int(string):  # Regex for matching #M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})
  string, result = string.upper(), 0
  for roman_number, value in [['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40]['X',10],['IX',9],['V',5],['IV',4],['I',1]]:  # if you use {} the list will be in the wrong order 
    while string.startswith(roman_number):  result, string = result+value, string[len(roman_number):]
  return str(result)

### replace a string by another while retaining original string case ###############################################################################
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
             {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")}, {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")}, # Japanese Kana    # cjk radicals supplement
             {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")}, {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")}] # windows: TypeError: ord() expected a character, but string of length 2 found #{"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")}, #{"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")}, #{"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")}, #{"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}, # included as of Unicode 8.0                             #{"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}  # compatibility ideographs
  encodings, encoding = ['iso8859-1', 'utf-16', 'utf-16be', 'utf-8'], ord(string[0])
  if 0 <= encoding < len(encodings):  string = string[1:].decode('cp949') if encoding == 0 and language == 'ko' else string[1:].decode(encodings[encoding])      # If we're dealing with a particular language, we might want to try another code page.
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
 
  ### loop through unicode and replace special chars with spaces then map if found ###
  original_string, string, i = string, list(string), 0
  while i < len(string):
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
def clean_string(string, no_parenthesis=False):
  if not string: return ""
  if "`"     in string:                                                    string = string.replace("`", "'")                                                         # translate anidb apostrophes into normal ones #s = s.replace('&', 'and')       
  if no_parenthesis and "(" in string:                                     string = re.sub(r'\(.*?\)', ' ', string)                                                  # or not delete_parenthesis and not re.search('.*?\((19[0-9]{2}|20[0-2][0-9])\).*?', string, re.IGNORECASE) 
  elif "(" in string and not " (" in string:                               string = string.replace("(", " (")
  elif ")" in string and not ") " in string:                               string = string.replace(")", ") ")
  if "[" in string or "{" in string:                                       string = re.sub(r'[\[\{](?![0-9]{1,3}[\]\}]).*?[\]\}]', '', string).replace("[", '').replace("]", '')    # remove "[xxx]" groups but ep numbers inside brackets as Plex cleanup keep inside () but not inside [] #look behind: (?<=S) < position < look forward: (?!S)
  if string.endswith(", The"):                                             string = "The " + ''.join( string.split(", The", 1) )                                     # ", The" is rellocated in front
  if string.endswith(", A"):                                               string = "A "   + ''.join( string.split(", A"  , 1) )                                     # ", A"   is rellocated in front
  for word in whack_pre_clean:                                             string = replace_insensitive(string, word) if word.lower() in string.lower() else string  #
  for char in  FILTER_CHARS:                                               string = string.replace(char, " ") if char in string else string                          # replace os forbidden chars with spaces
  if re.match(".*?[\(\[\{]?[0-9a-fA-F]{8}[\[\)\}]?.*", string.split(" ")[-1]):  string = re.sub('[0-9a-fA-F]{8}', '', string) #" ".join(string.split(" ")[:-1])                                                 # CRCs removal
  for rx in ("-", "_", "()", "[]", "{}"):                                  string = string[len(rx):   ] if string.startswith(rx) else string                         # In python 2.2.3: string = string.strip(string, " -_")#if string.startswith(("-")): string=string[1:]
  for rx in ("-", "_", "()", "[]", "{}", "- copy"):                        string = string[ :-len(rx) ] if string.lower().endswith  (rx) else string                 # In python 2.2.3: string = string.strip(string, " -_")
  string = encodeASCII(string)                                                                                                                                       # Translate them
  return " ".join([word for word in filter(None, string.split()) if word.lower() not in whack]).strip()                                                              # remove double spaces + words present in "whack" list #filter(None, string.split())

### Add files into Plex database ########################################################################
def add_episode_into_plex(mediaList, files, file, root, path, show, season=1, ep=1, title="", year=None, ep2="", rx="", tvdb_mapping={}):
  if title==title.lower() or title==title.upper() and title.count(" ")>0: title = title.title()  # capitalise if all caps or all lowecase and one space at least
  if ep==0:    episode, season = 1, 0                                                            # s01e00 and S00e00 => s00e01
  if not ep2:  ep2 = ep                                                                          # make ep2 same as ep for loop and tests
  if ep > ep2 or show=="" and path:
    Log("Warning - show: '%s', s%02de%03d-%03d, file: '%s' has ep1 > ep2, or show empty" % (show, season, ep, ep2, file))
    ep2 = ep
  if year =="": year=None
  if not keep_zero_size_files and str(os.path.getsize(file))=="0":  return #do not keep dummy files by default unless this file present in Logs folder
  if     os.path.isfile(os.path.join(LOG_PATH,"dummy.mp4")):  file = os.path.join(LOG_PATH,"dummy.mp4")                  #with dummy.mp4(not empy file) in Logs folder to get rid of Plex Media Scanner.log exceptions, it will remove most eps with size 0 which oculd remove series
  if tvdb_mapping and ep  in tvdb_mapping:  season, ep  = tvdb_mapping[ep ]
  if tvdb_mapping and ep2 in tvdb_mapping:  season, ep2 = tvdb_mapping[ep2]
  for epn in range(ep, ep2+1):
    if len(show) == 0: Log("add_episode_into_plex() - BAZINGA - show empty, report logs to dev ASAP")
    else:
      tv_show, tv_show.display_offset = Media.Episode(show, season, epn, title, year), (epn-ep)*100/(ep2-ep+1)
      tv_show.parts.append(file); #
      mediaList.append(tv_show)   # at this level otherwise only one episode per multi-episode is showing despite log below correct
  index = str(series_rx.index(rx)) if rx in series_rx else str(anidb_rx.index(rx)+len(series_rx)) if rx in anidb_rx else ""  # rank of the regex used from 0
  Log("\"%s\" s%04de%03d%s \"%s\"%s%s" % (show, season, ep, "" if ep==ep2 else "-%03d" % ep2, os.path.basename(file), " \"%s\"" % index if index else "", " \"%s\" " % title if title else ""))  #Stack.Scan(path, files, mediaList, [])

### Add files into array ################################################################################
def explore_path(root, subdir, file_tree, plexignore_files=[], plexignore_dirs=[]):
  fullpath=os.path.join(subdir, ".plexignore")
  if os.path.isfile(fullpath):
    with open(fullpath, 'r') as plexignore:                                                      # Log(".plexignore")
      for pattern in plexignore:                                                                 #
        pattern = pattern.strip()                                                                # remove useless spaces at both ends
        if pattern == '' or pattern[0] == '#': continue                                          # skip comment and emopy lines, go to next for iteration
        if '/' not in pattern:  plexignore_files.append(fnmatch.translate(pattern))              # patterns for this folder gets converted and added to files.
        elif pattern[0] != '/': plexignore_dirs.append(pattern)                                  # patterns for subfolders added to folders
  files, dirs = [], []                                                                           ### Process all files and folders ###
  for item in os.listdir(subdir):                                                                # Loop current folder files and folders
    fullpath = os.path.join(subdir, item)                                                        #
    if os.path.isdir(fullpath):                                                                  ### dirs
      for rx in ignore_dirs_rx:                                                                  # Loop through unwanted folders list
        if re.match(rx, item, re.IGNORECASE):  Log("Folder: '%s' match ignore_dirs_rx: '%s'" % (fullpath[len(root):], rx)); break   # If folder in list of skipped folder exit this loop
      else:  dirs.append(fullpath)                                                               # .plexignore subfolder restrictions management
    else: #if os.path.isfile(fullpath):                                                          ### is a file ###
      for rx in ignore_files_rx+plexignore_files:                                                # Filter trailers and sample files
        if re.match(rx, item, re.IGNORECASE):  Log("File:   '%s' match %s: '%s'" % (fullpath[len(root):], "ignore_files_rx" if rx in ignore_files_rx else "plexignore_files", rx)); break
      else: 
        if   '.' in item and item.lower().rsplit('.', 1)[1] in video_exts:       files.append(fullpath)
        elif '.' in item and item.lower().rsplit('.', 1)[1] not in ignore_exts:  Log("File:   '%s' extension not in video_exts" %(fullpath[len(root):]))                                        ### files
  dirs.sort(); files.sort(key=natural_sort_key)
  for item in dirs:
    plexignore_recursive_files = plexignore_recursive_dirs = []                                  # Split recursive entries, this one for next folder's subfolders
    for rx in plexignore_dirs:                                                                   # On each patter string
      pattern = rx.split("/")                                                                    # Create array splitting by / so all folders separated and patter last
      if pattern[0].lower() == Utils.SplitPath(item)[-1].lower():                                # first folder the same
        if len(pattern) == 2: plexignore_recursive_files.append(fnmatch.translate(pattern[1]))   # One folder, for next folder current files
        if len(pattern) >= 3: plexignore_recursive_dirs.append( "",join(pattern[1:]))            # 2+ folders, for next folder subfolders
    explore_path(root, item, file_tree, plexignore_recursive_files, plexignore_recursive_dirs)   # call next folder and will inherit restrictions
  if files:  file_tree["" if subdir==root else subdir.replace(root, "")[1:]] = files             # add files to file_tree array

### Look for episodes ###################################################################################
def Scan(path, files, mediaList, subdirs, language=None, root=None, **kwargs):
  if not path == "":  return  # Exit every other iteration than the root scan

  ### Rename log file with library name if XML file can be accessed ###
  global LOG_FILE_LIBRARY
  LOG_FILE_LIBRARY = LOG_FILE[:-4] + " - " + PLEX_LIBRARY[root] + LOG_FILE[-4:] if root in PLEX_LIBRARY else LOG_FILE #LOG_FILE stays un-touched, and is used to custom update LOG_FILE_LIBRARY with the library name
  Log(("=== Library Scan: \"%s\", Root: \"%s\", Skipped mediums ===" % (PLEX_LIBRARY[root] if root in PLEX_LIBRARY else "X-Plex-Token.id file missing", root)).ljust(157, '='))
  file_tree = {}; explore_path(root, root, file_tree)                                                         # Build file_tree which output skipped medium in logs
  with open(os.path.join(LOG_PATH, LOG_FILE_LIBRARY[:-4]+" - filelist"+LOG_FILE_LIBRARY[-4:]), 'w') as file:  ### Create a log with the library files relative path in logs folder for T/S 
    for folder in sorted(file_tree):                                                                          # convert to ansi, then notepad++ to replace \r\n to \n if needed + batch to recreate dummy library for tests
      for filename in file_tree[folder]:  file.write( filename.replace(root, "")[1:] + "\n")                  # for each folder, for each file, write the relative path with windows line ending 
  Log("=== filelist created - now processing it ===".ljust(157, '='))
  
  ### Main loop for folders ###
  for path in sorted(file_tree):                                                                              # Loop to add all series while on the root folder Scan call, which allows subfolders to work
    files, folder_year, folder_season, reverse_path, AniDB_op, counter, folder_show = file_tree[path], None, None, list(reversed(Utils.SplitPath(path))), {}, 1, None #
    
    ### bluray folder management ###                                                                          # source: https://github.com/doublerebel/plex-series-scanner-bdmv/blob/master/Plex%20Series%20Scanner%20(with%20disc%20image%20support).py
    if len(reverse_path) >= 3 and reverse_path[0].lower() == 'stream' and paths[1].lower() == 'bdmv':
      if reverse_path[0].lower() == 'stream': reverse_path.pop(0)
      if reverse_path[0].lower() == 'bdmv' :  reverse_path.pop(0)
      ep = clean_string(reverse_path[0], True)
      if len(reverse_path)>1:  reverse_path.pop(0)
      Log("BluRay folder detected - using as equivalent to filename ep: '%s', reverse_path: '%s'" % (ep, reverse_path[0]))
    
    ### Extract season folder to reduce complexity and use folder as serie name ###
    for folder in reverse_path[:-1]:                   # remove root folder from test, [:-1] Doesn't thow errors but gives an empty list if items don't exist, might not be what you want in other cases
      for rx in season_rx :                            # in anime, more specials folders than season folders, so doing it first
        match = re.match(rx, folder, re.IGNORECASE)
        if match:
          reverse_path.remove(folder)                  # All ways to remove: reverse_path.pop(-1), reverse_path.remove(thing|array[0])
          if rx!=season_rx[-1]:  folder_season = season = int( match.group('season')) if match.groupdict().has_key('season') and match.group('season') else 0; break
          match = None                                 # Continue as if nothing happend, will go to second folder
      if match: break                                  # cascade break
    else:  season = 1                                  # Season is 1 by default is season folder not present
    
    ### Capture title form anidb.id or use folder name ###
    folder_show, guid, tvdb_mapping = reverse_path[0], "", {}
    if not re.search(".*? ?\[(anidb|tvdb|tmdb|imdb)-(tt)?[0-9]{1,7}\]", folder_show, re.IGNORECASE):
      for file_path in ("anidb.id", "Extras/anidb.id", "tvdb.id", "Extras/tvdb.id", "tmdb.id", "Extras/tmdb.id", "tsdb.id", "Extras/tsdb.id", "imdb.id", "Extras/imdb.id"):
        if os.path.isfile(os.path.join(root, path, file_path)):
          with open(os.path.join(root, path, file_path), 'r') as guid_file:
            guid = guid_file.read().strip()
            folder_show = "%s [%s-%s]" % (clean_string(reverse_path[0]), os.path.splitext(os.path.basename(file_path))[0], guid)
          if guid and "tvdb" in file_path and not folder_season: 
            try:
              Log('http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/en.xml' % guid)
              result    = urllib2.urlopen('http://thetvdb.com/api/A27AD9BE0DA63333/series/%s/all/en.xml' % guid).read()
              tvdbanime =  etree.fromstring(result)
              for episode in tvdbanime.xpath('Episode'):
                SeasonNumber    = episode.xpath('SeasonNumber'   )[0].text if episode.xpath('SeasonNumber'   )[0].text else ''
                EpisodeNumber   = episode.xpath('EpisodeNumber'  )[0].text if episode.xpath('EpisodeNumber'  )[0].text else ''
                absolute_number = episode.xpath('absolute_number')[0].text if episode.xpath('absolute_number')[0].text else ''
                if absolute_number:  tvdb_mapping[int(absolute_number)] = (int(SeasonNumber), int(EpisodeNumber))
            except: Log("tvdb xml loading issue")
          break
      else:  folder_show = folder_show.replace(" - ", " ").split(" ", 2)[2]  if folder_show.lower().startswith(("saison","season","series")) and len(folder_show.split(" ", 2))==3 else clean_string(folder_show) # Dragon Ball/Saison 2 - Dragon Ball Z/Saison 8 => folder_show = "Dragon Ball Z"
    Log("\"%s\"%s%s" % (folder_show if path else "Root Folder (show name will be taken from filename)", " from foldername: \"%s\"" % path if path!=folder_show else "", ", Season: \"%d\"" % (folder_season) if folder_season is not None else "") )
    
    ### Main File loop to start adding files now ###
    movie_list, counter = {}, 500
    for file in files:                                                                                                                                                             # "files" is a list of media files full path, File is one of the entries
      filename                                       = os.path.splitext(os.path.basename(file))[0]                                                                                 # remove folders and extension(mp4)
      show, year, season, ep, ep2, title, folder_use = folder_show, folder_year, 1 if folder_season is None else folder_season, clean_string(filename, False), None, "", False     # misc, year      = VideoFiles.CleanName(filename_no_ext)
      if ep==folder_show or len(files)==1 and ("movie" in ep.lower()+folder_show.lower() or "gekijouban" in folder_show.lower()):  ep, title = "01", folder_show                   ### Movies ### 
      elif folder_show:                                                                                                                                                            ### Remove folder name from file name to reduce complexity and favor folder name over filename ### (who put crappy folder names and clean filenames anyway?)  # if not at root and containing folder exist and has name different from "_" (scrubed to "")
        if ep.lower().startswith(folder_show.lower()):  ep, folder_use = ep[len(folder_show):].lstrip(), True                                                                      #remove cleansed folder name from cleansed filename and remove potential space
        if folder_season > 1:
          for prefix in ("%s s%d" % (folder_show, folder_season), "%s s%02d" % (folder_show, folder_season)):                                                                      #"%s %d " % (folder_show, folder_season), 
            if ep.lower().startswith(prefix.lower()):  ep =  replace_insensitive(ep, prefix , "").lstrip()                                                                         # Series S2  like transformers (bad naming)  # Serie S2  in season folder, Anidb specials regex doesn't like
        if ep.lower().startswith(("special", "picture drama", "omake")):                               season, title  = 0, ep.title()                                              ### If specials, season is 0 and if title empty use as title ### 
        
      words, misc = filter(None, ep.split()), " ".join( [clean_string(os.path.basename(x), True) for x in files]).lower()                                  # put all filenames in folder in a string to count if ep number valid or present in multiple files ###clean_string was true ###
      for word in words:                     
        ep=word.lower().strip()                                                                                                                             # cannot use words[words.index(word)] otherwise# if word=='': continue filter prevent "" on double spaces
        if "(" in ep and len(ep)==6 and ep[0]=='(' and ep[5]==')' and ep[1:5].isdigit():  ep = ep [1:5]                                                     # remove parenthesis from year in parenthesis
        if '-' in ep and len(filter(None, ep.split('-',1)))==2:                                                                                             # If separator in string
          if re.match("^(ep?[ -]?)?(?P<ep>[0-9]{1,3})(-|ep?|-ep?)(?P<ep2>[0-9]{1,3})", ep, re.IGNORECASE):  ep="Skip"; break                                # if multi ep: make it non digit and exit so regex takes care of it
          ep = ep.split('-',1)[0] if ''.join(letter for letter in ep.split('-',1)[0] if letter.isdigit()) else ep.split('-',1)[1]                           # otherwise all after separator becomes word#words.insert(words.index(word)+1, "-".join(ep.split("-",1)[1:])) #.insert(len(a), x) is equivalent to a.append(x). #???
        if ep.endswith(("v1", "v2", "v3", "v4")):  ep=ep[:-2].rstrip('-')                                                                                   # 
        if ep.upper().startswith(("ed", "op", "ncop", "nced")): break                                                                                       # "OP/ED xx" goes to regex
        if "trailer" in ep:                                                             season, ep, title = 0, "201",               "Trailer";       break  # remove ?
        if "." in ep and ep.split(".", 1)[0].isdigit() and ep.split(".")[1].isdigit():  season, ep, title = 0, ep.split(".", 1)[0], "Special " + ep; break  # ep 12.5 = "1" title "Special 12.5"
        if   ep.isdigit() and len(ep)==4 and (int(ep)< 1900 or folder_season and int(ep[0:1])==folder_season):  season, ep = int(ep[0:2]), ep[2:4]          # 1206 could be season 12 episode 06  #Get assigned from left ot right
        elif ep.isdigit() and len(ep)==4:  filename = clean_string( " ".join(words).replace(ep, "(%s)" % ep));  continue                                    # take everything after supposed episode number
        else:                                                                                                                                               # 
          if ''.join(letter for letter in ep if letter.isdigit())=="": continue                                                                               #
          if ep in ("", "-") or ''.join(letter for letter in ep if letter.isdigit())=="" or path and misc.count(ep)>=3 or ep in clean_string(folder_show, True) and clean_string(filename, True).count(ep)!=2:  continue
          for prefix in ["ep", "e", "act", "s"]:                                                                                                            #
            if ep.startswith(prefix) and len(ep)>len(prefix) and ep[len(prefix):].isdigit(): ep, season = ep[len(prefix):], 0 if prefix=="s" else season    # E/EP/act before ep number ex: Trust and Betrayal OVA-act1 # to solve s00e002 "Code Geass Hangyaku no Lelouch S5 Picture Drama 02 'Stage 3.25'.mkv" "'Stage 3 25'" 
        if not path:  show = clean_string( " ".join(words[:words.index(word)-1]) if len(words)-words.index(word)-1 >1 else "No title", False)               #  
        title = clean_string( " ".join(words[ words.index(word)+1:]) if len(words)-words.index(word)>1 else "", False)                                      # take everything after supposed episode number
        break
      if ep.isdigit():  add_episode_into_plex(mediaList, files, file, root, path, show, season, int(ep), title, year, int(ep2) if ep2 and ep2.isdigit() else None, "None", tvdb_mapping);  continue
      
      ### Check for series_rx + anidb_rx + roman_rx ###
      ep = clean_string(filename, False)
      for rx in series_rx + anidb_rx: # + roman_rx:        #if rx in roman_rx:  ep = clean_string(ep.rsplit(' ', 1)[1] if ' ' in ep else ep) ### move that to chech from the beginning ?
        match = re.search(rx, ep, re.IGNORECASE)
        if match:
          if match.groupdict().has_key('show'  ) and match.group('show'  ) and not path:  show   = clean_string( match.group('show' )) # Mainly if file at root or _ folder
          if match.groupdict().has_key('title' ) and match.group('title' ):               title  = clean_string( match.group('title'))
          if match.groupdict().has_key('season') and match.group('season'):               season = int(match.group('season'))
          if match.groupdict().has_key('ep2'   ) and match.group('ep2'   ):               ep2    = match.group('ep2') 
          if match.groupdict().has_key('ep'    ) and match.group('ep'    ):               ep     = match.group('ep')
          elif rx not in anidb_rx[:-1]:                                               # if no ep in regex
            movie_list[season] = movie_list[season]+1 if season in movie_list else 1  #add movies using year as season, starting at 1
            ep = str(movie_list[season])                                              # Year alone is season Year and ep incremented, good for series, bad for movies but cool for movies in series folder...
          else: ep = "01"                                                             #No ep number, anidb usefull ?????
          if rx in anidb_rx[:-1]:                                                     ### AniDB Specials ################################################################
            offset, season = AniDBOffset [ anidb_rx.index(rx) ], 0                    # offset = 100 for OP, 150 for ED, etc... #Log("ep: '%s', rx: '%s', file: '%s'" % (ep, rx, file))
            if not ep.isdigit() and len(ep)>1 and ep[:-1].isdigit():                  ### OP/ED with letter version Example: op2a
              AniDB_op [ offset + int(ep[:-1]) ] = ord( ep[-1:].lower() ) - ord('a')  # {101: 0 for op1a / 152: for ed2b} and the distance between a and the version we have here
              ep, offset  = str( int( ep[:-1] ) ), offset + sum( AniDB_op.values() )  # "if xxx isdigit() else 1" implied since OP1a for example... # get the offset (100, 150, 200, 300, 400) + the sum of all the mini offset caused by letter version (1b, 2b, 3c = 4 mini offset)
            ep = str( offset + int(ep))                                               # Add episode number to the offset, 01 by default from the match group above
          #elif rx in roman_rx:  ep = roman_to_int(ep)                                ### Roman numbers ### doesn't work is ep title present
          add_episode_into_plex(mediaList, files, file, root, path, show, season, int(ep), title, year, int(ep2) if ep2 and ep2.isdigit() else None, rx, tvdb_mapping)
          break
      if match: continue  # next file iteration
      
      if "-" in ep and len(ep.split("-"))>1:  title=ep.split("-")[1]                                     # Log("*no episode number found for ep: \"%s\", filename: \"%s\", word: '%s'" % (ep, filename, word))
      for word in ep.split(" "):                                                                         #
        if word in folder_show:  ep = replace_insensitive (ep, word, sep=" ")                            # title.replace(word, "", 1)
      title, counter = ep.strip(), counter +1                                                            #
      add_episode_into_plex(mediaList, files, file, root, path, show, 0, counter, title, year, None, "") # Log("ep: '%s', clean filename ep: '%s', file: '%s'" % (ep, clean_string(filename, False), file))
    Log("".ljust(157, '-'))                                                                              # Scan(path, files, mediaList, [])
  Log("")                                                                                                # VideoFiles.Scan(path, files, mediaList, [], root) # Filter out bad stuff and duplicates.

if __name__ == '__main__':
  print "Absolute Series Scanner:"
  path, files, media = sys.argv[1], [os.path.join(path, file) for file in os.listdir(path)], []
  Scan(path[1:], files, media, [])
  print "Media:", media
