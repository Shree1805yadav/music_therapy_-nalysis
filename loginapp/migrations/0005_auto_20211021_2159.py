# Generated by Django 3.1.1 on 2021-10-21 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0004_auto_20211021_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdata',
            name='user',
        ),
        migrations.AddField(
            model_name='formdata',
            name='User',
            field=models.CharField(default='', max_length=100),
        ),
    ]
