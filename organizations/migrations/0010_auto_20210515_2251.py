# Generated by Django 3.1.4 on 2021-05-15 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_organization_proprietor'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='pad',
            field=models.ImageField(blank=True, upload_to='company_docs'),
        ),
        migrations.AddField(
            model_name='organization',
            name='signature',
            field=models.ImageField(blank=True, upload_to='company_docs'),
        ),
    ]
