# _*_coding: utf-8 _*_
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from os.path import join
from village.views import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    # (r'^erahtur/', include('erahtur.foo.urls')),
    (r'^$', redirect),
    url(r'^login_page/$', login_page, name="login_page"),
    url(r'^organizations/$', org_list, name='org_list'),
    url(r'^publications/tags/(\d+)/$', pubs_by_tag, name='pubs_by_tag'),
    url(r'^publications/news/$', direct_to_template, 
        {'template': 'publications/all_publications_types.html'}, 
        name='all_publications_types'),
    url(r'^publications/news/(\w+)/(\d+)/$', pub_list, name='pub_list'),
    url(r'^organizations/(\d+)/$', organization, name='organization'),
    url(r'^publications/(\d+)/$', publication, name='publication'),
    url(r'^publications/(\d+)/comments/new/$', add_comment, name='add_comment'),
    url(r'^ajax_news_block/$', ajax_news_block, name='ajax_news_block'),
    url(r'^pub_archive/$', publications_archive, name='publications_archive'),
    url(r'^pub_archive_months/(\d{4})/(\d+)/$', pub_archive_months, name='pub_archive_months'),
    url(r'^history/$', hist_list, name='hist_list'),
    url(r'^history/(\d+)/$', history, name='history'),
    url(r'^neighbours/$', neighbour_list, name='neighbour_list'),
    url(r'^neighbours/(\d+)/$', neighbour, name='neighbour'),
    url(r'^creation/$', direct_to_template, {'template': 'creation/creation.html'}, name='creation'),
    url(r'^creation/music/$', music, name='music'),
    url(r'^creation/photoalbums/$', photoalbums_list, name='photoalbums'),
    url(r'^creation/photoalbum/(\d+)/$', photoalbum, name='photoalbum'),
    url(r'^creation/panorams/(\d+)/$', panorama, name='panorama'),
    url(r'^creation/panorams_list/$', panorams_list, name='panorams_list'),
    url(r'^creation/panorams/tags/(\d+)/$', panorams_by_tag, name='panorams_by_tag'),
    url(r'^links/$', links, name='links'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #(r'^accounts/', include('registration.urls')),
    #(r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/log_in/$', log_in),
    (r'^accounts/logout/$', logout),
    (r'^accounts/login_please', direct_to_template, {'template':'login_error.html'}),
    (r'^accounts/registration/$', registration),
    (r'^accounts/is_username_unique/$', is_username_unique),
    #(r'^accounts/create_user_profile/$', create_user_profile),
    (r'^accounts/user_profile_handle/$', user_profile_handle),
    (r'^accounts/user_profile_creation_error/$', direct_to_template, {'template': 'user_profile_creation_error.html'}),
    #(r'^accounts/user_profile_creation_error/$', direct_to_template, {'template': 'user_profile_creation_error.html'}),
    (r'^accounts/user_profile/(\w+)/$', user_profile),
    (r'^accounts/thanks/$', direct_to_template, {'template':'registration/thanks.html',}),
    url(r'^search/$', search, name='search'),
    (r'^forum/', include('forum.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
