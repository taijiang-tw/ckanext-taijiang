from pylons import config

import ckan.model as model # get_licenses should be in core

import ckan.plugins as p
import ckan.lib.helpers as helpers
import ckan.lib.formatters as formatters

import ckanext.taijiang.lists as lists


def get_languages():
   return lists.LANGUAGES

def get_encodings():
   return lists.ENCODINGS

def get_theme_keywords_1():
   return lists.THEME_KEYWORDS_1

def get_theme_keywords_2():
   return lists.THEME_KEYWORDS_2

def get_theme_keywords_3():
   return lists.THEME_KEYWORDS_3

def get_theme_keywords_4():
   return lists.THEME_KEYWORDS_4

def get_theme_keywords_5():
   return lists.THEME_KEYWORDS_5

def get_temp_res():
   return lists.TEMP_RES

def extras_to_dict(pkg):
   extras_dict = {}
   if pkg and 'extras' in pkg:
       for extra in pkg['extras']:
            extras_dict[extra['key']] = extra['value']
   return extras_dict
