Absolute Series Scanner (ASS):
==============================
Better ABsolute Scanner (BABS) has been replaced by Absolute Series Scanner (ASS), which i have entirely re-written.
I recommend installing the "Absolute Series Scanner" as it supports nearly everything out of the box, normal season numbering, absolute numbering (a requirement with AniDB and anime in general), grouping folders, DVD folders (limited)...

It also supports direct matchin by putting an *.id file with the series id (anidb, tvdb, tmdb) or at the end of the sereis title by adding " [anidb-12345]" or " [tvdb-1234567]" with hte relevant sereis id. Giving a tvdb id will make the absolute series show with tvdb seasons transparently.


HTTP Anidb Metadata Agent (HAMA)
================================
HAMA was initially created By Atomicstrawberry until v0.4 included.
I have used a date stamp ex 2015-08-31 for the versions

Here are HAMA agent features:

    * Separate language order selection for the series name and episode titles in Agent Settings (Supports Kanji characters in folders, filenames, titles)
    * Episode summary (in English only) courtesy of TVDB  through episode mapping
    * Uses studio from mapping file then AniDB (as often missing from AniDB)
    * Search part entirely local through AniDB HTML API database file anime-titles.xml
    * AniDB ID to TVDB/TMDB ID matching (with studio and episode mapping list) with ScudLee's xml mapping file (anime-list-full.xml)
    * Warnings in Series or Episode description (no poster available, episode summary empty, TVDB id not in mapping file) to allow the community to update more easily the mapping XML or TVDB, list of missing episodes
    * Posters from TVDB (assign a poster to each anidb id in anidb to tvdb mapping file to avoid poster duplicates)
    * TVDB episode screenshots from TVDB 
    * Collection mapping from ScudLee's movie collection ammended with AniDB RelatedAnime field
    
Metadata source
===============
I use AniDB HTTP title database file and ScudLee's XML files with his approval
   * anime-titles.xml:	        http://anidb.net/api/anime-titles.xml.gz [API: http://wiki.anidb.net/w/API]
   * anime-list-full.xml:	Maps the AniDB ID to the TVDB ID, providing studio,episode mapping matrix, tmdb/tmdb id
   * anime-movieset-list.xml:	Allows movies to be grouped together
   * tvdb benner and serie xml: episode titles and summaries, screenshot, posters
   * anidb serie xml:           Serie information, poster
   * Plex theme song:           Serie theme song

ScudLee's XMLs:                 https://github.com/ScudLee/anime-lists/
ScudLee's XBMC AniDB mod agent: http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010

Installation
============

Get the latest zip package in (https://forums.plex.tv/discussion/77636/release-http-anidb-metadata-agent-hama#latest).
It contains all data folders to create. Copy all folders to the respective plex main folder:
   . "Scanners"         "Series/Absolute series Scanner.py" goes inside
   . "Plug-ins"         Hama agent "Hama.bundle" folder goes inside
   . "Plug-ins support" Agent data folders (com.plexapp.agents.hama/DataItems/Anidb|OMDB|plex|TMDB|TVDB) goes inside
   . "Logs"             "X-Plex-Token.id"      Put from an item view xml the url token inside to have a log per library
                        "no_timestamp"         delete to have timestamps in logs)
                        "keep_zero_size_files" delete to have Plex skip empty files)
   
Copy the agent folder ("Hama.bundle") in to your Plug-Ins folder. You can find out how to find your Plug-Ins folder [here](https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)

    * Windows XP, Server 2003, Home Server:     C:\Documents and Settings\yourusername\Local Settings\Application Data\Plex Media Server\Plug-Ins\
    * Windows Vista/7/8:                        %LOCALAPPDATA%\Plex Media Server\Plug-Ins\ (%LOCALAPPDATA% = C:\Users\XXXXX\AppData\Local\)
    * Mac OS X:                                 ~/Library/Application Support/Plex Media Server/Plug-Ins
    * Linux:                                    $PLEX_HOME/Library/Application Support/Plex Media Server/Plug-Ins
    * QNAP:                                     /share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Plug-ins
                                                /root/Library/Plex Media Server/Plug-ins (also present here If running only)
    * Synology:                                 (/volume1)/Plex/Library/Application Support/Plex Media Server/Plug-ins 

'%LOCALAPPDATA%\Plex Media Server\Scanners\Series\'                                       # Windows Vista/7/8
'%USERPROFILE%\Local Settings\Application Data\Plex Media Server\Scanners\Series\'        # Windows XP, 2003, Home Server
'$HOME/Library/Application Support/Plex Media Server/Scanners/Series'                     # Mac OS
'$PLEX_HOME/Library/Application Support/Plex Media Server/Scanners/Series',               # Linux
'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series', # Debian,Fedora,CentOS,Ubuntu
'/usr/local/plexdata/Plex Media Server/Scanners/Series',                                  # FreeBSD
'/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/Scanners/Series',              # FreeNAS
'${JAIL_ROOT}/var/db/plexdata/Plex Media Server/Scanners/Series',                         # FreeNAS
'/c/.plex/Library/Application Support/Plex Media Server/Scanners/Series',                 # ReadyNAS
'/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Scanners/Series',        # QNAP
'/volume1/Plex/Library/Application Support/Plex Media Server/Scanners/Series',            # Synology, Asustor
'/raid0/data/module/Plex/sys/Plex Media Server/Scanners/Series',                          # Thecus
'/raid0/data/PLEX_CONFIG/Plex Media Server/Scanners/Series'                               # Thecus Plex community    

MANDATORY: Go into the agent data folder ("Plug-In Support/Data/com.plexapp.agents.hama/DataItems") and create the following folders in it: (folders are included in Zip archive on thread, i recently added "TVDB/episodes" folder for TVDB screenshots)
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
=========
If no folder in data was created or data moved there and no new option was added to the agent settings, it will work.
   . Update scanner file with the latest from https://github.com/ZeroQI/Absolute-Series-Scanner/blob/master/Series/Absolute%20Series%20Scanner.py
   . replace agent "_ _init_ _.py" with the latest from https://github.com/ZeroQI/Hama/blob/master/Hama.bundle/Contents/Code/__init__.py
If it doesn't, get latest zip and start from scratch, but no need to delete "Plug-in Support" folder

After restarting Plex servers, the new agent will be loaded and you will find all agents settings in the official framework agent settings window:
   * "Plex > Settings > Server > Agents > TV Shows > HamaTV > Agent settings"

I did change the metadata id from the Anidb ID to "anidb-xxxxx" with xxxxx being the anidbid.
You can use anidb.id file in series or Series/Extras folder or in the serie name " [anidbid-xxxxx]" at the end of serie folder name, works also for tvdb " [tvdb-xxxxxxx]"

Troubleshooting:
================

If nothing is scanned or episodes are missing, or file or series not geting into the GUI, that is the scanner doing...
Include the following logs then:

Support thread for Scanner: https://forums.plex.tv/discussion/113967/absolute-series-scanner-for-anime-mainly/#latest
Scanner logs:               [...]/Plex Media Server/Logs/Plex Media Scanner.log                       (scanner crash info)
                            [...]/Plex Media Server/Logs/Plex Media Scanner (custom ASS).log          (episodes info)
                            [...]/Plex Media Server/Logs/Plex Media Scanner (custom ASS) filelist.log (library file list)

If files and series are showing in Plex GUI but no metadata is downloaded or some is but no poster, that is the Agent doing
If posters are missing, check that all the data folders are created and the agent is where it should be:

Support thread for agent:   https://forums.plex.tv/discussion/77636/release-http-anidb-metadata-agent-hama#latest
Agent logs:                 [...]/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.hama.log
Hama specific html logs:    [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB.htm
                            [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB.htm
                            [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/themes.htm
                            [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list.htm
                            [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Episodes.htm

To Do (if anybody is motivated)
=====

   * Package of Studio Logos. Will not work on that but somebody else can
	https://forums.plex.tv/discussion/120618/new-studio-logos-for-media-flags-bundle
	https://forums.plex.tv/index.php/topic/77636-release-http-anidb-metadata-agent-hama/?p=451061

   * Package of Theme Songs, as local loading supported (name convention: Data/com.plexapp.agents.hama/DataItems/Plex/anidbid.mp3). Plex use 30s songs but use seasons, so a package of songs capped at 30s should share the same legality. Will not work on that but local loading works
   * Add RSS links to AniDB missing episodes summary ?
