from pylons import config
import ckan.plugins as p
from ckan.common import json
from geomet import wkt
import re
import logging
import dateutil
from datetime import date

log = logging.getLogger(__name__)


def extras_to_dict(pkg):
   extras_dict = {}
   if pkg and 'extras' in pkg:
       for extra in pkg['extras']:
            extras_dict[extra['key']] = extra['value']
   return extras_dict

def geojson_to_wkt(value):
   return wkt.dumps(json.loads(value))

def latest_news(truncate=2):
   return p.toolkit.get_action('ckanext_pages_list')(None, {'private': False})[::-1][:truncate]

def date_to_iso(value, temp_res=None):
   result = ''
   result = dateutil.parser.parse(value).isoformat().split('T')[0]
   if temp_res is not None:
      if temp_res == u'month':
         result = result.split('-')[0] + '-' + result.split('-')[1]
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
      start_time = result[0].get('start_time')
      begin = dateutil.parser.parse(start_time).isoformat().split('T')[0]
   else:
      begin = date.today().isoformat()
   
   data_dict = {
            'sort': 'end_time desc',
            'rows': 1,
            'q': 'end_time:[* TO *]',
   }
   result = p.toolkit.get_action('package_search')({}, data_dict)['results']
   if len(result) == 1:
      end_time = result[0].get('end_time')
      end = dateutil.parser.parse(end_time).isoformat().split('T')[0]
   else:
      end = date.today().isoformat()
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

def get_field_choices(dataset_type):
   from ckanext.scheming import helpers as scheming_helpers
   schema = scheming_helpers.scheming_get_dataset_schema(dataset_type)
   fields = dict()
   for field in schema['dataset_fields']:
      if field.get('choices'):
         choices_new = dict()
         for choice in field.get('choices'):
            choices_new[choice['value']] = choice['label']['zh_TW'] if isinstance(choice['label'], dict) else choice['label']
         fields[field['field_name']] = choices_new
   return fields

def get_time_period():
   time_period_dict = get_field_choices('dataset')['time_period']
   time_period_list = []
   for value, label in time_period_dict.iteritems():
      splitted = re.split(r'[-()]', label)
      time_period_list.append((label, splitted[-3], splitted[-2]))
   time_period_list.sort(key=lambda tup:tup[1])
   return time_period_list

def string_to_list(value):
   if value == [u''] or value == None:
      return []
   if isinstance(value, list):
      return value
   return [value]

def get_gmap_config():
    '''
        Returns a dict with all configuration options related to the
        Google Maps API (ie those starting with 'ckanext.taijiang.gmap')
    '''
    namespace = 'ckanext.taijiang.gmap.'

    gmap_configs = dict([(k.replace(namespace, ''), v) for k, v in config.iteritems()
            if k.startswith(namespace)])

    if not gmap_configs.get('api_key'):
        log.critical('''Please specify a ckanext.taijiang.gmap.api_key
                     in your config for the Google Maps layer''')

    return dict([(k.replace(namespace, ''), v) for k, v in config.iteritems()
                 if k.startswith(namespace)])
