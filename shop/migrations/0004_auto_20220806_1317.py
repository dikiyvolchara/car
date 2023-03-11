# Generated by Django 3.2.7 on 2022-08-06 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220806_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltire',
            name='qr_code',
            field=models.TextField(blank=True, help_text='QR-code генерується автоматично', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tire',
            name='qr_code',
            field=models.ImageField(blank=True, help_text='QR-code генерується автоматично', null=True, upload_to='media/qr_codes'),
        ),
    ]