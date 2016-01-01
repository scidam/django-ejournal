# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0002_auto_20160101_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'1097e35a56d04bb08dbd062dbea96f07', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
