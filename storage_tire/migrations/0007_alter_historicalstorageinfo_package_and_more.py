# Generated by Django 4.1 on 2023-04-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_tire', '0006_historicalstorageinfo_package_storageinfo_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstorageinfo',
            name='package',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='storageinfo',
            name='package',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
