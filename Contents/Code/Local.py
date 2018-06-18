### Local ###

### Imports ###  "common.GetPosters" = "from common import GetPosters"
import common
from common                  import GetMeta, GetXml, SaveDict, Dict, natural_sort_key, GetMediaDir, GetLibraryRootPath
import os                         # path, listdir
import re  #match, ignorecase

### Variables ###  Accessible in this module (others if 'from MyAnimeList import xxx', or 'import MyAnimeList.py' calling them with 'MyAnimeList.Variable_name'
      
### Functions ###  
  
### Local ###
def GetMetadata(media, movie):
  Log.Info("".ljust(157, '-'))
  Log.Info("Local.GetMetadata()")
  if movie: return
  
  Local_dict          = {}
  dir                 = GetMediaDir(media, movie)
  library, root, path = GetLibraryRootPath(dir)
  if not path in ('_unknown_folder', '.'):
  
    Log.Info('Local.GetMetadata() - dir: {}, library:{}, root:{}, path:{}'.format(dir, library, root, path))
    series_root_folder  = os.path.join(root, path.split(os.sep, 1)[0])
    subfolder_count     = len([file for file in os.listdir(series_root_folder) if os.path.isdir(os.path.join(series_root_folder, file))])
    Log.Info('Local.GetMetadata() - series_root_folder: {}, subfolder_count: {}'.format(series_root_folder, subfolder_count))
    
    ### Extract season and transparent folder to reduce complexity and use folder as serie name ###
    reverse_path, season_folder_first = list(reversed(path.split(os.sep))), False
    SEASON_RX = [ 'Specials',                                                                                                                                           # Specials (season 0)
                  '(Season|Series|Book|Saison|Livre|S)[ _\-]*(?P<season>[0-9]{1,2}).*',                                                                                 # Season ##, Series #Book ## Saison ##, Livre ##, S##, S ##
                  '(?P<show>.*?)[\._\- ]+[sS](?P<season>[0-9]{2})',                                                                                                     # (title) S01
                  '(?P<season>[0-9]{1,2})a? Stagione.*',                                                                                                                # ##a Stagione
                  '(?P<season>[0-9]{1,2}).*',	                                                                                                                          # ##
                  '^.*([Ss]aga]|([Ss]tory )?[Aa][Rr][KkCc]).*$'                                                                                                         # Last entry in array, folder name droped but files kept: Story, Arc, Ark, Video
                ]                                                                                                                                                       #
    for folder in reverse_path[:-1]:                 # remove root folder from test, [:-1] Doesn't thow errors but gives an empty list if items don't exist, might not be what you want in other cases
      for rx in SEASON_RX :                          # in anime, more specials folders than season folders, so doing it first
        if re.match(rx, folder, re.IGNORECASE):      # get season number but Skip last entry in seasons (skipped folders)
          reverse_path.remove(folder)                # Since iterating slice [:] or [:-1] doesn't hinder iteration. All ways to remove: reverse_path.pop(-1), reverse_path.remove(thing|array[0])
          if rx!=SEASON_RX[-1] and len(reverse_path)>=2 and folder==reverse_path[-2]:  season_folder_first = True
          break
   
    if len(reverse_path)>1 and not season_folder_first and subfolder_count>1:  ### grouping folders only ###
      Log.Info("Grouping folder found, root: {}, path: {}, Grouping folder: {}, subdirs: {}, reverse_path: {}".format(root, path, os.path.basename(series_root_folder), subfolder_count, reverse_path))
      SaveDict( reverse_path[-1], Local_dict, 'collection')
    else:  Log.Info("Grouping folder not found, root: {}, path: {}, Grouping folder: {}, subdirs: {}, reverse_path: {}".format(root, path, os.path.basename(series_root_folder), subfolder_count, reverse_path))
       
  return Local_dict