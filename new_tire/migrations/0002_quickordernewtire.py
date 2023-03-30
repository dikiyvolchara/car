# Generated by Django 4.1 on 2023-03-30 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('new_tire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickOrderNewTire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(verbose_name='телефон')),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('-', '-'), ('Бронь', 'Бронь'), ('Не відповів', 'Не відповів'), ('Забрав', 'Забрав'), ('Відмова', 'Відмова')], default='-', max_length=50, null=True)),
                ('complete', models.BooleanField(default=False, verbose_name='Виконаний')),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_tire_client', to=settings.AUTH_USER_MODEL)),
                ('tire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quikoreder_new_tire', to='new_tire.tire', verbose_name='ID шин')),
            ],
            options={
                'verbose_name': 'Швидке замовлення',
                'verbose_name_plural': 'Швидкі замовлення',
                'ordering': ['complete'],
            },
        ),
    ]
