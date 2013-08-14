HTTP Anidb Metadata Agent (HAMA)
================================
Created By Atomicstrawberry and maintained until v0.4 <br />
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
