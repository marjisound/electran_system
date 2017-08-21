from django.contrib import messages
from django.http import HttpResponse
from management.models import Question, QuestionSemester, Mark, UserSemester
from django.template import Template, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import os
import json
import datetime
from django.utils import timezone


# @login_required()
def all_questions(request, slug=None):
    try:
        current_question = Question.objects.get(slug__exact=slug)
        question_semester = QuestionSemester.objects.filter(question__id=current_question.id, semester__sem_is_active=True)
        if len(question_semester) != 1:
            return HttpResponse('no')
        user_semester = UserSemester.objects.get(user_id=request.user.id, semester_id=question_semester[0].semester_id)

    except ObjectDoesNotExist:
        return HttpResponse('no')
    else:
        # List of unmarked questions in active semester in descending order
        user_marks = Mark.objects.filter(
            user_semester__user__id=request.user.id,
            final_mark=None,
            user_semester__semester__sem_is_active=True).order_by('-click_datetime')

        # *************** getting the specific question file based on question class name field in db ***********
        question_class_name = current_question.question_class
        question = __import__('questions.custom.question_classes.' + question_class_name, globals(), locals(), ['Question'], 0)
        question_class = getattr(question, 'Question')
        question_instance = question_class()

        # create random value
        program_random_value = question_instance.generate_random()
        program_random_value_json = json.dumps(program_random_value)

        # *************** dealing with the previous unanswered questions ***********

        if user_marks:
            user_mark_obj = user_marks[0]
            time_diff = timezone.now() - user_mark_obj.click_datetime
            if time_diff > datetime.timedelta(minutes=15):

                update_mark_zero(user_marks[0].id)
                clear_session(request, ['program_random_value', 'qus_sem_id'])
                create_save_new_mark(question_semester[0], user_semester, program_random_value_json)
                # to do: create random here
                if request.POST:
                    return create_http_response(request, 'invalid_question', context={
                        'slug': slug,
                        'type': 'expire'
                    })
            else:
                not_answered_slug = list(
                    user_marks.values('question_semester__question__slug'))[0]['question_semester__question__slug']

                not_answered_qus_sem_id = list(user_marks.values('question_semester'))[0]['question_semester']

                # check if session is empty
                if not request.session.__contains__('program_random_value'):
                    update_mark_zero(user_marks[0].id)
                    create_save_new_mark(question_semester[0], user_semester, program_random_value_json)
                    if request.POST:
                        return create_http_response(request, 'invalid_question', context={
                            'slug': slug,
                            'type': 'error'
                        })

                else:
                    if not_answered_qus_sem_id == request.session.__getitem__('qus_sem_id'):
                        if not_answered_slug == slug:
                            program_random_value = request.session.__getitem__('program_random_value')
                        else:
                            if request.POST:
                                return create_http_response(request, 'invalid_question', context={
                                    'slug': slug,
                                    'type': 'error'
                                })
                            else:
                                messages.error(request,
                                               ('This question was not answered. You can '
                                                'go to a new question after answering this question'))
                                return redirect('questions:all_questions', slug=not_answered_slug)
                    else:
                        update_mark_zero(user_marks[0].id)
                        create_save_new_mark(question_semester[0], user_semester, program_random_value_json)
                        clear_session(request, ['program_random_value', 'qus_sem_id'])
                        if request.POST:
                            return create_http_response(request, 'invalid_question', context={
                                'slug': slug,
                                'type': 'error'
                            })

                        # to do: create random here

        else:
            if request.POST:
                return create_http_response(request, 'invalid_question', context={
                    'slug': slug,
                    'type': 'error'
                })
            create_save_new_mark(question_semester[0], user_semester, program_random_value_json)
            # to do: create random here

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

            user_random_value = question_instance.generate_user_random_display(program_random_value)
            is_valid = question_instance.is_valid(student_answer)
            if is_valid:
                expected_answer = question_instance.expected_answer(program_random_value)
                display_expected_answer = question_instance.expected_answer_display_format(expected_answer)
                test_answer = question_instance.test_answer(student_answer, expected_answer)
                student_answer_json = json.dumps(student_answer)
                correct_answer_json = json.dumps(expected_answer)
                if test_answer:
                    user_mark = 1
                    messages.success(request, question_instance.correct_answer_message)
                else:
                    user_mark = 0
                    messages.error(request, question_instance.wrong_answer_message)

                updated_mark = Mark.objects.get(id=user_marks[0].id)
                updated_mark.user_answer = student_answer_json
                updated_mark.final_mark = user_mark
                updated_mark.correct_answer = correct_answer_json
                updated_mark.mark_datetime = timezone.now()

                updated_mark.save(force_update=True)
                clear_session(request, ['program_random_value', 'qus_sem_id'])

                context = {'random_value': user_random_value,
                           'answer': student_answer,
                           'correct_answer': display_expected_answer,
                           'is_form': False,
                           'result': test_answer,
                           'slug': slug}

                if hasattr(question_instance, 'display_correct'):
                    context['display_correct'] = question_instance.display_correct

                return create_http_response(request, question_class_name, context)

            else:
                messages.error(request, question_instance.wrong_format_message)
        else:
            request.session.__setitem__('program_random_value', program_random_value)
            request.session.__setitem__('qus_sem_id', question_semester[0].id)
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


def update_mark_zero(mark_id):
    updated_mark = Mark.objects.get(id=mark_id)
    updated_mark.final_mark = 0
    updated_mark.mark_datetime = timezone.now()
    updated_mark.save(force_update=True)


def clear_session(request, value):
    for item in value:
        if request.session.__contains__(item):
            request.session.__delitem__(item)


def create_save_new_mark(question_semester, user_semester, program_random_value_json):
    mark_record = Mark(question_semester=question_semester,
                       user_semester=user_semester,
                       question_parameters=program_random_value_json)

    mark_record.save()


