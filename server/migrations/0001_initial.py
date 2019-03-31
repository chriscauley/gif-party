# Generated by Django 2.1.7 on 2019-03-31 15:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import unrest.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data_hash', models.BigIntegerField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, unrest.models.JsonMixin),
        ),
        migrations.CreateModel(
            name='SourceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('src', models.ImageField(upload_to='source_images')),
            ],
        ),
    ]
