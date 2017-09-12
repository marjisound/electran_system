
var $ = django.jQuery.noConflict();
var defer = $.Deferred();
$(document).ready(function () {

    userSemIdOld = $('#id_user_semester').val();
    questionSemIdOld = $('#id_question_semester').val();

    resetSemQuestionSelects();
    $('#id_semester').change(function () {
        semId = $(this).val();
        semester_change(semId);
    });

    if ($('#id_semester') && $('#id_semester').val()) {
        semId = $('#id_semester').val();
        if ($('p.errornote')) {
            userSemId = userSemIdOld;
            questionSemId = questionSemIdOld;
        }else {
            userSemId = $('#id_txt_user_semester').val();
            questionSemId = $('#id_txt_question_semester').val();
        }

        semester_change(semId);
        $.when(defer).done(function () {
           $('#id_user_semester').val(userSemId);
           $('#id_question_semester').val(questionSemId);

        });
    }


});

function resetSemQuestionSelects() {
    $('#id_user_semester >option').remove();
    $('#id_question_semester >option').remove();

    $('#id_user_semester').append($('<option></option>').val('').html('---------'));
    $('#id_question_semester').append($('<option></option>').val('').html('---------'));
}

function semester_change(semId) {
    resetSemQuestionSelects();
    $.ajax({
            "type"     : "GET",
            "url"      : "/admin_semester_choices/?semester_id="+semId,
            "dataType" : "json",
            "cache"    : false,
            "success"  : function(json) {
                studentList = json[0];
                questionList = json[1];

                for(var j = 0, len=studentList.length; j < len; j++){
                    $('#id_user_semester').append($('<option></option>').val(studentList[j].usersemester).html(studentList[j].student_name));
                }

                for(var j = 0, len=questionList.length; j < len; j++){
                    $('#id_question_semester').append($('<option></option>').val(questionList[j].questionsemester).html(questionList[j].question_title));
                }
                defer.resolve();
            }

    });

}

