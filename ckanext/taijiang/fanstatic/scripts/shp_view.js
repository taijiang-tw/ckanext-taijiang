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
      self.el.append($('<div></div>').attr('id', 'map'));
      self.map = ckan.commonLeafletMap('map', this.options.map_config);
      
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
          jQuery.each(feature.properties, function(key, value) {
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

      loadshp({
        url: url,
        encoding: preload_package.encoding,
        EPSG: preload_resource.resource_crs
      }, function(data) {
        gjLayer.addData(data);
        self.map.fitBounds(gjLayer.getBounds());
        self.map.spin(false);
      });
    }
  }
});
