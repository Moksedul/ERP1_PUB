# Generated by Django 3.2.8 on 2021-11-10 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_auto_20211109_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='date_time_stamp',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='last_updated_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]