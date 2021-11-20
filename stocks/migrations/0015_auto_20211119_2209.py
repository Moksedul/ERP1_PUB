# Generated by Django 3.2.8 on 2021-11-19 16:09

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0013_auto_20210919_2339'),
        ('stocks', '0014_finishedstock_number_of_bag'),
    ]

    operations = [
        migrations.AddField(
            model_name='finishedstock',
            name='business_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='organizations.organization'),
        ),
        migrations.AddField(
            model_name='finishedstock',
            name='store_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='stocks.store'),
        ),
        migrations.AlterField(
            model_name='finishedstock',
            name='pre_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.prestock'),
        ),
    ]
