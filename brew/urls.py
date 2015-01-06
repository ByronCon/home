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


    # ## Batch
    # Index """
    url(r'^ferment/$', views.BatchIndexView.as_view(), name='batch_index'),
    # Detail
    url(r'^ferment/(?P<pk>\d+)/$', views.BatchDetailView.as_view(), name='batch_detail'),


    # ## Bottling
    # Index

    # Detail
    url(r'^bottle/(?P<pk>\d+)/$', views.wip, name='bottling_detail'),

    url(r'^measure', views.wip, name='measure'),
    url(r'^bottle', views.wip, name='bottle'),
    url(r'^enjoy', views.wip, name='enjoy'),
)
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)