#from dateutil.parser import parse as date_parse
from datetime import datetime as date_parse

import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import unflatten, Invalid
from ckan.logic.validators import int_validator
from ckan.common import _
import numbers
import re
import json

def not_empty(value, context):
   if value == '':
      raise Invalid(_('Column is empty'))
   return value

def positive_integer_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   value = int_validator(value, context)
   if value < 1:
      raise Invalid(_('Must be a positive integer'))
   return value

def long_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   pattern = re.compile('^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$')
   if re.match(pattern, value) is None:
      raise Invalid(_('Must be a valid longitude coordinate'))
   return value

def lat_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   pattern = re.compile('^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$')
   if re.match(pattern, value) is None:
      raise Invalid(_('Must be a valid latitude coordinate'))
   return value

def float_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   try:
      value = float(value)
   except ValueError:
      raise Invalid(_('Must be an integer or a float'))
   return value
      
def positive_float_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   value = float_validator(value, context)
   if value < 1:
      raise Invalid(_('Must be a positive float'))
   return value

def json_validator(value, context):
   if value == '':
      return value
   try:
      json.loads(value)
   except ValueError:
      raise Invalid('Invalid JSON')
   return value
