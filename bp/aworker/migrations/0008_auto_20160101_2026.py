# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aworker', '0007_auto_20160101_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractusermixin',
            name='user',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default=b'288c17b8df49445f884ad71066ce7a8a', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
