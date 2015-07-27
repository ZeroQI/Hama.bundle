HTTP Anidb Metadata Agent (HAMA)
================================
HAMA was initially created By Atomicstrawberry until v0.4 included.

The support thread is located [here](http://forums.plexapp.com/index.php/topic/77636-release-http-anidb-metadata-agent-hama/)

Here are the features:

    * Separate language order selection for the series name and episode titles in Agent Settings (Supports Kanji characters in folders, filenames, titles)
    * Episode summary courtesy of TVDB (in English only) through episode mapping
    * Uses studio from mapping file then AniDB (as often missing from AniDB)
    * Search part entirely local through AniDB HTML API database file anime-titles.xml
    * AniDB ID to TVDB/TMDB ID matching (with studio and episode mapping list) with ScudLee's xml mapping file (anime-list-full.xml)
    * Warnings in Series or Episode description (no poster available, episode summary empty, TVDB id not in mapping file) to allow the community to update more easily the mapping XML or TVDB, list of missing episodes


ScudLee xml mapping files
==========================
I use AniDB HTTP title database file

   * anime-titles.xml:	Mentioned http://wiki.anidb.net/w/API and downloadable http://anidb.net/api/anime-titles.xml.gz once a day MAXIMUM

I also use the following XML files from ScudLee with his approval:

   * anime-list-full.xml:	Maps the AniDB ID to the TVDB ID, providing the studio 
				and episode mapping matrix
   * anime-movieset-list.xml:	Allows movies to be grouped together

[Source]           (https://github.com/ScudLee/anime-lists/)
[XBMC Forum thread](http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010)

Better ABsolute Scanner (BABS) has been replaced by Absolute Series Scanner (ASS), which i have entirely re-written
==============================================================================================================================
I recommend installing this scanner as it supports absolute numbering, a requirement with AniDB and anime in general.
It supports nearly everything out of the box. Please note all user specific scanner type directories are NOT created by default
[Source](https://github.com/ZeroQI/Absolute-Series-Scanner/blob/master/Series/Absolute%20Series%20Scanner.py)

Installation Folder:

    * *nix:	~/Library/Application Support/Plex Media Server/Scanners/Series/BABS.py
    * Synology:	(/volume1)/Plex/Library/Application Support/Plex Media Server/Scanners/Series/BABS.py

Installation
============

Get the latest zip package in [this thread](https://forums.plex.tv/discussion/77636/release-http-anidb-metadata-agent-hama#latest).
It contains most data folders to create, or download all files there.

Copy the agent folder ("Hama.bundle") in to your Plug-Ins folder. You can find out how to find your Plug-Ins folder [here](https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)

    * Windows XP, Server 2003, Home Server:     C:\Documents and Settings\yourusername\Local Settings\Application Data\Plex Media Server\Plug-Ins\
    * Windows Vista/7/8:                        %LOCALAPPDATA%\Plex Media Server\Plug-Ins\ (%LOCALAPPDATA% = C:\Users\XXXXX\AppData\Local\)
    * Mac OS X:                                 ~/Library/Application Support/Plex Media Server/Plug-Ins
    * Linux:                                    $PLEX_HOME/Library/Application Support/Plex Media Server/Plug-Ins
    * QNAP:                                     /share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Plug-ins
                                                /root/Library/Plex Media Server/Plug-ins (also present here If running only)
    * Synology:                                 (/volume1)/Plex/Library/Application Support/Plex Media Server/Plug-ins 

(Optional) If you want a local cache for images and theme songs:

Go into the agent data folder ("Plug-In Support/Data/com.plexapp.agents.hama/DataItems") and create the following folders in it:

    * "AniDB"
    * "Plex"
    * "OMDB"
    * "TVDB"
    * "TVDB/_cache/fanart/original"
    * "TVDB/episodes"
    * "TVDB/fanart/original"
    * "TVDB/fanart/vignette"
    * "TVDB/graphical"
    * "TVDB/posters"
    * "TVDB/seasons"
    * "TVDB/seasonswide"
    * "TVDB/text"

The XMLs are downloaded (cached) and a copy is saved here and used in case of connection issues:

   * anime-titles.xml        AniDB HTTP API, contain all anime titles, downloaded from http://anidb.net/api/anime-titles.xml.gz
   * anime-list-master.xml   ScudLee's AniDB to TVDB xml mapping file, give studio and episode mapping list for te episode overview, downloaded from [here](https://raw.github.com/ScudLee/anime-lists/master/anime-list-master.xml)
   * anime-movieset-list.xml ScudLee's movie collection (Because XBMC only supports movie collection and the files were developed for AniDB mod XBMC plugin), downloaded from [here](https://raw.github.com/ScudLee/anime-lists/master/anime-movieset-list.xml)

Agents can only write data in data folder as binary objects or as dictionaries, but cannot create folders unfortunately.
I use these folders to cache all pictures, theme songs, since they are not cached by Plex.
This way, even if you recreate the whole Plex anime folder entry, you do not have to download the same file again.

HAMA downloads the XMLs from the internet (using Plex cache for 1 week), then local, then resource folder.
For pictures and theme songs, it takes from the cache first, then the internet

Updating:
   * replace "_ _init_ _.py" with the latest [here](https://github.com/ZeroQI/Hama/blob/master/Hama.bundle/Contents/Code/__init__.py)
   * If no folder in data was created or data moved there and no new option was added to the agent settings, it will work

After restarting Plex servers, the new agent will be loaded and you will find all agents settings in the official framework agent settings window:
   * "Plex > Settings > Server > Agents > TV Shows > HamaTV > Agent settings"


Troubleshooting:
================

Check the data folders are created and the agent is where it should be, paste the agent logs relevant section

Plex Logs:

    * Agent logs:        [...]/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.hama.log
    * Media Scannerlogs: [...]/Plex Media Server/Logs/Plex Media Scanner.log
    * Scanner logs:      [...]/Plex Media Server/Logs/Plex Media Scanner (custom ASS).log

Hama specific html logs to allow to update databases for missing info or to list missing episodes:

    * [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list.htm
    * [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/themes.htm
    * [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB.htm
    * [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB.htm
    * [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Episodes.htm

To Do
=====

   * Package of Studio Logos. Will not work on that but somebody else can
	https://forums.plex.tv/discussion/120618/new-studio-logos-for-media-flags-bundle
	https://forums.plex.tv/index.php/topic/77636-release-http-anidb-metadata-agent-hama/?p=451061

   * Package of Theme Songs, as local loading supported (name convention: Data/com.plexapp.agents.hama/DataItems/Plex/anidbid.mp3). Plex use 30s songs but use seasons, so a package of songs capped at 30s should share the same legality. Will not work on that but local loading works
   * Add RSS links to AniDB missing episodes summary
