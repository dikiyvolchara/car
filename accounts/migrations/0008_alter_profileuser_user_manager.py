# Generated by Django 4.1 on 2023-03-14 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_profileuser_user_manager_delete_manageruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='user_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_manager', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер клієнта'),
        ),
    ]