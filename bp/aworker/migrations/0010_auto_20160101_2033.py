# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0009_auto_20160101_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'6b67c3b56d5640f281cdb36e8db72e0d', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
