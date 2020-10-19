# Generated by Django 3.1.1 on 2020-10-18 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=50)),
                ('fathers_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mothers_name', models.CharField(blank=True, max_length=50, null=True)),
                ('spouse_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=11, null=True)),
                ('hourly_rate', models.FloatField()),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('joining_date', models.DateField(default=django.utils.timezone.now)),
                ('photo', models.ImageField(default='default.jpg', upload_to='employee_photo')),
            ],
        ),
    ]