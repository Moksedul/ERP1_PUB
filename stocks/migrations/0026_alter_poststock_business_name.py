# Generated by Django 3.2.8 on 2021-12-07 14:39

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0013_auto_20210919_2339'),
        ('stocks', '0025_poststock_business_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poststock',
            name='business_name',
            field=models.ForeignKey(on_delete=django.db.models.fields.Empty, to='organizations.organization'),
        ),
    ]
