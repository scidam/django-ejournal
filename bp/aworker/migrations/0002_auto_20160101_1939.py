# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'61fd6f80ed094b0b97e5a808a88589c8', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
