# Generated by Django 3.0.6 on 2020-08-26 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalvoucher',
            name='from_account',
            field=models.ForeignKey(blank=True, default=14, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Accounts'),
        ),
    ]
