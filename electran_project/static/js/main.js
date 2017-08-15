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

  $('div[id^="date_question_container_"],div[id^="date_category_container_"]').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        sideBySide: true,
        ignoreReadonly: true
    });

  $('div[id^="date_category_container_"]').on('dp.change', function (e) {
      var date = e.date;

    //   alert('helllo');
    // var catid = $(this).data('category-id');
    // var value = $(this).val();
    // $("input[data-cat-id-date=" + catid + "]").val(value);
  });

  $('button[id^="category_date_btn_"]').click( function(e) {
      e.preventDefault();
      var catid = $(this).data('category-btn');
      var value = $("#category_date_" + catid).val()
      console.log(value)
      $("input[data-cat-id-date=" + catid + "]").val(value);
  });
});
