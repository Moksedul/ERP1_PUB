# Generated by Django 3.1.1 on 2020-10-11 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200830_1844'),
        ('local_sale', '0003_localsale_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localsale',
            name='company_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.companies'),
        ),
    ]
