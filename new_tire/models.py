from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

# Create your models here.
class Width(models.Model):
    name = models.PositiveIntegerField(verbose_name='Width')

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

class Height(models.Model):
    name = models.PositiveIntegerField()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

class Radius(models.Model):
    name = models.PositiveIntegerField()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

class Brand(models.Model):
    name = models.CharField(max_length=55)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

class Kind(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

class Season(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

class Tire(models.Model):

    width = models.ForeignKey(
        Width,
        on_delete=models.CASCADE,
        related_name='tire_width',
        verbose_name='Ширина',
        null=True,
        blank=True)

    height = models.ForeignKey(
        Height,
        on_delete=models.CASCADE,
        related_name='tire_height',
        verbose_name='Витсота',
        null=True,
        blank=True)

    radius = models.ForeignKey(
        Radius,
        on_delete=models.CASCADE,
        related_name='tire_radius',
        verbose_name='Радіус',
        null=True,
        blank=True)

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='tire_brand',
        verbose_name='Бренд',
        null=True,
        blank=True)

    description = models.CharField(max_length=255)

    kind = models.ForeignKey(
        Kind,
        on_delete=models.CASCADE,
        related_name='tire_kind',
        verbose_name='Тип',
        null=True,
        blank=True)

    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='tire_season',
        verbose_name='Сезон',
        null=True,
        blank=True)

    country = models.CharField(max_length=55)

    year = models.CharField(max_length=55)

    in_stock = models.PositiveIntegerField()

    price_one = models.PositiveIntegerField()
    price_two = models.PositiveIntegerField()
    price_three = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(
        max_length=300,
        db_index=True,
        unique=True,
        blank=True)

    articul = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name='Артикул')

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super(Tire, self).save()

        if not self.slug:
            self.slug = slugify(str(self.description).replace("/", "-") + '-' + str(self.brand) + '-' + str(self.id)).replace("/", "-")
            super(Tire, self).save(*args, **kwargs)
        
        if not self.articul:

            self.articul = '01-'+ str(self.id)

            super(Tire, self).save()

        # if not self.category_size:
        #     get_category = self.description
        #     get_category = get_category.split()
        #     self.category_size = Category.objects.get(size=get_category[0])
        #     super(Tire, self).save()



    def get_absolute_url(self):
        return reverse('tires:tire_detail', kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.description)


class QuickOrderNewTire(models.Model):
    
    CHOICES = (
        ('-', '-'),
        ('Бронь', 'Бронь'),
        ('Не відповів', 'Не відповів'),
        ('Забрав', 'Забрав'),
        ('Відмова', 'Відмова'),
    )

    phone = models.IntegerField(verbose_name="телефон")
    tire = models.ForeignKey(Tire, related_name='quikoreder_new_tire', on_delete=models.CASCADE,  blank=True, null=True, verbose_name='ID шин')
    price = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=CHOICES, blank=True, null=True, default='-')
    client = models.ForeignKey(User, related_name='new_tire_client', on_delete=models.CASCADE, blank=True, null=True)
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