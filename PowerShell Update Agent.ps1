#Create object, replace extension dot with underscore
$README_md         = new-object System.Net.WebClient
$Info_plist        = new-object System.Net.WebClient
$DefaultPrefs_json = new-object System.Net.WebClient
$__init___py       = new-object System.Net.WebClient

#Download files
$README_md.DownloadFile(        "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/README.md"                 , "README.md"                 )
$Info_plist.DownloadFile(       "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Info.plist"       , "Contents/Info.plist"       )
$DefaultPrefs_json.DownloadFile("https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/DefaultPrefs.json", "Contents/DefaultPrefs.json")
$__init___py.DownloadFile(      "https://raw.githubusercontent.com/ZeroQI/Hama.bundle/master/Contents/Code/__init__.py" , "Contents/Code/__init__.py" )
