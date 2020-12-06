# Generated by Django 3.0.6 on 2020-12-07 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0007_auto_20201207_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salevoucher',
            name='fotka_rate',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='salevoucher',
            name='fotka_weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='salevoucher',
            name='moisture_weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='salevoucher',
            name='seed_weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
