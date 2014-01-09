from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from django.contrib import admin
from mentor.questionaire import views as questionaire

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mentor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', lambda request: render(request, "main.html")),

    # admin area
    url(r'^admin/', include(admin.site.urls)),
    
    # login, logout
    url(r'^admin/login/$', 'djangocas.views.login', name='admin-login'),
    url(r'^admin/logout/$', 'djangocas.views.logout', name='admin-logout'),
    
    # Questionaire
    url(r'^questionaire/?$', questionaire.listing, name='questionaire-listing'),
    url(r'^questionaire/edit/(?P<questionaire_id>.+)?$', questionaire.edit_questionaire, name='questionaire-editing'),
    url(r'^questionaire/add/?$', questionaire.add_questionaire, name='questionaire-adding'),
    url(r'^questionaire/detail/(?P<questionaire_id>.+)?$', questionaire.detail, name='questionaire-detail'),


)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
