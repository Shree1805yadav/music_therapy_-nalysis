# Generated by Django 3.1.1 on 2021-10-21 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0005_auto_20211021_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formdata',
            old_name='User',
            new_name='user',
        ),
    ]