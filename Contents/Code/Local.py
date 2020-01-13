### Local ###

### Imports ###  "common.GetPosters" = "from common import GetPosters"
# Python Modules #
import os      # path, listdir
import re      # match, ignorecase
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###
SEASON_RX = [                                                                       ### Seasons Folders
              r'^Specials',                                                         # Specials (season 0)
              r'^(Season|Series|Book|Saison|Livre|S)[ _\-\.]*(?P<season>\d{1,2})',  # Season / Series / Book / Saison / Livre / S
              r'^(?P<show>.*?)[\._\- ]+S(?P<season>\d{2})$',                        # (title) S01
              r'^(?P<season>\d{1,2})',                                              # ##
              r'^(Saga|(Story )?Ar[kc])']                                           # Last entry, folder name droped but files kept: Saga / Story Ar[kc] / Ar[kc]
      
### Functions ###  
def GetMetadata(media, movie):
  Log.Info("=== Local.GetMetadata() ===".ljust(157, '='))
  Local_dict          = {}
  dir                 = common.GetMediaDir(media, movie)
  library, root, path = common.GetLibraryRootPath(dir)

  if movie: return Local_dict

  Log.Info("dir:     {}".format(dir))
  Log.Info("library: {}".format(library))
  Log.Info("root:    {}".format(root))
  Log.Info("path:    {}".format(path))

  if not path in ('_unknown_folder', '.'):
  
    series_root_folder = os.path.join(root, path.split(os.sep, 1)[0])
    Log.Info("series_root_folder:  {}".format(series_root_folder))
    Log.Info("Grouping folder:     {}".format(os.path.basename(series_root_folder)))
    if not os.path.exists(series_root_folder):
      Log.Info('files are currently inaccessible')
      return Local_dict
    subfolder_count    = len([file for file in os.listdir(series_root_folder) if os.path.isdir(os.path.join(series_root_folder, file))])
    Log.Info("subfolder_count:     {}".format(subfolder_count))
    
    ### Extract season and transparent folder to reduce complexity and use folder as serie name ###
    reverse_path, season_folder_first = list(reversed(path.split(os.sep))), False
    for folder in reverse_path[:-1]:                 # remove root folder from test, [:-1] Doesn't thow errors but gives an empty list if items don't exist, might not be what you want in other cases
      for rx in SEASON_RX:                           # in anime, more specials folders than season folders, so doing it first
        if re.search(rx, folder, re.IGNORECASE):     # get season number but Skip last entry in seasons (skipped folders)
          reverse_path.remove(folder)                # Since iterating slice [:] or [:-1] doesn't hinder iteration. All ways to remove: reverse_path.pop(-1), reverse_path.remove(thing|array[0])
          if rx!=SEASON_RX[-1] and len(reverse_path)>=2 and folder==reverse_path[-2]:  season_folder_first = True
          break
   
    Log.Info("reverse_path:        {}".format(reverse_path))
    Log.Info("season_folder_first: {}".format(season_folder_first))
    if len(reverse_path)>1 and not season_folder_first and subfolder_count>1:  ### grouping folders only ###
      Log.Info("[ ] collection (Grouping folder): {}".format(SaveDict([reverse_path[-1]], Local_dict, 'collections')))
    else:  Log.Info("Grouping folder not found")
       
  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("Local_dict: {}".format(DictString(Local_dict, 1)))
  return Local_dict
