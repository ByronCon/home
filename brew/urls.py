from django.conf.urls import patterns, url

from brew import views

urlpatterns = patterns('',

    #ex: /brew/
    url(r'^$', views.HomePageView.as_view(), name='index'),


    # Recipe index      - ex: /brew/prepare
    url(r'^prepare/$', views.RecipeIndexView.as_view(), name='recipe_index'),

    # Recipe detail     - ex: /brew/prepare/1/
    url(r'^prepare/(?P<pk>\d+)/$', views.recipe_detail, name='recipe_detail_OLD'),
    url(r'^prepare/(?P<pk>\d+)/$', views.RecipeDetailView.as_view(), name='recipe_detail'),

    # Recipe create     - ex: /brew/prepare/new
    url(r'^prepare/new/$', views.RecipeCreate.as_view(), name='recipe_create'),

    # Recipe Change     - eg: /brew/prepare/1/update/
    url(r'^prepare/(?P<pk>\d+)/update/$', views.RecipeUpdate.as_view(), name='recipe_update'),

    # Recipe Delete     - eg: /brew/prepare/1/remove
    url(r'^prepare/(?P<pk>\d+)/remove/$', views.RecipeDelete.as_view(), name='recipe_delete'),

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


    # not required? use enjoy model instead.
    # # ## Bottling
    # # Index
    # url(r'bottle/$', views.BottlingIndexView.as_view(), name='bottling_index'),
    # # Detail
    # url(r'^bottle/(?P<pk>\d+)/$', views.BottlingDetailView.as_view(), name='bottling_detail'),
    # # Create
    # #url(r'^ferment/(?P<pk>\d+)/bottle/$', views.BottlingCreateView2.as_view(), name='bottling_create2'),
    # url(r'^bottle/new/$', views.BottlingCreateView.as_view(), name='bottling_create'),

    ### Drink
    # Index
    url(r'enjoy/$', views.DrinkIndexView.as_view(), name='drink_index'),
    # Detail
    url(r'^enjoy/(?P<pk>\d+)/$', views.DrinkDetailView.as_view(), name='drink_detail'),
    # Drink Change     - eg: /brew/prepare/1/update/
    url(r'^enjoy/(?P<pk>\d+)/update/$', views.DrinkUpdate.as_view(), name='drink_update'),



    url(r'^measure', views.wip, name='measure'),
    #url(r'^bottle', views.wip, name='bottle'),
    #url(r'^enjoy', views.wip, name='enjoy'),


    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

)