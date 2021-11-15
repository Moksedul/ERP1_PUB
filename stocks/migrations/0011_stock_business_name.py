# Generated by Django 3.2.8 on 2021-11-15 13:32

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0013_auto_20210919_2339'),
        ('stocks', '0010_auto_20211113_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='business_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='organizations.organization'),
        ),
    ]