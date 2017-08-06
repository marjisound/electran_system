/*Menu-toggle*/
$(document).ready(function(){
  $("#menu-toggle").click(function(e) {
      e.preventDefault();
      $("#wrapper").toggleClass("active");
  });
  $(".catCheckAll").click(function () {
    var catid = $(this).val();
    $("input[data-catid=" + catid + "]").prop('checked', $(this).is(":checked"));
  });
   $("#checkAllQuestions").click(function () {
    var catid = $(this).val();
    $("input[type=checkbox]").prop('checked', $(this).is(":checked"));
  });

  $('div[id^="date_question_container_"]').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        sideBySide: true,
        ignoreReadonly: true
    });
});
