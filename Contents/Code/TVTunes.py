### televisiontunes.com ###
#http://www.tunefind.com/api

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
from common import Dict, Log, DictString

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(metadata, title1, title2):
  THEME_URL    = "http://www.televisiontunes.com/uploads/audio/{}.mp3"
  TVTunes_dict = {}
  Log.Info("".ljust(157, '-'))
  Log.Info("TVTunes.GetMetadata() - 'themes' - title: '{}', title2: '{}', Prefs['themes']: '{}'".format(title1, title2, Prefs['themes']))
  if 'TVTunes' in Prefs['themes'] and (title1 or title2):
    for url in set([THEME_URL.format(String.Quote(title1)), THEME_URL.format(String.Quote(title2))]):
      result = '*' if url in metadata.themes or Data.Exists(url.split('/')[-1]) else common.GetStatusCode(url)
      Log.Info("TVTunes.GetMetadata() - Return code: '{}', url: '{}'".format(result, url))
      if result in (200, "*"):  TVTunes_dict = {'themes': {url: ("TelevisionTunes/"+url.split('/')[-1], 1, None)}}

  Log.Info("TVTunes_dict: {}".format(DictString(TVTunes_dict, 1)))
  return TVTunes_dict
  