HTTP Anidb Metadata Agent (HAMA)
================================
Created By Atomicstrawberry and maintained until v0.4 <br />
<UL>
 <LI>http://forums.plexapp.com/index.php/topic/66918-release-http-anidb-metadata-agent-hama/</LI>
</UL>
Forked from v0.4 and maintained since by ZeroQI <br />
<UL>
 <LI>http://forums.plexapp.com/index.php/topic/77636-release-http-anidb-metadata-agent-hama/</LI>
</UL>
 <br />
Here are the changes Between v0.5 and v0.4:<BR />

New features
<UL>
   <LI> Search part entirely local <BR />Location: Hama.bundle\Contents\Resources\anime-titles.xml
   <LI> AniDB id to TVDB id matching (with studio and episode mapping list) with ScudLee's xml mapping file <BR />location: Hama.bundle\Contents\Resources\anime-list-full.xml
   <LI> Episode summary downloaded from theTVDB.com in english only through episode mapping
   <LI> using Studio from mapping file as often missing from AniDB.net
   <LI> Separate language order selection for the serie name and episode titles
   <LI> TVDB and AniDB serie, season and episode link integrated in summary
   <LI> Warnings in Serie or Episode description (no poster available, episode summary empty, TVDB id not in mapping file) to allow the community to update more easily the mapping XML or TVDB
</UL>

Improvements
<UL>
   <LI> Changed theTVDB.com picture function to reflect how the XML behaves, removing most un-necessary "thumbnail not available" logs.
   <LI> Changed theTVDB.com picture function to put season posters on seasons only [still in progress]
   <LI> Reduced the number of functions: searchByName and parseAnimeXml are directly called by the agent now
   <LI> Commented source code.
   <LI> Normalised Logging
   <LI> imported movie bolean from AniDB.net xml
   <LI> Commented some file formats in the source for clarity when reading
</UL>

ScudLee xml mapping files
==========================
I use the following XML files from ScudLee with his approval:
<UL>
   <LI> anime-list-full.xml: maps the AniDB id to the TVDB id, providing the studio and episode mapping matrix</LI>
   <LI> anime-movieset-list.xml: allow to group movies together</LI>
</UL>
Source, format, contributing: https://github.com/ScudLee/anime-lists/blob/master/README.md
XBMC Forum thread: http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010


Better ABsolute Scanner (BABS)
==============================
I also use that scanner cojointly as it allows for absolute numbering, a requirement with AniDB.
http://forums.plexapp.com/index.php/topic/31081-better-absolute-scanner-babs/

Installation
============

Get the latest zip package in the thread: https://forums.plex.tv/index.php?app=core&module=attach&section=attach&attach_id=29291. It does contain most data folders to create, or download all files there.


Copy the agent folder ("Hama.bundle") in: (Source: https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)

     - Windows Windows XP, Server 2003, Home Server: C:\Documents and Settings\yourusername\Local Settings\Application Data\Plex Media Server\Plug-Ins\
     - Windows Vista, Windows 7, Windows 8:          %LOCALAPPDATA%\Plex Media Server\Plug-Ins\ (%LOCALAPPDATA% = C:\Users\XXXXX\AppData\Local\)
     - Mac OS X:                                     ~/Library/Application Support/Plex Media Server/Plug-Ins
     - Linux:                                        $PLEX_HOME/Library/Application Support/Plex Media Server/Plug-Ins
     - QNAP:                                         /share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Plug-ins
                                                     /root/Library/Plex Media Server/Plug-ins (also present here If running only)
     - Synology:                                     /volume1/Plex/Library/Application Support/Plex Media Server/Plug-ins
                                                     Plex/Library/Application Support/Plex Media Server/Plug-ins (In File Station, no console needed)

Go into the agent data folder ("com.plexapp.agents.hama") in ("plug-in Support/Data"):
     - Synology:                                     /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama

Create the following folders in it:
   . AniDB Posters
   . Theme Songs
   . XMLs
   . TVDB:
     - "_cache/fanart/original"
     - "fanart/original"
     - "fanart/vignette"
     - "graphical"
     - "posters"
     - "seasons"
     - "text"
The XMLs are downloaded (cached for 2 weeks) and a copy is saved here and used in case of internet issue
   . anime-titles.xml        AniDB HTTP API, contain all anime titles, downloaded from http://anidb.net/api/anime-titles.xml.gz
   . anime-list-master.xml   ScudLee's AniDB to TVDB xml mapping file, give studio and episode mapping list for te episode overview, downloaded from https://raw.github.com/ScudLee/anime-lists/master/anime-list-master.xml
   . anime-movieset-list.xml ScudLee's movie collection (Because XBMC only support movie collection and the files were develloped for AniDB mod XBMC plugin), downloaded from https://raw.github.com/ScudLee/anime-lists/master/anime-movieset-list.xml

Agents can only write data in data folder as binary objects or as dictionaries, but cannot create folders unfortunatly (if i am wrong, let me know)
I use theses folders to cache all pictures, theme songs, since they are not cached by plex.
This way, even if you recreate the whole Plex anime folder entry, you do not have to download the same file again.

Updating:
   . replace __init__.py with the latest on https://github.com/ZeroQI/Hama/blob/master/Hama.bundle/Contents/Code/__init__.py
   . If no folder in data was created or data moved there and no new option was added to the agent settings, it will work

After restarting Plex servers, the new agent will be loaded and you will find all agents settings in the official framework agent settings window:
   . "Plex > Settings > Server > Agents > TV Shows > HamaTV > Agent settings"


Troubleshooting:
================

Check the data folders are created and the agent is where it should be, paste the agent logs relevant section

Plex Logs:
   . Synology:                                       Agent logs:        /volume1/Plex/Library/Application Support/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.hama.log
                                                     Media Server logs: /volume1/Plex/Library/Application Support/Plex Media Server/Logs/Plex Media Server.log
                                                     Media Scannerlogs: /volume1/Plex/Library/Application Support/Plex Media Server/Logs/Plex Media Scanner.log

Hama specific html logs to allow to update databases for missing info or to list missing episodes
   . /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list.htm
   . /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/themes.htm
   . /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB.htm
   . /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB.htm
   . /volume1/Plex/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Episodes.htm

To Do
=====
   . Package of Studio Logos (see post https://forums.plex.tv/index.php/topic/77636-release-http-anidb-metadata-agent-hama/?p=451061). Will not work on that but somebody else can
   . Package of Theme Songs supported, but none exist (name convention: anidbid.mp3). Plex use 30s songs but use seasons, so a package of songs capped at 30s should share the same legality. will not work on that but local loading works
   . Need to ammend the code so that not putting folders still download posters albeit without caching
   . Need to splig logs created so each contain one type of issue only (as overview missing in thetvdb flood poster missing messages for example)
   . Should i cache locally anidb XML? they are cached for 2 weeks so even if banned for a day, will allow to finish the next day...

