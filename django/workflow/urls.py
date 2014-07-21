from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'workflow.views.home', name='home'),
    url(r'^test/', 'workflow.views.test'),
    url(r'^display/', include('display.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
