from django.conf.urls import url
from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.all_questions, name='all_questions'),

]
