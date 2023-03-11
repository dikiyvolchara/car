# Generated by Django 4.1 on 2023-03-10 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=75, null=True)),
                ('delivery', models.TextField(blank=True, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('user_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_manager', to=settings.AUTH_USER_MODEL, verbose_name=' Менеджер клієнта:')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL, verbose_name='Профіль користувача')),
            ],
            options={
                'verbose_name': 'Особиста інформація',
            },
        ),
    ]