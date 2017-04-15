#Download files
(New-Object System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/README.md", "README.md")
(New-Object System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Info.plist", "Contents/Info.plist")
(New-Object System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/DefaultPrefs.json", "Contents/DefaultPrefs.json")
(New-Object System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/__init__.py" , "Contents/Code/__init__.py" )