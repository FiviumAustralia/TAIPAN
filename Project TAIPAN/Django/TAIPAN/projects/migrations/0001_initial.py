# Generated by Django 2.0.dev20170731193407 on 2017-08-07 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BuildDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_control', models.CharField(max_length=1)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=4000)),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Build')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BundleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_control', models.CharField(max_length=1)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=4000)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Bundle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IssueDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_control', models.CharField(max_length=1)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=4000)),
                ('linked_jira', models.CharField(max_length=4000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_control', models.CharField(max_length=1)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=4000)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestScenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TestScenarioDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_control', models.CharField(max_length=1)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=4000)),
                ('expected', models.CharField(max_length=4000)),
                ('actual', models.CharField(max_length=4000)),
                ('result', models.BooleanField()),
                ('comment', models.CharField(max_length=4000)),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Build')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.TestScenario')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bundledetail',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AddField(
            model_name='builddetail',
            name='bundle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Bundle'),
        ),
    ]
