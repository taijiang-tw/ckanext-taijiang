from pylons import config

from geomet import wkt
import json
import feedparser
from dateutil import tz
from time import mktime
from datetime import datetime as date_parse
import ckan.model as model # get_licenses should be in core

import ckan.plugins as p
import ckan.lib.helpers as helpers
import ckan.lib.formatters as formatters

import ckanext.taijiang.lists as lists


def get_data_types():
   return lists.DATA_TYPES

def get_languages():
   return lists.LANGUAGES

def get_encodings():
   return lists.ENCODINGS

def get_theme_keywords():
   return lists.THEME_KEYWORDS

def get_loc_keyword():
   return lists.LOC_KEYWORDS

def get_temp_res():
   return lists.TEMP_RES

def get_proj():
   return lists.PROJS

def extras_to_dict(pkg):
   extras_dict = {}
   if pkg and 'extras' in pkg:
       for extra in pkg['extras']:
            extras_dict[extra['key']] = extra['value']
   return extras_dict

def geojson_to_wkt(value):
   return wkt.dumps(json.loads(value))

def get_newsfeed(feed_url, truncate=3):
   news_dict = []
   rss_feed = feedparser.parse(feed_url)
   for entry in rss_feed.entries:
      updated_time = date_parse.fromtimestamp(mktime(entry.updated_parsed))
      updated_time = updated_time.replace(tzinfo=tz.tzutc())
      updated_time = updated_time.astimezone(tz.tzlocal()).strftime('%Y-%m-%d')
      news_dict.append({'title': entry.title,
            'description': entry.description.replace('[&#8230;]', '...'),
            'link': entry.link,
            'updated_time': updated_time})
   return news_dict[:truncate]
