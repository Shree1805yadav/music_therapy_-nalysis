# Generated by Django 3.1.7 on 2022-01-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0008_auto_20211022_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdata',
            name='Recommendation',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
