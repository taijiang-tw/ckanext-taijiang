===================================================
CKAN extension for taijiang.tw (台江內海研究資料集)
===================================================


This extension contains the plugin that add functions to `Taijiang Research Data Repository <http://taijiang.tw>`_


Prerequirements
----------------

- CKAN (version 2.3 and up): https://github.com/ckan/ckan
- modified ckanext-spatial: https://github.com/u10313335/ckanext-spatial
- ckanext-scheming: https://github.com/open-data/ckanext-scheming
- ckanext-repeating: https://github.com/open-data/ckanext-repeating
- Solr with mmseg4j installed


Install
--------

With your virtualenv activated:

::

   cd src
   git clone https://github.com/u10313335/ckanext-taijiang.git
   cd ckanext-taijiang
   python setup.py develop
   pip install -r requirements.txt

Add the following plugin to your CKAN ini file:

::

   ckan.plugins = taijiang_datasets ...

Then restart your server.


License
--------

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
