# Generated by Django 3.1.1 on 2020-10-21 17:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_auto_20201020_0237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.day'),
        ),
    ]