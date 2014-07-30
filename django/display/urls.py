from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^test/$', 'display.views.test'),
    url(r'^$', 'display.views.home', name='display_home'),
    url(r'^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', 'display.views.home', name="display_date"),
    url(r'^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<dept>[0-9a-zA-Z ]+)/$', 'display.views.home', name="display_date_dept"),

)

