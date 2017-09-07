from django.contrib import admin
from .forms import UserQuestionSemesterForm
from .models import (QuestionCategory,
                     Question,
                     Semester,
                     QuestionSemester,
                     UserSemester,
                     Mark,
                     Module,
                     UserQuestionSemester)

# Register your models here.
admin.site.register(QuestionCategory)
admin.site.register(Module)


class QuestionSemesterAdmin(admin.ModelAdmin):
    list_filter = ('semester', 'question_visibility')

admin.site.register(QuestionSemester, QuestionSemesterAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('category', 'question_class')

admin.site.register(Question, QuestionAdmin)


class MarkAdmin(admin.ModelAdmin):
    list_filter = ('user_semester__semester', 'user_semester__user', 'final_mark', 'question_semester__question')
    list_display = ('user_semester', 'question_semester', 'final_mark', 'mark_datetime')
    search_fields = ['user_semester__user__student_no', 'user_semester__user__email']

admin.site.register(Mark, MarkAdmin)


class SemesterAdmin(admin.ModelAdmin):
    list_filter = ('sem_is_active', 'sem_year', 'sem_month', 'sem_module')

admin.site.register(Semester, SemesterAdmin)


class UserSemesterAdmin(admin.ModelAdmin):
    list_filter = ('user', 'semester', 'is_registered_for_semester')

admin.site.register(UserSemester, UserSemesterAdmin)


class UserQuestionSemesterAdmin(admin.ModelAdmin):
    list_filter = ('user_semester', 'question_semester')
    form = UserQuestionSemesterForm

    class Media:
        js = ['/static/js/admin_semester_change.js']


admin.site.register(UserQuestionSemester, UserQuestionSemesterAdmin)




