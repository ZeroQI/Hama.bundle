import urllib
import json

def compute_integer_scores_for_vector_search(items):
  sorted_items = sorted(items, key=lambda item: item['score'], reverse=True)
  previous_score = 101
  for item in sorted_items:
    raw_score = int(round(item['score'] * 100))

    if raw_score >= previous_score:
      # Reduce down to previous score less 1 if collision or higher
      raw_score = previous_score - 1

    item['score'] = raw_score
    previous_score = raw_score
  
  return sorted_items

def get_results_from_vector_search(orig_title):
  api_url = "%s?name=%s" % (Prefs["vector_search_api"], urllib.quote(orig_title))
  
  try:
    response = HTTP.Request(api_url, cacheTime=CACHE_1DAY).content
    response_dict = json.loads(response)
    return compute_integer_scores_for_vector_search(response_dict)
  except Exception as e:
    Log.Debug("Got issue querying vector search API: " + str(e))
    return None