HTTP Anidb Metadata Agent (HAMA)
================================
Created By Atomicstrawberry and maintained until v0.4
Forked from v0.4 and maintained since by ZeroQI

Here are the changes since v0.4:<BR />

New features
<UL>
   <LI> Search part entirely local (anime-titles.xml file located in Hama.bundle\Contents\Resources)
   <LI> Matching the theTVDB.com ID from the AniDB.net ID through mapping file (anime-list-full.xml located in Hama.bundle\Contents\Resources)
   <LI> using Studio from mapping file as often missing from AniDB.net
   <LI> Episode summary downloaded from theTVDB.com in english only using the AniDB.net to TheTVDB.com
   <LI> Separate language order selection for the serie name and episode titles
   <LI> TheTVDB.com episode link integrated in summary. working on serie link and anidb links now
</UL>

Improvements
<UL>
   <LI> Changed theTVDB.com picture function to reflect how the XML behaves, removing most un-necessary "thumbnail not available" logs.
   <LI> Changed theTVDB.com picture function to put season posters on seasons only
   <LI> Reduced the number of functions: searchByName and parseAnimeXml are directly called by the agent now
   <LI> Commented source code. I believe it to be hightly readable under notepad now
   <LI> Normalised Logging, we can now see all files skipped and all cached queries, there should be the extreme minimum network request possible...
   <LI> imported movie bolean from AniDB.net xml
   <LI> Commented some file formats in the source for clarity when reading
</UL>

Bugs resolved
<UL>
   <LI> Anidb poster no longer downloading systematically
   <LI> Changed DefaultPrefs.json (couldn't open settings)
</UL>
