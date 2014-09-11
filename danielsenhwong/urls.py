from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'danielsenhwong.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Django user authentication
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
        
    # My applications
    url(r'^', include('home.urls')), # home
)