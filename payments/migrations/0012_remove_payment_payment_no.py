# Generated by Django 3.0.6 on 2021-10-28 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20210508_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_no',
        ),
    ]
