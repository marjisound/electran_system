from django.contrib import admin
from .models import QuestionCategory, Question, Semester, QuestionSemester, UserSemester, Mark

# Register your models here.
admin.site.register(QuestionCategory)


admin.site.register(QuestionSemester)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('category', 'question_class')

admin.site.register(Question, QuestionAdmin)


class MarkAdmin(admin.ModelAdmin):
    list_filter = ('question_semester', 'user_semester')

admin.site.register(Mark, MarkAdmin)


class SemesterAdmin(admin.ModelAdmin):
    list_filter = ('sem_is_active', 'sem_year', 'sem_month')

admin.site.register(Semester, SemesterAdmin)


class UserSemesterAdmin(admin.ModelAdmin):
    list_filter = ('user', 'semester', 'is_registered_for_semester')

admin.site.register(UserSemester, UserSemesterAdmin)