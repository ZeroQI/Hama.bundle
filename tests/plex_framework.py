# -*- coding: utf-8 -*-
''' Stand-ins for the parts of the Plex plug-in framework that HAMA uses, so its modules run outside Plex.
    Network calls fail on purpose: the tests must not depend on AniDB, TheTVDB or TheMovieDb being up.
'''
import __builtin__
import imp
import logging
import logging.handlers  # The framework imports it, and common.PlexLog.Open() uses it
import os
import re
import string
import sys
import tempfile
import threading
import unicodedata

reload(sys)
sys.setdefaultencoding('utf-8')  # As the framework's bootstrap.py does

### Framework/utils.py ###
def clean_up_string(s):
  s = unicode(s).replace('&', 'and')
  s = re.sub('[' + string.punctuation + ']', '', s).lower()
  s = re.sub('^(the|a) ', '', s)
  return re.sub('[ ]+', ' ', s).strip()

def longest_common_substring(first, second):
  S, T = clean_up_string(first), clean_up_string(second)
  L, LCS, longest = [[0] * (len(T)+1) for i in xrange(len(S)+1)], set(), 0
  for i in xrange(len(S)):
    for j in xrange(len(T)):
      if S[i] == T[j]:
        v = L[i+1][j+1] = L[i][j] + 1
        if v > longest:   longest, LCS = v, set()
        if v == longest:  LCS.add(S[i-v+1:i+1])
  return LCS.pop() if LCS else ''

def levenshtein_distance(first, second):
  first, second = clean_up_string(first), clean_up_string(second)
  if len(first) > len(second):  first, second = second, first
  if not second:                return len(first)
  previous = range(len(second)+1)
  for i, a in enumerate(first, 1):
    current = [i]
    for j, b in enumerate(second, 1):  current.append(min(current[j-1]+1, previous[j]+1, previous[j-1]+(a != b)))
    previous = current
  return previous[-1]

### Framework API objects ###
class String(object):
  def StripDiacritics(self, s):                return unicodedata.normalize('NFKD', unicode(s).replace(u'ß', u'ss').replace(u'ẞ', u'SS')).encode('ASCII', 'ignore')
  def LongestCommonSubstring(self, first, second):  return longest_common_substring(first, second)

class Util(object):
  def LevenshteinDistance(self, first, second):   return levenshtein_distance(first, second)

class MetadataSearchResult(object):
  def __init__(self, id, name=None, year=None, score=0, lang=None, thumb=None):
    self.id, self.name, self.year, self.score, self.lang, self.thumb = id, name, year, score, lang, thumb

class Offline(object):
  ''' HTTP, XML and JSON: any call raises, as a network error would '''
  def __init__(self, name):  self.name = name
  def __getattr__(self, attr):
    def call(*args, **kwargs):  raise IOError("{}.{}() is not available in tests".format(self.name, attr))
    return call

class Agent(object):
  TV_Shows = Movies = object

class Locale(object):
  class Language(object):
    English = 'en'

class Core(object):
  app_support_path = tempfile.mkdtemp(prefix='hama-tests-')  # HAMA writes its logs below this

class Thread(object):
  Lock = staticmethod(threading.Lock)

### Code loading ###
class CodeImporter(object):
  ''' Imports Contents/Code modules as the framework does: as UTF-8 source, which plain Python 2 refuses without a coding line (TheMovieDb.py has none) '''
  def __init__(self, code):  self.code = code
  def find_module(self, name, path=None):
    return self if '.' not in name and os.path.isfile(os.path.join(self.code, name + '.py')) else None
  def load_module(self, name):
    return sys.modules[name] if name in sys.modules else load(name, name + '.py')

def load(name, filename):
  path   = os.path.join(CODE, filename)
  source = open(path, 'rb').read()
  try:                 code = compile(source, path, 'exec')
  except SyntaxError:  code = compile(source.decode('utf-8'), path, 'exec')
  module = sys.modules[name] = imp.new_module(name)
  module.__file__ = path
  try:     exec code in module.__dict__
  except:  del sys.modules[name];  raise
  return module

CODE = None

def install(code):
  global CODE
  CODE = code
  sys.meta_path.insert(0, CodeImporter(code))
  for name, value in dict(String=String(), Util=Util(), MetadataSearchResult=MetadataSearchResult, Agent=Agent, Locale=Locale, Core=Core, Thread=Thread,
                          HTTP=Offline('HTTP'), XML=Offline('XML'), JSON=Offline('JSON'), Prefs={},
                          CACHE_1MINUTE=60, CACHE_1HOUR=3600, CACHE_1DAY=86400, CACHE_1WEEK=604800, CACHE_1MONTH=2592000).items():
    setattr(__builtin__, name, value)
