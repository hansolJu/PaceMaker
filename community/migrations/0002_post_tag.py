# Generated by Django 2.0.5 on 2018-05-24 09:29

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag',
            field=tagging.fields.TagField(blank=True, max_length=255, verbose_name='태그'),
        ),
    ]
