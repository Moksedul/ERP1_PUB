# Generated by Django 3.0.6 on 2021-05-17 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challan', '0015_auto_20210516_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challan',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]
