// shapefile preview module
ckan.module('shppreview', function (jQuery, _) {
  return {
    options: {
      table: '<table class="table table-striped table-bordered table-condensed"><tbody>{body}</tbody></table>',
      row:'<tr><th>{key}</th><td>{value}</td></tr>',
      style: {
        fillColor: '#03F',
        opacity: 0.7,
        fillOpacity: 0.1,
        weight: 2
      },
      i18n: {
        'error': _('An error occurred: %(text)s %(error)s')
      }
    },
    initialize: function () {
      var self = this;

      self.el.empty();
      self.el.append($("<div></div>").attr("id","map"));
      self.map = ckan.commonLeafletMap('map', this.options.map_config);
      
      // define EPSG Projections
      proj4.defs([
        [
	  'EPSG:3826',
	  '+title=TWD97 TM2 zone 121 +proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +units=m +no_defs'
	],
	[
	  'EPSG:3821',
	  '+title=TWD67 +proj=longlat +towgs84=-752,-358,-179,-.0000011698,.0000018398,.0000009822,.00002329 +ellps=aust_SA +units=degrees +no_defs'
	],
        [
	  'EPSG:3825', 
	  '+title=TWD97 TM2 zone 119 +proj=tmerc +lat_0=0 +lon_0=119 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +units=m +no_defs'
	],
	[
	  'EPSG:3828', 
	  '+title=TWD67 TM2 zone 121 +proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=aust_SA +units=m +no_defs'
        ]
      ]);
      var resource_crs = preload_resource['resource_crs'];
      self.feature_crs = ($.inArray(resource_crs, ['3826', '3821', '3825', '3828']) != -1) ? proj4('EPSG:'+resource_crs): proj4('EPSG:4326');
      self.leaflet_crs = proj4('EPSG:4326');

      // use CORS, if supported by browser and server
      if (jQuery.support.cors && preload_resource['original_url'] !== undefined) {
        jQuery.get(preload_resource['original_url'])
        .done(
          function(data){
            self.showPreview(preload_resource['original_url'], data);
          })
        .fail(
          function(jqxhr, textStatus, error) {
            jQuery.get(preload_resource['url'])
            .done(
              function(data){
                self.showPreview(preload_resource['url'], data);
              })
            .fail(
              function(jqXHR, textStatus, errorThrown) {
                self.showError(jqXHR, textStatus, errorThrown);
              }
            );
          }
        );
      } else {
        jQuery.get(preload_resource['url']).done(
          function(data){
            self.showPreview(preload_resource['url'], data);
          })
        .fail(
          function(jqXHR, textStatus, errorThrown) {
            self.showError(jqXHR, textStatus, errorThrown);
          }
        );
      }
    },

    showError: function (jqXHR, textStatus, errorThrown) {
      if (textStatus == 'error' && jqXHR.responseText.length) {
        this.el.html(jqXHR.responseText);
      } else {
        this.el.html(this.i18n('error', {text: textStatus, error: errorThrown}));
      }
    },

    showPreview: function (url, data) {
      var self = this;

      JSZipUtils.getBinaryContent(url, function(err, data) {
        if(err) throw err;

        var zip = new JSZip(data);
        var shpString =  zip.file(/.shp/)[0].name;
        var dbfString = zip.file(/.dbf/)[0].name;

        function TransCoord(x, y) {
          var result;
          if (proj4) {
            var p = proj4(self.feature_crs, self.leaflet_crs, [x, y]);
            result = {x: p[0], y: p[1]};
          }
          return result;
        }

        function highLightStyle(e) {
          gjLayer.eachLayer(function(l) {
            gjLayer.resetStyle(l);
          });
          e.target.setStyle({
            fillColor: '#FF0',
            fillOpacity: 0.6
          });
        }

        self.map.spin(true);
        var gjLayer = L.geoJson([], {
          style: self.options.style,
          onEachFeature: function(feature, layer) {
            var body = '';
            jQuery.each(feature.properties, function(key, value){
              if (value != null && typeof value === 'object') {
                value = JSON.stringify(value);
              }
              body += L.Util.template(self.options.row, {key: key, value: value});
            });
            var popupContent = L.Util.template(self.options.table, {body: body});
            layer.bindPopup(popupContent);
	    layer.on({click: highLightStyle});
          }
        }).addTo(self.map);

        shapefile = new Shapefile({
          shp: URL.createObjectURL(new Blob([zip.file(shpString).asArrayBuffer()])),
          dbf: URL.createObjectURL(new Blob([zip.file(dbfString).asArrayBuffer()]))
        }, function(data){
          var dbf = data.dbf;
          var dbfFields = dbf.fields;
          for (var i = 0; i < data.geojson.features.length; i++) {
            features = data.geojson.features[i].geometry.coordinates;
	    for (var number = 0; number < features.length; number++) {
              for (var j = 0; j < features[number].length; j++) {
	        var projcoordinates = TransCoord(features[number][j][0], features[number][j][1]);
	        features[number][j][0] = projcoordinates.x;
	        features[number][j][1] = projcoordinates.y;
              };
            };
	  };
          gjLayer.addData(data.geojson);
	  self.map.fitBounds(gjLayer.getBounds());
          self.map.spin(false);
        })
      });
    }
  };
});
