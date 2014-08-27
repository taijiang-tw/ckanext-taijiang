var map = L.mapbox.map('map', 'u10313335.j31lbogb')
    .setView([23.58, 120.58], 7);

var featureGroup = L.featureGroup().addTo(map);

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
if ($('#field-spatial').val() != '') {
  var geojson = jQuery.parseJSON($('#field-spatial').val());
  L.geoJson(geojson, { style: L.mapbox.simplestyle.style }).addTo(map);
}
$('#map').hide();
$(document).ready(function(){
  $('#show_map').click(function(){
    $('#map').toggle();
  });
  $('#convert_from_four_range').click(function() {
    if ($.isNumeric($('#field-x-min').val()) && $.isNumeric($('#field-x-max').val()) && $.isNumeric($('#field-y-min').val()) && $.isNumeric($('#field-y-max').val())){
      if (parseFloat($('#field-x-min').val()) > parseFloat($('#field-x-max').val()) || parseFloat($('#field-y-min').val()) > parseFloat($('#field-y-max').val())){
        alert('X (Y) 之最小值需小於最大值');
      }
      else{
        var geojson = '{"type":"Polygon","coordinates":[[['+$('#field-x-min').val()+','+$('#field-y-min').val()+'],['+$('#field-x-min').val()+','+$('#field-y-max').val()+'],['+$('#field-x-max').val()+','+$('#field-y-max').val()+'],['+$('#field-x-max').val()+','+$('#field-y-min').val()+'],['+$('#field-x-min').val()+','+$('#field-y-min').val()+']]]}';
        $('#field-spatial').val(geojson);
      }
    }
    else{
      alert('請輸入完整四至座標資訊');
    }
  });
});
var all_fields = ['#book-fields', '#scanned-image-fields', '#spatial-type-fields']
var need_book_fields = ['books'];
var need_scanned_image_fields = ['pics_non_spatial', 'pics_spatial'];
var need_spatial_fields = ['pics_spatial', 'grid', 'vector', 'tin', 'steropair'];
var sel_data_type = $('#field-data_type').val();
function show_fields(value) {
  var fields_toggle = [false, false, false];
  if ($.inArray(value, need_book_fields) != -1) {
    fields_toggle[0] = true;
  }
  if ($.inArray(value, need_scanned_image_fields) != -1) {
    fields_toggle[1] = true;
  }
  if ($.inArray(value, need_spatial_fields) != -1) {
    fields_toggle[2] = true;
  }
  $.each(all_fields, function(index, value) {
    if (fields_toggle[index]) {$(value).show();} else {$(value).hide();}
  });
}
$(function () {show_fields(sel_data_type)});
$('#field-data_type').on('select2-selecting', function(e) {show_fields(e.val)});
