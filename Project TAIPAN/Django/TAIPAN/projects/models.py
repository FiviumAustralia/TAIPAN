from django.db import models
from .declarations import Detail
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    pass


class ProjectDetail(Detail):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})


class Bundle(models.Model):
    pass


class BundleDetail(Detail):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('projects:bundle_detail', kwargs={'pk': self.pk})


class Build(models.Model):
    pass


class BuildDetail(Detail):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('projects:build_detail', kwargs={'pk': self.pk})


class TestScenario(models.Model):
    pass


class TestScenarioDetail(Detail):
    scenario = models.ForeignKey(TestScenario, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE)

    expected = models.CharField(max_length=4000)
    actual = models.CharField(max_length=4000)
    result = models.BooleanField()
    comment = models.CharField(max_length=4000)


class Issue(models.Model):
    pass


class IssueDetail(Detail):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE)

    linked_jira = models.CharField(max_length=4000)
