from pylons import config

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
