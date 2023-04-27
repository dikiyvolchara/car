# Generated by Django 4.1 on 2023-04-27 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=999, unique=True, verbose_name="Ім'я")),
                ('mobile', models.CharField(max_length=15, unique=True, verbose_name='Моб. тел:')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Клієнти',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='CompleteSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Комплектація:')),
                ('price', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Комплектація',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StorageInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tire_info', models.CharField(max_length=999, verbose_name='Шини:')),
                ('year', models.CharField(max_length=999, verbose_name='Рік:')),
                ('country', models.CharField(max_length=150, verbose_name='Країна:')),
                ('condition', models.CharField(max_length=999, verbose_name='Стан:')),
                ('number', models.IntegerField(verbose_name='Кількість:')),
                ('additional', models.TextField(verbose_name='Додатковий опис')),
                ('storage_from', models.DateTimeField(verbose_name='Зберігання з:')),
                ('storage_to', models.DateTimeField(verbose_name='Зберігання до:')),
                ('cost', models.IntegerField(blank=True, null=True, verbose_name='Вартість:')),
                ('payee', models.IntegerField(blank=True, null=True, verbose_name='Оплата')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('qr_code', models.ImageField(blank=True, help_text='QR-code генерується автоматично', null=True, upload_to='foto_storage_tire/qr_codes')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_tire.client', verbose_name='Клієнт:')),
                ('complete_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_tire.completeset', verbose_name='Комплектація:')),
            ],
            options={
                'verbose_name_plural': 'Шини',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='foto_storage_tire', verbose_name='Фото:')),
                ('inform', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='storage_tire.storageinfo', verbose_name='Фото шин\\дисків:')),
            ],
            options={
                'verbose_name_plural': 'Фото шин',
                'ordering': ['inform'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalStorageInfo',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('tire_info', models.CharField(max_length=999, verbose_name='Шини:')),
                ('year', models.CharField(max_length=999, verbose_name='Рік:')),
                ('country', models.CharField(max_length=150, verbose_name='Країна:')),
                ('condition', models.CharField(max_length=999, verbose_name='Стан:')),
                ('number', models.IntegerField(verbose_name='Кількість:')),
                ('additional', models.TextField(verbose_name='Додатковий опис')),
                ('storage_from', models.DateTimeField(verbose_name='Зберігання з:')),
                ('storage_to', models.DateTimeField(verbose_name='Зберігання до:')),
                ('cost', models.IntegerField(blank=True, null=True, verbose_name='Вартість:')),
                ('payee', models.IntegerField(blank=True, null=True, verbose_name='Оплата')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('qr_code', models.TextField(blank=True, help_text='QR-code генерується автоматично', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('client', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='storage_tire.client', verbose_name='Клієнт:')),
                ('complete_set', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='storage_tire.completeset', verbose_name='Комплектація:')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical storage info',
                'verbose_name_plural': 'historical Шини',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCompleteSet',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Комплектація:')),
                ('price', models.IntegerField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical complete set',
                'verbose_name_plural': 'historical Комплектація',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalClient',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=999, verbose_name="Ім'я")),
                ('mobile', models.CharField(db_index=True, max_length=15, verbose_name='Моб. тел:')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical client',
                'verbose_name_plural': 'historical Клієнти',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
