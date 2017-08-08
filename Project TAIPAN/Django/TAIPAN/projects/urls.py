from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    # /projects/
    url(r'^$', views.IndexView.as_view(), name='index'),


    # PROJECTS #
    # /projects/id/
    url(r'^(?P<pk>[0-9]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),

    # /projects/project/create/
    url(r'^project/create/$', views.ProjectCreate.as_view(), name='new_project'),

    # /projects/project/edit=id
    url(r'^project/edit=(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='edit_project'),

    # /projects/project/delete=id
    url(r'^project/delete=(?P<pk>[0-9]+)/$', views.ProjectDelete.as_view(), name='delete_project'),


    # BUNDLES #
    # /projects/id/bundles/id
    url(r'^(?P<project_id>[0-9]+)/bundles/(?P<pk>[0-9]+)/$', views.BundleDetailView.as_view(), name='bundle_detail'),

    # /projects/id/bundle/create
    url(r'^(?P<project_id>[0-9]+)/bundle/create/$', views.BundleCreate.as_view(), name='new_bundle'),

    # /projects/id/bundle/edit=id
    url(r'^(?P<project_id>[0-9]+)/bundle/edit=(?P<pk>[0-9]+)/$', views.BundleUpdate.as_view(), name='edit_bundle'),

    # /projects/id/bundle/delete=id
    url(r'^bundle/delete=(?P<pk>[0-9]+)/returning=(?P<project_id>[0-9]+)/$',
        views.BundleDelete.as_view(), name='delete_bundle'),


    # BUILDS #
    # /projects/id/bundles/id/builds/id
    url(r'^(?P<project_id>[0-9]+)/bundles/(?P<bundle_id>[0-9]+)/builds/(?P<pk>[0-9]+)/$',
        views.BuildDetailView.as_view(), name='build_detail'),

    # /projects/id/bundles/id/build/create
    url(r'^(?P<project_id>[0-9]+)/bundles/(?P<bundle_id>[0-9]+)/build/create/$',
        views.BuildCreate.as_view(), name='new_build'),

    # /projects/id/bundles/id/build/edit=id
    url(r'^(?P<project_id>[0-9]+)/bundles/(?P<bundle_id>[0-9]+)/build/edit=(?P<pk>[0-9]+)/$',
        views.BuildUpdate.as_view(), name='edit_build'),

    # /projects/id/bundles/id/build/delete=id
    url(r'^build/delete=(?P<pk>[0-9]+)/returning=(?P<bundle_id>[0-9]+)/$',
        views.BuildDelete.as_view(), name='delete_build'),

    # /projects/id/bundles/id/builds/id/tests/id
    # url(r'^(?P<project_id>[0-9]+)/bundles/(?P<bundle_id>[0-9]+)/builds/(?P<build_id>[0-9]+)/tests/(?P<scenario_id>[0-9]+)/$',
    #     views.test_detail, name='test_detail'),
    # # /projects/id/bundles/id/builds/id/issues/id
    # url(
    #     r'^(?P<project_id>[0-9]+)/bundles/(?P<bundle_id>[0-9]+)/builds/(?P<build_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/$',
    #     views.issue_detail, name='issue_detail'),
]
