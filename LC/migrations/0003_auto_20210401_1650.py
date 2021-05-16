# Generated by Django 3.1.1 on 2021-04-01 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_bank'),
        ('LC', '0002_lcproduct_bags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lc',
            name='bank_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='organizations.bank'),
        ),
    ]