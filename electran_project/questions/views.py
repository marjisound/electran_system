from django.contrib import messages
from django.http import HttpResponse
from management.models import Question
from django.template import Template, RequestContext
from django.core.exceptions import ObjectDoesNotExist
import os


# @login_required()
def all_questions(request, slug=None):
    pass
    try:
        class_exist = Question.objects.get(slug__exact=slug)
    except ObjectDoesNotExist:
        return HttpResponse('no')
    else:
        question_class_name = class_exist.question_class
        question = __import__('questions.custom.question_classes.' + question_class_name, globals(), locals(), ['Question'], 0)
        question_class = getattr(question, 'Question')
        question_instance = question_class()

        if request.method == 'POST':
            student_answer = request.POST.get('answer')
            program_random_value = request.session.__getitem__('program_random_value')
            user_random_value = question_instance.generate_user_random_display(program_random_value)
            is_valid = question_instance.is_valid(student_answer)
            if is_valid:
                expected_answer = question_instance.expected_answer(program_random_value)
                test_answer = question_instance.test_answer(student_answer, expected_answer)
                if test_answer:
                    messages.success(request, question_instance.correct_answer_message)
                else:
                    messages.error(request, question_instance.wrong_answer_message)

                context = {'random_value': user_random_value,
                           'answer': student_answer,
                           'correct_answer': expected_answer,
                           'is_form': False,
                           'result': test_answer}
                return create_http_response(request, question_class_name, context)

            else:
                messages.error(request, question_instance.wrong_format_message)
        else:
            program_random_value = question_instance.generate_random()
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

