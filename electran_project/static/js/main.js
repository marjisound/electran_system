/*Menu-toggle*/
$(document).ready(function(){


  $("#menu-toggle").click(function(e) {
      e.preventDefault();
      $("#wrapper").toggleClass("active");
  });
  $('#checkAllQuestions').click(function () {
    $(".catCheckAll").each(function () {
        $(this).prop('checked', $('#checkAllQuestions').prop('checked'))
        toggleCatQuestions($(this).val());
    })
  });

  $('#semesterModuleForm').submit(function (e) {
      if($('#semesterModule').val() === '0'){
          $('#semesterModuleError').fadeIn();
          return false;
      }
  });

  // to toggle the collapse for all categories in admin set questions for semester
  $('#catCollapseAll').click(function () {
      $('div[id^="collapse"]').collapse('toggle')
      var areaExpand = $('a[data-toggle="collapse"]').attr('aria-expanded')
      console.log(typeof areaExpand)
      if(areaExpand == 'true') {
          $('#catCollapseAll').text("Collapse All")
      }else{

          $('#catCollapseAll').text("Expand All")
      }
  });



  $(".catCheckAll").click(function () {
    var catid = $(this).val();
    toggleCatQuestions(catid);
  });

  $('div[id^="date_question_container_"],div[id^="date_category_container_"]').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        sideBySide: true,
        ignoreReadonly: true
    });

  $('button[id^="category_date_btn_"]').click( function(e) {
      e.preventDefault();
      var catid = $(this).data('category-btn');
      var value = $("#category_date_" + catid).val()
      $("input[data-cat-id-date=" + catid + "]").val(value);
  });

  // this function enable all the disabled checkboxes before the submit is done
  //  in order for them to go through with the post object
  $('#qus_sem_form').submit(function(e) {
      e.preventDefault();
      $('input[name="chk_question"]').attr('disabled', false);
      this.submit();
  });

  $('input[name="chk_question"]').click(function (e) {
      // var vis = ($(this).prop('checked'))? 'inline': 'none'
      if ($(this).prop('checked'))
          $('#divQuestionDetail' + $(this).val()).fadeIn()
      else
          $('#divQuestionDetail' + $(this).val()).fadeOut()

      $('#visible_question' + $(this).val()).prop('checked', $(this).prop('checked'))
  });
});

function toggleCatQuestions(catId) {
    $('#divCat' + catId + ' li[id^="liQuestion"]').each(function () {
        var parentElement = $('#chkCatCheckAll' + catId);
        var questionCheckBox = $(this).find('input[id^="qusTitle"]');

        if(!questionCheckBox.prop('disabled')) {
            questionCheckBox.prop('checked', $(parentElement).prop('checked'));

            if (parentElement.prop('checked')) {
                $(this).find('div[id^="divQuestionDetail"]').fadeIn();
            }
            else {
                $(this).find('div[id^="divQuestionDetail"]').fadeOut();
            }
        }
        $(this).find('input[id^="visible_question"]').prop('checked', $(parentElement).prop('checked'));
    })
}
