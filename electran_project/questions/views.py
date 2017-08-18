from django.contrib import messages
from django.http import HttpResponse
from management.models import Question, QuestionSemester, Mark, UserSemester
from django.template import Template, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
import os
import json
import datetime
from django.utils import timezone


# @login_required()
def all_questions(request, slug=None):
    try:
        class_exist = Question.objects.get(slug__exact=slug)
        question_semester = QuestionSemester.objects.filter(question__id=class_exist.id, semester__sem_is_active=True)
        user_semester = UserSemester.objects.get(user_id=request.user.id, semester_id=question_semester[0].semester_id)
        # if len(question_semester) != 1:
        #     return HttpResponse('no')

    except ObjectDoesNotExist:
        return HttpResponse('no')
    else:

        # *************** dealing with the previous unanswered questions ***********
        # user_marks = Mark.objects.filter(
        #     user_semester__user__id=request.user.id, final_mark=None).order_by('-click_datetime')

        # if user_marks:
        #     user_mark = user_marks[0]
        #     time_diff = timezone.now() - user_mark.click_datetime
        #     if time_diff > datetime.timedelta(minutes=15):
        #         user_mark.final_mark = 0
        #         user_mark.save()
        #     else:
        #         return HttpResponse('no')

        # *************** getting the specific question file based on question class name field in db ***********
        question_class_name = class_exist.question_class
        question = __import__('questions.custom.question_classes.' + question_class_name, globals(), locals(), ['Question'], 0)
        question_class = getattr(question, 'Question')
        question_instance = question_class()

        if request.method == 'POST':
            if hasattr(question_instance, 'ANSWER_TYPE'):
                if question_instance.ANSWER_TYPE == 'multiple':
                    student_answer = {}
                    for item in request.POST.keys():
                        if item.startswith('answer'):
                            student_answer[item] = request.POST.get(item)
                else:
                    student_answer = request.POST.get('answer')
            else:
                student_answer = request.POST.get('answer')

            program_random_value = request.session.__getitem__('program_random_value')
            user_random_value = question_instance.generate_user_random_display(program_random_value)
            is_valid = question_instance.is_valid(student_answer)
            if is_valid:
                expected_answer = question_instance.expected_answer(program_random_value)
                display_expected_answer = question_instance.expected_answer_display_format(expected_answer)
                test_answer = question_instance.test_answer(student_answer, expected_answer)
                if test_answer:

                    messages.success(request, question_instance.correct_answer_message)
                else:
                    messages.error(request, question_instance.wrong_answer_message)

                context = {'random_value': user_random_value,
                           'answer': student_answer,
                           'correct_answer': display_expected_answer,
                           'is_form': False,
                           'result': test_answer}
                return create_http_response(request, question_class_name, context)

            else:
                messages.error(request, question_instance.wrong_format_message)
        else:
            program_random_value = question_instance.generate_random()
            program_random_value_json = json.dumps(program_random_value)
            # expected_answer_json = json.dumps(question_instance.expected_answer(program_random_value))
            # mark_record = Mark(question_semester=question_semester[0],
            #                    user_semester=user_semester,
            #                    question_parameters=program_random_value_json,
            #                    correct_answer=expected_answer_json)
            request.session.__setitem__('program_random_value', program_random_value)
            user_random_value = question_instance.generate_user_random_display(program_random_value)

        context = {'random_value': user_random_value, 'is_form': True}

        return create_http_response(request, question_class_name, context)


def create_http_response(request, question_class_name, context):
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(dir_path, 'templates') + '/questions/' + question_class_name + '.html'
    html_str = open(file_path, 'r').read()
    template = Template(html_str)
    request_context = RequestContext(request)
    request_context.push(context)
    return HttpResponse(template.render(request_context))

