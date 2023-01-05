### anilist.co ###
# API exemple:  https://anilist.co/graphiql?query=%7B%0A%20%20anime%3A%20Media(idMal%3A%2023273%2C%20type%3A%20ANIME)%20%7B%0A%20%20%20%20title%20%7B%0A%20%20%20%20%20%20english%0A%20%20%20%20%7D%0A%20%20%20%20coverImage%20%7B%0A%20%20%20%20%20%20url%3A%20extraLarge%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A

### Imports ###
# Python Modules #
import os
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###
ARM_SERVER_URL = "https://arm.haglund.dev/api/v2/ids?source=anidb&include=anilist,myanimelist&id={id}"

GRAPHQL_API_URL = "https://graphql.anilist.co"
ANIME_DATA_DOCUMENT = """
query($id: Int, $malId: Int) {
  anime: Media(type: ANIME, id: $id, idMal: $malId) {
    coverImage {
      url: extraLarge
    }
    bannerImage
  }
}
""".strip()

### Functions ###
def MakeGraphqlQuery(document, variables):
  Log.Info("Query: {}".format(document))
  Log.Info("Variables: {}".format(variables))

  source   = variables.keys()[0]
  data     = JSON.StringFromObject({"query": document, "variables": variables})
  response = common.LoadFile(filename=str(variables[source])+'.json', relativeDirectory=os.path.join('AniList', 'json', source), url=GRAPHQL_API_URL, data=data, cache=CACHE_1DAY)

  # EX: {"data":null,"errors":[{"message":"Not Found.","hint":"Use POST request to access graphql subdomain.","status":404}]}
  if len(Dict(response, 'errors', default=[])) > 0:
    Log.Error("Got error: {}".format(Dict(response, 'errors')[0]))
    return None

  return Dict(response, "data")

def GetMetadata(AniDBid, MALid):
  Log.Info("=== AniList.GetMetadata() ===".ljust(157, '='))
  AniList_dict = {}

  # Try to match the AniDB id to an AniList id as it has a higher chance of being correct
  ALid = Dict(common.LoadFile(filename=AniDBid+'.json', relativeDirectory=os.path.join('AniList', 'json', 'AniDBid'), url=ARM_SERVER_URL.format(id=AniDBid)), "anilist", default=None)

  Log.Info("AniDBid={}, MALid={}, ALid={}".format(AniDBid, MALid, ALid))
  if not MALid or not MALid.isdigit(): return AniList_dict

  Log.Info("--- series ---".ljust(157, "-"))

  # Use the AniList id if we got one, but fall back to the MAL id
  variables = {}
  if ALid is not None:  SaveDict(ALid,       variables, "id"   )
  else:                 SaveDict(int(MALid), variables, "malId")

  # Fetch data
  data = MakeGraphqlQuery(ANIME_DATA_DOCUMENT, variables)

  if data:
    Log.Info("--- images ---".ljust(157, "-"))

    posterUrl = Dict(data, "anime", "coverImage", "url")
    if posterUrl:
      Log.Info("[ ] poster: {}".format(posterUrl)); SaveDict((os.path.join('AniList', 'poster',  os.path.basename(posterUrl)), common.poster_rank('AniList', 'posters'), None), AniList_dict, 'posters', posterUrl)

    bannerUrl = Dict(data, "anime", "bannerImage")
    if bannerUrl:
      Log.Info("[ ] banner: {}".format(bannerUrl)); SaveDict((os.path.join('AniList', 'banners', os.path.basename(bannerUrl)), common.poster_rank('AniList', 'banners'), None), AniList_dict, 'banners', bannerUrl)

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("AniList_dict: {}".format(DictString(AniList_dict, 4)))
  return AniList_dict
