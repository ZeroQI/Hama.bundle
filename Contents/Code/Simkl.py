### Simkl.com ###  
# API: http://docs.simkl.apiary.io/#introduction/apps-using-simkl-api/list-of-apps
# https://github.com/daviddavo/trackl/blob/master/trackl/apiconnect.py
# https://github.com/gboudreau/XBMCnfoTVImporter.bundle/blob/master/Contents/Code/__init__.py
# pageUrl = "http://127.0.0.1:32400/library/metadata/" + id + "/tree"
# nfoXML = XML.ElementFromURL(pageUrl).xpath('//MediaContainer/MetadataItem/MetadataItem/MetadataItem/MediaItem/MediaPart')[0]
#https://simkl.com/oauth/authorize?response_type=code&client_id=105022c0683a2e6116eaaac6fdc6c3179091172f5dfa6adc94e36030e951299b&redirect_uri=http://simkl.com
#
#response = requests.post(url+"&extended=full", data={'some': 'data'}, headers=headers)
#raise KeyError(request.POST)
  
### Imports ###
import common
from   common  import GetPosters
import json
import httplib
import ssl
  
#import ssl
#from   urllib2 import Request, urlopen

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name' ###

### APP details
API_KEY       = "105022c0683a2e6116eaaac6fdc6c3179091172f5dfa6adc94e36030e951299b"
#CLIENT_SECRET = "2d6db1f1a929bec2086eb8d89a3aff53be5a647973fa948e586567dba182b905"
REDIRECT_URL  = "http://simkl.com"
HEADERS       = {"Content-Type": "application/json",  "simkl-api-key": API_KEY}
CONTEXT       = ssl.SSLContext (ssl.PROTOCOL_TLSv1)  #Prevent "SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)"

### Functions ### 

### Call in startup with Simkl.Register()
def Register():
  Log.Info("Simkl.Register()")
  if Prefs['Simkl'] and not Data.Exists("Simkl.token"):
    connection = httplib.HTTPSConnection("api.simkl.com", context=CONTEXT)
    connection.request("GET", "/oauth/pin?client_id=%s&redirect_uri=%s" % (API_KEY, REDIRECT_URL), headers=HEADERS)
    json_dict = json.loads( connection.getresponse().read().decode("utf-8") )
    user_code = json_dict['user_code']  #{u'device_code': u'DEVICE_CODE', u'verification_url': u'https://simkl.com/pin', u'interval': 5, u'expires_in': 900, u'user_code': u'63B55', u'result': u'OK'}
    counter   = json_dict['expires_in']
    interval  = json_dict['interval']
    Log.Info("Level 1 - Copy code: '{}' and go to 'url': '{}', 'expires_in': '{}', 'interval': '{}'".format(user_code, json_dict['verification_url'].replace("\/", "/"), counter, interval))
    while counter>0:
      counter = counter - interval
      time.sleep(interval)
      connection.request("GET", "/oauth/pin/%s?client_id=%s" % (user_code, API_KEY), headers=HEADERS)
      json_dict = json.loads(connection.getresponse().read().decode("utf-8"))
      if json_dict["result"] == "OK":
        Log.Info("Level 2 - OK" + str(json_dict))  # {u'access_token': u'2a368368c90c5bfc8fe6ad2a71b0174fc488b368932351a2bebae0d75752ae08', u'result': u'OK'}
        Data.Save("Simkl.token", json_dict['access_token'])
      elif r["result"] == "KO":
        Log.Info("Level 2 - Pending user to validate pin" + str(json_dict))  #
    else:
      Log.Info("json_dict - Pin expired")
      return {}

def GetMetadata(metadata, media, movie, AniDBid, TVDBid):
  Log.Info("".ljust(157, '-'))
  Log.Info("Simkl.GetMetadata()")
  if Data.Exists("Simkl.token"):   ### Auth: PIN ###
    HEADERS["authorization"] = "Bearer " + Data.Load("Simkl.token")
    connection = httplib.HTTPSConnection("api.simkl.com", context=CONTEXT)
    
    ### User Settings ###
    #connection.request("GET", "/users/settings", headers=HEADERS)
    #json_dict = json.loads(connection.getresponse().read().decode("utf-8"))
    
    ###GET WATCHED
    #header:  {Content-Type:application/json, authorization: Bearer [token], simkl-api-key: [client_id]}
    #body:    [{"anidb": 70262639}]
    #type: movie, tv
    #title
    #year
    #hulu/netflix/tvdb/tmdb/imdb/anidb/
    connection.request("GET", "/sync/watched?extended=full", json.dumps([{"tvdb": int(TVDBid) if TVDBid else 0, "anidb": int(AniDBid) if AniDBid else 0}]), HEADERS)
    json_dict = json.loads(connection.getresponse().read().decode("utf-8"))
    if json_dict:
      if 'type' in json_dict:
        if 'type'=="movie":          Log.Info("Simkl.GetMetadata() - Found the movie")
        if 'type'=="tv":             Log.Info("Simkl.GetMetadata() - Found the TV or Anime show")
      if 'result' in json_dict:
        if 'result'=='true':         Log.Info("Simkl.GetMetadata() - Found a match and found in user's watchlist")
        if 'result'=='false':        Log.Info("Simkl.GetMetadata() - Found a match but could not find in user's watchlist")
        if 'result'=='not_found':    Log.Info("Simkl.GetMetadata() - Could not find a match in Simkl database with such Title\Year or ID")
      if 'result' in json_dict:
        if 'result'=='completed':    Log.Info("Simkl.GetMetadata() - User watched the movie or seen all episodes")
        if 'result'=='plantowatch':  Log.Info("Simkl.GetMetadata() - Found in users's Plan to Watch list")
        if 'result'=='dropped':      Log.Info("Simkl.GetMetadata() - Found in users's Not Interesting list")
      if 'watched' in json_dict:   	 Log.info("Simkl.GetMetadata() - YYYY-MM-DDTHH:MM:SS.000Z	Datetime in UTC format when the last episode or movie was watched")
      Log.Info("Simkl.GetMetadata() - 'token' exist" + str(json_dict))
    
    #con = http.client.HTTPSConnection("api.simkl.com")
    #con.request("GET", "/sync/all-items?extended=full" + typestring, headers=headers)
    #return json.loads(con.getresponse().read().decode("utf-8"))
  
    if movie: id = media.items[0].id
    else:
      for s in media.seasons:  #get first file path
        for e in media.seasons[s].episodes:
          id = media.seasons[s].episodes[e].id
          break
        break
    #https://api.simkl.com/ratings
    #https://api.simkl.com/redirect?client_id=
    #https://api.simkl.com/redirect?to=trailer&anidb=10846&client_id=105022c0683a2e6116eaaac6fdc6c3179091172f5dfa6adc94e36030e951299b
    # https://api.simkl.com/search?anidb=9541&fields=rank,droprate,simkl,ext,has_trailer&client_id=105022c0683a2e6116eaaac6fdc6c3179091172f5dfa6adc94e36030e951299b&extended=full
    #&extended=full
    #https://api.simkl.com/sync/history

    '''    
    last seen imagehttps://api.simkl.com/users/recently-watched-background/51?client_id=105022c0683a2e6116eaaac6fdc6c3179091172f5dfa6adc94e36030e951299b
    {
     "id": 342828,
     "url": "https://simkl.com/movies/342828/midnight-special",
     "title": "Midnight Special",
     "poster": "https://simkl.net/posters/30/3082850367420132f_0.jpg",
     "fanart": "https://simkl.net/fanart/43/4389778c118f40a6f_0.jpg"
    } 
     Collection
    '''
  return {}

def SetWatchedFlag(id, watched=True): #media.seasons[seasonNum].episodes[episodeNum].id  #https://forums.plex.tv/discussion/comment/520366#Comment_520366
  try:     plexViewCount = etree.fromstring( urllib.urlopen( PLEX_HOST+'/library/metadata/'+id ).read() ).find('Video').get('viewCount', 0)
  except:  plexViewCount = 0
  
  Log.Info("".ljust(157, '-'))
  Log.Info("SetWatchedFlag() - watched: '%s', plexViewCount: '%s'" % (str(watched), str(plexViewCount)))
  if(watched and not plexViewCount):  # If watched on simpl and not Plex, update Plex
    url = '127.0.0.1/:/scrobble?key=%s&identifier=com.plexapp.plugins.library'   % id  # If sage says it's watched, set it as watched in Plex
    try:                input = urllib.urlopen(url)
    except IOError, i:  Log.Debug("ERROR in setWatchedUnwatchedFlag: Unable to connect to PMS server"); return False
  if not watched and plexViewCount: # If watched on Plex but not Simkl update Simkl
    url = '127.0.0.1/:/unscrobble?key=%s&identifier=com.plexapp.plugins.library' % id
    
  '''
#https://github.com/ngovil21/Plex-Cleaner/blob/master/PlexCleaner.py
#Token from Plex directly
thispath = inspect.getfile(inspect.currentframe())
for i in range(1, 6): 
    thispath = os.path.dirname(thispath)
myprefpath = os.path.join(thispath, "Preferences.xml")
if os.path.exists(myprefpath):
    mypreftext = Core.storage.load(myprefpath)
else:
    Log("Did NOT find Preferences file - please check logfile and hierarchy. Aborting!")
    return
mytoken = XML.ElementFromString(mypreftext).xpath('//Preferences/@PlexOnlineToken')[0]
'''
