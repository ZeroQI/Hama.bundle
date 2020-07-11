### anilist.co ###
# API exemple:  https://anilist.co/graphiql?query=%7B%0A%20%20anime%3A%20Media(idMal%3A%2023273%2C%20type%3A%20ANIME)%20%7B%0A%20%20%20%20title%20%7B%0A%20%20%20%20%20%20english%0A%20%20%20%20%7D%0A%20%20%20%20coverImage%20%7B%0A%20%20%20%20%20%20url%3A%20extraLarge%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A

### Imports ###
# Python Modules #
import os
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict # Direct import of heavily used functions

### Variables ###
ARM_SERVER_URL = "https://relations.yuna.moe/api/ids?source=anidb&id={id}"

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
def GetAniListIdFromAniDbId(AniDBid):
  try:
    response = JSON.ObjectFromURL(ARM_SERVER_URL.format(id=AniDBid), cacheTime=CACHE_1WEEK)

    return Dict(response, "anilist", default=None)
  except Exception:
    return None

def MakeGraphqlQuery(document, variables):
  Log.Info("Making AniList GraphQL Query:\nQuery\n{}\nVariables: {}".format(document, variables))

  try:
    response = HTTP.Request(
      GRAPHQL_API_URL,
      method="POST",
      data=JSON.StringFromObject({
        "query": document,
        "variables": variables
      }),
      headers=common.COMMON_HEADERS,
      cacheTime=CACHE_1DAY,
      immediate=True
    )
    body = JSON.ObjectFromString(response.content)
  except Exception:
    return None

  if 'errors' in body and len(body.errors) > 0:
    Log.Error("Got error: {}".format(body.errors[0].message))
    return None

  return Dict(body, "data")

def GetMetadata(AniDBid, MALid):
  Log.Info("=== AniList.GetMetadata() ===".ljust(157, '='))
  AniList_dict = {}

  # Try to match the AniDB id to an AniList id as it has a higher chance of being correct
  ALid = GetAniListIdFromAniDbId(AniDBid)
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
      Log.Info("[ ] poster: {}".format(SaveDict((os.path.join('AniList', 'poster',  os.path.basename(posterUrl)), common.poster_rank('AniList', 'posters'), None), AniList_dict, 'posters', posterUrl)))

    bannerUrl = Dict(data, "anime", "bannerImage")
    if bannerUrl:
      Log.Info("[ ] banner: {}".format(SaveDict((os.path.join('AniList', 'banners', os.path.basename(bannerUrl)), common.poster_rank('AniList', 'banners'), None), AniList_dict, 'banners', bannerUrl)))

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info("AniList_dict: {}".format(DictString(AniList_dict, 4)))
  return AniList_dict
