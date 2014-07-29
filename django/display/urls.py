from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^test/$', 'display.views.test'),
    url(r'^$', 'display.views.home', name='display_home'),
)

