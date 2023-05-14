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
    slug = models.SlugField(unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['created', ]
        verbose_name_plural = 'Клієнти'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storage_info:client_storage_info', kwargs={'slug': self.slug})

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
        related_name='storage_client_tire',
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

    package = models.BooleanField(default=False, blank=True, null=True, db_index=False)

    additional = models.TextField(verbose_name='Додатковий опис')

    storage_from = models.DateTimeField(verbose_name='Зберігання з:')
    storage_to = models.DateTimeField(verbose_name='Зберігання до:')
    quantity_days = models.CharField(max_length=255, blank=True, null=True, verbose_name='Кількість днів:')

    cost = models.IntegerField(null=True, blank=True, verbose_name='Вартість:')
    payee = models.IntegerField(null=True, blank=True, verbose_name='Оплата')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    qr_code = models.ImageField(upload_to='foto_storage_tire/qr_codes', blank=True, null=True, help_text="QR-code генерується автоматично")

    history = HistoricalRecords()

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Шини'

    def save(self, *args, **kwargs):
        
        days = self.storage_to - self.storage_from
        if self.package:
            self.cost = days.days * self.complete_set.price * self.number + 50
        else:
            self.cost = days.days * self.complete_set.price * self.number
        self.quantity_days = days.days
        super(StorageInfo, self).save()

        if not self.qr_code:
            
            qrcode = segno.make(f'https://car-plus.kyiv.ua/storage_tire/{self.slug}/', error='l')
            out = BytesIO()
            qrcode.save(out, kind='png', dark='#000', light=None, scale=10)
            # qrcode.to_artistic(background='/car_env/media/LOGO-CAR.png', target=out, scale=40, kind='png')
            self.qr_code.save(f'{self.id}.png', File(out), save=False)

            super(StorageInfo, self).save()

        if not self.slug:
            self.slug = slugify(self.tire_info) + '-' + str(self.id)
            super(StorageInfo, self).save()

        
    def __str__(self):
        return self.tire_info

    def get_absolute_url(self):
        return reverse('storage_info:detail_storage_info', kwargs={'client_slug': self.client.slug, 'slug': self.slug})


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
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="250px">')