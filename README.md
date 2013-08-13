HTTP Anidb Metadata Agent (HAMA) v0.4 for plex By Atomicstrawberry
Forked since v0.4 by ZeroQI

Here are the changes since v0.4:

New features
   . Search part entirely local (anime-titles.xml file located in Hama.bundle\Contents\Resources)
   . Matching the theTVDB.com ID from the AniDB.net ID through mapping file (anime-list-full.xml located in Hama.bundle\Contents\Resources)
   . using Studio from mapping file as often missing from AniDB.net
   . Episode summary downloaded from theTVDB.com in english only using the AniDB.net to TheTVDB.com
   . Separate language order selection for the serie name and episode titles
   . TheTVDB.com episode link integrated in summary. working on serie link and anidb links now
 
Improvements
   . Changed theTVDB.com picture function to reflect how the XML behaves, removing most un-necessary "thumbnail not available" logs.
   . Changed theTVDB.com picture function to put season posters on seasons only
   . Reduced the number of functions: searchByName and parseAnimeXml are directly called by the agent now
   . Commented source code. I believe it to be hightly readable under notepad now
   . Normalised Logging, we can now see all files skipped and all cached queries, there should be the extreme minimum network request possible...
   . imported movie bolean from AniDB.net xml
   . Commented some file formats in the source for clarity when reading
 
Bugs
   . Anidb poster no longer downloading systematically
   . Changed DefaultPrefs.json (couldn't open settings)
