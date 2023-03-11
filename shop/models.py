# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# from django.db.models import deletion
# from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import segno
from io import BytesIO
from django.core.files import File
from PIL import Image as IMG
from PIL import ImageDraw


class Season(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Сезон:')
    image_icon = models.ImageField(upload_to='season_icon', blank=True)
    description = RichTextField(null=True, blank=True, verbose_name='Опис сезону:')
    slug = models.SlugField(unique=True)


    class Meta:
        ordering = ['name']
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезон'

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse('shop:Season', args=[self.slug])

class Kind(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип:')
    image_icon = models.ImageField(upload_to='kind_icon', blank=True)
    description = RichTextField(null=True, blank=True, verbose_name='Опис:')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип'
        verbose_name_plural = 'Тип'

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse('shop:Name', args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Назва бренду:")
    image_icon = models.ImageField(upload_to='brand_icon', blank=True)
    description = RichTextField(null=True, blank=True, verbose_name='Опис бренду:')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:brand_detail', kwargs={'slug': self.slug})

    #def get_absolute_url(self):
    #    return reverse('shop:TireListByCategory', args=[self.slug])

class BrandModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Модель:')
    brand = models.ForeignKey(Brand, related_name='brand_model', on_delete=models.CASCADE, verbose_name='Бренд моделі:')
    season = models.ForeignKey(Season, related_name='brand_model_season', on_delete=models.CASCADE, verbose_name='Сезон моделі')
    description = RichTextField(null=True, blank=True, verbose_name='Опис моделі:')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Модель'
        verbose_name_plural = 'Модель'

    def __str__(self):
        return self.name

    

    def get_absolute_url(self):
        return reverse('shop:brand_model_detail', kwargs={'brand_slug': self.brand.slug, 'slug': self.slug})
    #def get_absolute_url(self):
    #    return reverse('shop:TireListByCategory', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Категорія:')
    kind = models.ForeignKey(Kind, default=1, related_name='category_kind', on_delete=models.CASCADE, verbose_name='Тип категорії:')
    description = RichTextField(null=True, blank=True, verbose_name='Опис категорії:')
    slug = models.SlugField(unique=True)

    # SEO fields
    seo_title = models.CharField(max_length=64, blank=True, verbose_name="SEO Title")
    seo_description = models.TextField(blank=True, verbose_name='SEO Description')
    seo_keywords = models.CharField(max_length=120, blank=True, verbose_name='SEO Keywords')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_list', kwargs={'category_slug': self.slug})

class IndexSpeed(models.Model):
    name_one = models.CharField(max_length=2, unique=True, verbose_name='Індекс:')
    name_two = models.CharField(max_length=25, verbose_name='Значення:')

    class Meta:
        ordering = ['name_one']
        verbose_name = 'Індекс швидкості'
        verbose_name_plural = 'Індекси швидкості'

    def __str__(self):
        return self.name_one


class IndexLoad(models.Model):
    name_one = models.CharField(max_length=10, unique=True, verbose_name='Індекс:')
    name_two = models.CharField(max_length=25, verbose_name='Значення:')

    class Meta:
        ordering = ['name_one']
        verbose_name = 'Індекс навантаження'
        verbose_name_plural = 'Індекси навантаження'

    def __str__(self):
        return self.name_one


class Tire(models.Model):

    CHOICES = (
        ('-', '-'),
        ('Т', 'Т'),
        ('БК', 'БК'),
        ('КЛ', 'КЛ'),
        ('Л/П', 'Л/П'),
    )

    category = models.ForeignKey(Category, related_name='tire_category', on_delete=models.CASCADE, verbose_name='Категорія:')

    model = models.ForeignKey(BrandModel, related_name='tire_model', on_delete=models.CASCADE, verbose_name='Модель:')

    index_load = models.ForeignKey(
        IndexLoad, related_name='tire_index_load', on_delete=models.CASCADE, verbose_name='Індекс навантаження:')
    index_speed = models.ForeignKey(
        IndexSpeed, related_name='tire_index_speed', on_delete=models.CASCADE, verbose_name='Індекс швидкості:')

    condition = models.IntegerField(verbose_name='Стан:')
    year = models.IntegerField(verbose_name='Рік:', blank=True, null=True)
    country = models.CharField(max_length=150, verbose_name='Країна:', blank=True)
    in_stock = models.IntegerField(verbose_name='На складі, шт.:')
    available = models.BooleanField(default=True, verbose_name='В наявності:')

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Вартість:')
    new_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Нова вартість:')

    recommend = models.BooleanField(default=False, verbose_name='Рекомендуєм:')

    shipy = models.BooleanField(default=False, verbose_name='Шипы')
    lipuchka = models.BooleanField(default=False, verbose_name='Липучка')
    run_flat = models.BooleanField(default=False, verbose_name='RunFlat')
    conti_seal = models.BooleanField(default=False, verbose_name='ContiSeal')
    low_prof = models.BooleanField(default=False, verbose_name='Низк.проф.')
    mad = models.BooleanField(default=False, verbose_name='Грязевые')
    rain = models.BooleanField(default=False, verbose_name='Дождевые')


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True)

    choice = models.CharField(max_length=50, choices=CHOICES, blank=True, null=True) #позначки для адміна по шинам

    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True, help_text="QR-code генерується автоматично")

    articul = models.CharField(max_length=25, blank=True, null=True, verbose_name='Артикул')

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super(Tire, self).save()
        if not self.slug:
            self.slug = slugify(self.category.slug) + '-' + str(self.model.brand) + '-' + str(self.model.slug) + '-' + str(self.id)
            super(Tire, self).save()

        if not self.articul:

            self.articul = '02-'+ str(self.id)

            super(Tire, self).save()

        if self.qr_code:
            pass
        else:
            qrcode = segno.make(f'https://car-plus.kyiv.ua/{self.category.slug}/{self.slug}/', error='l')
            out = BytesIO()
            qrcode.save(out, kind='png', dark='#000', light=None, scale=10)
            # qrcode.to_artistic(background='/car_env/media/LOGO-CAR.png', target=out, scale=40, kind='png')
            self.qr_code.save(f'{self.id}.png', File(out), save=False)

            super(Tire, self).save()


    def get_absolute_url(self):
        return reverse('shop:tire_detail', kwargs={'category_slug': self.category.slug, "slug": self.slug})

    def __str__(self):
        return str(self.category)+'-'+str(self.model)+'-'+str(self.model.brand.name)



class Image(models.Model):
    image = models.ImageField(upload_to='foto', verbose_name='Зображення:')
    tire = models.ForeignKey(
        Tire, default=False, on_delete=models.CASCADE, verbose_name='Резина:')

    class Meta:
        ordering = ['tire']
        verbose_name = 'Зображення'
        verbose_name_plural = 'Зображення'

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="250px"')


class QuickOrder(models.Model):
    
    CHOICES = (
        ('-', '-'),
        ('Бронь', 'Бронь'),
        ('Не відповів', 'Не відповів'),
        ('Забрав', 'Забрав'),
        ('Відмова', 'Відмова'),
    )

    phone = models.IntegerField(verbose_name="телефон")
    tire = models.ForeignKey(Tire, related_name='quikoreder_tire', on_delete=models.CASCADE,  blank=True, null=True, verbose_name='ID шин')
    price = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=CHOICES, blank=True, null=True, default='-')
    client = models.ForeignKey(User, related_name='client', on_delete=models.CASCADE, blank=True, null=True)
    # manager = models.ForeignKey(User, related_name='quick_order_user', on_delete=models.CASCADE, blank=True, null=True)
    complete = models.BooleanField(default=False, verbose_name='Виконаний')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['complete']
        verbose_name = 'Швидке замовлення'
        verbose_name_plural = 'Швидкі замовлення'

    def __str__(self):
        return str(self.phone)