from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    # /projects/
    url(r'^$', views.IndexView.as_view(), name='index'),


    # PROJECTS #
    # /project/view=id/
    url(r'^project/view=(?P<pk>[0-9]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),

    # /project/create/
    url(r'^project/create/$', views.ProjectCreate.as_view(), name='new_project'),

    # /project/edit=id/
    url(r'^project/edit=(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='edit_project'),

    # /project/delete=id/
    url(r'^project/delete=(?P<pk>[0-9]+)/$', views.ProjectDelete.as_view(), name='delete_project'),


    # BUNDLES #
    # /bundle/view=id/
    url(r'^bundle/view=(?P<pk>[0-9]+)/$', views.BundleDetailView.as_view(), name='bundle_detail'),

    # /bundle/create&project=id
    url(r'^bundle/create&project=(?P<project_id>[0-9]+)/$', views.BundleCreate.as_view(), name='new_bundle'),

    # /bundle/edit=id/
    url(r'^bundle/edit=(?P<pk>[0-9]+)/$', views.BundleUpdate.as_view(), name='edit_bundle'),

    # /bundle/delete=id?returning=id/
    url(r'^bundle/delete=(?P<pk>[0-9]+)&returning=(?P<project_id>[0-9]+)/$',
        views.BundleDelete.as_view(), name='delete_bundle'),


    # BUILDS #
    # /build/view=id/
    url(r'^build/view=(?P<pk>[0-9]+)/$', views.BuildDetailView.as_view(), name='build_detail'),

    # /build/create&bundle=id/
    url(r'^build/create&bundle=(?P<bundle_id>[0-9]+)/$', views.BuildCreate.as_view(), name='new_build'),

    # /build/edit=id/
    url(r'^build/edit=(?P<pk>[0-9]+)/$', views.BuildUpdate.as_view(), name='edit_build'),

    # /build/delete=id?returning=id/
    url(r'^build/delete=(?P<pk>[0-9]+)&returning=(?P<bundle_id>[0-9]+)/$',
        views.BuildDelete.as_view(), name='delete_build'),


    # SUITES
    # /suite/view=id/
    url(r'^suite/view=(?P<pk>[0-9]+)/$', views.SuiteDetailView.as_view(), name='suite_detail'),


    # TESTS
    # /test/id
    url(r'^test/view=(?P<pk>[0-9]+)/$', views.TestScenarioDetailView.as_view(), name='test_detail'),

    # /test/create&suite=id/
    url(r'^test/create&build_test=(?P<suite_id>[0-9]+)/$', views.TestScenarioCreate.as_view(), name='new_test'),

    # /test/edit=id/
    url(r'^test/edit=(?P<pk>[0-9]+)/$', views.TestScenarioUpdate.as_view(), name='edit_test'),

    # /test/delete=id?returning=id/
    url(r'^test/delete=(?P<pk>[0-9]+)&returning=(?P<suite_id>[0-9]+)/$',
        views.TestScenarioDelete.as_view(), name='delete_test'),


    # BUILD TESTS
    # /build_test/id
    url(r'^build_test/view=(?P<pk>[0-9]+)/$', views.BuildTestDetailView.as_view(), name='build_test_detail'),

    # /build_tests/edit=id/
    url(r'^build_test/edit=(?P<pk>[0-9]+)/$', views.BuildTestUpdate.as_view(), name='edit_build_test'),


    # ISSUES
    # /issue/id
    url(r'^issue/view=(?P<pk>[0-9]+)/$', views.IssueDetailView.as_view(), name='issue_detail'),

    # /issue/create&build_test=id/
    url(r'^issue/create&build_test=(?P<build_test_id>[0-9]+)/$', views.IssueCreate.as_view(), name='new_issue'),

    # /issue/edit=id/
    url(r'^issue/edit=(?P<pk>[0-9]+)/$', views.IssueUpdate.as_view(), name='edit_issue'),

    # /issue/delete=id?returning=id/
    url(r'^issue/delete=(?P<pk>[0-9]+)&returning=(?P<build_id>[0-9]+)/$',
        views.IssueDelete.as_view(), name='delete_issue'),
]
