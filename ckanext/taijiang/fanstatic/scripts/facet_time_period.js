function set_time_period(start, end) {
  $('#field-start-time').val('');
  $('#field-end-time').val('');
  if (start == '') return;
  $('#field-start-time').val($.datepicker.formatDate('yy-mm-dd', new Date(start, 0, 1)));
  $('#dateSlider').dateRangeSlider("min", new Date(start, 0, 1));
  if (end != '') {
    $('#field-end-time').val($.datepicker.formatDate('yy-mm-dd', new Date(end, 11, 31)));
    $('#dateSlider').dateRangeSlider("max", new Date(end, 11, 31));
  } else {
    $('#field-end-time').val($.datepicker.formatDate('yy-mm-dd', new Date()));
    $('#dateSlider').dateRangeSlider("max", new Date());
  }
}
$('#field-time-period').on('select2-selecting', function(e) {
  var start = $(e.object.element).data('start');
  var end = $(e.object.element).data('end');
  set_time_period(start, end);
});
