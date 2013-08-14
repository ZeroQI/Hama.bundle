HTTP Anidb Metadata Agent (HAMA)
================================
Created By Atomicstrawberry and maintained until v0.4 <br />
<UL>
 <LI>http://forums.plexapp.com/index.php/topic/66918-release-http-anidb-metadata-agent-hama/</LI>
</UL>
Forked from v0.4 and maintained since by ZeroQI <br />
 <br />
Here are the changes since v0.4:<BR />

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

ScudLee mapping files
=====================
 <TABLE>
 <TR> <TD> <B>Source</B></TD> <TD>Git Dev repository: https://github.com/ScudLee/anime-lists <BR />
                             Dev Forum thread:   http://forum.xbmc.org/showthread.php?tid=142835 - XBMC Anidb.net MOD plugin</TD> </TR>
 <TR> <TD><B>anime-list-todo.xml</B></TD> <TD>This is a list of shows that don't yet have a mapping.
                              In a lot of cases they just need the tvdbid and defaulttvdbseason (and/or imdbid/tmdbid). 
                              More complicated ones may need individual episode mappings (particularly for OVAs linked to TV series).
                              Some of the shows are deliberately left out because the episodes were a mess on thetvdb when I looked,
                              but they may have been fixed since then (the scraper should still manage to find artwork without a mapping).</TD> </TR>
 <TR> <TD> <B>anime-list-unknown.xml</B></TD> <TD>This is a list of shows he couldn't find on thetvdb when he looked for them.</TD> </TR>
 <TR> <TD><B>anime-movieset-list.xml</B></TD> <TD>Still needs a lot of work. The format should be fairly obvious. 
                              "Official" collection titles for languages other than English need to be added...
                              Hentai titles are almost entirely missing...
                              Any recent movies/OVAs might be missing (he wrote the list a while back, and only did a minor update before posting it)...</TD> </TR>
 <TR> <TD><B>Help the XML get updated?</B></TD> <TD>http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010 <BR />
                              if you do one or two shows, PM (ScudLee), so as not to flood the thread with posts. 
                              if you do a whole batch, post it in the thread link indicated above. 
                              If you're familiar with Git and GitHub, 1) you can also clone ScudLee repo [https://github.com/ScudLee/anime-lists], edit your copy of anime-list-master.xml directly. 
                              and then make a Pull Request (@vaneska does it this way). That simplifies things greatly for me, but is a bit technical</TD> </TR>
 </TABLE>

I recommend an absolut mode scanner to match the AniDB episod numbering (no season, unlike TVDB) <BR />
Better ABsolute Scanner (BABS): http://forums.plexapp.com/index.php/topic/31081-better-absolute-scanner-babs/
