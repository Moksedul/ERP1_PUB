# Generated by Django 3.1.4 on 2021-05-10 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LC', '0004_auto_20210401_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lc',
            name='date_time_stamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]