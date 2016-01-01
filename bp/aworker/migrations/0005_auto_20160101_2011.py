# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0004_auto_20160101_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractusermixin',
            name='address',
            field=models.CharField(default='', max_length=300, verbose_name='Address', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='City', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='country',
            field=models.CharField(default='', max_length=3, verbose_name='Country code', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='organization',
            field=models.CharField(default='', max_length=500, verbose_name='Organization', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='phone',
            field=models.CharField(default='', max_length=15, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='position',
            field=models.CharField(default='', max_length=255, verbose_name='Position', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='role',
            field=models.CharField(default='AU', max_length=2, choices=[('AU', 'Author'), ('ED', 'Editor'), ('RE', 'Reviewer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='secondname',
            field=models.CharField(default='', max_length=100, verbose_name='Family name', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='thirdname',
            field=models.CharField(default='', max_length=100, verbose_name='Last name', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractusermixin',
            name='zipcode',
            field=models.CharField(default='', max_length=10, verbose_name='Zip code', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'060c00c670af4f41aef9c3ab91c29796', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
