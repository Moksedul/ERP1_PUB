# Generated by Django 3.1.1 on 2021-03-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LC', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lcproduct',
            name='bags',
            field=models.FloatField(default=0),
        ),
    ]
