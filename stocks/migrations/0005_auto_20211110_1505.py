# Generated by Django 3.2.8 on 2021-11-10 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20211110_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='date_time_stamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]