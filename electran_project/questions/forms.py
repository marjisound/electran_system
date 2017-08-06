from django import forms


class AddUsersToSemesterForm(forms.Form):

    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label='Select semester')
    file = forms.FileField(label='Upload your Excel file Here')
