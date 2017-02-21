### Plex.tv ###

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###

'''  Plex Theme songs list:  https://support.plex.tv/hc/en-us/articles/201178657-Current-TV-Themes
     Submit, Request songs:  https://support.plex.tv/hc/en-us/articles/201572843 / Limitations: 30s length, 44.1 Kh, 128 to 256 kbps / Naming convention: "TV Show Name - TVDBID.mp3"

     To do: TVDB has one song per serie but Japanese anime has one per season, having a song for AniDB series would be more factually correct using AniDB series definition.
            Can we add an OP video as Theme song? if not, recover theme song from opening video with ffmpeg script
            Package of anime theme songs 30s length indexed on anidbid OR TVDBid but with season xxxxx-s1
'''
def GetMetadata(metadata, TVDBid, TheTVDB_dict, error_log):
  THEME_URL = 'http://tvthemes.plexapp.com/%s.mp3'
  Plex_dict = {}
  Log.Info("".ljust(157, '-'))
  Log.Info("Plex.GetMetadata() - TVDBid: '{TVDBid}', song present: '{present}', Prefs['Themes']: '{setting}'".format(TVDBid=TVDBid, present = THEME_URL % TVDBid in metadata.themes, setting = Prefs['Plex']))
  if Prefs['Plex'] and TVDBid:
    if common.GetServerCode(THEME_URL % TVDBid) == 200:  #download for error_log test but leave as meta for template reason, and in case of new theme song source
      common.metadata_download (metadata, metadata.themes, THEME_URL % TVDBid, "Plex/%s.mp3" % TVDBid, 1, None)
      Plex_dict['themes'] = {THEME_URL % TVDBid: ("Plex/%s.mp3" % TVDBid, 2, None)}
  else:  error_log['Plex themes missing'].append("TVDBid: %s | Title: '%s' | %s" % (common.WEB_LINK % (common.TVDB_SERIE_URL % TVDBid, TheTVDB_dict['title']), TheTVDB_dict['title'], common.WEB_LINK % ("mailto:themes@plexapp.com?cc=&subject=Missing%%20theme%%20song%%20-%%20&#39;%s%%20-%%20%s.mp3&#39;" % (TheTVDB_dict['title'], TVDBid), 'Upload')))
  return Plex_dict
  
def TVTunes(metadata, TVDBid, TheTVDB_dict, mappingList):
  THEME_URL = "http://www.televisiontunes.com/uploads/audio/%s.mp3"
  TVTunes_dict = {}
  Log.Info("".ljust(157, '-'))
  if Prefs['Plex'] and 'name' in mappingList and mappingList['name']:
    if common.GetServerCode(THEME_URL % mappingList['name']) == 200:
      Log.Info("Plex.TelevisionTunes() - Song detected")
      #common.metadata_download (metadata, metadata.themes, THEME_URL % mappingList['name'], "TelevisionTunes/%s.mp3" % mappingList['name'], 1, None)
      TVTunes_dict['themes'] = {THEME_URL % mappingList['name']: ("TelevisionTunes/%s.mp3" % mappingList['name'], 2, None)}
    else:  Log.Info("Plex.TelevisionTunes() - no song present: '%s'" % THEME_URL % mappingList['name'])
  if Prefs['Plex'] and 'name' in mappingList and TheTVDB_dict['title'] and not TheTVDB_dict['title'] == mappingList['name']:
    if common.GetServerCode(THEME_URL % TheTVDB_dict['title']) == 200:
      #common.metadata_download (metadata, metadata.themes, THEME_URL % mappingList['name'], "TelevisionTunes/%s.mp3" % mappingList['name'], 1, None)
      TVTunes_dict['themes'] = {THEME_URL % TheTVDB_dict['title']: ("TelevisionTunes/%s.mp3" % TheTVDB_dict['title'], 2, None)}
    else:  Log.Info("Plex.TelevisionTunes() - no song present: '%s'" % THEME_URL % TheTVDB_dict['title'])
  return TVTunes_dict
  
