# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0008_auto_20160101_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractusermixin',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name='Email'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'47082580def54a33b2b8090300860cef', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
