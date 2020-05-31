# Generated by Django 3.0.6 on 2020-05-29 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20200521_1621'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField()),
                ('number_of_bag', models.FloatField()),
                ('weight', models.FloatField()),
                ('product_condition', models.CharField(choices=[(1, 'Processed'), (2, 'Un Processed')], default=1, max_length=50)),
                ('remarks', models.CharField(blank=True, max_length=200)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name_of_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Products')),
            ],
        ),
    ]
