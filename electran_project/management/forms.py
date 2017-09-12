from django import forms
from .models import Semester, QuestionSemester, Question, QuestionCategory, UserQuestionSemester


class NewSemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['sem_year', 'sem_month', 'sem_module', 'sem_is_active']


QUESTION_CHOICES = {}


class AddUsersToSemesterForm(forms.Form):

    file = forms.FileField(label='Upload your Excel file Here')


class UserQuestionSemesterForm(forms.ModelForm):

    semester = forms.ModelChoiceField(queryset=Semester.objects.all())

    class Meta:
        model = UserQuestionSemester
        fields = ['semester', 'user_semester', 'question_semester', 'question_deadline']

    def __init__(self, *args, **kwargs):
        super(UserQuestionSemesterForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and hasattr(kwargs['instance'], 'user_semester'):
            initial_sem_id = kwargs['instance'].user_semester.semester_id
            self.fields['semester'].initial = initial_sem_id












