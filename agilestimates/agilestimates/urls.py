from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import settings
from aep import views

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^main/$', views.index, name='index'),
    url(r'^aep/save_profile', views.save_profile, name="aep/profiles"),
    url(r'^aep/save_customer', views.save_customer, name="aep/customers"),
    url(r'^aep/save_user', views.save_user, name="aep/users"),
    url(r'^aep/save_sprint', views.save_sprint, name="aep/users"),
    url(r'^aep/save_project', views.save_project, name="aep/projects"),
    url(r'^aep/save_edit_profile', views.save_edit_profile, name="aep/profiles"),
    url(r'^aep/save_edit_customer', views.save_edit_customer, name="aep/customers"),
    url(r'^aep/save_edit_user', views.save_edit_user, name="aep/users"),
    url(r'^aep/save_edit_project', views.save_edit_project, name="aep/projects"),
    url(r'^aep/delete_profile/(?P<id>\d+)/$', views.delete_profile, name="aep/profiles"),
    url(r'^aep/delete_customer/(?P<id>\d+)/$', views.delete_customer, name="aep/customers"),
    url(r'^aep/delete_user/(?P<id>\d+)/$', views.delete_user, name="aep/users"),
    url(r'^aep/delete_project/(?P<id>\d+)/$', views.delete_project, name="aep/projects"),
    url(r'^aep/edit_profile/(?P<id>\d+)/$', views.edit_profile, name="aep/profiles"),
    url(r'^aep/edit_customer/(?P<id>\d+)/$', views.edit_customer, name="aep/customers"),
    url(r'^aep/edit_user/(?P<id>\d+)/$', views.edit_user, name="aep/users"),
    url(r'^aep/edit_project/(?P<id>\d+)/$', views.edit_project, name="aep/projects"),
    #url(r'^aep/add_user_project/(?P<id>\d+)/$', views.add_user_project, name="aep/projects"),
    url(r'^$', views.login, name='login'), 
    url(r'^aep/$', views.login, name="aep"),
    url(r'^aep/login_process', views.login_process, name="aep/login_process"),
    url(r'^aep/admin', views.admin, name="aep/admin"),
    url(r'^aep/logout', views.logout, name="aep/logout"),
    url(r'^aep/customers', views.customer, name="aep/customers"),
    url(r'^aep/profiles', views.profile, name="aep/profiles"),
    url(r'^aep/users', views.user, name="aep/users"),
    url(r'^aep/projects', views.project, name="aep/projects"),
    url(r'^aep/sprints', views.sprint, name="aep/sprints"),
    url(r'^aep/acharts', views.admin_charts, name="aep/admin_charts"),
    url(r'^aep/generate_chart', views.generate_chart, name="aep/generate_chart"),
    url(r'^aep/scan_project', views.scan, name="aep/scan"),
    url(r'^aep/scan_process', views.scan_process, name="aep/scan"),
    
    url(r'^login/$', views.login, name="aep/login"),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})
)