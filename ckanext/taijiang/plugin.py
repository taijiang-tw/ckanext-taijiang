import logging

from ckan.lib.plugins import DefaultGroupForm
import ckan.plugins as p
from datetime import datetime as date_parse
import json
import ckanext.taijiang.helpers as taijiang_helpers
from ckan.lib.navl.dictization_functions import Invalid
from ckan.logic import ValidationError
from ckanext.taijiang.logic.validators import not_empty, float_validator, positive_integer_validator, positive_float_validator, long_validator, lat_validator, json_validator
from ckanext.taijiang.logic.converters import remove_blank_wrap, checkbox_value

log = logging.getLogger(__name__)


class TaijiangDatasets(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.IFacets)


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

	schema.update({
	   'identifier': [_ignore_missing, _convert_to_extras],
	   'data_type': [_ignore_missing, _convert_to_extras],
	   'proj': [_ignore_missing, _convert_to_extras],
	   'language': [_ignore_missing, _convert_to_extras],
	   'encoding': [_ignore_missing, _convert_to_extras],
	   'temp_res': [_ignore_missing, _convert_to_extras],
	   'start_time': [_ignore_missing, _convert_to_extras],
	   'end_time': [_ignore_missing, _convert_to_extras],
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
           'book_from_local_chronicles_in_qing_dynasty': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_japan_officials': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_officials_in_postwar_period': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_inscriptions': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_newspapers': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_maps': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_taiwanese_governor_office_files': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_dutch_formosa': [_ignore_missing, checkbox_value, _convert_to_extras],
           'book_from_field_researches': [_ignore_missing, checkbox_value, _convert_to_extras],
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
        })

        return schema
    
    def validate(self, context, data_dict, schema, action):
        time_format = { u'date': ['%Y-%m-%d', 'YYYY-MM-DD'],
                u'month': ['%Y-%m', 'YYYY-MM'],
                u'year': ['%Y', 'YYYY'],
                u'decade': ['%Y', 'YYYY', 10],
                u'century': ['%Y', 'YYYY', 100] }
        temp_res = data_dict.get('temp_res', '')
        if temp_res:
            try:
                if (temp_res == u'decade' or temp_res == u'century'):
                    for time_type in ['start_time', 'end_time']:
                        res = int(data_dict[time_type])%time_format[temp_res][2]
                        if (res != 0):
                            data_dict[time_type] = str(int(data_dict[time_type]) - res)

                data_dict['start_time'] = date_parse.strptime(data_dict['start_time'],
                        time_format[temp_res][0])
                data_dict['end_time'] = date_parse.strptime(data_dict['end_time'],
                        time_format[temp_res][0])
            except ValueError:
                raise ValidationError({"Time format Error":
                    ["Incorrect data format, should be %s" % time_format[temp_res][1]]})
            data_dict['start_time'] = data_dict['start_time'].isoformat() + "Z"
            data_dict['end_time'] = data_dict['end_time'].isoformat() + "Z"
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
            'book_from_local_chronicles_in_qing_dynasty': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_japan_officials': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_officials_in_postwar_period': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_inscriptions': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_newspapers': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_maps': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_taiwanese_governor_office_files': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_dutch_formosa': [_ignore_missing, checkbox_value, _convert_from_extras],
            'book_from_field_researches': [_ignore_missing, checkbox_value, _convert_from_extras],
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
        })

        return schema

    ## IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_resource('fanstatic', 'ckanext-taijiang')

    ## IPackageController
    def before_search(self, search_params):
        def parse_date(date_string):
            '''
            Parse a date string or throw a nice error into the log. Re-raises
            the error for the plugin to catch.
            '''
            try:
                return date_parse.strptime(date_string, '%Y-%m-%d')
            except ValueError as e:
                log.debug('Date {0} not in the right format. Needs to be YYYY'
                        '-MM-DD'.format(date_string))
                raise e

        if (search_params.get('extras', None) and 'ext_begin_date' in
                search_params['extras'] and 'ext_end_date' in
                search_params['extras']):
            try:
                begin = parse_date(search_params['extras']['ext_begin_date'])
                end = parse_date(search_params['extras']['ext_end_date'])
            except ValueError:
                return search_params
            # Adding 'Z' manually here is evil, but we do this in core too.
            query = ("(start_time: [* TO {0}Z] AND "
                     "end_time: [{0}Z TO *]) OR "
                     "(start_time: [{0}Z TO {1}Z] AND "
                     "end_time: [{0}Z TO *])")
            query = query.format(begin.isoformat(), end.isoformat())
            search_params['q'] = query

        return search_params

    def before_index(self, data_dict):
        data_dict.update({'data_type_facet': '', 'proj_facet': '', 'language_facet': '',
                'encoding_facet': '', 'theme_keyword_facets': [], 'loc_keyword_facet': ''})
        for data_type_def in taijiang_helpers.get_data_types():
            if data_type_def[0] == data_dict.get('data_type'):
                data_dict['data_type_facet'] = data_type_def[1]
        for proj_def in taijiang_helpers.get_proj():
            if proj_def[0] == data_dict.get('proj'):
                data_dict['proj_facet'] = proj_def[1]
        for language_def in taijiang_helpers.get_languages():
            if language_def[0] == data_dict.get('language'):
                data_dict['language_facet'] = language_def[1]
        for encoding_def in taijiang_helpers.get_encodings():
            if encoding_def[0] == data_dict.get('encoding'):
                data_dict['encoding_facet'] = encoding_def[1]
        for theme_keyword_def in taijiang_helpers.get_theme_keywords():
            if data_dict.get('theme_keyword_1'):
                if theme_keyword_def[0] == data_dict.get('theme_keyword_1'):
                    data_dict['theme_keyword_facets'].append(theme_keyword_def[1])
            if data_dict.get('theme_keyword_2'):
                if theme_keyword_def[0] == data_dict.get('theme_keyword_2'):
                    data_dict['theme_keyword_facets'].append(theme_keyword_def[1])
            if data_dict.get('theme_keyword_3'):
                if theme_keyword_def[0] == data_dict.get('theme_keyword_3'):
                    data_dict['theme_keyword_facets'].append(theme_keyword_def[1])
            if data_dict.get('theme_keyword_4'):
                if theme_keyword_def[0] == data_dict.get('theme_keyword_4'):
                    data_dict['theme_keyword_facets'].append(theme_keyword_def[1])
            if data_dict.get('theme_keyword_5'):
                if theme_keyword_def[0] == data_dict.get('theme_keyword_5'):
                    data_dict['theme_keyword_facets'].append(theme_keyword_def[1])
        for loc_keyword_def in taijiang_helpers.get_loc_keyword():
            if loc_keyword_def[0] == data_dict.get('loc_keyword'):
                data_dict['loc_keyword_facet'] = loc_keyword_def[1]

        return data_dict

    ## IFacets
    def dataset_facets(self, facets_dict, package_type):
        facets_dict['date_facet'] = p.toolkit._('Date of Dataset')
        facets_dict['data_type_facet'] = p.toolkit._('Data Type')
        facets_dict['proj_facet'] = p.toolkit._('Project')
        facets_dict['language_facet'] = p.toolkit._('Language')
        facets_dict['encoding_facet'] = p.toolkit._('Encoding')
        facets_dict['theme_keyword_facets'] = p.toolkit._('Theme Keyword')
        facets_dict['loc_keyword_facet'] = p.toolkit._('Spatial Keyword')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        facets_dict['data_type_facet'] = p.toolkit._('Data Type')
        facets_dict['proj_facet'] = p.toolkit._('Project')
        facets_dict['language_facet'] = p.toolkit._('Language')
        facets_dict['encoding_facet'] = p.toolkit._('Encoding')
        facets_dict['theme_keyword_facets'] = p.toolkit._('Theme Keyword')
        facets_dict['loc_keyword_facet'] = p.toolkit._('Spatial Keyword')

        return facets_dict

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
	    'extras_to_dict',
	    'geojson_to_wkt',
            'get_newsfeed',
            'get_time_period',
            'date_to_iso',
            'get_default_slider_values',
            'get_date_url_param',
        )
        return _get_module_functions(taijiang_helpers, function_names)


def _get_module_functions(module, function_names):
    functions = {}
    for f in function_names:
        functions[f] = module.__dict__[f]

    return functions
