# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-18 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('djangocms_custommenu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StyleMenu',
            fields=[
                ('template', models.CharField(choices=[(b'zoom-masonry', 'Zoom masonry'), (b'dropdown-image', 'Dropdown image')], default=b'zoom-masonry', max_length=255, verbose_name='Template')),
                ('classes', models.CharField(blank=True, help_text='Comma separated list of classes to add to the element.', max_length=255)),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_custommenu_stylemenu', serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
