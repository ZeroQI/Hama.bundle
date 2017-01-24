### OMDB - Fetch the IMDB poster using imdbd on OMDB HTTP API ###  return 200 but not downloaded correctly - IMDB has a single poster, downloading through OMDB xml, prefered by mapping file

###  ###
def omdb_poster(metadata, imdbid_multiple, num=98):
  OMDB_HTTP_API_URL = "http://www.omdbapi.com/?i="
  if Prefs["GetOmdbPoster"] and imdbid.startswith("tt"):
    Log.Info("OMDB - background, Poster - imdbid: '%s'" % imdbid)
    for imdbid in imdbid_multiple.split(","):
      Log.Info("imdbid: '%s', url: '%s', filename: '%s'" % (imdbid, OMDB_HTTP_API_URL + imdbid, "OMDB/%s.jpg" % imdbid))
      try:                   OMDB = common.get_json(OMDB_HTTP_API_URL + imdbid, cache_time=CACHE_1WEEK * 56)
      except Exception as e: Log.Error("Exception - imdbid: '%s', url: '%s', filename: '%s', Exception: '%s'" % (imdbid, OMDB_HTTP_API_URL + imdbid, "OMDB/%s.jpg" % imdbid, e))
      else:
        if OMDB and 'Poster' in OMDB and OMDB['Poster'] not in ("N/A", "", None):  common.metadata_download (metadata.posters, OMDB['Poster'], num, "OMDB/%s.jpg" % imdbid)
        else:                                                                      Log.Info("No poster to download - " + OMDB_HTTP_API_URL + imdbid)
