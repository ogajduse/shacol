from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.colls, name='colls'),
    url(r'^filtering/$', views.filtering, name='filtering'),
    url(r'^graphs/$', views.graphs, name='graphs'),
    url(r'^delete/$', views.delete, name='delete'),
]
