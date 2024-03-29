# Generated by Django 3.2.10 on 2022-03-18 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('vouchers', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PreProcessingStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='YardLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessingStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_loss', models.FloatField(default=0)),
                ('date_time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('processing_completed', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=225)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_stock_added_by', to=settings.AUTH_USER_MODEL)),
                ('pre_processing_stocks', models.ManyToManyField(to='stocks.PreProcessingStock')),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='processing_stock_updated_by', to=settings.AUTH_USER_MODEL)),
                ('yard_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='stocks.yardlocation')),
            ],
        ),
        migrations.CreateModel(
            name='PreStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_adjustment', models.FloatField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('rate_per_kg', models.FloatField(default=0)),
                ('rate_per_mann', models.FloatField(default=0)),
                ('number_of_bag', models.FloatField(default=0)),
                ('weight_of_bags', models.FloatField(default=0)),
                ('date_time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('added_to_finished_stock', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=225)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock_added_by', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('store_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='stocks.store')),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='stock_updated_by', to=settings.AUTH_USER_MODEL)),
                ('voucher_no', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vouchers.buyvoucher')),
            ],
        ),
        migrations.AddField(
            model_name='preprocessingstock',
            name='pre_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.prestock'),
        ),
        migrations.CreateModel(
            name='PostStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=0)),
                ('rate_per_kg', models.FloatField(default=0)),
                ('bags', models.FloatField(default=0)),
                ('is_finished', models.BooleanField(default=False)),
                ('business_name', models.ForeignKey(on_delete=django.db.models.fields.Empty, to='organizations.organization')),
                ('processing_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.processingstock')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.products')),
                ('store', models.ForeignKey(default=1, on_delete=django.db.models.fields.Empty, to='stocks.store')),
            ],
        ),
        migrations.CreateModel(
            name='FinishedStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_per_kg', models.FloatField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('number_of_bag', models.FloatField(default=0)),
                ('date_time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('inventory_updated', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=225)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finished_stock_added_by', to=settings.AUTH_USER_MODEL)),
                ('business_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='organizations.organization')),
                ('processing_stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.processingstock')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.products')),
                ('store_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.Empty, to='stocks.store')),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='finished_stock_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
