from django.conf.urls import patterns, url

from brew import views

urlpatterns = patterns('',
    #ex: /brew/
    url(r'^$', views.HomePageView.as_view(),name='index'),


    # Recipe index      - ex: /brew/prepare
    url(r'^prepare/$', views.recipe_index, name='recipe_index'),

    # Recipe detail     - ex: /brew/prepare/1/
    url(r'^prepare/(?P<recipe_id>\d+)/$', views.recipe_detail, name='recipe_detail'),

    # Recipe Change
    url(r'^prepare/(?P<recipe_id>\d+)/update/$', views.recipe_update, name='recipe_update'),


    # ## Batch
    # Index """
    url(r'^ferment/$', views.BatchIndexView.as_view(), name='batch_index'),
    # Detail
    url(r'^ferment/(?P<pk>\d+)/$', views.BatchDetailView.as_view(), name='batch_detail'),
    # Create
    url(r'^ferment/new/$', views.batch_create, name='batch_create'),
    # Update
    url(r'^ferment/(?P<pk>\d+)/update/$', views.batch_update, name='batch_update'),
    # Delete
    url(r'^ferment/(?P<pk>\d+)/remove/$', views.batch_delete, name='batch_delete'),

    ### Measure
    # Index
    url(r'^measure/$', views.wip, name='measure_index'),
    # Create
    url(r'^measure/new/$', views.measure_create, name='measure_create'),


    # ## Bottling
    # Index
    url(r'bottle/$', views.BottlingIndexView.as_view(), name='bottling_index'),

    # Detail
    url(r'^bottle/(?P<pk>\d+)/$', views.BottlingDetailView.as_view(), name='bottling_detail'),

    url(r'^measure', views.wip, name='measure'),
    url(r'^bottle', views.wip, name='bottle'),
    url(r'^enjoy', views.wip, name='enjoy'),
)