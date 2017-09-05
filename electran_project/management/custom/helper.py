from django.db.models import Max, OuterRef, Exists, Q, Sum, F, Subquery, IntegerField
from management.models import QuestionSemester, Mark, UserQuestionSemester, Question


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


def get_questions_with_mark(sem_id=None, user_id=None):
    # mark before deadline
    subquery_before_deadline = \
        UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
                                            question_semester_id__exact=OuterRef('question_semester'),
                                            question_deadline__gte=OuterRef('mark_datetime')).values('question_deadline')

    marks_before_deadline = Mark.objects.filter(
                                                question_semester__semester_id__exact=OuterRef('questionsemester__semester'),
                                                user_semester_id__exact=OuterRef('semester__usersemester'),
                                                question_semester__question_id=OuterRef('pk'),
                                                )

    sum_before_deadline= marks_before_deadline.annotate(subquery=Exists(subquery_before_deadline)).filter(
        Q(mark_datetime__lte=F('question_semester__question_deadline')) | Q(subquery=True))\
        .annotate(max_mark_before=Max('final_mark')).values('max_mark_before').order_by('-max_mark_before')



    # mark after deadline
    exception_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
                                                             question_semester_id__exact=OuterRef('question_semester')
                                                             ).values('question_deadline')

    marks_after_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
                                                               question_semester_id__exact=OuterRef('question_semester'),
                                                               question_deadline__lt=OuterRef('mark_datetime')
                                                               ).values('question_deadline')

    sub_before_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
                                                              question_semester_id__exact=OuterRef('question_semester'),
                                                              question_deadline__gte=OuterRef('mark_datetime')
                                                              ).values('question_deadline')

    mark_before_deadline = Mark.objects.filter(
                                               question_semester_id__exact=OuterRef('question_semester'),
                                               user_semester_id__exact=OuterRef('user_semester'),
                                               final_mark__gte=OuterRef('final_mark')
                                               ).annotate(mark_pre_deadline=Exists(sub_before_deadline)).filter(
        Q(mark_datetime__lte=F('question_semester__question_deadline')) | Q(mark_pre_deadline=True)
    ).values('final_mark')

    sum_after_deadline = Mark.objects.filter(
                                             question_semester__semester_id__exact=OuterRef('semester'),
                                             user_semester_id__exact=OuterRef('semester__usersemester'),
                                             question_semester__question_id=OuterRef('pk'),
                                             ).annotate(exception_deadline=~Exists(exception_deadline),
                                                        after_deadline=Exists(marks_after_deadline),
                                                        before_deadline=~Exists(mark_before_deadline)).filter(
                                             Q(Q(mark_datetime__gt=F('question_semester__question_deadline'),
                                                 exception_deadline=True) |
                                                 Q(after_deadline=True)),
                                             Q(before_deadline=True)).annotate(max_mark_after=Max('final_mark')
                                                                               ).values('max_mark_after').order_by('-max_mark_after')

    questions_with_mark = Question.objects.filter(questionsemester__question_visibility__exact=True,
                                                  questionsemester__semester_id__exact=sem_id,
                                                  semester__usersemester__user_id__exact=user_id,
                                                  semester__sem_is_active=True).annotate(
                                                            max_mark_after=Subquery(sum_after_deadline[:1], output_field=IntegerField()),
                                                            max_mark_before=Subquery(sum_before_deadline[:1], output_field=IntegerField())).values(
                                                                            'question_title',
                                                                            'id',
                                                                            'category_id',
                                                                            'semester__sem_year',
                                                                            'semester__sem_month',
                                                                            'semester__sem_module__module_code',
                                                                            'mark_max_value',
                                                                            'max_mark_after',
                                                                            'max_mark_before',
                                                                            'order',
                                                                            'slug',
                                                                            'questionsemester__question_deadline',
                                                                            'questionsemester__userquestionsemester__question_deadline'
                                                                            )

    return questions_with_mark




