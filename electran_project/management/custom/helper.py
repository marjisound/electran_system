from django.db.models import Max
from management.models import QuestionSemester, Mark


def get_max_mark_for_question(marks, qus):
    """
    This function can calculate the best mark a student has obtained for a question
    considering that after the deadline has passed the mark is halved
    :param marks: queryset from Mark table
    :param qus: a specific record in QuestionSemester table
    :return: dictionary
    """
    question_marks = marks.filter(question_semester__question_id=qus.question.id)
    before_deadline = question_marks.filter(mark_datetime__lte=qus.question_deadline)
    before_deadline_max = before_deadline.aggregate(Max('final_mark'))
    after_deadline = question_marks.filter(mark_datetime__gt=qus.question_deadline)
    after_deadline_max = after_deadline.aggregate(Max('final_mark'))
    max_mark = None
    if before_deadline_max['final_mark__max'] is not None:
        if after_deadline_max['final_mark__max'] is not None:
            max_mark = max(before_deadline_max['final_mark__max'], (after_deadline_max['final_mark__max'] / 2))
        else:
            max_mark = before_deadline_max['final_mark__max']
    elif after_deadline_max['final_mark__max'] is not None:
        max_mark = after_deadline_max['final_mark__max'] / 2

    if isinstance(max_mark, float):
        if max_mark.is_integer():
            max_mark = int(max_mark)

    return {
        'max_mark': max_mark,
        'before_deadline_max': before_deadline_max['final_mark__max'],
        'after_deadline_max': after_deadline_max['final_mark__max'],
        'before_deadline_marks': before_deadline,
        'after_deadline_marks': after_deadline
    }


def calculate_student_mark(user_sem_id, sem_id):
    """
    :param user_sem_id: id of a record from UserSemester table
    :param sem_id: id of a record from Semester table
    :return:
    """
    question_list = QuestionSemester.objects.filter(semester_id__exact=sem_id, question_visibility__exact=True)
    all_marks = Mark.objects.filter(user_semester_id__exact=user_sem_id,
                                    final_mark__isnull=False, )
    questions_weight = 0
    all_qus_mark = 0
    before_deadline_mark = 0
    after_deadline_mark = 0

    for question in question_list:
        max_mark_dictionary = get_max_mark_for_question(marks=all_marks, qus=question)
        qus_mark = max_mark_dictionary['max_mark']
        before_deadline_max = max_mark_dictionary['before_deadline_max']
        after_deadline_max = max_mark_dictionary['after_deadline_max']

        mark_max_value = question.question.mark_max_value
        questions_weight += mark_max_value

        if qus_mark is not None:
            all_qus_mark += qus_mark

        if before_deadline_max is not None:
            before_deadline_mark += before_deadline_max

        if after_deadline_max is not None:
            after_deadline_mark += after_deadline_max

    return {
        'all_qus_mark': all_qus_mark,
        'all_qus_max_mark': questions_weight,
        'before_deadline_mark': before_deadline_mark,
        'after_deadline_mark': after_deadline_mark,
    }


# def calculate_student_mark(user_sem_id, sem_id):
#     """
#     :param user_sem_id: id of a record from UserSemester table
#     :param sem_id: id of a record from Semester table
#     :return:
#     """
#     question_list = QuestionSemester.objects.filter(semester_id__exact=sem_id, question_visibility__exact=True)
#
#     all_marks = Mark.objects.filter(user_semester_id__exact=user_sem_id,
#                                     final_mark__isnull=False, )
#     questions_weight = 0
#     all_qus_mark = 0
#     before_deadline_mark = 0
#     after_deadline_mark = 0
#
#     for question in question_list:
#         marks = list(Mark.objects.filter(user_semester_id__exact=user_sem_id, final_mark__isnull=False, question_semester_id=question.id).order_by('final_mark'))
#
#         max_mark_dictionary = get_max_mark_for_question(marks=all_marks, qus=question)
#         qus_mark = max_mark_dictionary['max_mark']
#         before_deadline_max = max_mark_dictionary['before_deadline_max']
#         after_deadline_max = max_mark_dictionary['after_deadline_max']
#
#         mark_max_value = question.question.mark_max_value
#         questions_weight += mark_max_value
#
#         if qus_mark is not None:
#             all_qus_mark += qus_mark
#
#         if before_deadline_max is not None:
#             before_deadline_mark += before_deadline_max
#
#         if after_deadline_max is not None:
#             after_deadline_mark += after_deadline_max
#
#     return {
#         'all_qus_mark': all_qus_mark,
#         'all_qus_max_mark': questions_weight,
#         'before_deadline_mark': before_deadline_mark,
#         'after_deadline_mark': after_deadline_mark,
#     }



