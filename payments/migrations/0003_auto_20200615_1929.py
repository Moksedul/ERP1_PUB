# Generated by Django 3.0.6 on 2020-06-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20200615_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payed_to',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
