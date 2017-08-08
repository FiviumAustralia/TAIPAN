from django import template
from django.http import Http404
from projects.models import *

register = template.Library()


@register.filter
def get_current(arg):
    if type(arg) is Project:
        return find_project(arg.id)
    elif type(arg) is Bundle:
        return find_bundle(arg.id)
    elif type(arg) is Build:
        return find_build(arg.id)
    elif type(arg) is TestScenario:
        return find_testscenario(arg.id)
    elif type(arg) is Issue:
        return find_issue(arg.id)
    else:
        raise TypeError("Type cannot be determined from input")


@register.filter
def get_bundles(project):
    return BundleDetail.objects.filter(status_control='C', project__id=project.id)


@register.filter
def get_builds(bundle):
    return BuildDetail.objects.filter(status_control='C', bundle__id=bundle.id)


@register.filter
def get_tests(build):
    return TestScenarioDetail.objects.filter(status_control='C', build__id=build.id)


@register.filter
def get_issues(build):
    return IssueDetail.objects.filter(status_control='C', build__id=build.id)


@register.filter
def find_project(project_id):
    try:
        return ProjectDetail.objects.filter(status_control='C').get(project__id=project_id)
    except BundleDetail.DoesNotExist:
        raise Http404("Project does not exist.")


@register.filter
def find_bundle(bundle_id):
    try:
        return BundleDetail.objects.filter(status_control='C').get(bundle__id=bundle_id)
    except BundleDetail.DoesNotExist:
        raise Http404("Bundle does not exist.")


@register.filter
def find_build(build_id):
    try:
        return BuildDetail.objects.filter(status_control='C').get(build__id=build_id)
    except BuildDetail.DoesNotExist:
        raise Http404("Build does not exist.")


@register.filter
def find_testscenario(test_id):
    try:
        return TestScenarioDetail.objects.filter(status_control='C').get(scenario__id=test_id)
    except TestScenarioDetail.DoesNotExist:
        raise Http404("Scenario does not exist.")


@register.filter
def find_issue(issue_id):
    try:
        return IssueDetail.objects.filter(status_control='C').get(issue__id=issue_id)
    except IssueDetail.DoesNotExist:
        raise Http404("Issue does not exist.")
