# Generated by Django 3.0.6 on 2020-06-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccounts',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='otheraccounts',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
