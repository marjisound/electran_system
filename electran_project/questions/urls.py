from django.conf.urls import url
from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.all_questions, name='all_questions'),
    # url(r'^(?P<question_class>[hex_to_binary])/$', views.hex_to_binary_conversion_view, name='test'),
    # url(r'^(?P<pk>\d+)/$', views.semester_question_setup, name='sem_qus_setup'),
    # url(r'^(?P<pk>\d+)/$', views.semester_question_setup, name='sem_qus_setup'),
]
