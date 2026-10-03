# -*- coding: utf-8 -*-
''' Offline tests of HAMA's search, run outside Plex:  python -m unittest discover -s tests -v
    Needs Python 2.7 and lxml, as Plex's plug-in framework has. tests/data holds small extracts of the AniDB titles and Anime-Lists files.
'''
import os
import unittest

import plex_framework

CODE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Contents', 'Code')
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
plex_framework.install(CODE)

from lxml import etree
import AniDB
import AnimeLists
import TheTVDBv2
import TheTVDBv4
hama = plex_framework.load('hama', '__init__.py')

AniDB.AniDBTitlesDB     = etree.parse(os.path.join(DATA, 'anime-titles.xml')).getroot()
AnimeLists.AniDBTVDBMap = etree.parse(os.path.join(DATA, 'anime-list-master.xml')).getroot()

class Results(list):
  ''' The search results container Plex passes to an agent '''
  def Append(self, result):  self.append(result)

class Media(object):
  ''' What Plex passes to a TV show search: the folder title, and seasons > episodes > items > parts > file '''
  def __init__(self, show, seasons):
    self.show = self.title = self.name = show
    self.year = self.filename = None
    part, item, episode, season = type('Part', (), {})(), type('Item', (), {})(), type('Episode', (), {})(), type('Season', (), {})()
    part.file, item.parts, episode.items, season.episodes = os.path.join(os.sep, 'tv', show, 'episode.mkv'), [part], [item], {'1': episode}
    self.seasons = dict((str(number), season) for number in seasons)

def search(show, seasons, module=hama):
  results = Results()
  module.Search(results, Media(show, seasons), 'en', False, False)
  return sorted(results, key=lambda result: -result.score)

class TestImports(unittest.TestCase):
  def test_every_module_imports(self):
    for filename in sorted(os.listdir(CODE)):
      if filename.endswith('.py') and filename != '__init__.py':  __import__(filename[:-3])

class TestSearch(unittest.TestCase):
  def test_forced_id_in_folder_name(self):
    top = search('Sousou no Frieren [tvdb-424536]', [2])[0]
    self.assertEqual((top.id, top.score), ('tvdb-424536', 100))

  def test_season_1_folder_matches_anidb(self):
    top = search('Sousou no Frieren', [1])[0]
    self.assertEqual((top.id, top.score), ('anidb-17617', 100))

  def test_tvdb_search_in_use_has_an_api_key(self):
    ''' #610: Search() called TheTVDBv4 while its API key was still 'TODO', so every TVDB call failed '''
    called, original = [], (TheTVDBv2.Search, TheTVDBv4.Search)
    TheTVDBv2.Search = lambda *args: called.append(TheTVDBv2) or 0
    TheTVDBv4.Search = lambda *args: called.append(TheTVDBv4) or 0
    try:      search('Sousou no Frieren', [2])
    finally:  TheTVDBv2.Search, TheTVDBv4.Search = original
    self.assertEqual(len(called), 1)
    self.assertNotIn(called[0].TVDB_API_KEY, ('', 'TODO'), '{} is used for TVDB search but has no API key'.format(called[0].__name__))

  def test_later_season_folder_matches_tvdb_through_anidb_titles(self):
    ''' #609: TheTVDB has no title search any more, so a season 2+ folder is matched through the AniDB titles '''
    for show, season, tvdbid in (('Sousou no Frieren', 2, '424536'), ('Oshi no Ko', 3, '421069'), ('Re ZERO Starting Life in Another World 2016', 4, '305089')):
      results = search(show, [season], TheTVDBv2)
      self.assertTrue(results, show)
      self.assertEqual(results[0].id, 'tvdb-' + tvdbid, show)

  def test_season_1_folder_gets_no_tvdb_results(self):
    ''' AniDB.Search() already searched the same titles for it, with AniDB numbering '''
    self.assertEqual(search('Sousou no Frieren', [1], TheTVDBv2), [])

if __name__ == '__main__':
  unittest.main()
