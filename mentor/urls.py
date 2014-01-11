from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from django.contrib import admin
from mentor.questionaire import views as questionaire
from settings import base

admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^$', lambda request: render(request, "main.html"), name='home'),

    # admin area
    url(r'^admin/', include(admin.site.urls)),
    
    # Questionaire
    # url(r'^questionaire/edit/(?P<questionaire_id>.+)?$', questionaire.edit_questionaire, name='questionaire-editing'),
    url(r'^questionaire/add/?$', questionaire.add_questionaire, name='questionaire-adding'),
    # url(r'^questionaire/detail/(?P<questionaire_id>.+)?$', questionaire.detail, name='questionaire-detail'),


)

# djangocas
if settings.USE_CAS:
    urlpatterns = patterns('',
        url(r'^accounts/login/$', 'djangocas.views.login', name='admin-login'),
        url(r'^accounts/logout/$', 'djangocas.views.logout', name='admin-logout'),
        ) + urlpatterns

    # urlpatterns = patterns('django.views.generic.simple', ('^admin/logout/$', 'redirect_to' ,
    #         {'url': '../../accounts/logout'})) + urlpatterns
# end djangocas

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
