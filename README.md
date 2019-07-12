Absolute Series Scanner (ASS):
==============================
If all video files are showing in plex at the right season and episode number, the scanner did its job.
Please view ASS readme here: https://github.com/ZeroQI/Absolute-Series-Scanner/blob/master/README.md

HTTP Anidb Metadata Agent (HAMA)
================================
HAMA was initially created By Atomicstrawberry until v0.4 [2015-08-31] included.
Here are HAMA agent features:

    * Both Movies and Series Agent
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
    * Trakt scrobbling supports Hama guids

Local Media Assets
==================
This Plex written agent is responsible for loading from the user folder the following local data if present:
- Subtitles
- Movie trailer
- Theme song
- Background
- Serie poster
- Serie Season poster

Its tickbox is located in Settings > Server > Agents > Shows > HamaTV | HamaMovies > "Local Media Assets (TV|Movies)"
- https://support.plex.tv/hc/en-us/articles/200220677-Local-Media-Assets-Movies
+ https://support.plex.tv/hc/en-us/articles/200220717-Local-Media-Assets-TV-Shows

Put this agent before HAMA to prioritize local files. Here is a table summarizing naming conventions:<BR />
<TABLE>
<THEAD>
<TR> <TH> Data type         </TH> <TH> Source                                          </TH> <TH> Comment               </TH> </TR>
</THEAD>
<TBODY>
<TR> <TD> fanart            </TD> <TD> art/backdrop/background/fanart-1.ext            </TD> <TD> -1 can be ommited     </TD> </TR>
<TR> <TD> Serie poster      </TD> <TD> Serie folder: Show name-1/folder/poster/show.ext</TD> <TD> (jpg, jpeg, png, tbn) </TD> </TR>
<TR> <TD> Season poster     </TD> <TD> Season folder: Season01a.ext                    </TD> <TD> (jpg, jpeg, png, tbn) </TD> </TR>
<TR> <TD> Banner            </TD> <TD> banner/banner-1.jpg                             </TD> <TD> (jpg, jpeg, png, tbn) </TD> </TR>
<TR> <TD> Theme song        </TD> <TD> theme.mp3                                       </TD> <TD> (mp3)                 </TD> </TR>
<TR> <TD> Subtitles         </TD> <TD> file name.ext                                   </TD> <TD> (srt, smi, ssa, ass)  </TD> </TR>
<TR> <TD> Trailers          </TD> <TD> MovieName-Trailer.ext or in "Trailers" folder   </TD> <TD>                       </TD> </TR>
<TR> <TD> Plexignore files  </TD> <TD> .plexignore                                     </TD> <TD>                       </TD> </TR>
</TBODY>
</TABLE>

https://support.plex.tv/hc/en-us/articles/200220677-Local-Media-Assets-Movies

Subtitle files are supported through that

"Local Media Assets (Movies)" in the HamaMovies agent list, any files you name as MovieName-Trailer.ext or place in a 'Trailers' folder inside the movie's folder are picked up by Plex as trailers. I've done this for a few things where I have the trailer as file, but I agree - it'd be even better if we can get Hama to add any S0E2xx as a 'trailer' extra too.

Plex's trailer feature also supports displaying trailers from a URL - the metadata agent just needs to add the relevant URL at which Plex can reach the trailer. If we added support for this, it'd mean that user who don't have the trailer as a file can also benefit from having the trailer available.

Metadata sources
================
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
    * tvdb banner and serie xml: episode titles and summaries, screenshot, posters
    * anidb serie xml:           Serie information, poster
    * Plex theme song:           Serie theme song

Hama creates specific html log files with links to facilitate updating the metadata databases used, for everyone's benefits and even list missing episodes:

- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB posters missing.htm
        - N/A
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB summaries missing.htm
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list anidbid missing.htm
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list studio logos.htm
        - anidbid: <a href='http://anidb.net/perl-bin/animedb.pl?show=anime&aid=266' target='_blank'>266</a> | Title: 'Case Closed' | AniDB and anime-list are both missing the studio<br />
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/anime-list tvdbid missing.htm
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB posters missing.htm
-       - <a href='http://thetvdb.com/wiki/index.php/Posters' target='_blank'>Restrictions</a><br />
-       - no example
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB season posters missing.htm
        - tvdbid: <a href='http://thetvdb.com/?tab=series&id=307112' target='_blank'>307112</a> | Title: 'Hybrid x Heart Magias Academy Ataraxia'
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB summaries missing.htm
<pre><code><a href='http://thetvdb.com/?tab=series&id=101621' target='_blank'>101621</a> missing summaries: ['s0e1', 's0e2', 's0e3', 's0e4', 's0e5', 's0e6', 's0e7', 's0e8', 's0e9', 's0e10', 's0e11', 's0e35', 's1932e0', 's1932e1', 's1932e3', 's1932e4', 's1932e5', 's1932e6', 's1932e7', 's1932e8', 's1932e9', 's1932e10', 's1932e11', 's1933e12', 's1933e13', 's1933e14', 's1933e15', 's1934e1', 's1934e2', 's1934e3', 's1934e6', 's1934e7', 's1934e8', 's1934e9', 's1934e10', 's1934e11', 's1934e12', 's1934e13', 's1935e1', 's1935e2', 's1935e3', 's1935e4', 's1935e5', 's1935e8', 's1935e10', 's1936e2', 's1936e4', 's1936e5', 's1936e6', 's1936e7', 's1936e8', 's1936e11', 's1937e1', 's1937e2', 's1937e9', 's1937e10', 's1937e11', 's1937e12', 's1938e1', 's1938e2', 's1938e3', 's1938e4', 's1938e5', 's1938e6', 's1938e7', 's1938e8', 's1938e9', 's1938e10', 's1938e12', 's1939e3', 's1939e4', 's1939e6']<br />
</code></pre>
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Plex themes missing.htm
        - <a href='https://plexapp.zendesk.com/hc/en-us/articles/201572843' target='_blank'>Restrictions</a><br />
        - tvdbid: <a href='http://thetvdb.com/?tab=series&id=79796' target='_blank'>79796</a> | Title: 'Air Gear' | <a href='mailto:themes@plexapp.com?cc=&subject=Missing%20theme%20song%20-%20&#39;%20-%2079796.mp3&#39;' target='_blank'>Upload</a><br />
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing episodes.htm
        - anidbid: <a href='http://anidb.net/perl-bin/animedb.pl?show=anime&aid=4196' target='_blank'>4196</a> | Title: 'Air Gear' | Missing Episodes: ['s1e1', 's1e2', 's1e3', 's1e4', 's1e5', 's1e6', 's1e7', 's1e8', 's1e9', 's1e10', 's1e11', 's1e12', 's1e13', 's1e14', 's1e15', 's1e16', 's1e17', 's1e18', 's1e19', 's1e20', 's1e21', 's1e22', 's1e23', 's1e24', 's1e25']<br />
        - tvdbid: <a href='http://thetvdb.com/?tab=series&id=78914' target='_blank'>78914</a> | Title: 'Full Metal Panic!' | Missing Episodes: ['s3e1', 's3e2', 's3e3', 's3e4', 's3e5', 's3e6', 's3e7', 's3e8', 's3e9', 's3e10', 's3e11', 's3e12', 's3e13']<br />
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Episode Summaries.htm
        - tvdbid: <a href='http://thetvdb.com/?tab=series&id=81797' target='_blank'>81797</a> | Title: 'One Piece' | Missing Episode Summaries: ['753']<br />  
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Special Summaries.htm
        - tvdbid: <a href='http://thetvdb.com/?tab=series&id=83322' target='_blank'>83322</a> | Title: 'A Certain Magical Index' | Missing Special Summaries: ['s0e1', 's0e2', 's0e3', 's0e4']<br /> 
- [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Missing Specials.htm
        - anidbid: <a href='http://anidb.net/perl-bin/animedb.pl?show=anime&aid=8166' target='_blank'>8166</a> | Title: 'A Bridge to the Starry Skies' | Missing Episodes: ['s0e2', 's0e1', 's0e3', 's0e5', 's0e4', 's0e8', 's0e7', 's0e6', 's0e9']<br />    

I did change the metadata id from the Anidb ID to "anidb-xxxxx" with xxxxx being the anidbid.
You can use anidb.id file in series or Series/Extras folder or in the serie name " [anidb-xxxxx]" at the end of serie folder name, works also for tvdb " [tvdb-xxxxxxx]". Older agents before that need to re-create the library to have a metadata.id beginning with "anidb-"

Agents' update() method is called only when adding new items to your library or when doing a "Force Refresh" or a "Fix Incorrect Match". 

Configuration
=============

Agents settings will have the Metadata source for each field customizable, but not all fields exists on all sources.
Fields shared by both series and episodes can use '|' to split the series from the episode part
Sources are:
- AnimeLists: collections
- 'AniDB'
- 'TheTVDB'
- 'MyAnimeList'
- 'FanartTV'
- 'OMDb': API key in agent settings needed
- 'TheMovieDb'
- 'Plex': themes
- 'AnimeLists'
- 'tvdb4': season posters
- 'TVTunes': themes
- 'Local': collections if grouping folder present

The titles priority can have the usual languages 'en', 'fr', 'sp', 'ja', etc... and the following for asian languages
The titles will be in the priority indicated first and secondarily by the metadata source

<TABLE>
<THEAD>
<TR> <TH> Languages codes       </TH> <TH> AniDB    </TH> <TH> TheTVDB </TH> </TR>
</THEAD>
<TBODY>
<TR> <TD> chinese (unspecified)    </TD> <TD> zh       </TD> <TD> zh   </TD> </TR>
<TR> <TD> chinese (traditional)    </TD> <TD> zh-Hant  </TD> <TD> N/A  </TD> </TR>
<TR> <TD> chinese (simplified)     </TD> <TD> zh-Hans  </TD> <TD> N/A  </TD> </TR>
<TR> <TD> chinese (cantonese)      </TD> <TD> zh-x-yue </TD> <TD> N/A  </TD> </TR>
<TR> <TD> chinese (mandarin)       </TD> <TD> zh-x-cmn </TD> <TD> N/A  </TD> </TR>
<TR> <TD> chinese (taiwanese)      </TD> <TD> zh-x-nan </TD> <TD> N/A  </TD> </TR>
<TR> <TD> japanese                 </TD> <TD> ja       </TD> <TD> ja   </TD> </TR>
<TR> <TD> japanese (transcription) </TD> <TD> jap      </TD> <TD> N/A  </TD> </TR>
<TR> <TD> korean                   </TD> <TD> ko       </TD> <TD> ko   </TD> </TR>
<TR> <TD> korean (transcription)   </TD> <TD> x-kot    </TD> <TD> N/A  </TD> </TR>
</TBODY>
</TABLE>

Installation
============
Get the latest source zip in github release for hama https://github.com/ZeroQI/Hama.bundle > "Clone or download > Download Zip
Folders to copy in Plex main folder:

    * "Scanners"         "Scanners/Series" folder needs creating. Absolute series Scanner.py" goes inside. 
    			 https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/Scanners/Series/Absolute%20Series%20Scanner.py
    * "Plug-ins"         https://github.com/ZeroQI/Hama.bundle > "Clone or download > Download Zip. Copy Hama.bundle-master.zip\Hama.bundle-master in plug-ins folders but rename to "Hama.bundle" (remove -master) 

Here is how to find the plug-in folder location:
https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-

Plex main folder location:

    * '%LOCALAPPDATA%\Plex Media Server\'                                        # Windows Vista/7/8
    * '%USERPROFILE%\Local Settings\Application Data\Plex Media Server\'         # Windows XP, 2003, Home Server
    * '$HOME/Library/Application Support/Plex Media Server/'                     # Mac OS
    * '$PLEX_HOME/Library/Application Support/Plex Media Server/',               # Linux
    * '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/', # Debian,Fedora,CentOS,Ubuntu
    * '/var/lib/plex/Plex Media Server/',                                        # Arch
    * '/usr/local/plexdata/Plex Media Server/',                                  # FreeBSD
    * '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/',              # FreeNAS
    * '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/',                         # FreeNAS
    * '/c/.plex/Library/Application Support/Plex Media Server/',                 # ReadyNAS
    * '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/',        # QNAP
    * '/volume1/Plex/Library/Application Support/Plex Media Server/',            # Synology, Asustor
    * '/raid0/data/module/Plex/sys/Plex Media Server/',                          # Thecus
    * '/raid0/data/PLEX_CONFIG/Plex Media Server/'                               # Thecus Plex community    

Hama auto-creates some folders in the agent data folder ("Plug-In Support/Data/com.plexapp.agents.hama/DataItems")
- "Logs"
- "AniDB"
- "Plex"
- "OMDB"
- "TMDB"
- "TheTVDB"
- "TheTVDB/banner/graphical"
- "TVDB/episodes"
- "TVDB/fanart/original"
- "TVDB/json"
- "TVDB/posters"
- "TVDB/seasons"
- "FanartTV"

Agents can only write data in data folder as binary objects or as dictionaries, but cannot create folders normally (worked  around now).
Any folder missing will crash the agent when an attempt to write inside is done. That is a Framework issue, all attemps are in try/except structure, to no avail...

I use these folders to cache all pictures, theme songs, since they are not cached by Plex.
This way, even if you recreate the whole Plex anime folder entry, you do not have to download the same file again.

Specific instal procedures go in the wiki:
- Ubuntu Server 16.04: https://github.com/ZeroQI/Hama.bundle/wiki/Installing-Hama-and-ASS-on-Ubuntu

Install issue under linux are generally permission issues...
- OpenMediaVault (Debian): "sudo chmod 775 -R /var/lib/plexmediaserver"
- Synology:"chown -R plex:users" + "chmod -R 700"
- FREENAS: chmod -R 777 /var/db/plexdata/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/. 
- if having: File "bundles-release/Framework.bundle-dist/Contents/Resources/Versions/2/Python/Framework/components/storage.py", line 81, in save IOError: [Errno 13] Permission denied: '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/._StoredValues'

touch /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/._StoredValues
chmod 777 /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/._StoredValues
chown plex:plex /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/._StoredValues
service plexmediaserver restart

    
Updating:
=========
If no folder in data was created or data moved there and no new option was added to the agent settings, it will work.

    * Update scanner file with the latest from https://github.com/ZeroQI/Absolute-Series-Scanner/blob/master/Scanners/Series/Absolute%20Series%20Scanner.py
    * replace agent "_ _init_ _.py" with the latest from https://github.com/ZeroQI/Hama.bundle/blob/master/Contents/Code/__init__.py
    * replace agent "DefaultPrefs.json" with the latest from https://github.com/ZeroQI/Hama.bundle/blob/master/Contents/DefaultPrefs.json
    
If it doesn't, get latest zip and start from scratch, but no need to delete "Plug-in Support" folder

After restarting Plex servers, the new agent will be loaded and you will find all agents settings in the official framework agent settings window:

    * "Plex > Settings > Server > Agents > TV Shows > HamaTV > Agent settings"

Troubleshooting:
================
If you ask for something already answered in the readme, or post scanner issues on the agent page or vice-versa, please donate (will be refered to as the RTFM tax)

If files and series are showing in Plex GUI with the right season, the scanner did its job
If you miss metadata (serie title wrong, no posters, summary, wrong episode title or summaries, ep screenshot, etc...), that is the Agent doing.

If posters are missing, check that all the data folders are created and logs show no right issue.
If subtitles are not loaded, check Settings > Server > Agents > Shows > HamaTV and please tick the "Local Media Assets (TV)" as is not by default.

To avoid already solved issues, and make sure you do include all relevant logs in one go, please do the following:
- delete the library
- stop plex
- Update to the latest Absolute Series Scanner (master branch), Hama (Master branch) and Plex
- deleting all Plex logs leaving folders intact
- restart Plex
- re-create the library
- including all the following logs: (location: https://support.plex.tv/hc/en-us/articles/200250417-Plex-Media-Server-Log-Files)
   - [...]/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.hama.log (Agent logs)
   - [...]/Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.system.log (show why the agent cannot launch)
   - [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/_Logs/root_folder.filelist.log (episodes info)
   - [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/_Logs/root_folder.scanner.log (episodes info)
   - [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/_Logs/root_folder.agent-search.log (guid assignment)
   - [...]/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/_Logs/root_folder.agent-update.log (metadata update)
   - Screen capture to illustrate if needed. Above logs are still mandatory

Support thread for agent:
- https://github.com/ZeroQI/Hama.bundle/issues (proven or confident enough it's a bug. Include the library name, the symptoms, the logs mentionned above)
- https://forums.plex.tv/discussion/77636/release-http-anidb-metadata-agent-hama#latest (not sure if bug, if bug will create a gihub issue ticket)

Bugs Fixes
==========
- [ ] https://github.com/ZeroQI/Hama.bundle/issues/245 Anidb poster priority to fix

Feature Requests: ([X] to be included in next version)
=================
- [ ] Package of Studio Logos. Wiki link https://github.com/ZeroQI/Hama.bundle/wiki/Plex-Studio-Icons.
- [ ] Package of 30s long Theme Songs, local loading works, name convention: Data/com.plexapp.agents.hama/DataItems/Plex/anidbid.mp3
- [ ] Any ideas ?

Note:
- [X] to be included in next version
- items removed from list once resolved in current code
- [Donation link](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=S8CUKCX4CWBBG&lc=IE&item_name=ZeroQI&item_number=Absolute%20Series%20Scanner%20%2b%20Http%20AniDB%20Metadata%20Agent&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)
