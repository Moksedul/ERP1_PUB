# Generated by Django 3.1.4 on 2021-05-16 21:13

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0010_auto_20210515_2251'),
        ('challan', '0012_auto_20210515_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='challan',
            name='sub_dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='organizations.persons'),
        ),
    ]
