from django.conf.urls import patterns, url

from brew import views

urlpatterns = patterns('',
    #ex: /brew/
    url(r'^$', views.index, name='index'),

    # Recipe index      - ex: /brew/prepare
    url(r'^prepare/$', views.recipe_index, name='recipe_index'),

    # Recipe detail     - ex: /brew/prepare/1/
    url(r'^prepare/(?P<recipe_id>\d+)/$', views.recipe_detail, name='recipe_detail'),

    # Recipe Change
    url(r'^prepare/(?P<recipe_id>\d+)/update/$', views.recipe_update, name='recipe_update'),

    # ex: /brew/prepare/1/
    # url(r'^prepare/(?P<recipe_id>\d+)/', views.prepare, name='prepare'),

    url(r'^ferment', views.wip, name='ferment'),
    url(r'^measure', views.wip, name='measure'),
    url(r'^bottle', views.wip, name='bottle'),
    url(r'^enjoy', views.wip, name='enjoy'),
)