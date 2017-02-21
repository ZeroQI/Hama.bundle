#Create object, replace extension dot with underscore
$README_md         = new-object System.Net.WebClient
$Info_plist        = new-object System.Net.WebClient
$DefaultPrefs_json = new-object System.Net.WebClient
$__init___py       = new-object System.Net.WebClient
$common_py         = new-object System.Net.WebClient
$AniDB_py          = new-object System.Net.WebClient
$AnimeLists_py     = new-object System.Net.WebClient
$TheTVDB_py        = new-object System.Net.WebClient
$TheMovieDB_py     = new-object System.Net.WebClient
$MyAnimeList_py    = new-object System.Net.WebClient
$FanartTV_py       = new-object System.Net.WebClient
$OMDb_py           = new-object System.Net.WebClient
$Plex_py           = new-object System.Net.WebClient
$Simkl_py          = new-object System.Net.WebClient

#Download files
$README_md.DownloadFile(        "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/README.md"                    , "README.md"                   )
$Info_plist.DownloadFile(       "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Info.plist"          , "Contents/Info.plist"         )
$DefaultPrefs_json.DownloadFile("https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/DefaultPrefs.json"   , "Contents/DefaultPrefs.json"  )
$__init___py.DownloadFile(      "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/__init__.py"    , "Contents/Code/__init__.py"   )
$common_py.DownloadFile(        "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/common.py"      , "Contents/Code/common.PY"     )
$AniDB_py.DownloadFile(         "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/AniDB.py"       ,  "Contents/Code/AniDB.py"     )
$AnimeLists_py.DownloadFile(    "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/AnimeLists.py"  , "Contents/Code/AnimeLists.py" )
$TheTVDB_py.DownloadFile(       "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/TheTVDB.py"     , "Contents/Code/TheTVDB.py"    )
$TheMovieDB_py.DownloadFile(    "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/TheMovieDB.py"  , "Contents/Code/TheMovieDB.py" )
$MyAnimeList_py.DownloadFile(   "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/MyAnimeList.py" , "Contents/Code/MyAnimeList.py")
$FanartTV_py.DownloadFile(      "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/FanartTV.py"    , "Contents/Code/FanartTV.py"   )
$OMDb_py.DownloadFile(          "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/OMDb.py"        , "Contents/Code/OMDb.py"       )
$Plex_py.DownloadFile(          "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/Plex.py"        , "Contents/Code/Plex.py"       )
$Simkl_py.DownloadFile(         "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/Simkl.py"       , "Contents/Code/Simkl.py"      )
