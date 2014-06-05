#from dateutil.parser import parse as date_parse
from datetime import datetime as date_parse

import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import unflatten, Invalid
from ckan.logic.validators import int_validator
from ckan.common import _
import numbers
import re

def not_empty(value, context):
   if value == '':
      raise Invalid(_('Column is empty'))
   return value

def postive_integer_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   value = int_validator(value, context)
   if value < 1:
      raise Invalid(_('Must be a postive integer'))
   return value

def lat_long_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   pattern = re.compile('\-?\d+(\.\d+)?')
   if re.match(pattern, value) is None:
      raise Invalid(_('Must be a valid latitude/longitude coordinate'))
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
      
def postive_float_validator(value, context):
   if value is None:
      return None
   if hasattr(value, 'strip') and not value.strip():
      return None
   value = float_validator(value, context)
   if value < 1:
      raise Invalid(_('Must be a postive float'))
   return value
