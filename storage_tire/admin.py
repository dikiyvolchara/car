from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Client, CompleteSet, StorageInfo, Image

# Register your models here.
class ClientAdmin(SimpleHistoryAdmin):
    fieldsets = (
        ('Ф.І.О.:', {
            'fields': ('name',)
        }),
        ('Номер:', {
            'fields': ('mobile',)
        }),
        ('Посилання:', {
            'classes': ('collapse', ),
            'fields': ('slug', )
        })
    )

    list_display = ['name', 'mobile']
    search_fields = ['name', 'mobile']
    prepopulated_fields = {'slug': ('name', )}
    history_list_display = ['name', 'mobile']

class CompleteSetAdmin(SimpleHistoryAdmin):
    fieldsets = (
        ('Комплектація:', {
            'fields': ('name', )
        }),
        ('Вартість:', {
            'fields': ('price', )
        })
    )

    list_display = ['name', 'price']
    history_list_display = ['name', 'price']

class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('image_url', )

class StorageInfoAdmin(SimpleHistoryAdmin):
    fieldsets = (
        ('Клієнт', {
            'fields': ('client', )
        }),
        ('Опис:', {
            'fields': (('tire_info', ), ('year', 'country'), 'condition', 'number')
        }),
        ('Комплектація:', {
            'fields': ('complete_set',)
        }),
        ('Пакети:', {
            'fields': ('package',)
        }),
        ('Додатковий опис, фурнфтура', {
            'fields': ('additional', )
        }),
        ('Термін:', {
            'fields': (('storage_from', ), ('storage_to', ) )
        }),
        ('Вартість \ Оплата:', {
            'fields': (('cost', ), ('payee',), ('quantity_days'))
        }),
        ('Посилання . QRCode:', {
            'classes': ('collapse',),
            'fields': (('qr_code', ), ('slug', ))
        })
    )

    list_display = ['client', 'tire_info', 'storage_from', 'storage_to']
    history_list_display = ['tire_info', 'cost', 'payee'', storage_from', 'storage_to']
    list_display_links = ['client', 'tire_info']
    search_fields = ['client', 'tire_info']

    # prepopulated_fields = {'slug': ('tire_info',)}

    inlines = [ImageAdmin]

admin.site.register(Client, ClientAdmin)
admin.site.register(CompleteSet, CompleteSetAdmin)
admin.site.register(StorageInfo, StorageInfoAdmin)