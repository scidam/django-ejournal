# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0006_auto_20160101_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'ebc04f5e54d2445c80e53296870a987d', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
