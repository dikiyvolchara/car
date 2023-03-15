# -*- coding: utf-8 -*-
from simple_history.admin import SimpleHistoryAdmin
# from simple_history import register
# from django.contrib.auth.models import User
from django.contrib import admin
from .models import Brand, Category, Tire, Season, Kind, BrandModel, IndexSpeed, IndexLoad, Image, QuickOrder

class IndexSpeedAdmin(admin.ModelAdmin):
    list_display = ['name_one', 'name_two']
    list_filter = ['name_one', 'name_two']


class IndexLoadAdmin(admin.ModelAdmin):
    list_display = ['name_one', 'name_two']
    list_filter = ['name_one', 'name_two']

class BrandAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'image_icon', 'description')
        }
        ),
        ('Автозаполнение', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }
        ),
    )

    list_display = ['name', ]
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name', ), }

class BrandModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'brand', 'season', 'description')
        }),
    ('Автозаповнення', {
        'classes': ('collapse',),
        'fields': ('slug',),
    }),
    )

    list_display = ['name', 'brand' ]
    autocomplete_fields = ['brand', ]
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name', ), }

class CategoryAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'kind', 'description')
        }),
        
        ('SEO Block', {
            'classes': ('collapse',),
            'fields': (
                    ('seo_title', ),
                    ('seo_description', ),
                    ('seo_keywords',)
                ),
        }),

        ('Автозаповнення', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )
    list_editable = ['slug', ]
    list_display = ['name', 'kind', 'slug']
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name', ), }

class SeasonAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'image_icon', 'description')
        }),
        ('Автозаповнення', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )

    list_display = ['name', ]
    prepopulated_fields = {'slug': ('name', ), }

class KindAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'image_icon', 'description')
        }),
        ('Автозаповнення', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )

    list_display = ['name', ]
    prepopulated_fields = {'slug': ('name', ), }


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('image_url',)

class TireAdmin(SimpleHistoryAdmin):

    fieldsets = (
        (None, {
            'fields': (('category', 'model'), ('index_load', 'index_speed'),
                            ('condition', 'year', 'country', 'in_stock', 'available'),
                        ('price', 'new_price'), 'recommend')
        }
        ),
        ('Дополнительная информация', {
            'classes': ('collapse',),
            'fields': (('shipy', 'lipuchka', 'run_flat', 'conti_seal', 'low_prof', 'mad', 'rain'), 'choice' )
        }
        ),
        ('Автозаполнение', {
            'classes': ('collapse',),
            'fields': ('slug', 'articul',)
        }
        ),
        ('QR-Code', {
            'classes': ('collapse',),
            'fields': ('qr_code',)
        }
        ),
    )

    list_display = ['articul', 'model', 'category', 'index_load', 'index_speed', 
                        'condition', 'in_stock', 'price', 'new_price', 'available']

    # prepopulated_fields = {'slug': ('category', 'model' ), }
    history_list_display = ['price', 'new_price']
    list_editable = ['condition', 'in_stock', 'available', 'price', 'new_price']
    list_display_links = ['articul', 'model']
    search_fields = ['articul', 'model__name', 'model__brand__name', 'category__name']

    # search_fields = ['category', 'model']
    inlines = [ImageAdmin]
    autocomplete_fields = ['category', 'model']  # поле для поиска по ForeignKey



class QuickOrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('phone', ('status', ), ('client', 'manager'), 'complete', 'created', 'updated')
        }
        ),
        ('Коментар:', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('comment',)
        }
        ),
        ('Шини:', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('tire',)
        }
        ),
    )

    list_display = ['id', 'phone', 'complete', 'status', 'created', 'updated', 'get_tire']
    readonly_fields = ['created', 'updated', 'tire']

    list_editable = ['complete',]
    list_display_links = ['id', 'phone']
    search_fields = ['phone',]
    

    def get_tire(self, obj):
        return obj.tire.category.name

    # def get_readonly_fields(self, request, obj=None):

    #     if obj.manager != None:
    #        return  self.readonly_fields + ['manager',]
    #     return self.readonly_fields


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tire, TireAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(BrandModel, BrandModelAdmin)
# admin.site.register(Image, ImageAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(IndexSpeed, IndexSpeedAdmin)
admin.site.register(IndexLoad, IndexLoadAdmin)
admin.site.register(QuickOrder, QuickOrderAdmin)