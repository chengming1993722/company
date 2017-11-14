# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 07:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_teacher_image'),
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后台开发', max_length=20, verbose_name='课程类别'),
        ),
        migrations.AddField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '初级'), ('gj', '高级'), ('zj', '中级')], default='cj', max_length=5, verbose_name='课程难度'),
        ),
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='服务操作系统', max_length=40, verbose_name='课程标签'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Teacher', verbose_name='教师'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=200, verbose_name='老师告诉你学到什么'),
        ),
        migrations.AddField(
            model_name='course',
            name='tonggao',
            field=models.CharField(default='', max_length=100, verbose_name='课程公告'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_know',
            field=models.CharField(default='', max_length=200, verbose_name='课程须知'),
        ),
    ]