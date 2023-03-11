from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileUser(models.Model):
    user_profile = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE, verbose_name='Профіль користувача')

    user_manager = models.ForeignKey(User, related_name='user_manager', on_delete=models.CASCADE, verbose_name='Менеджер клієнта:', blank=True, null=True)

    city = models.CharField(max_length=75, blank=True, null=True)
    delivery = models.TextField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Особиста інформація'

    def __str__(self):
        return str(self.user_profile.username)
