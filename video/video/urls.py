"""video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url
from django.views.static import serve

from search import views as search_views
from user import views as user_views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^$', search_views.search),
    # url(r'^login/$',user_views.login),
    # url(r'^logon/$', user_views.logon),
    # url(r'^input/$', search_views.input),
    # url(r'^search/$', search_views.search),
    url(r'^project/$', search_views.project),
    url(r'^list/$', search_views.list),
    # url(r'^logout', user_views.logout),
    # url(r'^userlist', search_views.userlist),
    # url(r'^matchlist', search_views.matchlist),
    # url(r'^update', search_views.update),
    # url(r'^inputmatch/$', search_views.inputmatch),
]
