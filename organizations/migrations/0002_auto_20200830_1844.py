# Generated by Django 3.0.6 on 2020-08-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persons',
            name='contact_number',
            field=models.CharField(blank=True, max_length=17, null=True, unique=True),
        ),
    ]
