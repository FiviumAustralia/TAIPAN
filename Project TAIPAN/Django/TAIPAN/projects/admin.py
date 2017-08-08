from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import *


# Register your models here.
@admin.register(ProjectDetail)
class ProjectDetailAdmin(VersionAdmin):
    pass


@admin.register(BundleDetail)
class BundleDetailAdmin(VersionAdmin):
    pass


@admin.register(BuildDetail)
class BuildDetailAdmin(VersionAdmin):
    pass


@admin.register(TestScenarioDetail)
class TestScenarioDetailAdmin(VersionAdmin):
    pass


@admin.register(IssueDetail)
class IssueDetailAdmin(VersionAdmin):
    pass
