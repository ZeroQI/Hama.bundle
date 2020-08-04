### televisiontunes.com ###
# https://www.tunefind.com/api

### Imports ###
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###
THEME_URL = "https://www.televisiontunes.com/uploads/audio/{}.mp3"

### Functions ###
def GetMetadata(metadata, title1, title2):
  Log.Info("=== TVTunes.GetMetadata() ===".ljust(157, '='))
  TVTunes_dict = {}

  Log.Info("Prefs['themes']: '{}', title: '{}', title2: '{}'".format(Prefs['themes'], title1, title2))
  Log.Info("--- themes ---".ljust(157, '-'))
  if 'TVTunes' in Prefs['themes'] and (title1 or title2):
    for url in [THEME_URL.format(String.Quote(t)) for t in (title1, title2) if t]:
      result = '*' if url in metadata.themes or Data.Exists(url.split('/')[-1]) else common.GetStatusCode(url)
      Log.Info("Return code: '{}', url: '{}'".format(result, url))
      if result in (200, "*"):  Log.Info("[ ] theme: {}".format(SaveDict(("TelevisionTunes/"+url.split('/')[-1], 1, None) , TVTunes_dict, 'themes', url)))

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("TVTunes_dict: {}".format(DictString(TVTunes_dict, 1)))
  return TVTunes_dict
  