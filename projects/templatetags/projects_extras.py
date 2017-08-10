from django import template
from projects.models import *

register = template.Library()


@register.filter
def get_bundles(project):
    return BundleDetail.objects.filter(project__id=project.id).exclude(status='ARCHIVED')


@register.filter
def get_builds(bundle):
    return BuildDetail.objects.filter(bundle__id=bundle.id).exclude(status='ARCHIVED')


@register.filter
def get_suite(bundle):
    return SuiteDetail.objects.filter(bundle__id=bundle.id).exclude(status='ARCHIVED')[0]


@register.filter
def get_tests(suite):
    return TestScenarioDetail.objects.filter(suite__id=suite.id).exclude(status='ARCHIVED')


@register.filter
def get_build_tests(build):
    return BuildTestDetail.objects.filter(build__id=build.id).exclude(status='ARCHIVED')


@register.filter
def check_failure(build):
    for test in get_build_tests(build):
        if test.result == 'FAILED':
            return 'FAILED'
        elif test.result == 'NONE':
            return 'INCOMPLETE'
    return 'PASSED'


@register.filter
def get_issues(build=None, build_test=None):
    tests = []
    if build is not None:
        tests = get_build_tests(build)
    if build_test is not None:
        tests.append(build_test)
    return IssueDetail.objects.filter(build_test__id__in=tests.id).exclude(status='ARCHIVED')


@register.filter
def generate_breadcrumbs(instance, f=True):
    breadcrumbs = []

    final = f
    obj = instance
    while True:
        if type(obj) is str:
            break
        breadcrumbs.append((obj, obj.get_absolute_url(), final))
        if type(obj) is BuildTestDetail:
            obj = obj.build
        elif type(obj) is TestScenarioDetail:
            obj = obj.suite
        elif type(obj) is SuiteDetail:
            obj = obj.bundle
        elif type(obj) is IssueDetail:
            obj = obj.build_test
        elif type(obj) is BuildDetail:
            obj = obj.bundle
        elif type(obj) is BundleDetail:
            obj = obj.project
        elif type(obj) is ProjectDetail:
            break
        else:
            raise TypeError('Cannot handle type: '+obj.__str__)
        final = False
    breadcrumbs.reverse()
    return breadcrumbs
