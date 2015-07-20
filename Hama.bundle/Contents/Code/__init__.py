2015-07-20 20:42:27,132 (-8e78940) :  INFO (core:347) - Starting framework core - Version: 2.6.2, Build: 9b6935b (Wed May 20 03:15:08 UTC 2015)
2015-07-20 20:42:27,132 (-8e78940) :  DEBUG (core:359) - Using the standard policy
2015-07-20 20:42:27,133 (-8e78940) :  DEBUG (core:448) - Starting runtime component.
2015-07-20 20:42:27,136 (-8e78940) :  DEBUG (core:448) - Starting caching component.
2015-07-20 20:42:27,136 (-8e78940) :  DEBUG (core:448) - Starting data component.
2015-07-20 20:42:27,137 (-8e78940) :  DEBUG (core:448) - Starting networking component.
2015-07-20 20:42:27,138 (-8e78940) :  DEBUG (networking:288) - Loaded HTTP cookies
2015-07-20 20:42:27,141 (-8e78940) :  DEBUG (networking:458) - Setting the default network timeout to 20.0
2015-07-20 20:42:27,143 (-8e78940) :  DEBUG (core:448) - Starting localization component.
2015-07-20 20:42:27,144 (-8e78940) :  INFO (localization:408) - Setting the default locale to en-us
2015-07-20 20:42:27,144 (-8e78940) :  DEBUG (core:448) - Starting messaging component.
2015-07-20 20:42:27,145 (-8e78940) :  DEBUG (core:448) - Starting debugging component.
2015-07-20 20:42:27,146 (-8e78940) :  DEBUG (core:448) - Starting services component.
2015-07-20 20:42:27,147 (-8e78940) :  DEBUG (core:448) - Starting myplex component.
2015-07-20 20:42:27,147 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/system/messaging/clear_events/com.plexapp.agents.hama'
2015-07-20 20:42:27,147 (-8e78940) :  DEBUG (core:448) - Starting notifications component.
2015-07-20 20:42:27,585 (-8e78940) :  DEBUG (accessor:68) - Creating a new model access point for provider com.plexapp.agents.hama in namespace 'metadata'
2015-07-20 20:42:27,601 (-8e78940) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/:/plugins/com.plexapp.system/resourceHashes'
2015-07-20 20:42:37,617 (-8e78940) :  CRITICAL (runtime:1293) - Exception getting hosted resource hashes (most recent call last):
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/components/runtime.py", line 1287, in get_resource_hashes
    json = self._core.networking.http_request("http://127.0.0.1:32400/:/plugins/com.plexapp.system/resourceHashes", timeout=10).content
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/components/networking.py", line 269, in content
    return self.__str__()
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/components/networking.py", line 247, in __str__
    self.load()
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/components/networking.py", line 187, in load
    f = self._opener.open(req, timeout=self._timeout)
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Platforms/Shared/Libraries/urllib2_new.py", line 438, in open
    response = self._open(req, data)
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Platforms/Shared/Libraries/urllib2_new.py", line 456, in _open
    '_open', req)
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Platforms/Shared/Libraries/urllib2_new.py", line 416, in _call_chain
    result = func(*args)
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Platforms/Shared/Libraries/urllib2_new.py", line 1217, in http_open
    return self.do_open(httplib.HTTPConnection, req)
  File "/volume2/Plex/Library/Application Support/Plex Media Server/Plug-ins/Framework.bundle/Contents/Resources/Platforms/Shared/Libraries/urllib2_new.py", line 1192, in do_open
    raise URLError(err)
URLError: <urlopen error timed out>

2015-07-20 20:42:37,642 (-b1f8490) :  DEBUG (services:265) - Plug-in is not daemonized - loading services from system
2015-07-20 20:42:37,642 (-8e78940) :  DEBUG (runtime:1111) - Created a thread named 'load_all_services'
2015-07-20 20:42:37,644 (-8e78940) :  DEBUG (runtime:1111) - Created a thread named 'get_server_info'
2015-07-20 20:42:37,645 (-8e78940) :  DEBUG (core:150) - Finished starting framework core
2015-07-20 20:42:37,645 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/:/plugins/com.plexapp.system/messaging/function/X0J1bmRsZVNlcnZpY2U6QWxsU2VydmljZXM_/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMApyMAo_'
2015-07-20 20:42:37,645 (-b8ee490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400'
2015-07-20 20:42:37,646 (-8e78940) :  DEBUG (core:558) - Loading plug-in code
2015-07-20 20:42:38,586 (-b8ee490) :  DEBUG (core:536) - Machine identifier is 00cefa69b70a51e33830a9e679ca10f35ac8f1e4
2015-07-20 20:42:38,592 (-b8ee490) :  DEBUG (core:537) - Server version is 0.9.12.4.1192-9a47d21
2015-07-20 20:42:39,469 (-8e78940) :  DEBUG (core:564) - Finished loading plug-in code
2015-07-20 20:42:39,816 (-b1f8490) :  DEBUG (services:362) - Loaded services
2015-07-20 20:42:39,828 (-b600490) :  DEBUG (services:438) - No shared code to load
2015-07-20 20:42:39,829 (-8e78940) :  DEBUG (preferences:258) - Loaded preferences from DefaultPrefs.json
2015-07-20 20:42:39,831 (-8e78940) :  DEBUG (preferences:178) - Loaded the user preferences for com.plexapp.agents.hama
2015-07-20 20:42:39,833 (-8e78940) :  DEBUG (agentkit:1094) - Creating new agent class called HamaTVAgent
2015-07-20 20:42:39,834 (-8e78940) :  DEBUG (agentkit:912) - Updating agent information: [{'media_types': ['TV_Show'], 'accepts_from': ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles'], 'fallback_agent': False, 'contributes_to': None, 'languages': ['en'], 'persist_stored_files': True, 'version': 0, 'primary_provider': True, 'prefs': True, 'name': 'HamaTV'}]
2015-07-20 20:42:39,836 (-8e78940) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/:/plugins/com.plexapp.system/messaging/function/X0FnZW50U2VydmljZTpVcGRhdGVJbmZv/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQo2CmRpY3QKbGlzdApkaWN0Cmxpc3QKbGlzdApsaXN0CjIKczIzCmNvbS5wbGV4YXBwLmFnZW50cy5oYW1hczEwCmlkZW50aWZpZXJyMQpzMTAKYWdlbnRfaW5mbzEKcjIKMTAKcjMKczExCm1lZGlhX3R5cGVzcjQKczEyCmFjY2VwdHNfZnJvbWIwczE0CmZhbGxiYWNrX2FnZW50bnMxNApjb250cmlidXRlc190b3I1CnM5Cmxhbmd1YWdlc2IxczIwCnBlcnNpc3Rfc3RvcmVkX2ZpbGVzaTAKczcKdmVyc2lvbmIxczE2CnByaW1hcnlfcHJvdmlkZXJiMXM1CnByZWZzczYKSGFtYVRWczQKbmFtZTEKczcKVFZfU2hvdzIKczI5CmNvbS5wbGV4YXBwLmFnZW50cy5sb2NhbG1lZGlhczMyCmNvbS5wbGV4YXBwLmFnZW50cy5vcGVuc3VidGl0bGVzMQpzMgplbnIwCg__'
2015-07-20 20:42:39,866 (-8e78940) :  DEBUG (agentkit:1094) - Creating new agent class called HamaMovieAgent
2015-07-20 20:42:39,867 (-8e78940) :  DEBUG (agentkit:912) - Updating agent information: [{'media_types': ['TV_Show'], 'accepts_from': ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles'], 'fallback_agent': False, 'contributes_to': None, 'languages': ['en'], 'persist_stored_files': True, 'version': 0, 'primary_provider': True, 'prefs': True, 'name': 'HamaTV'}, {'media_types': ['Movie'], 'accepts_from': ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles'], 'fallback_agent': False, 'contributes_to': None, 'languages': ['en'], 'persist_stored_files': True, 'version': 0, 'primary_provider': True, 'prefs': True, 'name': 'HamaMovies'}]
2015-07-20 20:42:39,870 (-8e78940) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/:/plugins/com.plexapp.system/messaging/function/X0FnZW50U2VydmljZTpVcGRhdGVJbmZv/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxMApkaWN0Cmxpc3QKZGljdApsaXN0Cmxpc3QKbGlzdApkaWN0Cmxpc3QKbGlzdApsaXN0CjIKczIzCmNvbS5wbGV4YXBwLmFnZW50cy5oYW1hczEwCmlkZW50aWZpZXJyMQpzMTAKYWdlbnRfaW5mbzIKcjIKcjYKMTAKcjMKczExCm1lZGlhX3R5cGVzcjQKczEyCmFjY2VwdHNfZnJvbWIwczE0CmZhbGxiYWNrX2FnZW50bnMxNApjb250cmlidXRlc190b3I1CnM5Cmxhbmd1YWdlc2IxczIwCnBlcnNpc3Rfc3RvcmVkX2ZpbGVzaTAKczcKdmVyc2lvbmIxczE2CnByaW1hcnlfcHJvdmlkZXJiMXM1CnByZWZzczYKSGFtYVRWczQKbmFtZTEKczcKVFZfU2hvdzIKczI5CmNvbS5wbGV4YXBwLmFnZW50cy5sb2NhbG1lZGlhczMyCmNvbS5wbGV4YXBwLmFnZW50cy5vcGVuc3VidGl0bGVzMQpzMgplbjEwCnI3CnMxMQptZWRpYV90eXBlc3I4CnMxMgphY2NlcHRzX2Zyb21iMHMxNApmYWxsYmFja19hZ2VudG5zMTQKY29udHJpYnV0ZXNfdG9yOQpzOQpsYW5ndWFnZXNiMXMyMApwZXJzaXN0X3N0b3JlZF9maWxlc2kwCnM3CnZlcnNpb25iMXMxNgpwcmltYXJ5X3Byb3ZpZGVyYjFzNQpwcmVmc3MxMApIYW1hTW92aWVzczQKbmFtZTEKczUKTW92aWUyCnMyOQpjb20ucGxleGFwcC5hZ2VudHMubG9jYWxtZWRpYXMzMgpjb20ucGxleGFwcC5hZ2VudHMub3BlbnN1YnRpdGxlczEKczIKZW5yMAo_'
2015-07-20 20:42:39,892 (-8e78940) :  DEBUG (__init__:90) - ### HTTP Anidb Metadata Agent (HAMA) Started ##############################################################################################################
2015-07-20 20:42:39,895 (-8e78940) :  DEBUG (__init__:92) - getMainTitle - LANGUAGE_PRIORITY: ['main', 'x-jat', 'en']
2015-07-20 20:42:39,916 (-8e78940) :  DEBUG (networking:167) - Fetching 'http://anidb.net/api/anime-titles.xml.gz' from the HTTP cache
2015-07-20 20:42:39,941 (-8e78940) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://anidb.net/api/anime-titles.xml.gz, Data filename: anime-titles.xml
2015-07-20 20:42:40,355 (-8e78940) :  DEBUG (networking:167) - Fetching 'http://rawgithub.com/ScudLee/anime-lists/master/anime-list-master.xml' from the HTTP cache
2015-07-20 20:42:40,371 (-8e78940) :  DEBUG (__init__:718) - xmlElementFromFile - Serie XML could not be saved locally
2015-07-20 20:42:40,371 (-8e78940) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://rawgithub.com/ScudLee/anime-lists/master/anime-list-master.xml, Data filename: ('anime-list-master', '.xml')
2015-07-20 20:42:40,511 (-8e78940) :  DEBUG (networking:167) - Fetching 'http://rawgithub.com/ScudLee/anime-lists/master/anime-movieset-list.xml' from the HTTP cache
2015-07-20 20:42:40,525 (-8e78940) :  DEBUG (__init__:718) - xmlElementFromFile - Serie XML could not be saved locally
2015-07-20 20:42:40,526 (-8e78940) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://rawgithub.com/ScudLee/anime-lists/master/anime-movieset-list.xml, Data filename: ('anime-movieset-list', '.xml')
2015-07-20 20:42:40,535 (-8e78940) :  DEBUG (__init__:98) - ### HTTP Anidb Metadata Agent (HAMA) Ended ################################################################################################################
2015-07-20 20:42:40,542 (-8e78940) :  INFO (core:609) - Started plug-in
2015-07-20 20:42:40,543 (-8e78940) :  DEBUG (socketinterface:160) - Starting socket server
2015-07-20 20:42:40,544 (-8e78940) :  DEBUG (runtime:1111) - Created a thread named 'start'
2015-07-20 20:42:40,545 (-8e78940) :  INFO (socketinterface:184) - Socket server started on port 50786
2015-07-20 20:42:40,545 (-8e78940) :  INFO (pipeinterface:25) - Entering run loop
2015-07-20 20:42:40,546 (-8e78940) :  DEBUG (runtime:717) - Handling request GET /:/prefixes
2015-07-20 20:42:40,550 (-8e78940) :  DEBUG (runtime:814) - Found route matching /:/prefixes
2015-07-20 20:42:40,552 (-8e78940) :  DEBUG (runtime:918) - Response: [200] MediaContainer, 148 bytes
2015-07-20 20:42:40,619 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgoyNHM3CmVwaXNvZGVzMTMKTGlnaHQgTXkgRmlyZXM0Cm5hbWVzMQoxczgKZXBpc29kaWNzMjcKQnViYmxlZ3VtIENyaXNpcyBUb2t5byAyMDQwczQKc2hvd3MxCjFzNgpzZWFzb25zMTg5CiUyRnZvbHVtZTIlMkZNZWdhUmFpZCUyRkFuaW1lJTJGSmFwJTIwU3ViJTIwRW4lMkZfdGVzdCUyMFVzZXJzJTJGbWFnbnVtZG9vbWd1eSUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyMC0lMjAyNCUyMC0lMjBMaWdodCUyME15JTIwRmlyZSUyRW1rdnM4CmZpbGVuYW1lczQxCjBkYTM5YTNlZTVlNmI0YjBkMzI1NWJmZWY5NTYwMTg5MGFmZDgwNzA5czgKcGxleEhhc2hzMgotMXM4CmR1cmF0aW9uczYKMjg3Nzk0czIKaWRyMAo_
2015-07-20 20:42:40,660 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgoyNHM3CmVwaXNvZGVzMTMKTGlnaHQgTXkgRmlyZXM0Cm5hbWVzMQoxczgKZXBpc29kaWNzMjcKQnViYmxlZ3VtIENyaXNpcyBUb2t5byAyMDQwczQKc2hvd3MxCjFzNgpzZWFzb25zMTg5CiUyRnZvbHVtZTIlMkZNZWdhUmFpZCUyRkFuaW1lJTJGSmFwJTIwU3ViJTIwRW4lMkZfdGVzdCUyMFVzZXJzJTJGbWFnbnVtZG9vbWd1eSUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyMC0lMjAyNCUyMC0lMjBMaWdodCUyME15JTIwRmlyZSUyRW1rdnM4CmZpbGVuYW1lczQxCjBkYTM5YTNlZTVlNmI0YjBkMzI1NWJmZWY5NTYwMTg5MGFmZDgwNzA5czgKcGxleEhhc2hzMgotMXM4CmR1cmF0aW9uczYKMjg3Nzk0czIKaWRyMAo_
2015-07-20 20:42:40,661 (-b1f8490) :  INFO (agentkit:936) - Searching for matches for {'openSubtitlesHash': None, 'episode': '24', 'name': 'Light My Fire', 'episodic': '1', 'show': 'Bubblegum Crisis Tokyo 2040', 'season': '1', 'filename': '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FBubblegum%20Crisis%20Tokyo%202040%2FBubblegum%20Crisis%20Tokyo%202040%20-%2024%20-%20Light%20My%20Fire%2Emkv', 'plexHash': '0da39a3ee5e6b4b0d3255bfef95601890afd80709', 'duration': '-1', 'id': '287794'}
2015-07-20 20:42:40,662 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/287794/tree'
2015-07-20 20:42:40,689 (-b1f8490) :  DEBUG (__init__:107) - === Search - Begin - ================================================================================================
2015-07-20 20:42:40,690 (-b1f8490) :  INFO (__init__:108) - search() - Title: 'Bubblegum Crisis Tokyo 2040', name: 'Light My Fire', filename: '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FBubblegum%20Crisis%20Tokyo%202040%2FBubblegum%20Crisis%20Tokyo%202040%20-%2024%20-%20Light%20My%20Fire%2Emkv', manual:'True'
2015-07-20 20:42:40,908 (-b1f8490) :  DEBUG (__init__:213) - search() - AniDB - temp score: '100', id: '   345', title: 'Bubblegum Crisis Tokyo 2040' 
2015-07-20 20:42:40,909 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: '100', id: '   345', title: 'Bubblegum Crisis Tokyo 2040' 
2015-07-20 20:42:42,629 (-b1f8490) :  DEBUG (__init__:214) - === Search - End - =================================================================================================
2015-07-20 20:42:42,642 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (104 bytes)
2015-07-20 20:42:42,643 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 668 bytes
2015-07-20 20:42:43,633 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgoyNHM3CmVwaXNvZGVzMTMKTGlnaHQgTXkgRmlyZXM0Cm5hbWVzMQoxczgKZXBpc29kaWNzMjcKQnViYmxlZ3VtIENyaXNpcyBUb2t5byAyMDQwczQKc2hvd3MxCjFzNgpzZWFzb25zMTg5CiUyRnZvbHVtZTIlMkZNZWdhUmFpZCUyRkFuaW1lJTJGSmFwJTIwU3ViJTIwRW4lMkZfdGVzdCUyMFVzZXJzJTJGbWFnbnVtZG9vbWd1eSUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyMC0lMjAyNCUyMC0lMjBMaWdodCUyME15JTIwRmlyZSUyRW1rdnM4CmZpbGVuYW1lczQxCjBkYTM5YTNlZTVlNmI0YjBkMzI1NWJmZWY5NTYwMTg5MGFmZDgwNzA5czgKcGxleEhhc2hzMgotMXM4CmR1cmF0aW9uczYKMjg3Nzk0czIKaWRyMAo_
2015-07-20 20:42:43,635 (-b1f8490) :  DEBUG (runtime:49) - Received packed state data (80 bytes)
2015-07-20 20:42:43,637 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgoyNHM3CmVwaXNvZGVzMTMKTGlnaHQgTXkgRmlyZXM0Cm5hbWVzMQoxczgKZXBpc29kaWNzMjcKQnViYmxlZ3VtIENyaXNpcyBUb2t5byAyMDQwczQKc2hvd3MxCjFzNgpzZWFzb25zMTg5CiUyRnZvbHVtZTIlMkZNZWdhUmFpZCUyRkFuaW1lJTJGSmFwJTIwU3ViJTIwRW4lMkZfdGVzdCUyMFVzZXJzJTJGbWFnbnVtZG9vbWd1eSUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyRkJ1YmJsZWd1bSUyMENyaXNpcyUyMFRva3lvJTIwMjA0MCUyMC0lMjAyNCUyMC0lMjBMaWdodCUyME15JTIwRmlyZSUyRW1rdnM4CmZpbGVuYW1lczQxCjBkYTM5YTNlZTVlNmI0YjBkMzI1NWJmZWY5NTYwMTg5MGFmZDgwNzA5czgKcGxleEhhc2hzMgotMXM4CmR1cmF0aW9uczYKMjg3Nzk0czIKaWRyMAo_
2015-07-20 20:42:43,638 (-b1f8490) :  INFO (agentkit:936) - Searching for matches for {'openSubtitlesHash': None, 'episode': '24', 'name': 'Light My Fire', 'episodic': '1', 'show': 'Bubblegum Crisis Tokyo 2040', 'season': '1', 'filename': '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FBubblegum%20Crisis%20Tokyo%202040%2FBubblegum%20Crisis%20Tokyo%202040%20-%2024%20-%20Light%20My%20Fire%2Emkv', 'plexHash': '0da39a3ee5e6b4b0d3255bfef95601890afd80709', 'duration': '-1', 'id': '287794'}
2015-07-20 20:42:43,639 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/287794/tree'
2015-07-20 20:42:43,665 (-b1f8490) :  DEBUG (__init__:107) - === Search - Begin - ================================================================================================
2015-07-20 20:42:43,666 (-b1f8490) :  INFO (__init__:108) - search() - Title: 'Bubblegum Crisis Tokyo 2040', name: 'Light My Fire', filename: '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FBubblegum%20Crisis%20Tokyo%202040%2FBubblegum%20Crisis%20Tokyo%202040%20-%2024%20-%20Light%20My%20Fire%2Emkv', manual:'True'
2015-07-20 20:42:43,865 (-b1f8490) :  DEBUG (__init__:213) - search() - AniDB - temp score: '100', id: '   345', title: 'Bubblegum Crisis Tokyo 2040' 
2015-07-20 20:42:43,866 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: '100', id: '   345', title: 'Bubblegum Crisis Tokyo 2040' 
2015-07-20 20:42:45,585 (-b1f8490) :  DEBUG (__init__:214) - === Search - End - =================================================================================================
2015-07-20 20:42:45,599 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (104 bytes)
2015-07-20 20:42:45,599 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 668 bytes
2015-07-20 20:42:48,323 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlVwZGF0ZU1ldGFkYXRh/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMTAKczIKZW5zNApsYW5nYjFzNQpmb3JjZWIwczgKcGVyaW9kaWNzNgoyODc3OTRzNApkYmlkaTAKczcKdmVyc2lvbm5zMTAKcGFyZW50R1VJRG5zOApwYXJlbnRJRHM3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZXM0Mwpjb20ucGxleGFwcC5hZ2VudHMuaGFtYTovL2FuaWRiLTM0NT9sYW5nPWVuczQKZ3VpZHM5CmFuaWRiLTM0NXMyCmlkcjAK
2015-07-20 20:42:48,327 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlVwZGF0ZU1ldGFkYXRh/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMTAKczIKZW5zNApsYW5nYjFzNQpmb3JjZWIwczgKcGVyaW9kaWNzNgoyODc3OTRzNApkYmlkaTAKczcKdmVyc2lvbm5zMTAKcGFyZW50R1VJRG5zOApwYXJlbnRJRHM3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZXM0Mwpjb20ucGxleGFwcC5hZ2VudHMuaGFtYTovL2FuaWRiLTM0NT9sYW5nPWVuczQKZ3VpZHM5CmFuaWRiLTM0NXMyCmlkcjAK
2015-07-20 20:42:48,328 (-b1f8490) :  DEBUG (model:32) - Loading model with GUID com.plexapp.agents.hama://anidb-345?lang=en
2015-07-20 20:42:48,333 (-b1f8490) :  ERROR (model:201) - Cannot read model from /volume2/Plex/Library/Application Support/Plex Media Server/Metadata/TV Shows/3/ace69abeede2e37fd2b302b1ca9bb5708de74eb.bundle/Contents/com.plexapp.agents.hama
2015-07-20 20:42:48,334 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/287794/tree'
2015-07-20 20:42:48,361 (-b1f8490) :  DEBUG (__init__:243) - --- Update Begin -------------------------------------------------------------------------------------------
2015-07-20 20:42:48,361 (-b1f8490) :  DEBUG (__init__:244) - update2 - metadata ID: 'anidb-345', Title: 'None',([...], [...], True)
2015-07-20 20:42:48,365 (-b1f8490) :  DEBUG (__init__:571) - anidbTvdbMapping - AniDB-TVDB Mapping - anidb:345 tvbdid: 76538 studio:  defaulttvdbseason: 1
2015-07-20 20:42:48,371 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://tvthemes.plexapp.com/76538.mp3', num: '1', filename: 'Plex/anidb-345.mp3'
2015-07-20 20:42:48,832 (-b1f8490) :  DEBUG (__init__:673) - metadata_download - metadata_download failed, url: 'http://tvthemes.plexapp.com/76538.mp3', num: '1', filename: Plex/anidb-345.mp3
2015-07-20 20:42:48,832 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - loading serie xml: 76538
2015-07-20 20:42:48,990 (-b1f8490) :  DEBUG (networking:167) - Fetching 'http://thetvdb.com/api/A27AD9BE0DA63333/series/76538/all/en.xml' from the HTTP cache
2015-07-20 20:42:49,005 (-b1f8490) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://thetvdb.com/api/A27AD9BE0DA63333/series/76538/all/en.xml, Data filename: TVDB/76538.xml
2015-07-20 20:42:49,012 (-b1f8490) :  DEBUG (__init__:545) - ['Action', 'Adventure', 'Animation', 'Science-Fiction']
2015-07-20 20:42:49,013 (-b1f8490) :  DEBUG (__init__:545) - IMDB ID was empty, loaded through tvdb serie xml, IMDBID: 'tt0175385'
2015-07-20 20:42:49,014 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - loaded serie xml: 76538 Bubblegum Crisis Tokyo 2040
2015-07-20 20:42:49,015 (-b1f8490) :  DEBUG (__init__:545) - ### TVDB - Build 'tvdb_table' ###
2015-07-20 20:42:49,067 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - tvdb_table: ['s1e1', 's1e10', 's1e11', 's1e12', 's1e13', 's1e14', 's1e15', 's1e16', 's1e17', 's1e18', 's1e19', 's1e2', 's1e20', 's1e21', 's1e22', 's1e23', 's1e24', 's1e25', 's1e26', 's1e3', 's1e4', 's1e5', 's1e6', 's1e7', 's1e8', 's1e9']
2015-07-20 20:42:49,067 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - Episodes without Summary: []
2015-07-20 20:42:49,113 (-b1f8490) :  DEBUG (networking:167) - Fetching 'http://thetvdb.com/api/A27AD9BE0DA63333/series/76538/banners.xml' from the HTTP cache
2015-07-20 20:42:49,128 (-b1f8490) :  DEBUG (__init__:602) - getImagesFromTVDB - Loading picture XML worked: http://thetvdb.com/api/A27AD9BE0DA63333/series/76538/banners.xml
2015-07-20 20:42:49,131 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/76538-1.jpg', num: '1', filename: 'TVDB/fanart/original/76538-1.jpg'
2015-07-20 20:42:49,207 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/76538-3.jpg', num: '2', filename: 'TVDB/fanart/original/76538-3.jpg'
2015-07-20 20:42:49,233 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/76538-2.jpg', num: '3', filename: 'TVDB/fanart/original/76538-2.jpg'
2015-07-20 20:42:49,244 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/posters/76538-2.jpg', num: '2', filename: 'TVDB/posters/76538-2.jpg'
2015-07-20 20:42:49,262 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/posters/76538-1.jpg', num: '3', filename: 'TVDB/posters/76538-1.jpg'
2015-07-20 20:42:49,277 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/seasons/4343-1.jpg', num: '6', filename: 'TVDB/seasons/4343-1.jpg'
2015-07-20 20:42:49,288 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/seasons/76538-0.jpg', num: '7', filename: 'TVDB/seasons/76538-0.jpg'
2015-07-20 20:42:49,321 (-b1f8490) :  DEBUG (networking:167) - Fetching 'https://api.tmdb.org/3/configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd' from the HTTP cache
2015-07-20 20:42:49,336 (-b1f8490) :  DEBUG (__init__:626) - getImagesFromTMDB - by IMDBID - url: https://api.tmdb.org/3/find/tt0175385?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id
2015-07-20 20:42:49,356 (-b1f8490) :  DEBUG (networking:167) - Fetching 'https://api.tmdb.org/3/find/tt0175385?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id' from the HTTP cache
2015-07-20 20:42:49,371 (-b1f8490) :  DEBUG (__init__:657) - getImagesFromOMDB - imdbid: 'tt0175385', url: 'http://www.omdbapi.com/?i=tt0175385', filename: 'OMDB/tt0175385.jpg'
2015-07-20 20:42:49,380 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://www.omdbapi.com/?i=tt0175385'
2015-07-20 20:42:52,270 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://ia.media-imdb.com/images/M/MV5BMTY1MzM2MDE3Ml5BMl5BanBnXkFtZTcwODk3ODYxMQ@@._V1_SX300.jpg', num: '98', filename: 'OMDB/tt0175385.jpg'
2015-07-20 20:42:52,314 (-b1f8490) :  DEBUG (__init__:407) - MODE AniDB DETECTED
2015-07-20 20:42:52,314 (-b1f8490) :  DEBUG (__init__:407) - update() - AniDB Serie XML: http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=345, AniDB/345.xml
2015-07-20 20:42:52,348 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=345'
2015-07-20 20:42:53,022 (-b1f8490) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=345, Data filename: AniDB/345.xml
2015-07-20 20:42:53,026 (-b1f8490) :  DEBUG (__init__:407) - update() - AniDB Serie XML: loaded ok
2015-07-20 20:42:53,027 (-b1f8490) :  ERROR (__init__:407) - update() - AniDB title
2015-07-20 20:42:53,028 (-b1f8490) :  DEBUG (__init__:545) - update - AniDB title changed: 'Bubblegum Crisis Tokyo 2040' original title: 'Bubblegum Crisis Tokyo 2040'
2015-07-20 20:42:53,033 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Start Date: 1998-10-08
2015-07-20 20:42:53,034 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Ratings: 5.21
2015-07-20 20:42:53,048 (-b1f8490) :  DEBUG (__init__:546) - update - genres: [('Sci-Fi', 600), ('Special Squads', 600), ('Mecha', 400), ('Action', 400), ('Adventure', 300), ('Romance', 200), ('Future', 200), ('Angst', 200), ('Tragedy', 200)] ['Sci-Fi', 'Special Squads', 'Mecha', 'Action', 'Adventure', 'Romance', 'Future', 'Angst', 'Tragedy']
2015-07-20 20:42:53,050 (-b1f8490) :  DEBUG (__init__:546) - AniDB Genres (Weight): Sci-Fi (600) Special Squads (600) Mecha (400) Action (400) Adventure (300) Romance (200) Future (200) Angst (200) Tragedy (200) 
2015-07-20 20:42:53,074 (-b1f8490) :  DEBUG (__init__:595) - anidbCollectionMapping - anidbid is not part of any collection, related_anime_list: '['68']'
2015-07-20 20:42:53,075 (-b1f8490) :  DEBUG (__init__:546) - AniDB Creator data: AIC is a studio, Hayashi Hiroki is a director, Takaoka Jun`ichi is a director, Yamada Masaki is a director, 
2015-07-20 20:42:53,075 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB description + link
2015-07-20 20:42:53,078 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Poster, url: 'http://img7.anidb.net/pics/anime/150431.jpg'
2015-07-20 20:42:53,083 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199250.jpg', num: '1', filename: 'TVDB/episodes/199250.jpg'
2015-07-20 20:42:53,096 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e19', tvdb_ep: 's1e19', season: '1', epNumVal: '19', defaulttvdbseason: '1', title: 'Are You Experienced?', summary: 'The streets of Tokyo become ever more deserted as'
2015-07-20 20:42:53,100 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199249.jpg', num: '1', filename: 'TVDB/episodes/199249.jpg'
2015-07-20 20:42:53,109 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e18', tvdb_ep: 's1e18', season: '1', epNumVal: '18', defaulttvdbseason: '1', title: 'We Built This City', summary: 'The ADP and the Knight Sabers have come to the res'
2015-07-20 20:42:53,113 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199248.jpg', num: '1', filename: 'TVDB/episodes/199248.jpg'
2015-07-20 20:42:53,129 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e17', tvdb_ep: 's1e17', season: '1', epNumVal: '17', defaulttvdbseason: '1', title: 'Moving Waves', summary: 'The ADP ""Totem Pole"" HQ is swarming with rogue b'
2015-07-20 20:42:53,132 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199247.jpg', num: '1', filename: 'TVDB/episodes/199247.jpg'
2015-07-20 20:42:53,150 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e16', tvdb_ep: 's1e16', season: '1', epNumVal: '16', defaulttvdbseason: '1', title: 'I Surrender', summary: 'Drawn to see Sylia by Galatea's powers, Linna, Pri'
2015-07-20 20:42:53,153 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199246.jpg', num: '1', filename: 'TVDB/episodes/199246.jpg'
2015-07-20 20:42:53,158 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e15', tvdb_ep: 's1e15', season: '1', epNumVal: '15', defaulttvdbseason: '1', title: 'Minute by Minute', summary: 'Whilst Mason takes control of the mysterious and p'
2015-07-20 20:42:53,162 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199245.jpg', num: '1', filename: 'TVDB/episodes/199245.jpg'
2015-07-20 20:42:53,174 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e14', tvdb_ep: 's1e14', season: '1', epNumVal: '14', defaulttvdbseason: '1', title: 'Shock Treatment', summary: 'Angered by Sylia's refusal to explain the dark sec'
2015-07-20 20:42:53,178 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199240.jpg', num: '1', filename: 'TVDB/episodes/199240.jpg'
2015-07-20 20:42:53,191 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e9', tvdb_ep: 's1e9', season: '1', epNumVal: '9', defaulttvdbseason: '1', title: 'My Nation Underground', summary: 'When reports come in of boomers disappearing aroun'
2015-07-20 20:42:53,194 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199244.jpg', num: '1', filename: 'TVDB/episodes/199244.jpg'
2015-07-20 20:42:53,215 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e13', tvdb_ep: 's1e13', season: '1', epNumVal: '13', defaulttvdbseason: '1', title: 'Atom Heart Mother', summary: 'Something dangerous is lurking in Sylia's father's'
2015-07-20 20:42:53,219 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199239.jpg', num: '1', filename: 'TVDB/episodes/199239.jpg'
2015-07-20 20:42:53,228 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e8', tvdb_ep: 's1e8', season: '1', epNumVal: '8', defaulttvdbseason: '1', title: 'Fire Ball', summary: 'Ever wanted to get to know Priss better? Her frien'
2015-07-20 20:42:53,232 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199243.jpg', num: '1', filename: 'TVDB/episodes/199243.jpg'
2015-07-20 20:42:53,249 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e12', tvdb_ep: 's1e12', season: '1', epNumVal: '12', defaulttvdbseason: '1', title: 'Made in Japan', summary: 'With Nene stuck at work and Linna out of town, Pri'
2015-07-20 20:42:53,253 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199238.jpg', num: '1', filename: 'TVDB/episodes/199238.jpg'
2015-07-20 20:42:53,254 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e7', tvdb_ep: 's1e7', season: '1', epNumVal: '7', defaulttvdbseason: '1', title: 'Look at Yourself', summary: 'When a remote controlled boomer working on n under'
2015-07-20 20:42:53,258 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199242.jpg', num: '1', filename: 'TVDB/episodes/199242.jpg'
2015-07-20 20:42:53,264 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e11', tvdb_ep: 's1e11', season: '1', epNumVal: '11', defaulttvdbseason: '1', title: 'Sheer Heart Attack', summary: 'Linna's job begins to dominate her life, with all'
2015-07-20 20:42:53,268 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199237.jpg', num: '1', filename: 'TVDB/episodes/199237.jpg'
2015-07-20 20:42:53,278 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e6', tvdb_ep: 's1e6', season: '1', epNumVal: '6', defaulttvdbseason: '1', title: 'Get It On', summary: 'Stuck in the factory, Linna, Priss and Nene are lo'
2015-07-20 20:42:53,281 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199241.jpg', num: '1', filename: 'TVDB/episodes/199241.jpg'
2015-07-20 20:42:53,378 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e10', tvdb_ep: 's1e10', season: '1', epNumVal: '10', defaulttvdbseason: '1', title: 'Woke Up with a Monster', summary: 'A  boomer-eating monster is stalking underground T'
2015-07-20 20:42:53,381 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's0e2', tvdb_ep: 's0e2', season: '0', epNumVal: '2', defaulttvdbseason: '1', title: 'Still Alive and Well', summary: ''
2015-07-20 20:42:53,385 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199236.jpg', num: '1', filename: 'TVDB/episodes/199236.jpg'
2015-07-20 20:42:53,404 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e5', tvdb_ep: 's1e5', season: '1', epNumVal: '5', defaulttvdbseason: '1', title: 'Rough and Ready', summary: 'When a rogue boomer takes over a factory and start'
2015-07-20 20:42:53,408 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's0e1', tvdb_ep: 's0e1', season: '0', epNumVal: '1', defaulttvdbseason: '1', title: 'Walking on the Moon', summary: ''
2015-07-20 20:42:53,411 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199235.jpg', num: '1', filename: 'TVDB/episodes/199235.jpg'
2015-07-20 20:42:53,420 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e4', tvdb_ep: 's1e4', season: '1', epNumVal: '4', defaulttvdbseason: '1', title: 'Machine Head', summary: 'When Priss is trapped in a cafe with a rogue boome'
2015-07-20 20:42:53,423 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199255.jpg', num: '1', filename: 'TVDB/episodes/199255.jpg'
2015-07-20 20:42:53,438 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e24', tvdb_ep: 's1e24', season: '1', epNumVal: '24', defaulttvdbseason: '1', title: 'Light My Fire', summary: 'Now fused with the upper levels of Genom Tower, Ga'
2015-07-20 20:42:53,441 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199234.jpg', num: '1', filename: 'TVDB/episodes/199234.jpg'
2015-07-20 20:42:53,443 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e3', tvdb_ep: 's1e3', season: '1', epNumVal: '3', defaulttvdbseason: '1', title: 'Keep Me Hanging On', summary: 'Whilst Nigel begins work on a hardsuit for the Kni'
2015-07-20 20:42:53,448 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199254.jpg', num: '1', filename: 'TVDB/episodes/199254.jpg'
2015-07-20 20:42:53,468 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e23', tvdb_ep: 's1e23', season: '1', epNumVal: '23', defaulttvdbseason: '1', title: 'Hydra', summary: 'From the heights of Genom Tower, Galatea has reach'
2015-07-20 20:42:53,471 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199233.jpg', num: '1', filename: 'TVDB/episodes/199233.jpg'
2015-07-20 20:42:53,492 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e2', tvdb_ep: 's1e2', season: '1', epNumVal: '2', defaulttvdbseason: '1', title: 'Fragile', summary: 'The mysterious rock singer and Knight Saber Priss'
2015-07-20 20:42:53,496 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199253.jpg', num: '1', filename: 'TVDB/episodes/199253.jpg'
2015-07-20 20:42:53,505 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e22', tvdb_ep: 's1e22', season: '1', epNumVal: '22', defaulttvdbseason: '1', title: 'Physical Graffiti', summary: 'As the Knight Sabers set about escaping from the b'
2015-07-20 20:42:53,508 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199232.jpg', num: '1', filename: 'TVDB/episodes/199232.jpg'
2015-07-20 20:42:53,517 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e1', tvdb_ep: 's1e1', season: '1', epNumVal: '1', defaulttvdbseason: '1', title: 'Can't Buy a Thrill', summary: 'In the 2030's, an earthquake destroyed most of Tok'
2015-07-20 20:42:53,520 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199252.jpg', num: '1', filename: 'TVDB/episodes/199252.jpg'
2015-07-20 20:42:53,522 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e21', tvdb_ep: 's1e21', season: '1', epNumVal: '21', defaulttvdbseason: '1', title: 'Close to the Edge', summary: 'As the giant boomer tries to fuse with Linna, Nene'
2015-07-20 20:42:53,525 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/76538/199251.jpg', num: '1', filename: 'TVDB/episodes/199251.jpg'
2015-07-20 20:42:53,550 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e20', tvdb_ep: 's1e20', season: '1', epNumVal: '20', defaulttvdbseason: '1', title: 'One of These Nights', summary: 'Galatea steps things up a notch when she takes con'
2015-07-20 20:42:53,551 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C1', epNumVal: '101', ep_title: 'Opening'
2015-07-20 20:42:53,552 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C2', epNumVal: '151', ep_title: 'Ending'
2015-07-20 20:42:53,553 (-b1f8490) :  DEBUG (__init__:546) - update - DURATION: 36000000, numEpisodes: 24
2015-07-20 20:42:53,553 (-b1f8490) :  DEBUG (__init__:549) - --- Update end -------------------------------------------------------------------------------------------------
2015-07-20 20:42:53,711 (-b1f8490) :  DEBUG (model:225) - Serializing to /volume2/Plex/Library/Application Support/Plex Media Server/Metadata/TV Shows/3/ace69abeede2e37fd2b302b1ca9bb5708de74eb.bundle/Contents/com.plexapp.agents.hama/Info.xml
2015-07-20 20:42:53,714 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (104 bytes)
2015-07-20 20:42:53,714 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 16 bytes
2015-07-20 20:43:56,470 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgo1MnM3CmVwaXNvZGVzMzAKVGhlIEVwaWNpc2ggQmF0dGxlIENvbW1lbmNldGghczQKbmFtZXMxCjFzOAplcGlzb2RpY3MxNgpDcmF5b24gU2hpbi1jaGFuczQKc2hvd3MxCjFzNgpzZWFzb25zMTc5CiUyRnZvbHVtZTIlMkZNZWdhUmFpZCUyRkFuaW1lJTJGSmFwJTIwU3ViJTIwRW4lMkZfdGVzdCUyMFVzZXJzJTJGbWFnbnVtZG9vbWd1eSUyRkNyYXlvbiUyMFNoaW4tY2hhbiUyRkNyYXlvbiUyMFNoaW4tY2hhbiUyMC0lMjAwNTIlMjAtJTIwVGhlJTIwRXBpY2lzaCUyMEJhdHRsZSUyMENvbW1lbmNldGghJTJFbXA0czgKZmlsZW5hbWVzNDEKMGRhMzlhM2VlNWU2YjRiMGQzMjU1YmZlZjk1NjAxODkwYWZkODA3MDlzOApwbGV4SGFzaHMyCi0xczgKZHVyYXRpb25zNgoyODgxNjdzMgppZHIwCg__
2015-07-20 20:43:56,472 (-b1f8490) :  DEBUG (runtime:49) - Received packed state data (80 bytes)
2015-07-20 20:43:56,475 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgo1MnM3CmVwaXNvZGVzMzAKVGhlIEVwaWNpc2ggQmF0dGxlIENvbW1lbmNldGghczQKbmFtZXMxCjFzOAplcGlzb2RpY3MxNgpDcmF5b24gU2hpbi1jaGFuczQKc2hvd3MxCjFzNgpzZWFzb25zMTc5CiUyRnZvbHVtZTIlMkZNZWdhUmFpZCUyRkFuaW1lJTJGSmFwJTIwU3ViJTIwRW4lMkZfdGVzdCUyMFVzZXJzJTJGbWFnbnVtZG9vbWd1eSUyRkNyYXlvbiUyMFNoaW4tY2hhbiUyRkNyYXlvbiUyMFNoaW4tY2hhbiUyMC0lMjAwNTIlMjAtJTIwVGhlJTIwRXBpY2lzaCUyMEJhdHRsZSUyMENvbW1lbmNldGghJTJFbXA0czgKZmlsZW5hbWVzNDEKMGRhMzlhM2VlNWU2YjRiMGQzMjU1YmZlZjk1NjAxODkwYWZkODA3MDlzOApwbGV4SGFzaHMyCi0xczgKZHVyYXRpb25zNgoyODgxNjdzMgppZHIwCg__
2015-07-20 20:43:56,476 (-b1f8490) :  INFO (agentkit:936) - Searching for matches for {'openSubtitlesHash': None, 'episode': '52', 'name': 'The Epicish Battle Commenceth!', 'episodic': '1', 'show': 'Crayon Shin-chan', 'season': '1', 'filename': '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FCrayon%20Shin-chan%2FCrayon%20Shin-chan%20-%20052%20-%20The%20Epicish%20Battle%20Commenceth!%2Emp4', 'plexHash': '0da39a3ee5e6b4b0d3255bfef95601890afd80709', 'duration': '-1', 'id': '288167'}
2015-07-20 20:43:56,477 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/288167/tree'
2015-07-20 20:43:56,519 (-b1f8490) :  DEBUG (__init__:107) - === Search - Begin - ================================================================================================
2015-07-20 20:43:56,520 (-b1f8490) :  INFO (__init__:108) - search() - Title: 'Crayon Shin-chan', name: 'The Epicish Battle Commenceth!', filename: '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FCrayon%20Shin-chan%2FCrayon%20Shin-chan%20-%20052%20-%20The%20Epicish%20Battle%20Commenceth!%2Emp4', manual:'True'
2015-07-20 20:43:56,807 (-b1f8490) :  DEBUG (__init__:213) - search() - AniDB - temp score: '100', id: '   708', title: 'Crayon Shin-chan' 
2015-07-20 20:43:56,808 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: '100', id: '   708', title: 'Crayon Shin-chan' 
2015-07-20 20:43:56,851 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '   872', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,340 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  3106', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,341 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  3107', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,371 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  3316', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,583 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4622', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,585 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4624', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,586 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4625', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,587 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4626', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,588 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4627', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,600 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4703', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,602 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4704', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,603 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4705', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,604 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4706', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,606 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4707', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,642 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  4910', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,767 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 29', id: '  5858', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,859 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  6550', title: 'Crayon Shin-chan' 
2015-07-20 20:43:57,951 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: '  7254', title: 'Crayon Shin-chan' 
2015-07-20 20:43:58,063 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 26', id: '  8115', title: 'Crayon Shin-chan' 
2015-07-20 20:43:58,149 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 25', id: '  8780', title: 'Crayon Shin-chan' 
2015-07-20 20:43:58,244 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 25', id: '  9542', title: 'Crayon Shin-chan' 
2015-07-20 20:43:58,319 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 64', id: ' 10252', title: 'Crayon Shin-chan' 
2015-07-20 20:43:58,378 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: ' 22', id: ' 10843', title: 'Crayon Shin-chan' 
2015-07-20 20:43:58,433 (-b1f8490) :  DEBUG (__init__:214) - === Search - End - =================================================================================================
2015-07-20 20:43:58,455 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (104 bytes)
2015-07-20 20:43:58,455 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 9672 bytes
2015-07-20 20:44:21,296 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlVwZGF0ZU1ldGFkYXRh/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMTAKczIKZW5zNApsYW5nYjFzNQpmb3JjZWIwczgKcGVyaW9kaWNzNgoyODgxNjdzNApkYmlkaTAKczcKdmVyc2lvbm5zMTAKcGFyZW50R1VJRG5zOApwYXJlbnRJRHM3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZXM0Mwpjb20ucGxleGFwcC5hZ2VudHMuaGFtYTovL2FuaWRiLTcwOD9sYW5nPWVuczQKZ3VpZHM5CmFuaWRiLTcwOHMyCmlkcjAK
2015-07-20 20:44:21,298 (-b1f8490) :  DEBUG (runtime:49) - Received packed state data (80 bytes)
2015-07-20 20:44:21,300 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlVwZGF0ZU1ldGFkYXRh/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMTAKczIKZW5zNApsYW5nYjFzNQpmb3JjZWIwczgKcGVyaW9kaWNzNgoyODgxNjdzNApkYmlkaTAKczcKdmVyc2lvbm5zMTAKcGFyZW50R1VJRG5zOApwYXJlbnRJRHM3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZXM0Mwpjb20ucGxleGFwcC5hZ2VudHMuaGFtYTovL2FuaWRiLTcwOD9sYW5nPWVuczQKZ3VpZHM5CmFuaWRiLTcwOHMyCmlkcjAK
2015-07-20 20:44:21,302 (-b1f8490) :  DEBUG (model:32) - Loading model with GUID com.plexapp.agents.hama://anidb-708?lang=en
2015-07-20 20:44:21,335 (-b1f8490) :  DEBUG (model:230) - Deserializing from /volume2/Plex/Library/Application Support/Plex Media Server/Metadata/TV Shows/8/3165b2a7a69c275886c28e018032f11952ab340.bundle/Contents/com.plexapp.agents.hama/Info.xml
2015-07-20 20:44:21,527 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/288167/tree'
2015-07-20 20:44:21,579 (-b1f8490) :  DEBUG (__init__:243) - --- Update Begin -------------------------------------------------------------------------------------------
2015-07-20 20:44:21,579 (-b1f8490) :  DEBUG (__init__:244) - update2 - metadata ID: 'anidb-708', Title: 'Crayon Shin-chan',([...], [...], True)
2015-07-20 20:44:21,587 (-b1f8490) :  DEBUG (__init__:568) - anidbTvdbMapping - Missing tvdbid for anidbid 708
2015-07-20 20:44:21,587 (-b1f8490) :  DEBUG (__init__:571) - anidbTvdbMapping - AniDB-TVDB Mapping - anidb:708 tvbdid: unknown studio:  defaulttvdbseason: 1
2015-07-20 20:44:21,594 (-b1f8490) :  DEBUG (__init__:407) - MODE AniDB DETECTED
2015-07-20 20:44:21,594 (-b1f8490) :  DEBUG (__init__:407) - update() - AniDB Serie XML: http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=708, AniDB/708.xml
2015-07-20 20:44:21,647 (-b1f8490) :  DEBUG (networking:167) - Fetching 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=708' from the HTTP cache
2015-07-20 20:44:21,664 (-b1f8490) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=708, Data filename: AniDB/708.xml
2015-07-20 20:44:21,694 (-b1f8490) :  DEBUG (__init__:407) - update() - AniDB Serie XML: loaded ok
2015-07-20 20:44:21,694 (-b1f8490) :  ERROR (__init__:407) - update() - AniDB title
2015-07-20 20:44:21,695 (-b1f8490) :  DEBUG (__init__:463) - update - AniDB title need no change: 'Crayon Shin-chan' original title: 'Crayon Shin-chan' metadata.title 'Crayon Shin-chan'
2015-07-20 20:44:21,697 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Start Date: 1992-04-13
2015-07-20 20:44:21,698 (-b1f8490) :  DEBUG (__init__:407) - update - AniDB Ratings: 5.60*
2015-07-20 20:44:21,713 (-b1f8490) :  DEBUG (__init__:546) - AniDB Genres (Weight): [('Seinen', 600), ('4-koma', 600), ('Elementary School', 600), ('Manga', 600), ('Ecchi', 400), ('School Life', 400), ('Comedy', 400), ('Daily Life', 300), ('Friendship', 300), ('Present', 200)]*
2015-07-20 20:44:21,721 (-b1f8490) :  DEBUG (__init__:593) - anidbCollectionMapping - anidbid (anidb-708) is part of collection: Crayon Shin-chan Collection', related_anime_list: '['3106', '872', '3107', '4624', '4627', '4703', '4705', '4707', '4625', '3316', '4622', '4626', '4704', '4706', '4910', '5858', '6550', '7254', '8070', '8115', '8780', '9542', '10252', '10843']', 
2015-07-20 20:44:21,722 (-b1f8490) :  DEBUG (__init__:546) - AniDB Creator data: Usui Yoshito is a writer, Hongou Mitsuru is a director, Hara Keiichi is a director, Mutou Yuuji is a director, 
2015-07-20 20:44:21,723 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB description + link
2015-07-20 20:44:21,724 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Poster, url: 'http://img7.anidb.net/pics/anime/153029.jpg'
2015-07-20 20:44:21,728 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e1', tvdb_ep: '', season: '1', epNumVal: '1', defaulttvdbseason: '1', title: 'Pee Strike!', summary: ''
2015-07-20 20:44:21,731 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e2', tvdb_ep: '', season: '1', epNumVal: '2', defaulttvdbseason: '1', title: 'To Be a Man?', summary: ''
2015-07-20 20:44:21,734 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e3', tvdb_ep: '', season: '1', epNumVal: '3', defaulttvdbseason: '1', title: 'Safe As a Dry Hump', summary: ''
2015-07-20 20:44:21,736 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e4', tvdb_ep: '', season: '1', epNumVal: '4', defaulttvdbseason: '1', title: 'Get Your Hands Off My Happy Cake!', summary: ''
2015-07-20 20:44:21,739 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e5', tvdb_ep: '', season: '1', epNumVal: '5', defaulttvdbseason: '1', title: 'Gigantic One-Eyed Monster', summary: ''
2015-07-20 20:44:21,742 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e6', tvdb_ep: '', season: '1', epNumVal: '6', defaulttvdbseason: '1', title: 'Gum Is a Good Food to Eat', summary: ''
2015-07-20 20:44:21,744 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e7', tvdb_ep: '', season: '1', epNumVal: '7', defaulttvdbseason: '1', title: 'A Mutha [BLEEP]ing Bunny!', summary: ''
2015-07-20 20:44:21,747 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e8', tvdb_ep: '', season: '1', epNumVal: '8', defaulttvdbseason: '1', title: 'The Shin Must Poop On?', summary: ''
2015-07-20 20:44:21,749 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e9', tvdb_ep: '', season: '1', epNumVal: '9', defaulttvdbseason: '1', title: 'Shady Real Estate Office, Ho!', summary: ''
2015-07-20 20:44:21,752 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e20', tvdb_ep: '', season: '1', epNumVal: '20', defaulttvdbseason: '1', title: 'Gratuitous Child Nudity', summary: ''
2015-07-20 20:44:21,754 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e28', tvdb_ep: '', season: '1', epNumVal: '28', defaulttvdbseason: '1', title: 'The Stalker Song', summary: ''
2015-07-20 20:44:21,757 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e13', tvdb_ep: '', season: '1', epNumVal: '13', defaulttvdbseason: '1', title: 'Swimming, Diving Scuba Team', summary: ''
2015-07-20 20:44:21,760 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e35', tvdb_ep: '', season: '1', epNumVal: '35', defaulttvdbseason: '1', title: 'AIDS Is Hilarious', summary: ''
2015-07-20 20:44:21,762 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e26', tvdb_ep: '', season: '1', epNumVal: '26', defaulttvdbseason: '1', title: 'Gratuitous Grandparent Nudity', summary: ''
2015-07-20 20:44:21,765 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e29', tvdb_ep: '', season: '1', epNumVal: '29', defaulttvdbseason: '1', title: 'Double Fried Flavor!', summary: ''
2015-07-20 20:44:21,767 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e33', tvdb_ep: '', season: '1', epNumVal: '33', defaulttvdbseason: '1', title: 'Tummy Clock Says It's Three', summary: ''
2015-07-20 20:44:21,770 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e18', tvdb_ep: '', season: '1', epNumVal: '18', defaulttvdbseason: '1', title: 'The Girls of 34C', summary: ''
2015-07-20 20:44:21,773 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e27', tvdb_ep: '', season: '1', epNumVal: '27', defaulttvdbseason: '1', title: 'Shin Wars', summary: ''
2015-07-20 20:44:21,775 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e19', tvdb_ep: '', season: '1', epNumVal: '19', defaulttvdbseason: '1', title: 'The Herpes Effect', summary: ''
2015-07-20 20:44:21,778 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e23', tvdb_ep: '', season: '1', epNumVal: '23', defaulttvdbseason: '1', title: 'Your IQ's Like 5, Right?', summary: ''
2015-07-20 20:44:21,780 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e21', tvdb_ep: '', season: '1', epNumVal: '21', defaulttvdbseason: '1', title: 'At Least They Pay for the Ouchie?', summary: ''
2015-07-20 20:44:21,783 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e14', tvdb_ep: '', season: '1', epNumVal: '14', defaulttvdbseason: '1', title: 'More of a "Snug" Than a "Magnum"', summary: ''
2015-07-20 20:44:21,785 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e10', tvdb_ep: '', season: '1', epNumVal: '10', defaulttvdbseason: '1', title: 'Can't Abort 'em When They're Not Yours', summary: ''
2015-07-20 20:44:21,788 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e16', tvdb_ep: '', season: '1', epNumVal: '16', defaulttvdbseason: '1', title: 'Sticky's My Favorite Flavor', summary: ''
2015-07-20 20:44:21,791 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e17', tvdb_ep: '', season: '1', epNumVal: '17', defaulttvdbseason: '1', title: 'OK, but I'm a Power Bottom', summary: ''
2015-07-20 20:44:21,793 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e25', tvdb_ep: '', season: '1', epNumVal: '25', defaulttvdbseason: '1', title: 'Condescending Spanish for Heiresses', summary: ''
2015-07-20 20:44:21,796 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e15', tvdb_ep: '', season: '1', epNumVal: '15', defaulttvdbseason: '1', title: 'In the Interest of Increased Ratings?', summary: ''
2015-07-20 20:44:21,798 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e22', tvdb_ep: '', season: '1', epNumVal: '22', defaulttvdbseason: '1', title: 'Damn You, Telepathy!', summary: ''
2015-07-20 20:44:21,801 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e30', tvdb_ep: '', season: '1', epNumVal: '30', defaulttvdbseason: '1', title: 'Miscarriage Return Policy', summary: ''
2015-07-20 20:44:21,803 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e32', tvdb_ep: '', season: '1', epNumVal: '32', defaulttvdbseason: '1', title: 'It's Actually Better for Anal', summary: ''
2015-07-20 20:44:21,806 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e34', tvdb_ep: '', season: '1', epNumVal: '34', defaulttvdbseason: '1', title: 'Green Like Good Boy Pills', summary: ''
2015-07-20 20:44:21,808 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e24', tvdb_ep: '', season: '1', epNumVal: '24', defaulttvdbseason: '1', title: 'Stop Referencing the Show!', summary: ''
2015-07-20 20:44:21,811 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e31', tvdb_ep: '', season: '1', epNumVal: '31', defaulttvdbseason: '1', title: 'Lucky Bastard Fever!', summary: ''
2015-07-20 20:44:21,814 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e12', tvdb_ep: '', season: '1', epNumVal: '12', defaulttvdbseason: '1', title: 'Get Yours, or Die!', summary: ''
2015-07-20 20:44:21,816 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e11', tvdb_ep: '', season: '1', epNumVal: '11', defaulttvdbseason: '1', title: 'Irregular Tampons on Sale!', summary: ''
2015-07-20 20:44:21,819 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e36', tvdb_ep: '', season: '1', epNumVal: '36', defaulttvdbseason: '1', title: 'How to Bury a Smack-Addict Clown', summary: ''
2015-07-20 20:44:21,821 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e37', tvdb_ep: '', season: '1', epNumVal: '37', defaulttvdbseason: '1', title: 'The Emperor's Love', summary: ''
2015-07-20 20:44:21,824 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e38', tvdb_ep: '', season: '1', epNumVal: '38', defaulttvdbseason: '1', title: 'Her Little Gang-Bang Miracles', summary: ''
2015-07-20 20:44:21,826 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e39', tvdb_ep: '', season: '1', epNumVal: '39', defaulttvdbseason: '1', title: 'Childrens Were Our Future', summary: ''
2015-07-20 20:44:21,829 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e40', tvdb_ep: '', season: '1', epNumVal: '40', defaulttvdbseason: '1', title: 'Shin Chan: The High School Years', summary: ''
2015-07-20 20:44:21,832 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e41', tvdb_ep: '', season: '1', epNumVal: '41', defaulttvdbseason: '1', title: 'Tell the Cops She Looked Eighteen', summary: ''
2015-07-20 20:44:21,834 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e42', tvdb_ep: '', season: '1', epNumVal: '42', defaulttvdbseason: '1', title: 'I Can't Find Your %*#&ing Legs', summary: ''
2015-07-20 20:44:21,837 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e43', tvdb_ep: '', season: '1', epNumVal: '43', defaulttvdbseason: '1', title: 'An Angel Gets Its Period', summary: ''
2015-07-20 20:44:21,839 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e44', tvdb_ep: '', season: '1', epNumVal: '44', defaulttvdbseason: '1', title: 'Unlicensed Therapy', summary: ''
2015-07-20 20:44:21,842 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e45', tvdb_ep: '', season: '1', epNumVal: '45', defaulttvdbseason: '1', title: 'A Total Jack Barnes Move', summary: ''
2015-07-20 20:44:21,844 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e46', tvdb_ep: '', season: '1', epNumVal: '46', defaulttvdbseason: '1', title: 'Gonna Need More Fingers', summary: ''
2015-07-20 20:44:21,847 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e47', tvdb_ep: '', season: '1', epNumVal: '47', defaulttvdbseason: '1', title: 'Sexy-Ass Wild Fartin' Cowboy', summary: ''
2015-07-20 20:44:21,849 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e48', tvdb_ep: '', season: '1', epNumVal: '48', defaulttvdbseason: '1', title: 'Morning Vacuuming', summary: ''
2015-07-20 20:44:21,852 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e49', tvdb_ep: '', season: '1', epNumVal: '49', defaulttvdbseason: '1', title: 'Unfortunately for You, I Had Ribs', summary: ''
2015-07-20 20:44:21,854 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e50', tvdb_ep: '', season: '1', epNumVal: '50', defaulttvdbseason: '1', title: 'Domestic Abuse Isn't That Funny', summary: ''
2015-07-20 20:44:21,857 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e51', tvdb_ep: '', season: '1', epNumVal: '51', defaulttvdbseason: '1', title: 'Box for Hire?', summary: ''
2015-07-20 20:44:21,860 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e52', tvdb_ep: '', season: '1', epNumVal: '52', defaulttvdbseason: '1', title: 'The Epicish Battle Commenceth!', summary: ''
2015-07-20 20:44:22,026 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C31', epNumVal: '151', ep_title: 'Ending 18'
2015-07-20 20:44:22,027 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C30', epNumVal: '150', ep_title: 'Ending 17'
2015-07-20 20:44:22,027 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C29', epNumVal: '149', ep_title: 'Ending 16'
2015-07-20 20:44:22,028 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C28', epNumVal: '148', ep_title: 'Ending 15'
2015-07-20 20:44:22,029 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C27', epNumVal: '147', ep_title: 'Ending 14'
2015-07-20 20:44:22,030 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C26', epNumVal: '146', ep_title: 'Ending 13'
2015-07-20 20:44:22,031 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C25', epNumVal: '145', ep_title: 'Ending 12'
2015-07-20 20:44:22,031 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C24', epNumVal: '144', ep_title: 'Ending 11'
2015-07-20 20:44:22,032 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C23', epNumVal: '143', ep_title: 'Ending 10'
2015-07-20 20:44:22,033 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C22', epNumVal: '142', ep_title: 'Ending 9'
2015-07-20 20:44:22,034 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C21', epNumVal: '141', ep_title: 'Ending 8'
2015-07-20 20:44:22,035 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C20', epNumVal: '140', ep_title: 'Ending 7'
2015-07-20 20:44:22,035 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C19', epNumVal: '139', ep_title: 'Ending 6'
2015-07-20 20:44:22,036 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C18', epNumVal: '138', ep_title: 'Ending 5'
2015-07-20 20:44:22,037 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C17', epNumVal: '137', ep_title: 'Ending 4'
2015-07-20 20:44:22,038 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C16', epNumVal: '136', ep_title: 'Ending 3'
2015-07-20 20:44:22,039 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C15', epNumVal: '135', ep_title: 'Ending 2'
2015-07-20 20:44:22,039 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C14', epNumVal: '134', ep_title: 'Ending 1'
2015-07-20 20:44:22,040 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C13', epNumVal: '113', ep_title: 'Opening 13'
2015-07-20 20:44:22,041 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C12', epNumVal: '112', ep_title: 'Opening 12'
2015-07-20 20:44:22,042 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C11', epNumVal: '111', ep_title: 'Opening 11'
2015-07-20 20:44:22,042 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C10', epNumVal: '110', ep_title: 'Opening 10'
2015-07-20 20:44:22,043 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C9', epNumVal: '109', ep_title: 'Opening 9'
2015-07-20 20:44:22,044 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C8', epNumVal: '108', ep_title: 'Opening 8'
2015-07-20 20:44:22,045 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C7', epNumVal: '107', ep_title: 'Opening 7'
2015-07-20 20:44:22,046 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C6', epNumVal: '106', ep_title: 'Opening 6'
2015-07-20 20:44:22,046 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C5', epNumVal: '105', ep_title: 'Opening 5'
2015-07-20 20:44:22,047 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C4', epNumVal: '104', ep_title: 'Opening 4'
2015-07-20 20:44:22,048 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C3', epNumVal: '103', ep_title: 'Opening 3'
2015-07-20 20:44:22,049 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C2', epNumVal: '102', ep_title: 'Opening 2'
2015-07-20 20:44:22,050 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C1', epNumVal: '101', ep_title: 'Opening 1'
2015-07-20 20:44:22,089 (-b1f8490) :  DEBUG (__init__:546) - update - DURATION: 78000000, numEpisodes: 52
2015-07-20 20:44:22,115 (-b1f8490) :  DEBUG (__init__:549) - --- Update end -------------------------------------------------------------------------------------------------
2015-07-20 20:44:22,319 (-b1f8490) :  DEBUG (model:225) - Serializing to /volume2/Plex/Library/Application Support/Plex Media Server/Metadata/TV Shows/8/3165b2a7a69c275886c28e018032f11952ab340.bundle/Contents/com.plexapp.agents.hama/Info.xml
2015-07-20 20:44:22,322 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (104 bytes)
2015-07-20 20:44:22,323 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 16 bytes
2015-07-20 20:46:09,307 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgoxMnM3CmVwaXNvZGVzOApTdHlsaXNoIXM0Cm5hbWVzMQoxczgKZXBpc29kaWNzMTMKRGV2aWwgTWF5IENyeXM0CnNob3dzMQoxczYKc2Vhc29uczE0OAolMkZ2b2x1bWUyJTJGTWVnYVJhaWQlMkZBbmltZSUyRkphcCUyMFN1YiUyMEVuJTJGX3Rlc3QlMjBVc2VycyUyRm1hZ251bWRvb21ndXklMkZEZXZpbCUyME1heSUyMENyeSUyRkRldmlsJTIwTWF5JTIwQ3J5JTIwLSUyMDEyJTIwLSUyMFN0eWxpc2ghJTJFbWt2czgKZmlsZW5hbWVzNDEKMGRhMzlhM2VlNWU2YjRiMGQzMjU1YmZlZjk1NjAxODkwYWZkODA3MDlzOApwbGV4SGFzaHMyCi0xczgKZHVyYXRpb25zNgoyODgyNjlzMgppZHIwCg__
2015-07-20 20:46:09,308 (-b1f8490) :  DEBUG (runtime:49) - Received packed state data (80 bytes)
2015-07-20 20:46:09,311 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlNlYXJjaA__/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoyCmRpY3QKZGljdAo2CnMyCmVuczQKbGFuZ2IxczYKbWFudWFsYjFzNwpwcmltYXJ5aTAKczcKdmVyc2lvbnIxCnM2Cmt3YXJnc3M3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZTEwCm5zMTcKb3BlblN1YnRpdGxlc0hhc2hzMgoxMnM3CmVwaXNvZGVzOApTdHlsaXNoIXM0Cm5hbWVzMQoxczgKZXBpc29kaWNzMTMKRGV2aWwgTWF5IENyeXM0CnNob3dzMQoxczYKc2Vhc29uczE0OAolMkZ2b2x1bWUyJTJGTWVnYVJhaWQlMkZBbmltZSUyRkphcCUyMFN1YiUyMEVuJTJGX3Rlc3QlMjBVc2VycyUyRm1hZ251bWRvb21ndXklMkZEZXZpbCUyME1heSUyMENyeSUyRkRldmlsJTIwTWF5JTIwQ3J5JTIwLSUyMDEyJTIwLSUyMFN0eWxpc2ghJTJFbWt2czgKZmlsZW5hbWVzNDEKMGRhMzlhM2VlNWU2YjRiMGQzMjU1YmZlZjk1NjAxODkwYWZkODA3MDlzOApwbGV4SGFzaHMyCi0xczgKZHVyYXRpb25zNgoyODgyNjlzMgppZHIwCg__
2015-07-20 20:46:09,312 (-b1f8490) :  INFO (agentkit:936) - Searching for matches for {'openSubtitlesHash': None, 'episode': '12', 'name': 'Stylish!', 'episodic': '1', 'show': 'Devil May Cry', 'season': '1', 'filename': '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FDevil%20May%20Cry%2FDevil%20May%20Cry%20-%2012%20-%20Stylish!%2Emkv', 'plexHash': '0da39a3ee5e6b4b0d3255bfef95601890afd80709', 'duration': '-1', 'id': '288269'}
2015-07-20 20:46:09,313 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/288269/tree'
2015-07-20 20:46:09,333 (-b1f8490) :  DEBUG (__init__:107) - === Search - Begin - ================================================================================================
2015-07-20 20:46:09,334 (-b1f8490) :  INFO (__init__:108) - search() - Title: 'Devil May Cry', name: 'Stylish!', filename: '%2Fvolume2%2FMegaRaid%2FAnime%2FJap%20Sub%20En%2F_test%20Users%2Fmagnumdoomguy%2FDevil%20May%20Cry%2FDevil%20May%20Cry%20-%2012%20-%20Stylish!%2Emkv', manual:'True'
2015-07-20 20:46:10,448 (-b1f8490) :  DEBUG (__init__:213) - search() - AniDB - temp score: '100', id: '  4776', title: 'Devil May Cry' 
2015-07-20 20:46:10,449 (-b1f8490) :  DEBUG (__init__:214) - search() - AniDB - score: '100', id: '  4776', title: 'Devil May Cry' 
2015-07-20 20:46:11,254 (-b1f8490) :  DEBUG (__init__:214) - === Search - End - =================================================================================================
2015-07-20 20:46:11,267 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (104 bytes)
2015-07-20 20:46:11,268 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 656 bytes
2015-07-20 20:46:13,440 (-b1f8490) :  DEBUG (runtime:717) - Handling request GET /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlVwZGF0ZU1ldGFkYXRh/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMTAKczIKZW5zNApsYW5nYjFzNQpmb3JjZWIwczgKcGVyaW9kaWNzNgoyODgyNjlzNApkYmlkaTAKczcKdmVyc2lvbm5zMTAKcGFyZW50R1VJRG5zOApwYXJlbnRJRHM3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZXM0NApjb20ucGxleGFwcC5hZ2VudHMuaGFtYTovL2FuaWRiLTQ3NzY%40bGFuZz1lbnM0Cmd1aWRzMTAKYW5pZGItNDc3NnMyCmlkcjAK
2015-07-20 20:46:13,442 (-b1f8490) :  DEBUG (runtime:49) - Received packed state data (80 bytes)
2015-07-20 20:46:13,444 (-b1f8490) :  DEBUG (runtime:814) - Found route matching /:/plugins/com.plexapp.agents.hama/messaging/function/X0FnZW50S2l0OlVwZGF0ZU1ldGFkYXRh/Y2VyZWFsMQoxCmxpc3QKMApyMAo_/Y2VyZWFsMQoxCmRpY3QKMTAKczIKZW5zNApsYW5nYjFzNQpmb3JjZWIwczgKcGVyaW9kaWNzNgoyODgyNjlzNApkYmlkaTAKczcKdmVyc2lvbm5zMTAKcGFyZW50R1VJRG5zOApwYXJlbnRJRHM3ClRWX1Nob3dzMTAKbWVkaWFfdHlwZXM0NApjb20ucGxleGFwcC5hZ2VudHMuaGFtYTovL2FuaWRiLTQ3NzY@bGFuZz1lbnM0Cmd1aWRzMTAKYW5pZGItNDc3NnMyCmlkcjAK
2015-07-20 20:46:13,446 (-b1f8490) :  DEBUG (model:32) - Loading model with GUID com.plexapp.agents.hama://anidb-4776?lang=en
2015-07-20 20:46:13,468 (-b1f8490) :  ERROR (model:201) - Cannot read model from /volume2/Plex/Library/Application Support/Plex Media Server/Metadata/TV Shows/8/d0ec8403604cf66ad67c1704771193fe9a6f6c5.bundle/Contents/com.plexapp.agents.hama
2015-07-20 20:46:13,469 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://127.0.0.1:32400/library/metadata/288269/tree'
2015-07-20 20:46:13,488 (-b1f8490) :  DEBUG (__init__:243) - --- Update Begin -------------------------------------------------------------------------------------------
2015-07-20 20:46:13,489 (-b1f8490) :  DEBUG (__init__:244) - update2 - metadata ID: 'anidb-4776', Title: 'None',([...], [...], True)
2015-07-20 20:46:13,521 (-b1f8490) :  DEBUG (__init__:571) - anidbTvdbMapping - AniDB-TVDB Mapping - anidb:4776 tvbdid: 80224 studio:  defaulttvdbseason: 1
2015-07-20 20:46:13,527 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://tvthemes.plexapp.com/80224.mp3', num: '1', filename: 'Plex/anidb-4776.mp3'
2015-07-20 20:46:14,721 (-b1f8490) :  DEBUG (__init__:673) - metadata_download - metadata_download failed, url: 'http://tvthemes.plexapp.com/80224.mp3', num: '1', filename: Plex/anidb-4776.mp3
2015-07-20 20:46:14,721 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - loading serie xml: 80224
2015-07-20 20:46:15,660 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://thetvdb.com/api/A27AD9BE0DA63333/series/80224/all/en.xml'
2015-07-20 20:46:16,084 (-b1f8490) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://thetvdb.com/api/A27AD9BE0DA63333/series/80224/all/en.xml, Data filename: TVDB/80224.xml
2015-07-20 20:46:16,090 (-b1f8490) :  DEBUG (__init__:545) - ['Action', 'Adventure', 'Animation', 'Fantasy']
2015-07-20 20:46:16,091 (-b1f8490) :  DEBUG (__init__:545) - IMDB ID was empty, loaded through tvdb serie xml, IMDBID: 'tt1048049'
2015-07-20 20:46:16,092 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - loaded serie xml: 80224 Devil May Cry
2015-07-20 20:46:16,093 (-b1f8490) :  DEBUG (__init__:545) - ### TVDB - Build 'tvdb_table' ###
2015-07-20 20:46:16,120 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - tvdb_table: ['s1e1', 's1e10', 's1e11', 's1e12', 's1e2', 's1e3', 's1e4', 's1e5', 's1e6', 's1e7', 's1e8', 's1e9']
2015-07-20 20:46:16,121 (-b1f8490) :  DEBUG (__init__:545) - update2 - TVDB - Episodes without Summary: ['s0e0']
2015-07-20 20:46:16,130 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://thetvdb.com/api/A27AD9BE0DA63333/series/80224/banners.xml'
2015-07-20 20:46:16,539 (-b1f8490) :  DEBUG (__init__:602) - getImagesFromTVDB - Loading picture XML worked: http://thetvdb.com/api/A27AD9BE0DA63333/series/80224/banners.xml
2015-07-20 20:46:16,542 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-5.jpg', num: '1', filename: 'TVDB/fanart/original/80224-5.jpg'
2015-07-20 20:46:16,571 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-4.jpg', num: '2', filename: 'TVDB/fanart/original/80224-4.jpg'
2015-07-20 20:46:16,593 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-2.jpg', num: '3', filename: 'TVDB/fanart/original/80224-2.jpg'
2015-07-20 20:46:16,605 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-3.jpg', num: '4', filename: 'TVDB/fanart/original/80224-3.jpg'
2015-07-20 20:46:16,619 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-6.jpg', num: '5', filename: 'TVDB/fanart/original/80224-6.jpg'
2015-07-20 20:46:16,621 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-1.jpg', num: '6', filename: 'TVDB/fanart/original/80224-1.jpg'
2015-07-20 20:46:16,631 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/fanart/original/80224-7.jpg', num: '7', filename: 'TVDB/fanart/original/80224-7.jpg'
2015-07-20 20:46:16,644 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/posters/80224-1.jpg', num: '2', filename: 'TVDB/posters/80224-1.jpg'
2015-07-20 20:46:16,659 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/posters/80224-2.jpg', num: '3', filename: 'TVDB/posters/80224-2.jpg'
2015-07-20 20:46:16,670 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/seasons/80224-1-2.jpg', num: '10', filename: 'TVDB/seasons/80224-1-2.jpg'
2015-07-20 20:46:16,691 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/seasons/80224-1.jpg', num: '11', filename: 'TVDB/seasons/80224-1.jpg'
2015-07-20 20:46:16,703 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/seasons/80224-1-3.jpg', num: '12', filename: 'TVDB/seasons/80224-1-3.jpg'
2015-07-20 20:46:16,722 (-b1f8490) :  DEBUG (networking:167) - Fetching 'https://api.tmdb.org/3/configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd' from the HTTP cache
2015-07-20 20:46:16,737 (-b1f8490) :  DEBUG (__init__:626) - getImagesFromTMDB - by IMDBID - url: https://api.tmdb.org/3/find/tt1048049?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id
2015-07-20 20:46:16,769 (-b1f8490) :  DEBUG (networking:172) - Requesting 'https://api.tmdb.org/3/find/tt1048049?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id'
2015-07-20 20:46:19,428 (-b1f8490) :  DEBUG (__init__:657) - getImagesFromOMDB - imdbid: 'tt1048049', url: 'http://www.omdbapi.com/?i=tt1048049', filename: 'OMDB/tt1048049.jpg'
2015-07-20 20:46:19,436 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://www.omdbapi.com/?i=tt1048049'
2015-07-20 20:46:23,870 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://ia.media-imdb.com/images/M/MV5BMTI4NTY0MDY3NV5BMl5BanBnXkFtZTcwMjk5MjA3MQ@@._V1_SX300.jpg', num: '98', filename: 'OMDB/tt1048049.jpg'
2015-07-20 20:46:23,878 (-b1f8490) :  DEBUG (__init__:407) - MODE AniDB DETECTED
2015-07-20 20:46:23,879 (-b1f8490) :  DEBUG (__init__:407) - update() - AniDB Serie XML: http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=4776, AniDB/4776.xml
2015-07-20 20:46:23,895 (-b1f8490) :  DEBUG (networking:172) - Requesting 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=4776'
2015-07-20 20:46:24,626 (-b1f8490) :  DEBUG (__init__:728) - xmlElementFromFile - Serie XML url: http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid=4776, Data filename: AniDB/4776.xml
2015-07-20 20:46:24,631 (-b1f8490) :  DEBUG (__init__:407) - update() - AniDB Serie XML: loaded ok
2015-07-20 20:46:24,632 (-b1f8490) :  ERROR (__init__:407) - update() - AniDB title
2015-07-20 20:46:24,633 (-b1f8490) :  DEBUG (__init__:545) - update - AniDB title changed: 'Devil May Cry' original title: 'Devil May Cry'
2015-07-20 20:46:24,634 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Start Date: 2007-06-14
2015-07-20 20:46:24,635 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Ratings: 3.97
2015-07-20 20:46:24,658 (-b1f8490) :  DEBUG (__init__:546) - update - genres: [('Parallel Universe', 600), ('Action Game', 600), ('Shounen', 600), ('Fantasy', 600), ('Game', 600), ('Fantasy World', 600), ('Action', 600), ('Alternative Present', 600), ('Swordplay', 600), ('Present', 600), ('Comedy', 200), ('Underworld', 200), ('Horror', 200)] ['Parallel Universe', 'Action Game', 'Shounen', 'Fantasy', 'Game', 'Fantasy World', 'Action', 'Alternative Present', 'Swordplay', 'Present', 'Comedy', 'Underworld', 'Horror']
2015-07-20 20:46:24,660 (-b1f8490) :  DEBUG (__init__:546) - AniDB Genres (Weight): Parallel Universe (600) Action Game (600) Shounen (600) Fantasy (600) Game (600) Fantasy World (600) Action (600) Alternative Present (600) Swordplay (600) Present (600) Comedy (200) Underworld (200) Horror (200) 
2015-07-20 20:46:24,683 (-b1f8490) :  DEBUG (__init__:595) - anidbCollectionMapping - anidbid is not part of any collection, related_anime_list: '[]'
2015-07-20 20:46:24,684 (-b1f8490) :  DEBUG (__init__:546) - AniDB Creator data: Madhouse is a studio, Capcom is a writer, Itagaki Shin is a director, Inoue Toshiki is a producer, Abe Hisashi is a director, 
2015-07-20 20:46:24,685 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB description + link
2015-07-20 20:46:24,686 (-b1f8490) :  DEBUG (__init__:546) - update - AniDB Poster, url: 'http://img7.anidb.net/pics/anime/7804.jpg'
2015-07-20 20:46:24,691 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330226.jpg', num: '1', filename: 'TVDB/episodes/330226.jpg'
2015-07-20 20:46:24,701 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e1', tvdb_ep: 's1e1', season: '1', epNumVal: '1', defaulttvdbseason: '1', title: 'Devil May Cry', summary: 'Dante, a supernatural mercenary, is hired as the b'
2015-07-20 20:46:24,705 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330227.jpg', num: '1', filename: 'TVDB/episodes/330227.jpg'
2015-07-20 20:46:24,727 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e2', tvdb_ep: 's1e2', season: '1', epNumVal: '2', defaulttvdbseason: '1', title: 'Highway Star', summary: 'Dante reluctantly accepts a mission from Lady to s'
2015-07-20 20:46:24,731 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330228.jpg', num: '1', filename: 'TVDB/episodes/330228.jpg'
2015-07-20 20:46:24,738 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e3', tvdb_ep: 's1e3', season: '1', epNumVal: '3', defaulttvdbseason: '1', title: 'Not Love', summary: 'The daughter of the mayor starts seeing a mysterio'
2015-07-20 20:46:24,741 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330229.jpg', num: '1', filename: 'TVDB/episodes/330229.jpg'
2015-07-20 20:46:24,759 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e4', tvdb_ep: 's1e4', season: '1', epNumVal: '4', defaulttvdbseason: '1', title: 'Rolling Thunder', summary: 'Lady meets up with a strange demon-woman who has a'
2015-07-20 20:46:24,763 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330230.jpg', num: '1', filename: 'TVDB/episodes/330230.jpg'
2015-07-20 20:46:24,785 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e5', tvdb_ep: 's1e5', season: '1', epNumVal: '5', defaulttvdbseason: '1', title: 'In Private', summary: 'Dante finds himself followed by a customer from a'
2015-07-20 20:46:24,789 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330231.jpg', num: '1', filename: 'TVDB/episodes/330231.jpg'
2015-07-20 20:46:24,790 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e6', tvdb_ep: 's1e6', season: '1', epNumVal: '6', defaulttvdbseason: '1', title: 'Rock Queen', summary: 'Dante is hired to protect treasure hunters from a'
2015-07-20 20:46:24,794 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/330232.jpg', num: '1', filename: 'TVDB/episodes/330232.jpg'
2015-07-20 20:46:24,811 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e7', tvdb_ep: 's1e7', season: '1', epNumVal: '7', defaulttvdbseason: '1', title: 'Wishes Come True', summary: 'A man receives a visit from a demonic mask which c'
2015-07-20 20:46:24,814 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/333703.jpg', num: '1', filename: 'TVDB/episodes/333703.jpg'
2015-07-20 20:46:24,825 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e8', tvdb_ep: 's1e8', season: '1', epNumVal: '8', defaulttvdbseason: '1', title: 'Once Upon a Time', summary: 'A man named Aaron keep on insisting that Dante is'
2015-07-20 20:46:24,829 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/333704.jpg', num: '1', filename: 'TVDB/episodes/333704.jpg'
2015-07-20 20:46:24,841 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e9', tvdb_ep: 's1e9', season: '1', epNumVal: '9', defaulttvdbseason: '1', title: 'Death Poker', summary: 'Dante is hired by a woman to deter her brother's g'
2015-07-20 20:46:24,845 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/333705.jpg', num: '1', filename: 'TVDB/episodes/333705.jpg'
2015-07-20 20:46:24,847 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e10', tvdb_ep: 's1e10', season: '1', epNumVal: '10', defaulttvdbseason: '1', title: 'The Last Promise', summary: 'Dante is attacked by Barusa, a former servant of S'
2015-07-20 20:46:24,850 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/333706.jpg', num: '1', filename: 'TVDB/episodes/333706.jpg'
2015-07-20 20:46:24,872 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e11', tvdb_ep: 's1e11', season: '1', epNumVal: '11', defaulttvdbseason: '1', title: 'Showtime!', summary: 'Dante encounters Patty's mother, and Sid's careful'
2015-07-20 20:46:24,876 (-b1f8490) :  DEBUG (__init__:666) - metadata_download - url: 'http://thetvdb.com/banners/episodes/80224/333707.jpg', num: '1', filename: 'TVDB/episodes/333707.jpg'
2015-07-20 20:46:24,887 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's1e12', tvdb_ep: 's1e12', season: '1', epNumVal: '12', defaulttvdbseason: '1', title: 'Stylish!', summary: 'With Dante impaled and crucified in the demon dime'
2015-07-20 20:46:24,888 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C2', epNumVal: '151', ep_title: 'Ending'
2015-07-20 20:46:24,891 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's0e151', tvdb_ep: 's0e151', season: '0', epNumVal: '151', defaulttvdbseason: '1', title: 'Ending', summary: ''
2015-07-20 20:46:24,892 (-b1f8490) :  DEBUG (__init__:546) - AniDB specials title - Season: '0', epNum.text: 'C1', epNumVal: '101', ep_title: 'Opening'
2015-07-20 20:46:24,896 (-b1f8490) :  DEBUG (__init__:546) - TVDB mapping episode summary - anidb_ep: 's0e101', tvdb_ep: 's0e101', season: '0', epNumVal: '101', defaulttvdbseason: '1', title: 'Opening', summary: ''
2015-07-20 20:46:24,897 (-b1f8490) :  DEBUG (__init__:546) - update - DURATION: 18000000, numEpisodes: 12
2015-07-20 20:46:24,898 (-b1f8490) :  DEBUG (__init__:549) - --- Update end -------------------------------------------------------------------------------------------------
2015-07-20 20:46:24,981 (-b1f8490) :  DEBUG (model:225) - Serializing to /volume2/Plex/Library/Application Support/Plex Media Server/Metadata/TV Shows/8/d0ec8403604cf66ad67c1704771193fe9a6f6c5.bundle/Contents/com.plexapp.agents.hama/Info.xml
2015-07-20 20:46:24,986 (-b1f8490) :  DEBUG (runtime:106) - Sending packed state data (1064 bytes)
2015-07-20 20:46:24,986 (-b1f8490) :  DEBUG (runtime:918) - Response: [200] str, 16 bytes
