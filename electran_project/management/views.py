from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from validate_email import validate_email
from .models import (Question, QuestionCategory, Semester, QuestionSemester, UserSemester)
from .forms import NewSemesterForm, AddUsersToSemesterForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .custom import validation
from django.db import Error, IntegrityError
from django.template import Context
from django.template import Template

from django.contrib.auth import get_user_model

User = get_user_model()


def get_questions(semesters=[]):
    categories = QuestionCategory.objects.order_by('order')
    questions = Question.objects.order_by()

    questions_with_cats = []

    for cat in categories:
        qus_cat = {'cat': cat, 'qus': []}
        for qus in questions:
            for sem in semesters:
                if sem['question_id'] == qus.id:
                    qus.checked = 'checked'
                    qus.deadline = sem['question_deadline']
                    if sem['question_visibility']:
                        qus.visible = 'checked'
            if qus.category.id == cat.id:
                qus_cat['qus'].append(qus)
        qus_cat['qus'] = sorted(qus_cat['qus'], key=lambda x: x.order)
        questions_with_cats.append(qus_cat)
    return questions_with_cats

@login_required()
def homePage(request):

    template = 'management/index.html'
    questions_with_cats = get_questions()
    context_dict = {
        'que_cat': questions_with_cats,
    }
    return render(request,template,context_dict)

@login_required()
def semester_create(request):

    if request.method == 'POST':
        form = NewSemesterForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return homePage(request)
        else:
            print('ERROR form invalid')
    else:
        form = NewSemesterForm()

    return render(request, 'management/semester_create.html',{
            'form': form
    })


# @login_required()
def semester_question_setup(request, pk=None):
    if request.method == 'POST':

        question_chk_name = 'chk_question'
        checked_questions = request.POST.getlist(question_chk_name)
        QuestionSemester.objects.filter(semester_id=pk).delete()

        for item in checked_questions:

            question_obj = Question.objects.get(id=int(item))
            semester_obj = Semester.objects.get(id=int(pk))
            date_name = 'date_question_' + item  # name of date input field in html for question_deadline
            date = request.POST.get(date_name)
            visible_name = 'visible_question_' + item  # name of checkbox input field for question_visibility
            visibility = request.POST.get(visible_name)

            if not visibility:
                visibility = False
            elif visibility == 'True':
                visibility = True

            if validation.validate_date(date):
                obj = QuestionSemester(question=question_obj,
                                       semester=semester_obj,
                                       question_deadline=date,
                                       question_visibility=visibility)
                obj.save()
            else:
                messages.error(request, 'Could not add questions. Date fields are required for checked questions')
                return HttpResponseRedirect(reverse('questions:sem_qus_setup', kwargs={'pk': pk}))
        messages.success(request, 'Questions added successfully')
        return homePage(request)
    else:
        try:
            semester = Semester.objects.get(pk=pk)
            qus_sem_detail = QuestionSemester.objects.filter(semester=pk).values()
            questions_with_cats = get_questions(qus_sem_detail)
            context_dict = {
                'semester': semester,
                'que_cat': questions_with_cats,
            }
            return render(request,'management/semester_question_setup.html', context_dict)
        except Exception as e:
            raise Http404


def add_users_to_semester(request):
    if request.method == 'POST':
        form = AddUsersToSemesterForm(request.POST, request.FILES)
        if form.is_valid():
            semester_obj = form.cleaned_data.get('semester')
            file_handle = request.FILES['file']
            user_list_record = file_handle.get_records()
            user_titles_array = file_handle.get_array()[0]

            mandatory_titles = {
                'first_name': 'First name',
                'last_name': 'Surname',
                'student_no': 'ID number',
                'email': 'Email address'
            }

            message = 'your Excel file does not have these titles:'
            excel_titles = []

            for key, value in mandatory_titles.items():
                if value not in user_titles_array:
                    message = message + (' ' + value + ',')
                    excel_titles.append(value)

            if len(excel_titles) == 0:
                user_creation_error = ''
                user_add_sem_error = ''
                sem_user_added = []  # list of users that already existed and were added to semester
                sem_user_created = []  # list of newly created users and added to semester

                for student in user_list_record:
                    prepared_dict = {
                        'student_no': student[mandatory_titles['student_no']],
                        'email': student[mandatory_titles['email']],
                        'first_name': student[mandatory_titles['first_name']],
                        'last_name': student[mandatory_titles['last_name']],
                        'password': User.objects.make_random_password()
                    }

                    empty_valued_titles = []
                    filled_value_titles = []

                    for title, value in prepared_dict.items():
                        if value == '':
                            empty_valued_titles.append(title)
                        if value != '' and title != 'password':
                            filled_value_titles.append((title, value))

                    if len(empty_valued_titles) > 0:
                        messages.error(request, ('The record with title \"{0}\" and'
                                                 ' value \"{1}\" has an empty value '
                                                 'for one or more mandatary field/fields').format(
                                                                                    filled_value_titles[0][0],
                                                                                    filled_value_titles[0][1]))
                        continue
                    elif not validate_email(student[mandatory_titles['email']]):
                        messages.error(request, ('System could not save the '
                                                 'record with email \"{0}\" because the email address does not have'
                                                 'a valid format').format(student[mandatory_titles['email']]))
                        continue

                    error_message = '\"{0}({1})\", '.format(prepared_dict['email'], prepared_dict['student_no'])
                    try:
                        obj = User.objects.get(student_no=prepared_dict['student_no'], email=prepared_dict['email'])
                        semester_user_obj, created = UserSemester.objects.get_or_create(user=obj, semester=semester_obj)
                        if created:
                            sem_user_added.append(semester_user_obj)
                    except User.DoesNotExist:
                        try:
                            obj = User.objects.create(first_name=prepared_dict['first_name'],
                                                      last_name=prepared_dict['last_name'],
                                                      student_no=prepared_dict['student_no'],
                                                      email=prepared_dict['email'],
                                                      password=prepared_dict['password'])

                        except IntegrityError:
                            user_creation_error += error_message

                        except Error:
                            user_creation_error += error_message

                        else:
                            try:
                                semester_user_obj = UserSemester.objects.create(user=obj, semester=semester_obj)
                                sem_user_created.append(semester_user_obj)
                            except IntegrityError:
                                user_add_sem_error += error_message

                            except Error:
                                user_add_sem_error += error_message

                if user_creation_error:
                    messages.error(request, ('System could not create these users because '
                                             'integrity of the database is affected: ' + user_creation_error[:-2]))
                elif user_add_sem_error:
                    messages.error(request, ('System could not add these users to semester because '
                                             'integrity of the database is affected: ' + user_add_sem_error[:-2]))

                messages.success(request, ('Out of {0} users, {1} users created and added and '
                                           '{3} existing users added to the semester {2}').format(
                                                                            len(user_list_record),
                                                                            len(sem_user_created),
                                                                            str(semester_obj),
                                                                            len(sem_user_added)))
            else:
                messages.error(request, message)

            new_form = AddUsersToSemesterForm()
            return render(request, 'management/upload_users.html', {'form': new_form})

    else:
        form = AddUsersToSemesterForm()
    return render(request, 'management/upload_users.html', {'form': form})


# @login_required()
class SemesterListView(ListView):
    model = Semester
    template_name = 'management/semester_list_view.html'
    context_object_name = 'semesters'


    # def get_context_data(self, **kwargs):
    #     context = super(SemesterListView, self).get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

# @login_required()
def test_view(request, pk=None):
    pass
    # test = HexToBinaryConversion()
    # random_hex = test.generate_random()
    # expected_answer = test.expected_answer(random_hex)
    # return render(request,'management/test.html',{'form':test})
