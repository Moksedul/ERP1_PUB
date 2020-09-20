# Generated by Django 3.0.6 on 2020-09-20 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200830_1844'),
        ('vouchers', '0002_auto_20200826_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalvoucher',
            name='person_name',
            field=models.ForeignKey(default='name deleted', on_delete=django.db.models.deletion.SET_DEFAULT, to='organizations.Persons'),
        ),
    ]
