# Generated by Django 3.1.1 on 2022-01-23 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0012_recommendation_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recommendation',
            old_name='path',
            new_name='music_path',
        ),
    ]
