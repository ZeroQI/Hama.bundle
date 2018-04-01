#Root
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/README.md"                    -OutFile "README.md"

#Contents
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Info.plist"          -OutFile "Contents/Info.plist"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/DefaultPrefs.json"   -OutFile "Contents/DefaultPrefs.json"

#Contents/Code
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/__init__.py"    -OutFile "Contents/Code/__init__.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/common.py"      -OutFile "Contents/Code/common.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/AnimeLists.py"  -OutFile "Contents/Code/AnimeLists.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/AniDB.py"       -OutFile "Contents/Code/AniDB.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/TheTVDB.py"     -OutFile "Contents/Code/TheTVDB.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/FanartTV.py"    -OutFile "Contents/Code/FanartTV.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/TheMovieDb.py"  -OutFile "Contents/Code/TheMovieDb.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/MyAnimeList.py" -OutFile "Contents/Code/MyAnimeList.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/TVTunes.py"     -OutFile "Contents/Code/TVTunes.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/OMDb.py"        -OutFile "Contents/Code/OMDb.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/Plex.py"        -OutFile "Contents/Code/Plex.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/Beta-Agent/Contents/Code/Local.py"       -OutFile "Contents/Code/Local.py"
