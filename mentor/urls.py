from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mentor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', lambda request: render(request, "main.html")),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
