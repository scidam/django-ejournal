# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0003_auto_20160101_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'5c6bb13a975045ac8ff993138f2cd8bf', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
