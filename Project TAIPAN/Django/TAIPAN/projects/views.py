from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.http import HttpResponseRedirect
from datetime import datetime
import reversion


# Create your views here.
class IndexView(ListView):
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return ProjectDetail.objects.filter(status_control='C')


class ProjectDetailView(DetailView):
    model = ProjectDetail
    context_object_name = 'pd'
    template_name = 'projects/project/project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context


class BundleDetailView(DetailView):
    model = BundleDetail
    context_object_name = 'bd'
    template_name = 'projects/bundles/bundle.html'

    def get_context_data(self, **kwargs):
        context = super(BundleDetailView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        context['bundle'] = Bundle.objects.get(pk=self.kwargs['pk'])
        return context


class BuildDetailView(DetailView):
    model = BuildDetail
    context_object_name = 'bid'
    template_name = 'projects/builds/build.html'

    def get_context_data(self, **kwargs):
        context = super(BuildDetailView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        context['bundle'] = Bundle.objects.get(pk=self.kwargs['bundle_id'])
        context['build'] = Build.objects.get(pk=self.kwargs['pk'])
        return context


# class TestDetailView(DetailView):
#     model = TestScenarioDetail
#     context_object_name = 'td'
#     template_name = 'projects/bundles/builds/tests/scenario.html'


# class IssueDetailView(DetailView):
#     model = IssueDetail
#     context_object_name = 'isd'
#     template_name = 'projects/bundles/builds/issues/issue.html'


class ProjectCreate(CreateView):
    model = ProjectDetail
    fields = ['name', 'description']
    template_name = 'projects/project/projectdetail_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            master = Project()
            master.save()
            detail = form.save(commit=False)
            detail.project = master
            detail.status_control = 'C'
            detail.start_datetime = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:index'))


class BundleCreate(CreateView):
    model = BundleDetail
    fields = ['name', 'description']
    template_name = 'projects/bundles/bundledetail_form.html'

    def get_context_data(self, **kwargs):
        context = super(BundleCreate, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            project = Project.objects.get(pk=self.kwargs['project_id'])
            master = Bundle()
            master.save()
            detail = form.save(commit=False)
            detail.project = project
            detail.bundle = master
            detail.status_control = 'C'
            detail.start_datetime = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:project_detail', kwargs={'pk': self.kwargs['project_id']}))


class BuildCreate(CreateView):
    model = BuildDetail
    fields = ['name', 'description']
    template_name = 'projects/builds/builddetail_form.html'

    def get_context_data(self, **kwargs):
        context = super(BuildCreate, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        context['bundle'] = Bundle.objects.get(pk=self.kwargs['bundle_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            bundle = Bundle.objects.get(pk=self.kwargs['bundle_id'])
            master = Build()
            master.save()
            detail = form.save(commit=False)
            detail.bundle = bundle
            detail.build = master
            detail.status_control = 'C'
            detail.start_datetime = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:bundle_detail', kwargs={'pk': self.kwargs['bundle_id']}))


class ProjectUpdate(UpdateView):
    model = ProjectDetail
    fields = ['name', 'description']
    template_name = 'projects/project/projectdetail_form.html'

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.status_control = 'C'
            detail.start_datetime = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:index'))


class BundleUpdate(UpdateView):
    model = BundleDetail
    fields = ['name', 'description']
    template_name = 'projects/bundles/bundledetail_form.html'

    def get_context_data(self, **kwargs):
        context = super(BundleUpdate, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.status_control = 'C'
            detail.start_datetime = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:project_detail', kwargs={'pk': self.kwargs['project_id']}))


class BuildUpdate(UpdateView):
    model = BuildDetail
    fields = ['name', 'description']
    template_name = 'projects/builds/builddetail_form.html'

    def get_context_data(self, **kwargs):
        context = super(BuildUpdate, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        context['bundle'] = Bundle.objects.get(pk=self.kwargs['bundle_id'])
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            detail = form.save(commit=False)
            detail.status_control = 'C'
            detail.start_datetime = datetime.now()
            detail.save()
        return HttpResponseRedirect(reverse('projects:bundle_detail',
                                            kwargs={'pk': self.kwargs['bundle_id'],
                                                    'project_id': self.kwargs['project_id']}))


# We override delete here to prevent records being deleted
class ProjectDelete(DeleteView):
    model = ProjectDetail
    success_url = 'projects:index'

    def delete(self, request, *args, **kwargs):
        with reversion.create_revision():
            detail = self.get_object()
            detail.end_datetime = datetime.now()
            detail.status_control = 'X'
            detail.save()
        return HttpResponseRedirect(reverse(self.success_url))


class BundleDelete(DeleteView):
    model = BundleDetail
    success_url = 'projects:project_detail'

    def delete(self, request, *args, **kwargs):
        with reversion.create_revision():
            detail = self.get_object()
            detail.end_datetime = datetime.now()
            detail.status_control = 'X'
            detail.save()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk': self.kwargs['project_id']}))


class BuildDelete(DeleteView):
    model = BuildDetail
    success_url = 'projects.bundle_detail'

    def delete(self, request, *args, **kwargs):
        with reversion.create_revision():
            detail = self.get_object()
            detail.end_datetime = datetime.now()
            detail.status_control = 'X'
            detail.save()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk': self.kwargs['bundle_id']}))
