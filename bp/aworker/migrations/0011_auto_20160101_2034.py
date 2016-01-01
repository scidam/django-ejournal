# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0010_auto_20160101_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'c2ef599f2b754f40a1cf72c2c3d213b6', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
