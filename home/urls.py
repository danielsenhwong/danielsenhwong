from django.conf.urls import patterns, include, url

from home import views

urlpatterns = patterns('home.views',
  url(r'^contact/$', 'contact', name='contact'), # contact/
  url(r'^$', 'index'), # /
