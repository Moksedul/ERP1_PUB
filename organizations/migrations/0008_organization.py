# Generated by Django 3.1.4 on 2021-05-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
