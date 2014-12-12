from pylons import config

from geomet import wkt
import json
import feedparser
from dateutil import tz
from time import mktime
import datetime
from datetime import datetime as date_parse
import dateutil
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

def get_time_period():
   return lists.TIME_PERIODS

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

def date_to_iso(value, temp_res):
   result = ''
   result = dateutil.parser.parse(value).isoformat().split('T')[0]
   if temp_res == u'month':
      result = result.split('-')[0] + result.split('-')[1]
   elif temp_res == u'year' or temp_res == u'decade' or temp_res == u'century':
      result = result.split('-')[0]
   return result

def get_default_slider_values():
   data_dict = {
         'sort': 'start_time asc',
         'rows': 1,
          'q': 'start_time:[* TO *]',
   }
   result = p.toolkit.get_action('package_search')({}, data_dict)['results']
   if len(result) == 1:
      date = filter(lambda x: x['key'] == 'start_time',
            result[0].get('extras', []))
      begin = dateutil.parser.parse(date[0]['value']).isoformat().split('T')[0]
   else:
      begin = datetime.date.today().isoformat()
   
   data_dict = {
            'sort': 'end_time desc',
            'rows': 1,
            'q': 'end_time:[* TO *]',
   }
   result = p.toolkit.get_action('package_search')({}, data_dict)['results']
   if len(result) == 1:
      date = filter(lambda x: x['key'] == 'end_time',
            result[0].get('extras', []))
      end = dateutil.parser.parse(date[0]['value']).isoformat().split('T')[0]
   else:
      end = datetime.date.today().isoformat()
   return begin, end

def get_date_url_param():
   params = ['', '']
   for k, v in p.toolkit.request.params.items():
      if k == 'ext_begin_date':
         params[0] = v
      elif k == 'ext_end_date':
         params[1] = v
      else:
         continue
   return params
