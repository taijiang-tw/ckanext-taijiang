import logging

# Bad imports: this should be in the toolkit

from ckan.lib.plugins import DefaultGroupForm

import ckan.plugins as p

import ckanext.taijiang.helpers as taijiang_helpers

from ckanext.taijiang.logic.validators import create_db_date, show_db_date

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
	_not_empty = p.toolkit.get_validator('not_empty')
        
	schema.update({
	   'author': [_not_empty, unicode],
	   'identifier': [_ignore_missing, _convert_to_extras],
	   'language': [_ignore_missing, _convert_to_extras],
	   'encoding': [_ignore_missing, _convert_to_extras],
	   'temp_res': [_ignore_missing, _convert_to_extras],
	   'start_time': [_ignore_missing, show_db_date, _convert_to_extras],
	   'end_time': [_ignore_missing, show_db_date, _convert_to_extras],
	   'theme_keyword_1': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_2': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_3': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_4': [_ignore_missing, _convert_to_extras],
	   'theme_keyword_5': [_ignore_missing, _convert_to_extras],
	   'author_phone': [_ignore_missing, _convert_to_extras],
	   'maintainer_phone': [_ignore_missing, _convert_to_extras],
        })

        return schema

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
        _ignore_empty = p.toolkit.get_validator('ignore_empty')

        schema.update({
	    'identifier': [_ignore_missing, _convert_from_extras],
            'language': [_ignore_missing, _convert_from_extras],
	    'encoding': [_ignore_missing, _convert_from_extras],
	    'temp_res': [_ignore_missing, _convert_from_extras],
	    'start_time': [_ignore_missing, _ignore_empty, create_db_date, _convert_from_extras],
	    'end_time': [_ignore_missing, _ignore_empty, create_db_date, _convert_from_extras],
	    'theme_keyword_1': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_2': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_3': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_4': [_ignore_missing, _convert_from_extras],
	    'theme_keyword_5': [_ignore_missing, _convert_from_extras],
	    'author_phone': [_ignore_missing, _convert_from_extras],
	    'maintainer_phone': [_ignore_missing, _convert_from_extras],
        })

        return schema

    def update_config(self, config):
        
       p.toolkit.add_template_directory(config, 'templates')

    ## ITemplateHelpers
    def get_helpers(self):

        function_names = (
            'get_languages',
	    'get_encodings',
	    'get_theme_keywords_1',
	    'get_theme_keywords_2',
	    'get_theme_keywords_3',
	    'get_theme_keywords_4',
	    'get_theme_keywords_5',
	    'get_temp_res',
	    'extras_to_dict',
        )
        return _get_module_functions(taijiang_helpers, function_names)


def _get_module_functions(module, function_names):
    functions = {}
    for f in function_names:
        functions[f] = module.__dict__[f]

    return functions
