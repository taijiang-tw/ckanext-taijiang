console.log($('#field-temp_res').val());

if ($('#field-temp_res').val() == '') {
  $('#field-start-time').attr('readonly', true);
  $('#field-end-time').attr('readonly', true);
}

function control_fields(value) {
  $('#field-start-time').attr('readonly', false);
  $('#field-end-time').attr('readonly', false);
  if ($.inArray(value, ['']) == 0) {
    $('#field-start-time').val('');
    $('#field-start-time').attr('readonly', true);
    $('#field-end-time').val('');
    $('#field-end-time').attr('readonly', true);
  }
}
$('#field-temp_res').on('select2-selecting', function(e) {control_fields(e.val)});
