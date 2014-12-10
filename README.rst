=====================================================================
Dataset for Taijiang Project (台江內海研究資料集) Extension for CKAN
=====================================================================


This extension contains the plugin that add functions to `Taijiang Research Database <http://taijiang.tw>`_


Prerequirements
----------------

- CKAN: https://github.com/ckan/ckan
- ckanext-spatial: https://github.com/ckan/ckanext-spatial


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

   ckan.plugins = ... taijiang_datasets

Then restart your server.


License
--------

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
