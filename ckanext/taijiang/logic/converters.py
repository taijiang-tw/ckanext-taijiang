from ckan.lib.navl.dictization_functions import Missing

def remove_blank_wrap(value, context):
   
   return "".join(value.split())

def checkbox_value(value,context):

   return 'yes' if not isinstance(value, Missing) else 'no'
