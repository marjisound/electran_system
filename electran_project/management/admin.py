from django.contrib import admin
from .models import QuestionCategory, Question, Semester, QuestionSemester, UserSemester, Mark, Module

# Register your models here.
admin.site.register(QuestionCategory)
admin.site.register(Module)


admin.site.register(QuestionSemester)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('category', 'question_class')

admin.site.register(Question, QuestionAdmin)


class MarkAdmin(admin.ModelAdmin):
    list_filter = ('user_semester__semester', 'user_semester__user', 'final_mark', 'question_semester')
    list_display = ('user_semester', 'question_semester', 'final_mark', 'mark_datetime')
    search_fields = ['user_semester__user__student_no', 'user_semester__user__email']

admin.site.register(Mark, MarkAdmin)


class SemesterAdmin(admin.ModelAdmin):
    list_filter = ('sem_is_active', 'sem_year', 'sem_month', 'sem_module')

admin.site.register(Semester, SemesterAdmin)


class UserSemesterAdmin(admin.ModelAdmin):
    list_filter = ('user', 'semester', 'is_registered_for_semester')

admin.site.register(UserSemester, UserSemesterAdmin)