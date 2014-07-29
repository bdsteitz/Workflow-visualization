from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'workflow.views.home', name='home'),
    url(r'^display/', include('display.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login', 'workflow.views.login', name="login"),
    url(r'^logout', 'workflow.views.logout', name="logout"),
)
