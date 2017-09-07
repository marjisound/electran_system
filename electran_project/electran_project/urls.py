"""electran_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from management import views
from django.views.defaults import page_not_found


urlpatterns = [
    url(r'^$', views.homePage, name='home'),
    url(r'^management/', include('management.urls', namespace='management')),
    url(r'^questions/', include('questions.urls', namespace='questions')),
    url(r'^admin_semester_choices/', views.admin_semester_choices),
    url(r'^admin/', admin.site.urls),
    url(r'^account/confirm-email/$', page_not_found, {'exception': Exception('Not Found')}),
    url(r'^account/', include('allauth.urls')),



]
