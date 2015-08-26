# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=255)),
                ('text', models.TextField(null=True)),
                ('image', models.ImageField(upload_to=b'tweet_images')),
                ('search', models.CharField(max_length=255)),
            ],
        ),
    ]
