# Generated by Django 3.0.6 on 2021-09-19 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_auto_20210919_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='company_address',
            field=models.TextField(max_length=500),
        ),
    ]
