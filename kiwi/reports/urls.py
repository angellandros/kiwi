from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^day/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/json/$', views.view1_json, name='json1'),
    url(r'^day/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.view1_html, name='html1'),
    url(r'^devices/(?P<type>[a-z]+)/(?P<status>[a-z]+)/$', views.view2_html, name='html2'),
]

