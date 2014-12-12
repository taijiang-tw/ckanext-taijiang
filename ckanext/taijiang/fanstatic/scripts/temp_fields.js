if ($('#field-temp_res').val() == '') {
  $('#field-start-time').attr('disabled', true);
  $('#field-end-time').attr('disabled', true);
}

function control_fields(value) {
  $('#field-start-time').attr('disabled', false);
  $('#field-end-time').attr('disabled', false);
  if ($.inArray(value, ['']) == 0) {
    $('#field-start-time').val('');
    $('#field-start-time').attr('disabled', true);
    $('#field-end-time').val('');
    $('#field-end-time').attr('disabled', true);
  }
}
$('#field-temp_res').on('select2-selecting', function(e) {control_fields(e.val)});
