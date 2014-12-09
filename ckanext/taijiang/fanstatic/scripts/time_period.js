function set_time_period(start, end) {
  $('#field-temp_res').select2('val', 'year');
  $('#field-temp_res').attr('readonly', true);
  $('#field-start-time').val(start);
  $('#field-start-time').attr('disabled', false);
  $('#field-start-time').attr('readonly', true);
  $('#field-end-time').val(end);
  $('#field-end-time').attr('disabled', false);
  $('#field-end-time').attr('readonly', true);
}
$('#field-time_period').on('select2-selecting', function(e) {
  console.log(e);
  $('#field-theme_keyword_1').select2('val', e.val);
  $('#field-theme_keyword_1').attr('readonly', true);
  var start = $(e.object.element).data('start');
  var end = $(e.object.element).data('end');
  set_time_period(start, end);
  if (e.val == '自行輸入') {
    $('#field-theme_keyword_1').attr('readonly', false);
    $('#field-theme_keyword_1').select2('val', '');
    $('#field-temp_res').attr('readonly', false);
    $('#field-start-time').attr('readonly', false);
    $('#field-end-time').attr('readonly', false);
  }
});
