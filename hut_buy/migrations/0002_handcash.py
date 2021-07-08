# Generated by Django 3.0.6 on 2021-07-07 15:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hut_buy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HandCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.FloatField()),
            ],
        ),
    ]