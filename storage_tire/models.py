from django.db import models
from simple_history.models import HistoricalRecords
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import segno
from io import BytesIO
from django.core.files import File
from PIL import Image as IMG
from PIL import ImageDraw

# Create your models here.

#Model clients for storega tires
class Client(models.Model):
    name = models.CharField(max_length=999, unique=True, verbose_name="Ім'я")
    mobile = models.CharField(max_length=15, unique=True, verbose_name="Моб. тел:")
    created = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['created', ]
        verbose_name_plural = 'Клієнти'

    def __str__(self):
        return self.name

#Complete Set for storage tires
class CompleteSet(models.Model):
    name = models.CharField(max_length=255, verbose_name="Комплектація:")
    price = models.IntegerField()
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Комплектація'

    def __str__(self):
        return self.name

#Informations storage tires
class StorageInfo(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клієнт:')

    tire_info = models.CharField(max_length=999, verbose_name='Шини:')
    year = models.CharField(max_length=999, verbose_name='Рік:')
    country = models.CharField(max_length=150, verbose_name='Країна:')
    condition = models.CharField(max_length=999, verbose_name='Стан:')
    number = models.IntegerField(verbose_name='Кількість:')

    #complete set tires
    complete_set = models.ForeignKey(
        CompleteSet,
        on_delete = models.CASCADE,
        verbose_name='Комплектація:'
    )

    additional = models.TextField(verbose_name='Додатковий опис:')

    storage_from = models.DateTimeField(verbose_name='Зберігання з:')
    storage_to = models.DateTimeField(verbose_name='Зберігання до:')

    cost = models.IntegerField(null=True, blank=True, verbose_name='Вартість:')
    payee = models.IntegerField(null=True, blank=True, verbose_name='Оплата')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['created']
        verbose_name_plural = 'Шини'

    def save(self, *args, **kwargs):
        # super(StorageInfo, self).save()

        # if self.complete_set == 'Шини':
        #     day = self.storage_to - self.storage_from
        #     cost = day.days * self.complete_set.price * self.number
        #     super(StorageInfo, self).save()
        # else:

        days = self.storage_to - self.storage_from
        self.cost = days.days * self.complete_set.price * self.number
        super(StorageInfo, self).save()

        



    def __str__(self):
        return self.tire_info


#Foto storage tires
class Image(models.Model):
    image = models.ImageField(upload_to='foto_storage_tire', verbose_name='Фото:')
    inform = models.ForeignKey(
        StorageInfo,
        default=False,
        on_delete=models.CASCADE,
        verbose_name='Фото шин\дисків:')

    class Meta:
        ordering = ['inform']
        verbose_name_plural = 'Фото шин'

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="250px"')