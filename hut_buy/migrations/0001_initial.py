# Generated by Django 3.0.6 on 2020-11-16 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HutBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hut_name', models.CharField(max_length=20)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('date_time_stamp', models.DateTimeField(auto_now=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HutProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('price', models.FloatField()),
                ('hut_buy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hut_buy.HutBuy')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Products')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('hut_buy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hut_buy.HutBuy')),
            ],
        ),
    ]