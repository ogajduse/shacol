from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.colls, name='colls'),
    url(r'^filtering/$', views.filtering, name='filtering'),
]
