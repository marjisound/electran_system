from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages
from validate_email import validate_email
from .models import (Question, QuestionCategory, Semester, QuestionSemester, UserSemester, Mark, UserQuestionSemester)
from .forms import NewSemesterForm, AddUsersToSemesterForm
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .custom import validation
from django.db import Error, IntegrityError
from django.conf import settings
from django.db.models import Count, Max, Sum, Exists, OuterRef, F, Q, Value, CharField
from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress
from .custom import helper
from django.db.models.functions import Concat
import django_excel
import json

from django.contrib.auth import get_user_model
User = get_user_model()


def home_get_questions(sem_id=None, user_id=None):

    categories = QuestionCategory.objects.order_by('order')

    questions = helper.get_questions_with_mark(sem_id=sem_id, user_id=user_id)
    questions_with_cats = []

    for cat in categories:
        qus_cat = {'cat': cat, 'qus': []}
        cat_has_qus = False
        for qus in questions:
            if qus['category_id'] == cat.id:
                cat_has_qus = True
                mark_before_deadline = qus['max_mark_before'] if qus['max_mark_before'] is not None else 0
                mark_after_deadline = qus['max_mark_after'] / 2 if qus['max_mark_after'] is not None else 0
                qus['max_mark'] = mark_before_deadline + mark_after_deadline

                if qus['user_deadline']:
                    qus['question_deadline'] = qus['user_deadline']
                else:
                    qus['question_deadline'] = qus['main_deadline']

                if isinstance(qus['max_mark'], float) and (qus['max_mark']).is_integer():
                    qus['max_mark'] = int(qus['max_mark'])

                qus_cat['qus'].append(qus)
        qus_cat['qus'] = sorted(qus_cat['qus'], key=lambda x: x['order'])
        if cat_has_qus:
            questions_with_cats.append(qus_cat)
    return questions_with_cats


def get_questions(semesters=[]):
    categories = QuestionCategory.objects.order_by('order')

    questions = Question.objects.order_by()

    questions_with_cats = []

    for cat in categories:
        qus_cat = {'cat': cat, 'qus': []}
        cat_has_qus = False
        for qus in questions:
            for sem in semesters:
                if sem.question.id == qus.id:
                    qus.checked = 'checked'
                    qus.deadline = sem.question_deadline
                    if sem.question_visibility:
                        qus.visible = 'checked'
                    if sem.mark__final_mark__count > 0:
                        qus.disable = ' disabled'
                    else:
                        qus.disable = ' '
            if qus.category.id == cat.id:
                cat_has_qus = True
                qus_cat['qus'].append(qus)
        qus_cat['qus'] = sorted(qus_cat['qus'], key=lambda x: x.order)
        if cat_has_qus:
            questions_with_cats.append(qus_cat)
    return questions_with_cats


@login_required()
def homePage(request):

    semester = None
    has_multiple_modules = True
    questions_with_cats = []

    sem_active_list = list(Semester.objects.filter(sem_is_active__exact=True, users__exact=request.user.id))

    if len(sem_active_list) == 0:
        if request.session.__contains__('active_semester_id'):
            request.session.__delitem__('active_semester_id')

    elif len(sem_active_list) == 1:
        semester = sem_active_list[0]
        request.session.__setitem__('active_semester_id', semester.id)
        questions_with_cats = home_get_questions(sem_id=semester.id, user_id=request.user.id)


    else:
        semester = sem_active_list[0]
        if request.method == 'POST':
            try:
                selected_semester_id = int(request.POST.get('semester_module'))

                if not selected_semester_id:
                    template = 'management/invalid_request.html'
                    return render(request, template, {'type': 'module_session_error'})

                if selected_semester_id > 0:

                    request.session.__setitem__('active_semester_id', selected_semester_id)

            except (ObjectDoesNotExist, ValueError, TypeError):
                template = 'management/invalid_request.html'
                return render(request, template, {'type': 'sem_not_active'})

        has_multiple_modules = True
        if request.session.__contains__('active_semester_id'):
            semester_id = request.session.__getitem__('active_semester_id')
            semester = Semester.objects.get(sem_is_active__exact=True,
                                            id=semester_id)

            questions_with_cats = home_get_questions(sem_id=semester_id, user_id=request.user.id)

    template = 'management/index.html'
    context_dict = {
        'que_cat': questions_with_cats,
        'semester': semester,
        'semester_list': sem_active_list,
        'has_multiple_modules': has_multiple_modules
    }
    return render(request, template, context_dict)


@staff_member_required
def semester_create(request):

    if request.method == 'POST':
        form = NewSemesterForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('home'))
        else:
            print('ERROR form invalid')
    else:
        form = NewSemesterForm()

    return render(request, 'management/semester_create.html',{
            'form': form
    })


@staff_member_required
def semester_question_setup(request, pk=None):
    existing_questions = QuestionSemester.objects.filter(semester_id=pk).annotate(Count('mark__final_mark'))

    if request.method == 'POST':

        question_chk_name = 'chk_question'
        checked_questions = request.POST.getlist(question_chk_name)

        for item in checked_questions:
            date_name = 'date_question_' + item
            date = request.POST.get(date_name)

            if validation.validate_date(date):
                question_found = existing_questions.filter(question_id=int(item))
                visible_name = 'visible_question_' + item
                visibility = request.POST.get(visible_name)
                if not visibility:
                    visibility = False
                elif visibility == 'True':
                    visibility = True

                if question_found:

                    new_obj = QuestionSemester.objects.get(id=question_found[0].id)
                    new_obj.question_deadline = date
                    new_obj.question_visibility = visibility
                    new_obj.save(force_update=True)

                else:

                    question_obj = Question.objects.get(id=int(item))
                    semester_obj = Semester.objects.get(id=int(pk))
                    new_obj = QuestionSemester(question=question_obj,
                                               semester=semester_obj,
                                               question_deadline=date,
                                               question_visibility=visibility)
                    new_obj.save()

            else:
                messages.error(request, 'Could not add questions. Date fields are required for checked questions')
                return HttpResponseRedirect(reverse('management:sem_qus_setup', kwargs={'pk': pk}))
        print(checked_questions)
        for question in existing_questions:
            print(question.question.id)
            if str(question.question.id) not in checked_questions:
                if question.mark__final_mark__count == 0:
                    print('delete')
                    new_obj = QuestionSemester.objects.get(id=question.id)
                    new_obj.delete()

        messages.success(request, 'Questions added successfully')
        return HttpResponseRedirect(reverse('home'))
    else:
        try:
            semester = Semester.objects.get(pk=pk)
            questions_with_cats = get_questions(existing_questions)
            context_dict = {
                'semester': semester,
                'que_cat': questions_with_cats,
            }
            return render(request,'management/semester_question_setup.html', context_dict)
        except Exception as e:
            raise Http404


@staff_member_required
def add_users_to_semester(request, pk=None):
    sem_users = UserSemester.objects.filter(semester_id=pk)
    if request.method == 'POST':
        form = AddUsersToSemesterForm(request.POST, request.FILES)
        if form.is_valid():
            semester_obj = Semester.objects.get(id=int(pk))

            file_handle = request.FILES['file']
            user_list_record = file_handle.get_records()
            user_titles_array = file_handle.get_array()[0]

            mandatory_titles = settings.STUDENTS_MANDATORY_FIELDS
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
                already_existing_users = []

                for student in user_list_record:
                    prepared_dict = {
                        'student_no': student[mandatory_titles['student_no']],
                        'email': student[mandatory_titles['email']],
                        'first_name': student[mandatory_titles['first_name']],
                        'last_name': student[mandatory_titles['last_name']],
                        'username': student[mandatory_titles['username']],
                        'password': User.objects.make_random_password()
                    }

                    empty_valued_titles, filled_value_titles = divide_empty_and_full_dic_values(prepared_dict)

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
                        obj = User.objects.get(student_no=prepared_dict['student_no'], email=prepared_dict['email'],
                                               username=prepared_dict['username'])
                        semester_user_obj, created = UserSemester.objects.get_or_create(user=obj, semester=semester_obj)
                        if created:
                            sem_user_added.append(semester_user_obj)
                        else:
                            already_existing_users.append(semester_user_obj)
                    except User.DoesNotExist:
                        try:
                            obj = User.objects.create(first_name=prepared_dict['first_name'],
                                                      last_name=prepared_dict['last_name'],
                                                      student_no=prepared_dict['student_no'],
                                                      email=prepared_dict['email'],
                                                      username=prepared_dict['username'],
                                                      password=prepared_dict['password'])

                            new_email = EmailAddress(user=obj,
                                                     email=prepared_dict['email'],
                                                     verified=True,
                                                     primary=True)
                            new_email.save()

                        except IntegrityError:
                            user_creation_error += error_message

                        except Error:
                            user_creation_error += error_message

                        else:
                            try:
                                reset_pass_form = ResetPasswordForm({'email': prepared_dict['email'], 'name': 'Asghar'})
                                if reset_pass_form.is_valid():
                                    reset_pass_form.save(request)

                                semester_user_obj = UserSemester.objects.create(user=obj, semester=semester_obj)
                                sem_user_created.append(semester_user_obj)
                            except IntegrityError:
                                user_add_sem_error += error_message

                            except Error:
                                user_add_sem_error += error_message

                create_specific_messages(request, user_creation_error, user_add_sem_error,
                                         sem_user_created, already_existing_users, user_list_record,
                                         semester_obj, sem_user_added)
            else:
                messages.error(request, message)

            new_form = AddUsersToSemesterForm()
            semester = Semester.objects.get(pk=pk)
            return render(request, 'management/upload_users.html', {'form': new_form, 'semester': semester,
                                                                    'users': sem_users})

    else:
        semester = Semester.objects.get(pk=pk)
        form = AddUsersToSemesterForm()
    return render(request, 'management/upload_users.html', {'form': form, 'semester': semester,
                                                            'users': sem_users})


def divide_empty_and_full_dic_values(prepared_dict):
    empty_valued_titles = []
    filled_value_titles = []
    for title, value in prepared_dict.items():
        if value == '':
            empty_valued_titles.append(title)
        if value != '' and title != 'password':
            filled_value_titles.append((title, value))
    return empty_valued_titles, filled_value_titles


def create_specific_messages(request, user_creation_error, user_add_sem_error,
                             sem_user_created, already_existing_users, user_list_record,
                             semester_obj, sem_user_added):

    if len(sem_user_created) > 0 and len(sem_user_added) > 0:
        messages.success(request, ('Out of {0} users, {1} users created and added and '
                                   '{3} existing users added to the semester {2}').format(
            len(user_list_record),
            len(sem_user_created),
            str(semester_obj),
            len(sem_user_added)))

    elif len(sem_user_created) > 0 and len(sem_user_added) == 0:
        messages.success(request, 'Out of {0} users, {1} users created and added to the semester {2}'.format(
            len(user_list_record),
            len(sem_user_created),
            str(semester_obj)))

    elif len(sem_user_created) == 0 and len(sem_user_added) > 0:
        messages.success(request, ('Out of {0} users, no new user created but '
                                   '{2} existing users added to the semester {1}').format(
            len(user_list_record),
            str(semester_obj),
            len(sem_user_added)))
    else:
        messages.error(request, 'No user was added to this semester')

    if len(already_existing_users) > 0:

        str_existing_users = ''
        for user in already_existing_users:
            str_existing_users += (str(user.user) + ' ')

        if len(already_existing_users) == 1:
            messages.error(request, 'User {0} already existed in this semester'.format(str_existing_users))
        else:
            messages.error(request,
                           'These users already existed in this semester: {0}'.format(str_existing_users))

    if user_creation_error:
        messages.error(request, ('System could not create these users because '
                                 'integrity of the database is affected: ' + user_creation_error[:-2]))
    if user_add_sem_error:
        messages.error(request, ('System could not add these users to semester because '
                                 'integrity of the database is affected: ' + user_add_sem_error[:-2]))


@method_decorator(staff_member_required, name='dispatch')
class SemesterListView(ListView):
    model = Semester
    template_name = 'management/semester_list_view.html'
    context_object_name = 'semesters'


@staff_member_required
def report_marks(request):

    selected_semester = None
    semester_students = None
    total_mark = None
    selected_sem_id = None
    if request.method == 'POST':
        if 'export_excel' in request.POST:
            selected_sem_id = request.POST.get('submitted_semester')
        else:
            selected_sem_id = request.POST.get('selectedSemester')

    if selected_sem_id:
        try:
            selected_semester = Semester.objects.get(id=selected_sem_id)
            # semester_students = UserSemester.objects.filter(semester_id__exact=selected_sem_id,
            #                                                 is_registered_for_semester__exact=True,
            #                                                 user__is_admin=False)
            semester_students = list(UserSemester.objects.filter(semester_id__exact=selected_sem_id))

            # Maximum achivable mark
            achievable_mark = Question.objects.filter(
                questionsemester__semester_id__exact=selected_sem_id).aggregate(Sum('mark_max_value'))
            for user_sem in semester_students:

                # mark before deadline
                subquery_before_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=user_sem.id,
                                                                               question_semester_id__exact=OuterRef(
                                                                                   'question_semester_id'),
                                                                               question_deadline__gte=OuterRef(
                                                                                   'mark_datetime'))

                sum_before_deadline = Mark.objects.filter(question_semester__question_visibility__exact=True,
                                                          question_semester__semester_id__exact=selected_sem_id,
                                                          user_semester_id__exact=user_sem.id,
                                                          ).annotate(subquery=Exists(subquery_before_deadline)).filter(
                            Q(mark_datetime__lte=F('question_semester__question_deadline')) | Q(subquery=True)).values(
                            'question_semester_id').annotate(max_mark=Max('final_mark')).aggregate(Sum('max_mark'))

                # mark after deadline
                exception_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=user_sem.id,
                                                                         question_semester_id__exact=OuterRef(
                                                                             'question_semester_id'))

                subquery_after_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=user_sem.id,
                                                                              question_semester_id__exact=OuterRef(
                                                                                  'question_semester_id'),
                                                                              question_deadline__lt=OuterRef(
                                                                                  'mark_datetime'))

                sub_before_deadline = UserQuestionSemester.objects.filter(user_semester_id__exact=user_sem.id,
                                                                          question_semester_id__exact=OuterRef('question_semester'),
                                                                          question_deadline__gte=OuterRef('mark_datetime')
                                                                          ).values('question_deadline')

                mark_before_deadline = Mark.objects.filter(question_semester__question_visibility__exact=True,
                                                           question_semester_id__exact=OuterRef('question_semester'),
                                                           user_semester_id__exact=user_sem.id,
                                                           final_mark__gte=OuterRef('final_mark')
                                                           ).annotate(mark_pre_deadline=Exists(sub_before_deadline)).filter(
                    Q(mark_datetime__lte=F('question_semester__question_deadline')) | Q(mark_pre_deadline=True)
                ).values('final_mark')

                sum_after_deadline = Mark.objects.filter(question_semester__question_visibility__exact=True,
                                                         question_semester__semester_id__exact=selected_sem_id,
                                                         user_semester_id__exact=user_sem.id,
                                                         ).annotate(exception_deadline=~Exists(exception_deadline),
                                                                    after_deadline=Exists(
                                                                         subquery_after_deadline),
                                                                    before_deadline=~Exists(mark_before_deadline)).filter(
                    Q(Q(mark_datetime__gt=F('question_semester__question_deadline'), exception_deadline=True) |
                    Q(after_deadline=True)),Q(before_deadline=True)).values('question_semester_id').annotate(
                                                            max_mark=Max('final_mark')).aggregate(Sum('max_mark'))

                user_sem.sum_before_deadline = sum_before_deadline['max_mark__sum'] if sum_before_deadline['max_mark__sum'] is not None else 0
                user_sem.sum_after_deadline = sum_after_deadline['max_mark__sum']/2 if sum_after_deadline['max_mark__sum'] is not None else 0

                if isinstance(user_sem.sum_after_deadline, float) and (user_sem.sum_after_deadline).is_integer():
                    user_sem.sum_after_deadline = int(user_sem.sum_after_deadline )
                user_sem.mark = user_sem.sum_before_deadline + user_sem.sum_after_deadline

            total_mark = achievable_mark
            if 'export_excel' in request.POST:
                return prepare_export(semester_students, selected_semester)

        except ObjectDoesNotExist:
            pass

    semester_list = Semester.objects.all()
    context_dict = {
        'semester_list': semester_list,
        'selected_semester': selected_semester,
        'semester_students': semester_students,
        'total_mark': total_mark,
        'selected_sem_id': int(selected_sem_id) if selected_sem_id else None

    }
    template = 'management/report_marks.html'
    return render(request, template, context_dict)


def prepare_export(students, semester):
    mark_list = []
    file_name = str(semester)
    for student in students:
        obj = {}
        obj['student_no'] = student.user.student_no
        obj['first_name'] = student.user.first_name
        obj['last_name'] = student.user.last_name
        obj['email'] = student.user.email
        obj['mark'] = student.mark
        obj['mark_before_deadline'] = student.sum_before_deadline
        obj['mark_after_deadline'] = student.sum_after_deadline
        mark_list.append(obj)

    return django_excel.make_response_from_records(records=mark_list, file_type='xlsx', status=200, file_name=file_name)


@staff_member_required
def admin_semester_choices(request):
    action_list_question = []
    action_list_user = []

    semester_id = request.GET.get('semester_id')

    question_semester_list = Question.objects.filter(questionsemester__semester_id__exact=semester_id).values('questionsemester', 'question_title')
    user_semester_list = User.objects.filter(usersemester__semester_id__exact=semester_id).annotate(
        student_name=Concat('first_name', Value(' '), 'last_name', Value('('), 'student_no', Value(')'), output_field=CharField())
    ).values('usersemester', 'student_name')

    [action_list_user.append(each) for each in user_semester_list]
    [action_list_question.append(each) for each in question_semester_list]

    action_list = [action_list_user, action_list_question]

    json_output = json.dumps(action_list)
    return HttpResponse(json_output)


