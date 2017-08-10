# Generated by Django 2.0.dev20170731193407 on 2017-08-09 09:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BuildTestDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
                ('stage', models.CharField(choices=[('AWAITING', 'Awaiting Testing'), ('PROGRESSING', 'In Progress'), ('COMPLETE', 'Testing Complete')], default='AWAITING', max_length=10)),
                ('actual', models.CharField(blank=True, default=None, max_length=4000, null=True)),
                ('result', models.CharField(choices=[('PASSED', 'Pass'), ('FAILED', 'Fail'), ('NONE', 'N/A')], default='NONE', max_length=10)),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BuildDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BundleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IssueDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
                ('priority', models.CharField(choices=[('BLOCKER', 'Blocker'), ('CRITICAL', 'Critical'), ('MAJOR', 'Major'), ('MINOR', 'Minor'), ('TRIVIAL', 'Trivial'), ('NONE', 'No Priority')], default='NONE', max_length=10)),
                ('severity', models.CharField(choices=[('CRITICAL', 'Critical'), ('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low'), ('NONE', 'No Severity')], default='NONE', max_length=10)),
                ('resolution', models.CharField(choices=[('RESOLVED', 'Resolved'), ('OPEN', 'Open')], default='OPEN', max_length=10)),
                ('linked_jira', models.URLField(blank=True, null=True)),
                ('build_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BuildTestDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequirementDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
                ('req_id', models.CharField(max_length=10)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BundleDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuiteDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BundleDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestScenarioDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ARCHIVED', 'Archived'), ('ACTIVE', 'Active')], default='ACTIVE', max_length=10)),
                ('date_start', models.DateTimeField(default=datetime.datetime.now)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4000)),
                ('expected', models.CharField(blank=True, default=None, max_length=4000, null=True)),
                ('suite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.SuiteDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bundledetail',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='buildtestdetail',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.TestScenarioDetail'),
        ),
        migrations.AddField(
            model_name='builddetail',
            name='bundle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BundleDetail'),
        ),
    ]