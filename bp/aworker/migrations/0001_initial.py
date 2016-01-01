# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='Created')),
                ('duration', models.IntegerField(default=86400, help_text='Duration in sec.', verbose_name='Duration')),
                ('code', models.CharField(default=b'dc3fdbacb72e4658a52db8419b83edb6', max_length=32, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
