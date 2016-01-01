# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0005_auto_20160101_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'a044a90d21a34c7a892f8fec674b7220', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
