# Generated by Django 3.1.4 on 2021-05-10 23:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201010_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
