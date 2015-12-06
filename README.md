Absolute Series Scanner (ASS):
==============================
Better ABsolute Scanner (BABS) has been replaced by Absolute Series Scanner (ASS), which i have entirely re-written.
I recommend installing the "Absolute Series Scanner" as it supports nearly everything out of the box, normal season numbering, absolute numbering (a requirement with AniDB and anime in general), grouping folders, DVD folders (limited)...

Here are Absolute Series Scanner features: [!] = Exclusive to this scanner

    * [!] Allow grouping of series+movies in a parent folder (ex: Zero no tsukaima/[1] Princess no Rondo)
    * [!] Give episode titles extracted from the filename
    * [!] Support AniDB OP, ED, trailer, NCOP, etc... specials numbering
    * [!] DVD    folder support (some vob seem protected, pendign feedback on proportion from users)
    * [!] BluRay folder support (some vob seem protected, pendign feedback on proportion from users)
    * [!] create a filelist of the library for me to be able to re-create it with dummy files
    * [!] create a readable log of all files in last scan to allow checking for matching errors (and log skipped medias)
    * [!] direct matching passthrough with an *.id file with the series id (anidb, tvdb, tmdb) in serie or Extras Extras folder
    * [!] direct matching passthrough by appending to folder serie name folder " [anidb-12345]" or " [tvdb-1234567]" with serie id
    * [!] Giving a tvdb id will make the absolute series show with tvdb seasons transparently.
    * [!] Add all un-matched files as season 0 episodes 501+
    * Support Seasons/Sereis/saison/livre/Book for seasons
    * supports plexignore files
    * Clever episode number detection
    * Allow transparent use of Skip Ark/Story/Video folders
    * re-map specials characters
    * Manages multi-episodes (01-02, 01e02, 01-e02)
    * Manages movies and series in a single library together with the agent
    
HTTP Anidb Metadata Agent (HAMA)
================================
HAMA was initially created By Atomicstrawberry until v0.4 included.
I have used a date stamp ex 2015-08-31 for the versions

Here are HAMA agent features:

    * AniDB ID to TVDB/TMDB ID matching (with studio and episode mapping list) with ScudLee's xml mapping file
    * Posters from TVDB (assign a poster to each anidb id in anidb to tvdb mapping file to avoid poster duplicates)
    * TVDB episode screenshots
    * Episode summary (in English only) courtesy of TVDB through ScudLee's XML episode mappings
    * Uses studio from mapping file then AniDB (as often missing from AniDB)
    * Search part entirely local through AniDB HTML API database file anime-titles.xml
    * Separate language order selection for the series name and episode titles in Agent Settings (Supports Kanji characters in folders, filenames, titles)
    * Warnings in html report files (no poster available, episode summary empty, TVDB id not in mapping file) to allow the community to update more easily the mapping XML or TVDB, list of missing episodes
    * Collection mapping from ScudLee's movie collection ammended with AniDB RelatedAnime field
    * Unique posters by using the anidbid rank in the mapping to rotate the posters
    * when a serie is not found in AniDB, search TVDB and TMDB automatically
    
Metadata source
===============
I use AniDB HTTP title database file and ScudLee's XML files with his approval

ScudLee's XMLs:                 https://github.com/ScudLee/anime-lists/
ScudLee's XBMC AniDB mod agent: http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010

    * anime-titles.xml        AniDB HTTP API, contain all anime titles, downloaded from http://anidb.net/api/anime-titles.xml.gz
    * anime-list-master.xml   ScudLee's AniDB to TVDB xml mapping file, give studio and episode mapping list for te episode overview, downloaded from [here](https://raw.github.com/ScudLee/anime-lists/master/anime-list-master.xml)
    * anime-movieset-list.xml ScudLee's movie collection (Because XBMC only supports movie collection and the files were developed for AniDB mod XBMC plugin), downloaded from [here](https://raw.github.com/ScudLee/anime-lists/master/anime-movieset-list.xml)

HAMA downloads the XMLs from the internet (using Plex cache for 1 week), then local, then resource folder.
For pictures and theme songs, it takes from the cache first, then the internet

The XMLs are downloaded (cached) and a copy is saved In the agent data folders and used in case of connection issues
    * anime-titles.xml:	         http://anidb.net/api/anime-titles.xml.gz [API: http://wiki.anidb.net/w/API]
    * anime-list-full.xml:	 Maps the AniDB ID to the TVDB ID, providing studio,episode mapping matrix, tmdb/tmdb id
    * anime-movieset-list.xml: 	 Allows movies to be grouped together
    * tvdb benner and serie xml: episode titles and summaries, screenshot, posters
    * anidb serie xml:           Serie information, poster
    * Plex theme song:           Serie theme song

I did change the metadata id from the Anidb ID to "anidb-xxxxx" with xxxxx being the anidbid.
You can use anidb.id file in series or Series/Extras folder or in the serie name " [anidbid-xxxxx]" at the end of serie folder name, works also for tvdb " [tvdb-xxxxxxx]". Older agents before that need to re-create the library to have a metadata.id beginning with "anidb-"

Installation
============

Get the latest zip package in (https://forums.plex.tv/discussion/77636/release-http-anidb-metadata-agent-hama#latest).
Archive folders to copy in Plex main folder:

    * "Scanners"         "Scanners" is the only that has to be created. "Series/Absolute series Scanner.py" goes inside. 
    * "Plug-ins"         Hama agent "Hama.bundle" folder goes inside
    * "Plug-ins support" Agent data folders (com.plexapp.agents.hama/DataItems/Anidb|OMDB|plex|TMDB|TVDB) goes inside
    * "Logs"             "X-Plex-Token.id"      Put from an item view xml the url token inside to have a log per library
                         "no_timestamp"         delete to have timestamps in logs)
                         "keep_zero_size_files" delete to have Plex skip empty files)

Plex main folder location:

    * '%LOCALAPPDATA%\Plex Media Server\'                                        # Windows Vista/7/8
    * '%USERPROFILE%\Local Settings\Application Data\Plex Media Server\'         # Windows XP, 2003, Home Server
    * '$HOME/Library/Application Support/Plex Media Server/'                     # Mac OS
    * '$PLEX_HOME/Library/Application Support/Plex Media Server/',               # Linux
    * '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/', # Debian,Fedora,CentOS,Ubuntu
    * '/usr/local/plexdata/Plex Media Server/',                                  # FreeBSD
    * '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/',              # FreeNAS
    * '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/',                         # FreeNAS
    * '/c/.plex/Library/Application Support/Plex Media Server/',                 # ReadyNAS
    * '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/',        # QNAP
    * '/volume1/Plex/Library/Application Support/Plex Media Server/',            # Synology, Asustor
    * '/raid0/data/module/Plex/sys/Plex Media Server/',                          # Thecus
    * '/raid0/data/PLEX_CONFIG/Plex Media Server/'                               # Thecus Plex community    

MANDATORY: Go into the agent data folder ("Plug-In Support/Data/com.plexapp.agents.hama/DataItems") and make sure the following folders are all created: (folders are included in Zip archive on thread, i recently added "TVDB/episodes" folder for TVDB screenshots).

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

Agents can only write data in data folder as binary objects or as dictionaries, but cannot create folders unfortunately.
Any folder missing will crash the agent when an attempt to write inside is done. That is a Framework issue, all attemps are in try/except structure, to no avail...

I use these folders to cache all pictures, theme songs, since they are not cached by Plex.
This way, even if you recreate the whole Plex anime folder entry, you do not have to download the same file again.

Updating:
=========
If no folder in data was created or data moved there and no new option was added to the agent settings, it will work.

    * Update scanner file with the latest from https://github.com/ZeroQI/Absolute-Series-Scanner/blob/master/Series/Absolute%20Series%20Scanner.py
    * replace agent "_ _init_ _.py" with the latest from https://github.com/ZeroQI/Hama/blob/master/Hama.bundle/Contents/Code/__init__.py
    
If it doesn't, get latest zip and start from scratch, but no need to delete "Plug-in Support" folder

After restarting Plex servers, the new agent will be loaded and you will find all agents settings in the official framework agent settings window:

    * "Plex > Settings > Server > Agents > TV Shows > HamaTV > Agent settings"

Troubleshooting:
================

Install issue under linux are generally permission issues:
 OpenMediaVault (Debian): "sudo chmod 775 -R /var/lib/plexmediaserver"
 
If nothing is scanned or episodes are missing, or file or series not geting into the GUI, that is the scanner doing...
Include the following logs then:

Support thread for Scanner: https://forums.plex.tv/discussion/113967/absolute-series-scanner-for-anime-mainly/#latest
Scanner logs:
<ul>
  <li>[...]/Plex Media Server/Logs/Plex Media Scanner.log                       (scanner crash info)</li>
  <li>[...]/Plex Media Server/Logs/Plex Media Scanner (custom ASS).log          (episodes info)</li>
  <li>[...]/Plex Media Server/Logs/Plex Media Scanner (custom ASS) filelist.log (library file list)</li>
</ul>

If files and series are showing in Plex GUI but no metadata is downloaded or some is but no poster, that is the Agent doing
If posters are missing, check that all the data folders are created and the agent is where it should be:

Support thread for agent:
<ul>
  <li>https://forums.plex.tv/discussion/77636/release-http-anidb-metadata-agent-hama#latest</li>
</ul>

Agent logs:
<ul>
  <li>[...]/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.hama.log</li>
</ul>

Hama specific html logs:
<ul>
  <li>[...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB.htm</li>
  <li>[...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB.htm</li>
  <li>[...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/themes.htm</li>
  <li>[...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list.htm</li>
  <li>[...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Episodes.htm</li>
</ul>

Here is the feedback logs description and one example of every feedback:
   . AniDB.htm        
        - Aid: 00002 No poster present
 
   . Anime-list.htm    ScudLee;s XML file feedback
       - Aid: 00002 '3x3 Eyes' AniDB and anime-list are both missing the studio
       - Aid: 00002 '3x3 Eyes' AniDB have studio 'xxx' and XML have 'yyy'
       - Aid: 00002 '3x3 Eyes' has no matching tvdbid ('OAV') in mapping file
       - Aid: 00002 anime-list is missing the anidbid
 
   . Themes.htm       Plex TV theme support whose filename is based on TheTVDB.com id and last 30s max. Wouldn't mind somebody a package will all complete mp3 theme songs whose name would be the AniDB ID (to account for the seasons different songs)...
        - Aid: 00002 '3x3 Eyes' tvdbid: 70973 '3x3 Eyes' Missing theme song 3x3 Eyes' No English poster
        - aid: 00002 tvdbid: 70973 '3x3 Eyes' Overview Empty
        - aid: 00002 tvdbid:70973 s1e1 Overview Empty
To Do
=====

    * Package of Studio Logos. Will not work on that but somebody else can
	https://forums.plex.tv/discussion/120618/new-studio-logos-for-media-flags-bundle
	https://forums.plex.tv/index.php/topic/77636-release-http-anidb-metadata-agent-hama/?p=451061
    * Package of Theme Songs, as local loading supported (name convention: Data/com.plexapp.agents.hama/DataItems/Plex/anidbid.mp3). Plex use 30s songs but use seasons, so a package of songs capped at 30s should share the same legality. Will not work on that but local loading works
    * Add RSS links to AniDB missing episodes summary ?
    
    Studio icons
==========
For studio icons, for a comparison, XBMC uses png file, white-on-clear, sized 161px x 109px, and are saved in 'skin.aeon.nox"/media/flags/studios/' for example. 
 
On Plex however, it uses 512x288px .png located in '/volume1/Plex/Library/Application Support/Plex Media Server/Plug-ins/Media-Flags.bundle/Contents/Resources/Studio/'. substitutions.xml file in parent folder contain the mappings and needs amendind
 
Studio logos from http://forum.xbmc.or...d.php?tid=70398 [https://sites.google...imeStudios.zip] seem to work but are tiny. after playing with logos a bit, it seems:
  . no logos name in folder include dots, dash, exclamation point but can contain + and some contain spaces
 . if a logo\\NAS\Plex\Library\Application Support\Plex Media Server\Plug-ins\Media-Flags.bundle\Contents\Resources\Studio
is detected, if you replace it in PMS, it won't refresh even after clearing the browser cache...
 
After some research, to update Plex, the Media-Flags.bundle is here: https://github.com/p...tents/Resources Source: http://forums.plexap...4-studio-logos/. That would allow many to work on it and be included in the next release for everybody's benefits
 
There is an index file that needs ammending called substitutions.xml XML file [Plex\Library\Application Support\Plex Media Server\Plug-ins\Media-Flags.bundle\Contents\Resources\substitutions.xml] format is below:
```XML
<MediaFlagSubstitutions>
    <Studio>
        <match name="20th_Century_Fox" expression="20th century fox" />
        <match name="20th_Century_Fox" expression="fox 2000" />
        <match name="20th_Century_Fox" expression="fox film corp" />
        <match name="20th_Century_Fox" expression="twentieth century fox" />        [...]
        [...]
    </Studio>
    <VideoCodec>
        <match name="divx" expression=".*divx.*" />
        [...]
    </VideoCodec>
    <AudioCodec>
        <match name="dolbydigital" expression="a_ac3" />
        [...]
    </AudioCodec>
</MediaFlagSubstitutions>
```
