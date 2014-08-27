import logging

# Bad imports: this should be in the toolkit

from ckan.lib.plugins import DefaultGroupForm
import ckan.plugins as p
from datetime import datetime as date_parse
import ckanext.taijiang.helpers as taijiang_helpers
from ckan.lib.navl.dictization_functions import Invalid
from ckan.logic import ValidationError
from ckanext.taijiang.logic.validators import not_empty, float_validator, positive_integer_validator, positive_float_validator, long_validator, lat_validator, json_validator
from ckanext.taijiang.logic.converters import remove_blank_wrap

log = logging.getLogger(__name__)


class TaijiangDatasets(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)


    ## IDatasetForm
    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def package_form(self):
	return super(TaijiangDatasets, self).package_form()

    def _modify_package_schema(self, schema):

        # Import core converters and validators
        _convert_to_extras = p.toolkit.get_converter('convert_to_extras')
        _ignore_missing = p.toolkit.get_validator('ignore_missing')
	_package_name_validator = p.toolkit.get_validator('package_name_validator')

	schema.update({
	   'identifier': [_ignore_missing, _convert_to_extras],
	   'data_type': [_ignore_missing, _convert_to_extras],
	   'proj': [_ignore_missing, _convert_to_extras],
	   'language': [_ignore_missing, _convert_to_extras],
	   'encoding': [_ignore_missing, _convert_to_extras],
	   'temp_res': [_ignore_missing, _convert_to_extras],
	   'start_time': [not_empty, _ignore_missing, _convert_to_extras],
	   'end_time': [not_empty, _ignore_missing, _convert_to_extras],
	   'theme_keyword_1': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_2': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_3': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_4': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_5': [_ignore_missing, _convert_to_extras],
	   'loc_keyword': [_ignore_missing, _convert_to_extras],
	   'author_name': [not_empty, _ignore_missing, _convert_to_extras],
	   'author_mail': [_ignore_missing, _convert_to_extras],
	   'author_phone': [_ignore_missing, _convert_to_extras],
	   'maintainer_name': [_ignore_missing, _convert_to_extras],
	   'maintainer_mail': [_ignore_missing, _convert_to_extras],
	   'maintainer_phone': [_ignore_missing, _convert_to_extras],
	   'ref': [_ignore_missing, _convert_to_extras],
	   'spatial': [_ignore_missing, remove_blank_wrap, _convert_to_extras, json_validator],
	   'book_isbn': [_ignore_missing, _convert_to_extras],
	   'book_issn': [_ignore_missing, _convert_to_extras],
           'book_journal': [_ignore_missing, _convert_to_extras],
           'book_volume': [_ignore_missing, _convert_to_extras],
           'book_proceeding': [_ignore_missing, _convert_to_extras],
           'book_location': [_ignore_missing, _convert_to_extras],
           'book_publisher': [_ignore_missing, _convert_to_extras],
           'book_year': [_ignore_missing, _convert_to_extras],
           'book_query': [_ignore_missing, _convert_to_extras],
           'book_url': [_ignore_missing, _convert_to_extras],
           'book_his_material': [_ignore_missing, _convert_to_extras],
           'book_area_village': [_ignore_missing, _convert_to_extras],
           'book_area_religion': [_ignore_missing, _convert_to_extras],
           'book_area_family': [_ignore_missing, _convert_to_extras],
           'book_area_reservoir': [_ignore_missing, _convert_to_extras],
           'book_area_industry': [_ignore_missing, _convert_to_extras],
           'book_notes': [_ignore_missing, _convert_to_extras],
	   'scan_source': [_ignore_missing, _convert_to_extras],
	   'scan_size': [_ignore_missing, _convert_to_extras],
	   'scan_res': [_ignore_missing, positive_integer_validator, _convert_to_extras],
	   'x_min': [_ignore_missing, long_validator, _convert_to_extras],
	   'x_max': [_ignore_missing, long_validator, _convert_to_extras],
	   'y_min': [_ignore_missing, lat_validator, _convert_to_extras],
	   'y_max': [_ignore_missing, lat_validator, _convert_to_extras],
	   'crs': [_ignore_missing, positive_integer_validator, _convert_to_extras],
	   'spatial_res': [_ignore_missing, positive_float_validator, _convert_to_extras],
	   'scale': [_ignore_missing, positive_integer_validator, _convert_to_extras],
	   'preprocessing': [_ignore_missing, _convert_to_extras],
	   #'wave_band_min': [_ignore_missing, float_validator, _convert_to_extras],
	   #'wave_band_max': [_ignore_missing, float_validator, _convert_to_extras],
	   #'wave_band_bit': [_ignore_missing, positive_float_validator, _convert_to_extras],
        })

        return schema
    
    def validate(self, context, data_dict, schema, action):
        if 'temp_res' in data_dict:
            temp_res = data_dict['temp_res']
            if (temp_res == u'date'):
                try:
	            date_parse.strptime(data_dict['start_time'], '%Y-%m-%d')
		    date_parse.strptime(data_dict['end_time'], '%Y-%m-%d')
	        except ValueError:
	            raise ValidationError({"Time format Error": ["Incorrect data format, should be YYYY-MM-DD"]})
	    if (temp_res == u'month'):
                try:
                    date_parse.strptime(data_dict['start_time'], '%Y-%m')
		    date_parse.strptime(data_dict['end_time'], '%Y-%m')
                except ValueError:
	            raise ValidationError({"Time Format Error": ["Incorrect data format, should be YYYY-MM"]})
            if (temp_res == u'year'):
                try:
                    date_parse.strptime(data_dict['start_time'], '%Y')
                    date_parse.strptime(data_dict['end_time'], '%Y')
                except ValueError:
                    raise ValidationError({"Time format Error": ["Incorrect data format, should be YYYY"]})
            if (temp_res == u'decade'):
                try:
                    date_parse.strptime(data_dict['start_time'], '%Y')
                    date_parse.strptime(data_dict['end_time'], '%Y')
	            for time_type in ['start_time', 'end_time']:
		        res = int(data_dict[time_type])%10
		        if (res != 0):
		            data_dict[time_type] = str(int(data_dict[time_type]) - res)
                except ValueError:
	            raise ValidationError({"Time format Error": ["Incorrect data format, should be YYYY"]})
            if (temp_res == u'century'):
                try:
                    date_parse.strptime(data_dict['start_time'], '%Y')
                    date_parse.strptime(data_dict['end_time'], '%Y')
                    for time_type in ['start_time', 'end_time']:
                        res = int(data_dict[time_type])%100
                        if (res != 0):
                            data_dict[time_type] = str(int(data_dict[time_type]) - res)
                except ValueError:
                    raise ValidationError({"Time format Error": ["Incorrect data format, should be YYYY"]})
        '''
        if ('x_min' in data_dict and 'x_max' in data_dict and 'y_min' in data_dict and 'y_max' in data_dict):
	    if (data_dict['x_min'] != "" and data_dict['x_max'] != "" and data_dict['y_min'] != "" and data_dict['y_max'] != ""):
	        data_dict['spatial'] = "{\"type\": \"Polygon\",\"coordinates\": [[[" +\
	               data_dict['x_min'] + "," +\
		       data_dict['y_min'] + "],[" +\
		       data_dict['x_min'] + "," +\
		       data_dict['y_max'] + "],[" +\
		       data_dict['x_max'] + "," +\
		       data_dict['y_max'] + "],[" +\
		       data_dict['x_max'] + "," +\
		       data_dict['y_min'] + "],[" +\
		       data_dict['x_min'] + "," +\
		       data_dict['y_min'] + "]]]}"
	        #print data_dict['spatial']
        '''
        return p.toolkit.navl_validate(data_dict, schema, context)

    def create_package_schema(self):
        schema = super(TaijiangDatasets, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(TaijiangDatasets, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(TaijiangDatasets, self).show_package_schema()

        # Import core converters and validators
        _convert_from_extras = p.toolkit.get_converter('convert_from_extras')
        _ignore_missing = p.toolkit.get_validator('ignore_missing')

        schema.update({
	    'identifier': [_ignore_missing, _convert_from_extras],
	    'data_type': [_ignore_missing, _convert_from_extras],
	    'proj': [_ignore_missing, _convert_from_extras],
            'language': [_ignore_missing, _convert_from_extras],
	    'encoding': [_ignore_missing, _convert_from_extras],
	    'temp_res': [_ignore_missing, _convert_from_extras],
	    'start_time': [_ignore_missing, _convert_from_extras],
	    'end_time': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_1': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_2': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_3': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_4': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_5': [_ignore_missing, _convert_from_extras],
	    'loc_keyword': [_ignore_missing, _convert_from_extras],
	    'author_name': [_ignore_missing, _convert_from_extras],
	    'author_mail': [_ignore_missing, _convert_from_extras],
	    'author_phone': [_ignore_missing, _convert_from_extras],
	    'maintainer_name': [_ignore_missing, _convert_from_extras],
	    'maintainer_mail': [_ignore_missing, _convert_from_extras],
	    'maintainer_phone': [_ignore_missing, _convert_from_extras],
	    'ref': [_ignore_missing, _convert_from_extras],
	    'spatial': [_ignore_missing, _convert_from_extras, json_validator],
	    'book_isbn': [_ignore_missing, _convert_from_extras],
	    'book_issn': [_ignore_missing, _convert_from_extras],
            'book_journal': [_ignore_missing, _convert_from_extras],
            'book_volume': [_ignore_missing, _convert_from_extras],
            'book_proceeding': [_ignore_missing, _convert_from_extras],
            'book_location': [_ignore_missing, _convert_from_extras],
            'book_publisher': [_ignore_missing, _convert_from_extras],
            'book_year': [_ignore_missing, _convert_from_extras],
            'book_query': [_ignore_missing, _convert_from_extras],
            'book_url': [_ignore_missing, _convert_from_extras],
            'book_his_material': [_ignore_missing, _convert_from_extras],
            'book_area_village': [_ignore_missing, _convert_from_extras],
            'book_area_religion': [_ignore_missing, _convert_from_extras],
            'book_area_family': [_ignore_missing, _convert_from_extras],
            'book_area_reservoir': [_ignore_missing, _convert_from_extras],
            'book_area_industry': [_ignore_missing, _convert_from_extras],
            'book_notes': [_ignore_missing, _convert_from_extras],
	    'scan_source': [_ignore_missing, _convert_from_extras],
	    'scan_size': [_ignore_missing, _convert_from_extras],
	    'scan_res': [_ignore_missing, positive_integer_validator, _convert_from_extras],
	    'x_min': [_ignore_missing, long_validator, _convert_from_extras],
	    'x_max': [_ignore_missing, long_validator, _convert_from_extras],
	    'y_min': [_ignore_missing, lat_validator, _convert_from_extras],
	    'y_max': [_ignore_missing, lat_validator, _convert_from_extras],
	    'crs': [_ignore_missing, positive_integer_validator, _convert_from_extras],
	    'spatial_res': [_ignore_missing, positive_float_validator, _convert_from_extras],
	    'scale': [_ignore_missing, positive_integer_validator, _convert_from_extras],
	    'preprocessing': [_ignore_missing, _convert_from_extras],
	    #'wave_band_min': [_ignore_missing, float_validator, _ignore_empty, _convert_from_extras],
	    #'wave_band_max': [_ignore_missing, float_validator, _ignore_empty, _convert_from_extras],
	    #'wave_band_bit': [_ignore_missing, positive_float_validator, _ignore_empty, _convert_from_extras],
        })

        return schema
    
    def update_config(self, config):
        
       p.toolkit.add_template_directory(config, 'templates')
       p.toolkit.add_public_directory(config, 'public')
       p.toolkit.add_resource('fanstatic', 'ckanext-taijiang')

    ## ITemplateHelpers
    def get_helpers(self):

        function_names = (
            'get_data_types',
            'get_languages',
	    'get_encodings',
	    'get_theme_keywords',
	    'get_loc_keyword',
	    'get_temp_res',
	    'get_proj',
            'get_his_material',
	    'extras_to_dict',
        )
        return _get_module_functions(taijiang_helpers, function_names)


def _get_module_functions(module, function_names):
    functions = {}
    for f in function_names:
        functions[f] = module.__dict__[f]

    return functions
