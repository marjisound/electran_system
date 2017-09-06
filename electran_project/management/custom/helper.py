from django.db.models import Max, OuterRef, Exists, Q, F, Subquery, IntegerField
from django.db import models, connection
from management.models import Mark, UserQuestionSemester, Question


def get_questions_with_mark(sem_id=None, user_id=None):



    # # mark before deadline sub queries
    # subquery_before_deadline = \
    #     UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
    #                                         question_semester_id__exact=OuterRef('question_semester'),
    #                                         question_deadline__gte=OuterRef('mark_datetime')).values('question_deadline')
    #
    # marks_before_deadline = Mark.objects.filter(
    #                                             question_semester__semester_id__exact=OuterRef('questionsemester__semester'),
    #                                             user_semester_id__exact=OuterRef('semester__usersemester'),
    #                                             question_semester__question_id=OuterRef('pk'),
    #                                             )
    #
    # sum_before_deadline= marks_before_deadline.annotate(subquery=Exists(subquery_before_deadline)).filter(
    #     Q(mark_datetime__lte=F('question_semester__question_deadline')) | Q(subquery=True))\
    #     .annotate(max_mark_before=Max('final_mark')).values('max_mark_before').order_by('-max_mark_before')
    #
    # # mark after deadline sub queries
    # exception_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
    #                                                          question_semester_id__exact=OuterRef('question_semester')
    #                                                          ).values('question_deadline')
    #
    # marks_after_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
    #                                                            question_semester_id__exact=OuterRef('question_semester'),
    #                                                            question_deadline__lt=OuterRef('mark_datetime')
    #                                                            ).values('question_deadline')
    #
    # sub_before_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=OuterRef('user_semester'),
    #                                                           question_semester_id__exact=OuterRef('question_semester'),
    #                                                           question_deadline__gte=OuterRef('mark_datetime')
    #                                                           ).values('question_deadline')
    #
    # mark_before_deadline = Mark.objects.filter(
    #                                            question_semester_id__exact=OuterRef('question_semester'),
    #                                            user_semester_id__exact=OuterRef('user_semester'),
    #                                            final_mark__gte=OuterRef('final_mark')
    #                                            ).annotate(mark_pre_deadline=Exists(sub_before_deadline)).filter(
    #     Q(mark_datetime__lte=F('question_semester__question_deadline')) | Q(mark_pre_deadline=True)
    # ).values('final_mark')
    #
    # sum_after_deadline = Mark.objects.filter(
    #                                          question_semester__semester_id__exact=OuterRef('semester'),
    #                                          user_semester_id__exact=OuterRef('semester__usersemester'),
    #                                          question_semester__question_id=OuterRef('pk'),
    #                                          ).annotate(exception_deadline=~Exists(exception_deadline),
    #                                                     after_deadline=Exists(marks_after_deadline),
    #                                                     before_deadline=~Exists(mark_before_deadline)).filter(
    #                                          Q(Q(mark_datetime__gt=F('question_semester__question_deadline'),
    #                                              exception_deadline=True) |
    #                                              Q(after_deadline=True)),
    #                                          Q(before_deadline=True)).annotate(max_mark_after=Max('final_mark')
    #                                                                            ).values('max_mark_after').order_by('-max_mark_after')
    #
    # # The parent query
    # questions_with_mark = Question.objects.filter(questionsemester__question_visibility__exact=True,
    #                                               questionsemester__semester_id__exact=sem_id,
    #                                               semester__usersemester__user_id__exact=user_id,
    #                                               semester__sem_is_active=True).annotate(
    #                                                         max_mark_after=Subquery(sum_after_deadline[:1], output_field=IntegerField()),
    #                                                         max_mark_before=Subquery(sum_before_deadline[:1], output_field=IntegerField())).values(
    #                                                                         'question_title',
    #                                                                         'id',
    #                                                                         'category_id',
    #                                                                         'semester__sem_year',
    #                                                                         'semester__sem_month',
    #                                                                         'semester__sem_module__module_code',
    #                                                                         'mark_max_value',
    #                                                                         'max_mark_after',
    #                                                                         'max_mark_before',
    #                                                                         'order',
    #                                                                         'slug',
    #                                                                         'questionsemester__question_deadline',
    #                                                                         'questionsemester__userquestionsemester__question_deadline',
    #                                                                         )

    cur = connection.cursor()
    cur.callproc('questions_with_mark', [sem_id, user_id])
    questions_with_mark = dictfetchall(cur)
    # cur.close()

    # questions_with_mark = Question.objects.raw(my_query, [user_id, sem_id])

    return questions_with_mark


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

