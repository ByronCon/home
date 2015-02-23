from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'home.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # have brew urls handle itself
    url(r'^brew/', include('brew.urls', namespace="brew")),


    # Admin
    url(r'^admin/', include(admin.site.urls)),

	# Comments Framework
    (r'^comments/', include('django_comments.urls')),


	# Auth framework
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),

)
