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
    txt_user_semester = forms.CharField(widget=forms.HiddenInput)
    txt_question_semester = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = UserQuestionSemester
        fields = ['semester', 'user_semester', 'question_semester', 'question_deadline']

    def __init__(self, *args, **kwargs):
        super(UserQuestionSemesterForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and hasattr(kwargs['instance'], 'user_semester'):
            initial_sem_id = kwargs['instance'].user_semester.semester_id
            initial_user_sem_id = kwargs['instance'].user_semester_id
            initial_question_sem_id = kwargs['instance'].question_semester_id
            self.fields['semester'].initial = initial_sem_id
            self.fields['txt_user_semester'].initial = initial_user_sem_id
            self.fields['txt_question_semester'].initial = initial_question_sem_id












