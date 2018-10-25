### Plex.tv ###
'''  Plex Theme songs list:  https://support.plex.tv/hc/en-us/articles/201178657-Current-TV-Themes
     Submit, Request songs:  https://support.plex.tv/hc/en-us/articles/201572843 / Limitations: 30s length, 44.1 Kh, 128 to 256 kbps / Naming convention: "TV Show Name - TVDBID.mp3"

     To do: TVDB has one song per serie but Japanese anime has one per season, having a song for AniDB series would be more factually correct using AniDB series definition.
            Can we add an OP video as Theme song? if not, recover theme song from opening video with ffmpeg script
            Package of anime theme songs 30s length indexed on anidbid OR TVDBid but with season xxxxx-s1
'''
### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
from common import Dict, Log

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'

### Functions ###
def GetMetadata(metadata, error_log, TVDBid, title):
  url = 'http://tvthemes.plexapp.com/{}.mp3'.format(TVDBid)
  Log.Info("".ljust(157, '-'))
  if 'Plex' in Prefs['themes'] and TVDBid.isdigit():
    title  = title or TVDBid
    result = '*' if url in metadata.themes else common.GetStatusCode(url)
    Log.Info("Plex.GetMetadata() - Prefs['themes']: '{setting}, TVDBid: '{TVDBid}', result code: '{plex}', url: '{url}'".format(setting = Prefs['themes'], TVDBid=TVDBid, plex=result in(200, '*'), url=url))
    if result in(200, "*"):  return {'themes': {url: ("Plex/%s.mp3" % TVDBid, 2, None)}}
    else:                    error_log['Plex themes missing'].append("TVDBid: '{}' | Title: '{}' | {}".format(common.WEB_LINK % (common.TVDB_SERIE_URL + TVDBid, title), title, common.WEB_LINK % ("mailto:themes@plexapp.com?cc=&subject=Missing%%20theme%%20song%%20-%%20&#39;%s%%20-%%20%s.mp3&#39;" % (title, TVDBid), 'Upload')))
  else:  Log.Info("Plex.GetMetadata() - Not pulling meta - 'Plex' in Prefs['themes']: '{}', TVDBid: '{}'".format('Plex' in Prefs['themes'], TVDBid))
  return {}