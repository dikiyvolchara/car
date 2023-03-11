# Generated by Django 4.1 on 2022-08-21 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_historicaltire_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, verbose_name='телефон')),
                ('tire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quikoreder_tire', to='shop.tire', verbose_name='ID шин')),
            ],
        ),
    ]
