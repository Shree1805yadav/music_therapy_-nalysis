# Generated by Django 3.1.7 on 2022-01-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0010_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='user',
            field=models.CharField(default='', max_length=100),
        ),
    ]