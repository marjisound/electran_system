from django.conf.urls import url
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^semester_create$', views.semester_create, name='semester_create'),
    url(r'^test/(?P<slug>[\w-]+)/$',views.test_view,name='test'),
    url(r'^semester_list',views.SemesterListView.as_view(), name='semester_list'),
    url(r'^(?P<pk>\d+)/$', views.semester_question_setup, name='sem_qus_setup'),
    url(r'^upload_users/(?P<pk>\d+)/$', views.add_users_to_semester, name='upload_users'),
    url(r'^api/data/$',views.get_data, name='api-data'),
]
