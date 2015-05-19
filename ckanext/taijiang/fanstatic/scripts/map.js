// add a MapQuest tile layer
var mq = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; OpenStreetMap contributors, Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="//developer.mapquest.com/content/osm/mq_logo.png">',
  subdomains: '1234'
});
// add a Google Maps tile layer
var ggl = new L.Google('ROADMAP');
var ggls = new L.Google('HYBRID');
var map = L.map('map', {
  center: [23.04, 120.18],
  zoom: 11,
  maxZoom: 18
});
// add a NLSC tile layer
var nlsc = L.tileLayer('http://maps.nlsc.gov.tw/S_Maps/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=EMAP&STYLE=_null&TILEMATRIXSET=EPSG:3857&TILEMATRIX=EPSG:3857:{z}&TILEROW={y}&TILECOL={x}&FORMAT=image/png', {
  attribution: '內政部國土測繪中心'
});
// add MapQuest (default tile layer)
map.addLayer(mq);
// add layer control
map.addControl(new L.control.layers({"MapQuest": mq, "Google Maps": ggl, "Google Maps (衛星)": ggls, "通用版電子地圖": nlsc}));

featureGroup = L.featureGroup().addTo(map);

var drawControl = new L.Control.Draw({
  draw: {
    polygon: true,
    polyline: false,
    rectangle: true,
    circle: false,
    marker: true
  }
}).addTo(map);

map.on('draw:created', showPolygonArea);
map.on('draw:edited', showPolygonAreaEdited);

function showPolygonAreaEdited(e) {
  e.layers.eachLayer(function(layer) {
    showPolygonArea({ layer: layer });
  });
}

function showPolygonArea(e) {
  var geo = e.layer.toGeoJSON().geometry['coordinates'];
  var longs = [];
  var lats = [];
  for (i=0; i < geo[0].length; i++) {
      longs.push(geo[0][i][0]);
      lats.push(geo[0][i][1]);
  }
  $('#field-spatial').val(JSON.stringify(e.layer.toGeoJSON().geometry));
  featureGroup.clearLayers();
  featureGroup.addLayer(e.layer);
}

$('#map').hide();
if ($('#field-spatial').val() != '') {
  var geojson = jQuery.parseJSON($('#field-spatial').val());
  var extentLayer = L.geoJson(geojson, {style: function (feature) {
    return {color: feature.properties.color};
  }}).addTo(map);
  if (geojson.type == 'Point') {
    map.setView(L.latLng(geojson.coordinates[1], geojson.coordinates[0]), 9);
  } else {
    map.fitBounds(extentLayer.getBounds());
  }
  $('#map').show();
}
$(document).ready(function(){
  $('#show_map').click(function(){
    $('#map').toggle();
  });
  $('#convert_from_four_range').click(function() {
    if ($.isNumeric($('#field-x_min').val()) && $.isNumeric($('#field-x_max').val()) && $.isNumeric($('#field-y_min').val()) && $.isNumeric($('#field-y_max').val())){
      if (parseFloat($('#field-x_min').val()) > parseFloat($('#field-x_max').val()) || parseFloat($('#field-y_min').val()) > parseFloat($('#field-y_max').val())){
        alert('X (Y) 之最小值需小於最大值');
      }
      else{
        var geojson = '{"type":"Polygon","coordinates":[[['+$('#field-x_min').val()+','+$('#field-y_min').val()+'],['+$('#field-x_min').val()+','+$('#field-y_max').val()+'],['+$('#field-x_max').val()+','+$('#field-y_max').val()+'],['+$('#field-x_max').val()+','+$('#field-y_min').val()+'],['+$('#field-x_min').val()+','+$('#field-y_min').val()+']]]}';
        $('#field-spatial').val(geojson);
      }
    }
    else{
      alert('請輸入完整四至座標資訊');
    }
  });
});
