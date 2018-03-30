#Download files
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/README.md" -OutFile "README.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Info.plist" -OutFile "Contents/Info.plist"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/DefaultPrefs.json"-OutFile "Contents/DefaultPrefs.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/__init__.py" -OutFile "Contents/Code/__init__.py" 
