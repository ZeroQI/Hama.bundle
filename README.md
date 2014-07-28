HTTP Anidb Metadata Agent (HAMA)
================================
HAMA was initially created By Atomicstrawberry.

The support thread is located [here](http://forums.plexapp.com/index.php/topic/77636-release-http-anidb-metadata-agent-hama/)

Here are the features:

    * Separate language order selection for the serie name and episode titles in Agent Settings (Supports Kanji characters in folders, filenames, titles)
    * Episode summary courtesy of TVDB in english only through episode mapping
    * using Studio from mapping file then AniDB (as often missing from AniDB)
    * Search part entirely local through AniDB HTML API database file anime-titles.xml
    * AniDB id to TVDB/TMDB id matching (with studio and episode mapping list) with ScudLee's xml mapping file (anime-list-full.xml)
    * Warnings in Series or Episode description (no poster available, episode summary empty, TVDB id not in mapping file) to allow the community to update more easily the mapping XML or TVDB, list of missing episodes


ScudLee xml mapping files
==========================
I use the following XML files from ScudLee with his approval:

   * anime-list-full.xml:     maps the AniDB id to the TVDB id, providing the studio and episode mapping matrix
   * anime-movieset-list.xml: allow to group movies together

Source, format, contributing: https://github.com/ScudLee/anime-lists/blob/master/README.md
XBMC Forum thread:            http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010

I also use AniDB HTTP title database file

   * anime-titles.xml      mentionned http://wiki.anidb.net/w/API and downloadable http://anidb.net/api/anime-titles.xml.gz once a day MAXIMUM

Better ABsolute Scanner (BABS)
==============================
I recommend installing that scanner as it supports absolute numbering, a requirement with AniDB and anime in general.
Please note all user specific scanner type directories are NOT created by default
Source:   http://forums.plexapp.com/index.php/topic/31081-better-absolute-scanner-babs/

Installation Folder:
   . Ubuntu:   ~/Library/Application Support/Plex Media Server/Scanners/Series/BABS.py
   . Synology: (/volume1) /Plex/Library/Application Support/Plex Media Server/Scanners/Series/BABS.py

Installation
============

Get the latest zip package in the thread: https://forums.plex.tv/index.php?app=core&module=attach&section=attach&attach_id=29291. It does contain most data folders to create, or download all files there.
I am working to create release packages on GitHub currently

Copy the agent folder ("Hama.bundle") in: (Source: https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)

    * Windows Windows XP, Server 2003, Home Server: C:\Documents and Settings\yourusername\Local Settings\Application Data\Plex Media Server\Plug-Ins\
    * Windows Vista, Windows 7, Windows 8:          %LOCALAPPDATA%\Plex Media Server\Plug-Ins\ (%LOCALAPPDATA% = C:\Users\XXXXX\AppData\Local\)
    * Mac OS X:                                     ~/Library/Application Support/Plex Media Server/Plug-Ins
    *  Linux:                                        $PLEX_HOME/Library/Application Support/Plex Media Server/Plug-Ins
    * QNAP:                                         /share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Plug-ins
                                                     /root/Library/Plex Media Server/Plug-ins (also present here If running only)
    *     - Synology:                                     (/volume1) Plex/Library/Application Support/Plex Media Server/Plug-ins 

(Optional) Data folders if you want local cache for images and theme songs
Go into the agent data folder ("plug-in Support/Data/com.plexapp.agents.hama/DataItems"):
     - Synology:                                     /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems

Create the following folders in it:

    * "AniDB"
    * "Plex"
    * "OMDB"
    * "TVDB"
    * "TVDB/_cache/fanart/original"
    * "TVDB/fanart/original"
    * "TVDB/fanart/vignette"
    * "TVDB/graphical"
    * "TVDB/posters"
    * "TVDB/seasons"
    * "TVDB/seasonswide"
    * "TVDB/text"

The XMLs are downloaded (cached for 2 weeks) and a copy is saved here and used in case of connection issues:

   * anime-titles.xml        AniDB HTTP API, contain all anime titles, downloaded from http://anidb.net/api/anime-titles.xml.gz
   *  anime-list-master.xml   ScudLee's AniDB to TVDB xml mapping file, give studio and episode mapping list for te episode overview, downloaded from https://raw.github.com/ScudLee/anime-lists/master/anime-list-master.xml
   *  anime-movieset-list.xml ScudLee's movie collection (Because XBMC only support movie collection and the files were develloped for AniDB mod XBMC plugin), downloaded from https://raw.github.com/ScudLee/anime-lists/master/anime-movieset-list.xml

Agents can only write data in data folder as binary objects or as dictionaries, but cannot create folders unfortunatly
I use theses folders to cache all pictures, theme songs, since they are not cached by plex.
This way, even if you recreate the whole Plex anime folder entry, you do not have to download the same file again.

it downloads the XMLs from the internet (using pelx cache for 1 week), then local, then ressource folder
For pictures and theme songs, it takes from the cache first, then the internet

Updating:
   . replace __init__.py with the latest on https://github.com/ZeroQI/Hama/blob/master/Hama.bundle/Contents/Code/__init__.py
   . If no folder in data was created or data moved there and no new option was added to the agent settings, it will work

After restarting Plex servers, the new agent will be loaded and you will find all agents settings in the official framework agent settings window:
   . "Plex > Settings > Server > Agents > TV Shows > HamaTV > Agent settings"


Troubleshooting:
================

Check the data folders are created and the agent is where it should be, paste the agent logs relevant section

Plex Logs:

    * Agent logs:        /volume1/Plex/Library/Application Support/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.hama.log
    * Media Server logs: /volume1/Plex/Library/Application Support/Plex Media Server/Logs/Plex Media Server.log
    * Media Scannerlogs: /volume1/Plex/Library/Application Support/Plex Media Server/Logs/Plex Media Scanner.log

Hama specific html logs to allow to update databases for missing info or to list missing episodes:

    * /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list.htm
    * /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/themes.htm
    * /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB.htm
    * /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB.htm
    * /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Episodes.htm

To Do
=====

   * Package of Studio Logos (see post https://forums.plex.tv/index.php/topic/77636-release-http-anidb-metadata-agent-hama/?p=451061). Will not work on that but somebody else can
   * Package of Theme Songs, as local loading supported (name convention: Data/com.plexapp.agents.hama/DataItems/Plex/anidbid.mp3). Plex use 30s songs but use seasons, so a package of songs capped at 30s should share the same legality. will not work on that but local loading works
   * Add rss links to anidb missing episodes summary
