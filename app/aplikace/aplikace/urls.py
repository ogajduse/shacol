from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'aplikace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('website.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^website/', include('website.urls')),
]
