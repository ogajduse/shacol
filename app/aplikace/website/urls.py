from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.colls, name='colls'),
    url(r'^method/$', views.method, name='method'),
]
