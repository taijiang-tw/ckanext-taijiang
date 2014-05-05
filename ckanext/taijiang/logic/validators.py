#from dateutil.parser import parse as date_parse
from datetime import datetime as date_parse

#from ckan.logic import get_action
import ckan.plugins.toolkit as toolkit
from ckan import new_authz
from ckan.lib.navl.dictization_functions import unflatten, Invalid
from ckan.lib.field_types import DateType, DateConvertError


def create_db_date(value, context):

   try:
      value = date_parse.strptime(value, '%Y-%m-%d')
   except ValueError:
      raise Invalid("Incorrect data format, should be YYYY-MM-DD")

   return value

def show_db_date(value, context):

   try:
      #print toolkit.get_action("package_show")(context, {"id": context.get("id")})
      value = date_parse.strptime(value, '%Y-%m-%d')
   except ValueError:
      raise Invalid("Incorrect data format, should be YYYY-MM-DD")

   return value.strftime('%Y-%m-%d')
