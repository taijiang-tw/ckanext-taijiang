================================
Taijiang.tw (台江內海研究資料集)
================================

`Taijiang Research Data Repository <http://taijiang.tw>`_ is a research data repository for the humanities and areas studies in Taijiang Inland Sea Area, a region in Tainan City in Southern Taiwan.


Prerequirements
----------------

- **Taijiang.tw CKAN.** The code powering the Taijiang.tw instance of CKAN.

  - `release-taijiang-tw <https://github.com/taijiang-tw/ckan>`_ - The main development branch used for the current taijiang.tw.

- **Extensions.** We have developed several CKAN extensions. The `full list of installed extensions can be seen via the CKAN API <http://taijiang.tw/api/util/status>`_. Custom extensions include:

  - `taijiang-tw/ckanext-taijiang <https://github.com/taijiang-tw/ckanext-taijiang>`_ - Most taijiang.tw specific CKAN customizations are contained within this extension.
  - `taijiang-tw/ckanext-spatial <https://github.com/taijiang-tw/ckanext-spatial>`_ - Geospatial extension for CKAN.
  - `taijiang-tw/ckanext-geoview <https://github.com/taijiang-tw/ckanext-geoview>`_ - CKAN Geospatial ResourceView.
  - `taijiang-tw/taijiang-ckan-translations <https://github.com/taijiang-tw/taijiang-ckan-translations>`_ - Translations for Taijiang Research Data Repository.
  - `taijiang-tw/ckanext-dga-stats <https://github.com/taijiang-tw/ckanext-dga-stats>`_ - CKAN's built-in Statistics plugin modified for taijiang.tw.

- **Other Extensions.**

  - `open-data/ckanext-scheming <https://github.com/open-data/ckanext-scheming>`_ - Easy, sharable custom CKAN schemas.
  - `open-data/ckanext-repeating <https://github.com/open-data/ckanext-repeating>`_ - Repeating fields for CKAN.
  - `ckan/ckanext-pages <https://github.com/ckan/ckanext-pages>`_ - Simple CMS.
  - `datagovau/ckanext-ga-report <https://github.com/datagovau/ckanext-ga-report>`_ - Google analytics report for CKAN.
  - `ckan/ckanext-googleanalytics <https://github.com/ckan/ckanext-googleanalytics>`_ - CKAN extension to integrate Google Analytics data into CKAN. Gives download stats on package pages, list of most popular packages, etc.


Install
--------

With your virtualenv activated:

::

   cd src
   git clone https://github.com/taijiang-tw/ckanext-taijiang.git
   cd ckanext-taijiang
   python setup.py develop
   pip install -r requirements.txt

Add the following plugin and the Google Maps API key to your CKAN ini file:

::

   ckan.plugins = ... taijiang_datasets
   ckanext.taijiang.gmap.api_key = YOUR_GOOGLE_MAPS_API_KEY

Then restart your server.


License
--------

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
