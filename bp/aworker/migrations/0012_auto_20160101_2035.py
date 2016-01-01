# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aworker', '0011_auto_20160101_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'17fcdce6372c44778318d985961187ab', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
