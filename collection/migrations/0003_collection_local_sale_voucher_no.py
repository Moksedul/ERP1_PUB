# Generated by Django 3.1.1 on 2020-10-05 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('local_sale', '0002_auto_20201002_1248'),
        ('collection', '0002_collection_sale_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='local_sale_voucher_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='local_sale.localsale'),
        ),
    ]