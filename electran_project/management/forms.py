from django import forms
from .models import Semester, QuestionSemester, Question, QuestionCategory


class NewSemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['sem_year', 'sem_month', 'sem_module', 'sem_is_active']


QUESTION_CHOICES = {}


class AddUsersToSemesterForm(forms.Form):

    # semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label='Select semester')
    file = forms.FileField(label='Upload your Excel file Here')
