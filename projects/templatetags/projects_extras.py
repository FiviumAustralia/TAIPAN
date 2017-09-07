from django import template
from projects.models import *

register = template.Library()


@register.filter
def get_bundles(project, archived=False, desc=True):
    return BundleDetail.objects.filter(project__id=project.id).exclude(status='ARCHIVED')


@register.filter
def get_builds(bundle, archived=False, desc=True):
    if desc:
        return BuildDetail.objects.filter(bundle__id=bundle.id).exclude(status='ARCHIVED').order_by('-name')
    else:
        return BuildDetail.objects.filter(bundle__id=bundle.id).exclude(status='ARCHIVED').order_by('name')


@register.filter
def get_suite(bundle):
    return SuiteDetail.objects.exclude(status='ARCHIVED').get(bundle__id=bundle.id)


@register.filter
def get_tests(suite, archived=False):
    return TestScenarioDetail.objects.filter(suite__id=suite.id).exclude(status='ARCHIVED').order_by('reference_number')


@register.filter
def active_tests(suite):
    return TestScenarioDetail.objects.filter(suite__id=suite.id).exclude(status='ARCHIVED').exclude(requisite='NO')


@register.filter
def get_build_tests(build, archived=False, active=False):
    if active:
        tests = active_tests(get_suite(build.bundle))
        return BuildTestDetail.objects.filter(build__id=build.id).exclude(status='ARCHIVED').filter(test__id__in=tests.values_list('id')).order_by('name')
    return BuildTestDetail.objects.filter(build__id=build.id).exclude(status='ARCHIVED').order_by('name')


@register.filter
def check_failures(build):
    count = 0
    for test in get_build_tests(build):
        if test.result == 'FAILED':
            count += 1
        elif test.result == 'NONE':
            return -1
    return count


@register.filter
def get_issues(build=None, build_test=None):
    tests = []
    if build is not None:
        tests = get_build_tests(build)
    if build_test is not None:
        tests.append(build_test)
    return IssueDetail.objects.filter(build_test__id__in=tests.id).exclude(status='ARCHIVED')


@register.filter
def generate_breadcrumbs(instance, final=True):
    breadcrumbs = []

    final_crumb = final
    obj = instance
    while True:
        if type(obj) is str:
            break
        breadcrumbs.append((obj, obj.get_absolute_url(), final_crumb))
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
        final_crumb = False
    breadcrumbs.reverse()
    return breadcrumbs
