# Generated by Django 3.1.1 on 2022-01-23 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0011_recommendation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='path',
            field=models.CharField(default='', max_length=100),
        ),
    ]
