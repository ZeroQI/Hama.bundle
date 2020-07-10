### anilist.co ###
# API exemple:  https://anilist.co/graphiql?query=%7B%0A%20%20anime%3A%20Media(idMal%3A%2023273%2C%20type%3A%20ANIME)%20%7B%0A%20%20%20%20title%20%7B%0A%20%20%20%20%20%20english%0A%20%20%20%20%7D%0A%20%20%20%20coverImage%20%7B%0A%20%20%20%20%20%20url%3A%20extraLarge%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A

### Imports ###
# Python Modules #
import os
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict

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
      # Need Content-Type, the others might be unnecessary
      headers={'Content-Type': 'application/json'},
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

### Functions ###
def GetMetadata(AniDBid, MALid):
  Log.Info("=== AniList.GetMetadata() ===".ljust(157, '='))
  AniList_dict = {
    'posters': [],
    'banners': []
  }

  # Try to match the AniDB id to an AniList id as it has a higher chance of being correct
  ALid = GetAniListIdFromAniDbId(AniDBid)
  Log.Info("AniDBid={}, MALid={}, ALid={}".format(AniDBid, MALid, ALid))
  if not MALid or not MALid.isdigit(): return AniList_dict

  Log.Info("--- series ---".ljust(157, "-"))

  # Use the AniList id if we got one, but fall back to the MAL id
  if ALid is not None:
    variables = {
      "id": ALid
    }
  else:
    variables = {
      "malId": int(MALid)
    }

  # Fetch data
  data = MakeGraphqlQuery(ANIME_DATA_DOCUMENT, variables)

  if not data:
    return AniList_dict

  posterUrl = data["anime"]["coverImage"]["url"]
  posterPath = os.path.join('AniList', 'poster', posterUrl.split("/")[-1:][0])
  bannerUrl = data["anime"]["bannerImage"]
  bannerPath = os.path.join('AniList', 'banners', bannerUrl.split("/")[-1:][0])

  AniList_dict['posters'] = {
    posterUrl: (posterPath, common.poster_rank('AniList', 'posters'), None)
  }
  AniList_dict['banners'] = {
    bannerUrl: (bannerPath, common.poster_rank('AniList', 'banners'), None)
  }

  Log.Info("--- return ---".ljust(157, '-'))
  Log.Info(DictString(AniList_dict, 4))
  return AniList_dict
