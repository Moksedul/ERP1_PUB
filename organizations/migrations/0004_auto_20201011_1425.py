# Generated by Django 3.0.6 on 2020-10-11 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_persons_person_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persons',
            name='person_photo',
            field=models.ImageField(default='default.jpg', upload_to='person_photo'),
        ),
    ]
