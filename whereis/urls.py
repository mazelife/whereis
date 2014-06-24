from django.conf.urls import patterns, include, url
from django.contrib import admin

from locations.views import CreateLocation


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^add/$', CreateLocation.as_view(), name="add"),
    url(r'^admin/', include(admin.site.urls)),
)
