# Generated by Django 3.0.6 on 2020-09-20 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200830_1844'),
        ('vouchers', '0003_auto_20200920_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalvoucher',
            name='person_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='organizations.Persons'),
        ),
    ]