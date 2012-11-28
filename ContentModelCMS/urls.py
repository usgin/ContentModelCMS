from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^uri-gin/', include('uriredirect.urls')),
    url(r'^validate/', include('validation.urls')),
    #url(r'^', include('contentmodels.urls')),
)

from contentmodels.urls import urlpatterns as cm_urls
urlpatterns += cm_urls

from uriredirect.urls import urlpatterns as uri_urls
urlpatterns += uri_urls

