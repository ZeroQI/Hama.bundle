### anilist.co ###
# API exemple:  https://anilist.co/graphiql?query=%7B%0A%20%20anime%3A%20Media(idMal%3A%2023273%2C%20type%3A%20ANIME)%20%7B%0A%20%20%20%20title%20%7B%0A%20%20%20%20%20%20english%0A%20%20%20%20%7D%0A%20%20%20%20coverImage%20%7B%0A%20%20%20%20%20%20url%3A%20extraLarge%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A

### Imports ###
# Python Modules #
import os
# HAMA Modules #
import common
from common import Log, DictString, Dict, SaveDict

### Variables ###
GRAPHQL_API_URL = "https://graphql.anilist.co"
COVER_IMAGE_DOCUMENT = """
query($malId: Int!) {
  anime: Media(type: ANIME, idMal: $malId) {
    coverImage {
      url: extraLarge
    }
    bannerImage
  }
}
"""

def MakeGraphqlQuery(document, variables):
  headers = {
    'Accepts': '*/*',
    'Accept-Encoding': 'identity',
    'Content-Type': 'application/json',
  }
  Log.Info("Making AniList GraphQL Query:\nQuery\n{}\nVariables: {}".format(document, variables))
  response = HTTP.Request(
    GRAPHQL_API_URL,
    method="POST",
    data=JSON.StringFromObject({
      "query": document,
      "variables": variables
    }),
    headers=headers,
    cacheTime=CACHE_1DAY,
    immediate=True
  )
  body = JSON.ObjectFromString(response.content)

  Log.Info(response.content)
  if 'errors' in body and len(body.errors) > 0:
    Log.Error("Got error: {}".format(body.errors[0].message))
    return None

  return Dict(body, "data")

### Functions ###
def GetMetadata(MALid):
  Log.Info("=== AniList.GetMetadata() ===".ljust(157, '='))
  AniList_dict = {
    'posters': [],
    'banners': []
  }

  Log.Info("MALid: '%s'" % MALid)
  if not MALid or not MALid.isdigit(): return AniList_dict

  Log.Info("--- series ---".ljust(157, "-"))
  data = MakeGraphqlQuery(COVER_IMAGE_DOCUMENT, {
    "malId": int(MALid)
  })

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
