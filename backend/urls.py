"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin


from backend.core import urls as core_urls
from backend.reports import urls as reports_urls
from backend.accounts import urls as users_urls


# change admin title
admin.site.site_header = settings.ADMIN_SITE_HEADER
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(core_urls)),

    # API's
    url(r'^api/v1/reports/', include(reports_urls)),
    url(r'^api/v1/users/', include(users_urls))
]
