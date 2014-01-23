from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from django.contrib import admin
from mentor.questionaire import views as questionaire
from mentor.counter import views as counter 
from settings import base

admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^$', lambda request: render(request, "main.html"), name='home'),

    # admin area
    url(r'^admin/', include(admin.site.urls), name='admin-home'),
    url(r'^admin/report-questionaire', questionaire.report, name='questionaire-reporting'),
    url(r'^admin/report-counter', counter.report, name='counter-reporting'),
    url(r'^admin/counter-list', counter.list, name='counter-list'),
    
    # Questionaire
    url(r'^questionaire/add/?$', questionaire.add_questionaire, name='questionaire-adding'),
    url(r'^questionaire/thanks/?$', TemplateView.as_view(template_name='questionaire/thanks.html'), name='questionaire-thanks'),

    # Counter
    url(r'^goto/(?P<url>.*)/?$', counter.goto, name='counter-goto'),


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
