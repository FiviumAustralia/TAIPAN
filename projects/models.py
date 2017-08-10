from django.db import models
from django.urls import reverse
from datetime import datetime


# Create your models here.
class Detail(models.Model):
    STATUS_CHOICES = (
        ('ARCHIVED', 'Archived'),
        ('ACTIVE', 'Active'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    date_start = models.DateTimeField(default=datetime.now)
    date_modified = models.DateTimeField(default=datetime.now)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)

    class Meta:
        abstract = True


class ProjectDetail(Detail):
    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})


class BundleDetail(Detail):
    project = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('projects:bundle_detail', kwargs={'pk': self.pk})


class RequirementDetail(Detail):
    bundle = models.ForeignKey(BundleDetail, on_delete=models.CASCADE)
    req_id = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('projects:requirement_detail', kwargs={'pk': self.pk})


class BuildDetail(Detail):
    bundle = models.ForeignKey(BundleDetail, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('projects:build_detail', kwargs={'pk': self.pk})


class SuiteDetail(Detail):
    bundle = models.ForeignKey(BundleDetail, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('projects:suite_detail', kwargs={'pk': self.pk})


class TestScenarioDetail(Detail):
    suite = models.ForeignKey(SuiteDetail, on_delete=models.CASCADE)
    # requirement = models.ForeignKey(RequirementDetail, on_delete=models.SET_NULL, null=True, blank=True)

    expected = models.CharField(max_length=4000, null=True, blank=True, default=None)
    REQUISITE_CHOICES = {
        ('REMOVED', 'Removed'),
        ('REQUIRED', 'Yes'),
    }
    requisite = models.CharField(max_length=10, choices=REQUISITE_CHOICES, default='REQUIRED')

    def get_absolute_url(self):
        return reverse('projects:test_detail', kwargs={'pk': self.pk})


class BuildTestDetail(Detail):
    test = models.ForeignKey(TestScenarioDetail, on_delete=models.CASCADE)
    build = models.ForeignKey(BuildDetail, on_delete=models.CASCADE)

    STAGE_CHOICES = (
        ('AWAITING', 'Awaiting Testing'),
        ('PROGRESSING', 'In Progress'),
        ('COMPLETE', 'Testing Complete'),
    )
    RESULT_CHOICES = (
        ('PASSED', 'Pass'),
        ('FAILED', 'Fail'),
        ('NONE', 'N/A'),
    )
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default='AWAITING')
    actual = models.CharField(max_length=4000, null=True, blank=True, default=None)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, default='NONE')

    def get_absolute_url(self):
        return reverse('projects:build_test_detail', kwargs={'pk': self.pk})


class IssueDetail(Detail):
    build_test = models.ForeignKey(BuildTestDetail, on_delete=models.CASCADE)

    PRIORITY_CHOICES = (
        ('BLOCKER', 'Blocker'),
        ('CRITICAL', 'Critical'),
        ('MAJOR', 'Major'),
        ('MINOR', 'Minor'),
        ('TRIVIAL', 'Trivial'),
        ('NONE', 'No Priority'),
    )
    SEVERITY_CHOICES = (
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
        ('NONE', 'No Severity'),
    )
    RESOLUTION_CHOICES = (
        ('RESOLVED', 'Resolved'),
        ('OPEN', 'Open'),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='NONE')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='NONE')
    resolution = models.CharField(max_length=10, choices=RESOLUTION_CHOICES, default='OPEN')
    linked_jira = models.URLField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('projects:issue_detail', kwargs={'pk': self.pk})
