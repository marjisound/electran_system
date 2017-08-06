from django.contrib import admin
from .models import QuestionCategory, Question, Semester, QuestionSemester, UserSemester

# Register your models here.
admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Semester)
admin.site.register(QuestionSemester)
admin.site.register(UserSemester)
