# Generated by Django 3.0.6 on 2020-06-19 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0017_auto_20200619_1743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyvoucher',
            old_name='weight',
            new_name='weight_per_bag',
        ),
    ]