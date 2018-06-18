import certifi
import requests

API_URL    = 'https://api.tadata.me/imdb2ta/v2/?imdb_id=%s'
TAC_URL    = 'https://traileraddict.cache.tadata.me/%s'
TYPE_ORDER = ['trailer', 'feature_trailer', 'theatrical_trailer', 'behind_the_scenes', 'interview', 'deleted_scene']
Extras_Map = { 'trailer':             {'type': 'trailer',             'extra':         TrailerObject},
               'feature_trailer':     {'type': 'feature_trailer',     'extra':         TrailerObject},
               'theatrical trailer':  {'type': 'theatrical_trailer',  'extra':         TrailerObject},
               'behind the scenes':   {'type': 'behind_the_scenes',   'extra': BehindTheScenesObject},
               'interview':           {'type': 'interview',           'extra':       InterviewObject},
               'deleted_scene':       {'type': 'deleted_scene',       'extra':    DeletedSceneObject}
             }
HTTP_HEADERS = { "User-Agent": "Trailer Addict/%s (%s %s; Plex Media Server %s)" % (VERSION, Platform.OS, Platform.OSVersion, Platform.ServerVersion) }

####################################################################################################
def Start():  pass
####################################################################################################
class TrailerAddictAgent(Agent.Movies):

	name             = 'Trailer Addict'
	languages        = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to   = ['com.plexapp.agents.imdb', 'com.plexapp.agents.themoviedb' ]

	def search(self, results, media, lang):

		if   media.primary_agent == 'com.plexapp.agents.imdb':  imdb_id = media.primary_metadata.id
		elif media.primary_agent == 'com.plexapp.agents.themoviedb':
			imdb_id = Core.messaging.call_external_function( 'com.plexapp.agents.themoviedb', 'MessageKit:GetImdbId', kwargs = dict( tmdb_id = media.primary_metadata.id ))  # Get the IMDb id from the Movie Database Agent
			if not imdb_id:  Log("*** Could not find IMDb id for movie with The Movie Database id: %s ***" % (media.primary_metadata.id));  return None
		results.Append(MetadataSearchResult(id = imdb_id, score = 100))

	def update(self, metadata, media, lang):

		r = requests.get(API_URL % (metadata.id), headers=HTTP_HEADERS, verify=certifi.where())
		if 'error' in r.json():  Log("*** An error occurred: %s ***" % (r.json()['error']));  return None
		extras = []
		poster = r.json()['image'] if 'image' in r.json() else None
		html   = HTML.ElementFromString(requests.get(TAC_URL % (r.json()['url'].split('/')[-1]), headers=HTTP_HEADERS, verify=certifi.where()).text)
		for video in html.xpath('//a[@class="m_title"]'):
			Title = video.text.strip()
			title = Title.split('nterview - ')[-1].split('nterview- ')[-1] if title.startswith('interview') or title.startswith('generic interview') else Title.lower()
			if 'tv spot' in title:  continue
			for keywords in Extras_Map:
			  if keywords in title: extras.append({ 'type': Extras_Map[keywords]['type'], 'extra': Extras_Map[keywords]['extra']( url = 'ta://'+ video.get('href').lstrip('/'), title = Title, thumb = poster	) }); break
		#extras.sort(key=lambda e: TYPE_ORDER.index(e['type']))
		for extra in sorted(extras, key=lambda e: TYPE_ORDER.index(e['type']))
    #for extra in extras:
      metadata.extras.add(extra['extra'])

      
'''
  try: 
    t = InterviewObject()
    if Util.VersionAtLeast(Platform.ServerVersion, 0,9,9,13):
      find_extras = True
    else:
      find_extras = False
      Log('Not adding extras: Server v0.9.9.13+ required')
  except NameError, e:
    Log('Not adding extras: Framework v2.5.0+ required')
    find_extras = False


Type	Internal letter	Episode number
Specials	S	Episodes 001-100 
OPs       C	Episodes 101-150
EDs       C	Episodes 151-200
Trailers  T Episodes 201-300  'trailer':         TrailerObject,
Parodies  P	Episodes 301-400 
Others	  O	Episodes 401-500
unmapped		Episodes 501-600

extra_type_map = { 'trailer':         TrailerObject,
                   'deleted':         DeletedSceneObject,
                   'behindthescenes': BehindTheScenesObject,
                   'interview':       InterviewObject,
                   'scene':           SceneOrSampleObject,
                   'featurette':      FeaturetteObject,
                   'short':           ShortObject,
                   'other':           OtherObject
                  }


File suffix        Folder               Objects
=============================================================
-behindthescenes   Behind The Scenes    BehindTheScenesObject
-deleted           Deleted Scenes          DeletedSceneObject
-featurette        Featurettes               FeaturetteObject
-interview         Interviews                 InterviewObject
-scene             Scenes                 SceneOrSampleObject
-short             Shorts                         ShortObject
-trailer           Trailers                     TrailerObject
                                                  OtherObject    
    '''
