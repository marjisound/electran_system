
var $ = django.jQuery.noConflict();
var defer = $.Deferred();
$(document).ready(function () {

    var userSemId = $('#id_user_semester').val();
    var questionSemId = $('#id_question_semester').val();

    resetSemQuestionSelects();
    $('#id_semester').change(function () {
        semester_change($(this).val());
    });

    if ($('#id_semester') && $('#id_semester').val()) {
        semId = $('#id_semester').val();

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
                var studentList = json[0];
                var questionList = json[1];

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

