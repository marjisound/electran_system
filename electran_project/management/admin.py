from django.contrib import admin
from .models import QuestionCategory, Question, Semester, QuestionSemester, UserSemester

# Register your models here.
admin.site.register(QuestionCategory)

admin.site.register(Semester)
admin.site.register(QuestionSemester)
admin.site.register(UserSemester)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('category', 'question_class')

admin.site.register(Question, QuestionAdmin)