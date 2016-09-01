from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.UserCreateView.as_view(), name='user'),
    url(r'^(?P<pk>[0-9]+)$', views.UserUpdateView.as_view(), name='user-update')
]
