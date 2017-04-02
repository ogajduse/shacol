# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20170328_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collisions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_order', models.IntegerField()),
                ('input_hash', models.CharField(max_length=30)),
                ('total_time', models.CharField(max_length=30)),
                ('cycles', models.IntegerField()),
                ('coll_hash', models.CharField(max_length=30)),
                ('test_method', models.CharField(max_length=30)),
                ('bits', models.IntegerField()),
                ('git_revision', models.CharField(max_length=50)),
            ],
        ),
    ]
