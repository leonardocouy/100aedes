from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    url(r'^$', views.UserCreateView.as_view(), name='user'),
    url(r'^(?P<pk>[0-9]+)$', views.UserUpdateView.as_view(), name='user-update'),
    url(r'^auth$', obtain_jwt_token, name='auth-user'),
]