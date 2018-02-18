from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.forms import TextInput, Textarea, Select, CheckboxInput
from .forms import ModelFormWidgetMixin, BuildForm
from .templatetags import projects_extras
import reversion
import csv


# Generate CSV

def export_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + datetime.now().strftime("%Y%m%d-%H.%M.%S") + '_test_export.csv"'
    writer = csv.writer(response)
    queryset = projects_extras.get_tests(SuiteDetail.objects.get(pk=pk))
    for record in queryset:
        writer.writerow([record.reference_number, record.overview, record.steps, record.expected, record.requisite])
    return response


# Create your views here.
class IndexView(ListView):
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return ProjectDetail.objects.exclude(status='ARCHIVED')


# DETAILS
class ProjectDetailView(DetailView):
    model = ProjectDetail
    context_object_name = 'project'
    template_name = 'projects/project/project.html'


class BundleDetailView(DetailView):
    model = BundleDetail
    context_object_name = 'bundle'
    template_name = 'projects/bundles/bundle.html'


class BuildDetailView(DetailView):
    model = BuildDetail
    context_object_name = 'build'
    template_name = 'projects/builds/build.html'


class SuiteDetailView(DetailView):
    model = SuiteDetail
    context_object_name = 'suite'
    template_name = 'projects/bundles/suites/suite.html'


class TestScenarioDetailView(DetailView):
    model = TestScenarioDetail
    context_object_name = 'test_scenario'
    template_name = 'projects/bundles/suites/tests/scenario.html'


class BuildTestDetailView(DetailView):
    model = BuildTestDetail
    context_object_name = 'build_test'
    template_name = 'projects/builds/build_tests/build_test.html'


class IssueDetailView(DetailView):
    model = IssueDetail
    context_object_name = 'issue'
    template_name = 'projects/bundles/builds/issues/issue.html'


# CREATES
class ProjectCreate(ModelFormWidgetMixin, CreateView):
    model = ProjectDetail
    fields = ['name', 'description', 'project_logo']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
    }
    template_name = 'projects/project/project_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.save()
        return HttpResponseRedirect(reverse('projects:index'))


class BundleCreate(ModelFormWidgetMixin, CreateView):
    model = BundleDetail
    fields = ['name', 'description']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
    }
    template_name = 'projects/bundles/bundle_form.html'

    def get_context_data(self, **kwargs):
        context = super(BundleCreate, self).get_context_data(**kwargs)
        context['parent'] = ProjectDetail.objects.get(pk=self.kwargs['project_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            project = ProjectDetail.objects.get(pk=self.kwargs['project_id'])
            detail = form.save(commit=False)
            detail.project = project
            detail.save()
            # Create a test suite for the bundle
        with reversion.create_revision():
            suite = SuiteDetail(bundle=detail, name='{} Testing Suite'.format(detail.name),
                                description='Test suite for {}'.format(detail.name))
            suite.save()
        return HttpResponseRedirect(reverse('projects:project_detail', kwargs={'pk': self.kwargs['project_id']}))


class BuildCreate(ModelFormWidgetMixin, CreateView):
    model = BuildDetail
    fields = ['name', 'description', 'cascade_tests']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
        'cascade_tests': CheckboxInput(attrs={'class': 'small-field'}),
    }
    # form_class = BuildForm()
    template_name = 'projects/builds/build_form.html'

    def get_context_data(self, **kwargs):
        context = super(BuildCreate, self).get_context_data(**kwargs)
        context['parent'] = BundleDetail.objects.get(pk=self.kwargs['bundle_id'])
        return context

    def generate_tests(self, suite, build):
        for test in TestScenarioDetail.objects.filter(suite=suite):
            if test.requisite == 'YES':
                with reversion.create_revision():
                    build_test = BuildTestDetail(test=test,
                                                 build=build,
                                                 name='''{}\n{}'''.format(build.name, test.reference_number),
                                                 description='''{}\n\n{}'''.format(test.overview, test.steps),
                                                 expected=test.expected)
                    if build.cascade_tests:
                        if len(BuildTestDetail.objects.filter(test__id=build_test.test.id).exclude(status='ARCHIVED').order_by('-date_start')) > 0:
                            last_test = BuildTestDetail.objects.filter(test__id=build_test.test.id).exclude(status='ARCHIVED').order_by('-date_start')[0]
                            if last_test.result == 'PASSED':
                                build_test.actual = last_test.actual
                                build_test.result = last_test.result
                    build_test.save()

    def form_valid(self, form):
        with reversion.create_revision():
            bundle = BundleDetail.objects.get(pk=self.kwargs['bundle_id'])
            detail = form.save(commit=False)
            detail.bundle = bundle
            detail.save()
        # Generate build tests by looking at the bundle test suite
        self.generate_tests(suite=SuiteDetail.objects.get(bundle=bundle), build=detail)

        return HttpResponseRedirect(reverse('projects:bundle_detail', kwargs={'pk': self.kwargs['bundle_id']}))

# SuiteDetail does not require a create view since we're creating it above


class TestScenarioCreate(ModelFormWidgetMixin, CreateView):
    model = TestScenarioDetail
    fields = ['reference_number', 'overview', 'steps', 'expected']
    widgets = {
        'reference_number': TextInput(attrs={'class': 'tiny-field'}),
        'overview': TextInput(attrs={'class': 'small-field'}),
        'steps': Textarea(attrs={'class': 'large-field'}),
        'expected': Textarea(attrs={'class': 'large-field'}),
    }
    template_name = 'projects/bundles/suites/tests/test_form.html'

    def get_context_data(self, **kwargs):
        context = super(TestScenarioCreate, self).get_context_data(**kwargs)
        context['parent'] = SuiteDetail.objects.get(pk=self.kwargs['suite_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            suite = SuiteDetail.objects.get(pk=self.kwargs['suite_id'])
            detail = form.save(commit=False)
            detail.suite = suite
            detail.save()
        return HttpResponseRedirect(reverse('projects:suite_detail', kwargs={'pk': self.kwargs['suite_id']}))

# BuildTestDetail does not require a create view since we're creating them all above


class IssueCreate(ModelFormWidgetMixin, CreateView):
    model = IssueDetail
    fields = ['name', 'description', 'priority', 'severity']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
        'priority': Select(attrs={'class': 'selector'}),
        'severity': Select(attrs={'class': 'selector'}),
    }
    template_name = 'projects/builds/issue_form.html'

    def get_context_data(self, **kwargs):
        context = super(IssueCreate, self).get_context_data(**kwargs)
        context['parent'] = BuildTestDetail.objects.get(pk=self.kwargs['build_test_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            build_test = BuildTestDetail.objects.get(pk=self.kwargs['build_test_id'])
            detail = form.save(commit=False)
            detail.build_test = build_test
            detail.save()
        # Take us back to the build instead of the build test
        return HttpResponseRedirect(reverse('projects:bundle_detail', kwargs={'pk': detail.build_test.build.id}))


# UPDATES
class ProjectUpdate(ModelFormWidgetMixin, UpdateView):
    model = ProjectDetail
    fields = ['name', 'description', 'project_logo']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
    }
    template_name = 'projects/project/project_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.date_modified = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:index'))


class BundleUpdate(ModelFormWidgetMixin, UpdateView):
    model = BundleDetail
    fields = ['name', 'description']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
    }
    template_name = 'projects/bundles/bundle_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.date_modified = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:project_detail', kwargs={'pk': detail.project.id}))


class BuildUpdate(ModelFormWidgetMixin, UpdateView):
    model = BuildDetail
    fields = ['name', 'description']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
    }
    template_name = 'projects/builds/build_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.date_modified = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:bundle_detail', kwargs={'pk': detail.bundle.id}))

# SuiteDetail does not require an update view


class TestScenarioUpdate(ModelFormWidgetMixin, UpdateView):
    model = TestScenarioDetail
    fields = ['reference_number', 'overview', 'steps', 'expected', 'requisite']
    widgets = {
        'reference_number': TextInput(attrs={'class': 'tiny-field'}),
        'overview': TextInput(attrs={'class': 'small-field'}),
        'steps': Textarea(attrs={'class': 'large-field'}),
        'expected': Textarea(attrs={'class': 'large-field'}),
        'requisite': Select(attrs={'class': 'selector'})
    }
    template_name = 'projects/bundles/suites/tests/test_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.date_modified = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:suite_detail', kwargs={'pk': detail.suite.id}))


class BuildTestUpdate(ModelFormWidgetMixin, UpdateView):
    model = BuildTestDetail
    fields = ['actual', 'result']
    widgets = {
        'actual': Textarea(attrs={'class': 'large-field'}),
        'result': Select(attrs={'class': 'selector'})
    }
    template_name = 'projects/builds/build_tests/build_test_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.date_modified = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:build_detail', kwargs={'pk': detail.build.id}))


class IssueUpdate(ModelFormWidgetMixin, UpdateView):
    model = IssueDetail
    fields = ['name', 'description', 'priority', 'severity']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
        'priority': Textarea(attrs={'class': 'selector'}),
        'severity': Textarea(attrs={'class': 'selector'}),
    }
    template_name = 'projects/issues/issue_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.date_modified = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:build_detail', kwargs={'pk': detail.build.id}))


# We override delete here to prevent records being deleted
class ArchiveView(DeleteView):
    def archive(self):
        with reversion.create_revision():
            detail = self.get_object()
            detail.status = 'ARCHIVED'
            detail.save()


# DELETES
class ProjectDelete(ArchiveView):
    model = ProjectDetail
    success_url = 'projects:index'

    def delete(self, request, *args, **kwargs):
        self.archive()
        return HttpResponseRedirect(reverse(self.success_url))


class BundleDelete(ArchiveView):
    model = BundleDetail
    success_url = 'projects:project_detail'

    def delete(self, request, *args, **kwargs):
        self.archive()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk': self.kwargs['project_id']}))


class BuildDelete(ArchiveView):
    model = BuildDetail
    success_url = 'projects:bundle_detail'

    def delete(self, request, *args, **kwargs):
        for test in BuildTestDetail.objects.filter(build=self.get_object()):
            test.status = 'ARCHIVED'
            test.save()
        self.archive()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk': self.kwargs['bundle_id']}))

# SuiteDetail does not require a delete view since it is reliant on a BundleDetail


class TestScenarioDelete(ArchiveView):
    model = TestScenarioDetail
    success_url = 'projects:suite_detail'

    def delete(self, request, *args, **kwargs):
        self.archive()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk': self.kwargs['suite_id']}))

# BuildTestDetail does not require a delete view since it is reliant on a TestScenarioDetail


class IssueDelete(ArchiveView):
    model = IssueDetail
    success_url = 'projects:build_detail'

    def delete(self, request, *args, **kwargs):
        self.archive()
        # TODO when JIRA is implemented, issues raised by this program will require cleanup
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk': self.kwargs['build_id']}))
