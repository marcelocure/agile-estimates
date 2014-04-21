from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import settings
from aep import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^main/$', views.index, name='index'),
    url(r'^$', views.index, name='index'), 
    url(r'^aep/$', views.index, name='aep'),
    (r'^aep/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
