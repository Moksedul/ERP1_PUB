# Generated by Django 3.0.6 on 2020-05-23 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200522_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_company', models.CharField(max_length=200)),
                ('company_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('nid', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('contact_number', models.CharField(max_length=17, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('nid_photo', models.ImageField(blank=True, upload_to='nid_photo')),
            ],
        ),
    ]
