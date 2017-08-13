from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^day/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.view1, name='view1'),
    url(r'^device/(?P<device_id>[0-9a-z]+)/$', views.view2, name='view2'),
]

