from django.contrib import admin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import Tire, Width, Height, Radius, Brand, Kind, Season, QuickOrderNewTire

# Register your models here.

class TireResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        width = row['width']
        height = row['height']
        radius = row['radius']
        brand = row['brand']
        kind = row['kind']
        season = row['season']
        
        Width.objects.get_or_create(name=width, defaults={"name": width})
        Height.objects.get_or_create(name=height, defaults={"name": height})
        Radius.objects.get_or_create(name=radius, defaults={"name": radius})
        Brand.objects.get_or_create(name=brand, defaults={"name": brand})
        Kind.objects.get_or_create(name=kind, defaults={"name": kind})
        Season.objects.get_or_create(name=season, defaults={"name": season})

    width = fields.Field(
        column_name='width',
        attribute='width',
        widget=ForeignKeyWidget(model=Width, field='name')
    )
    height = fields.Field(
        column_name='height',
        attribute='height',
        widget=ForeignKeyWidget(model=Height, field='name')
    )
    radius = fields.Field(
        column_name='radius',
        attribute='radius',
        widget=ForeignKeyWidget(model=Radius, field='name')
    )
    brand = fields.Field(
        column_name='brand',
        attribute='brand',
        widget=ForeignKeyWidget(model=Brand, field='name')
    )
    kind = fields.Field(
        column_name='kind',
        attribute='kind',
        widget=ForeignKeyWidget(model=Kind, field='name')
    )
    season = fields.Field(
        column_name='season',
        attribute='season',
        widget=ForeignKeyWidget(model=Season, field='name')
    )


    class Meta:
        model = Tire
        import_id_fields = ('description',)
        fields = ('width', 'height', 'radius', 'brand', 'description', 'kind', 'season', 'country', 'year', 'in_stock', 'price_one', 'price_two', 'price_three')
        # skip_unchanged = True

class TireAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_classes = [TireResource]


    list_display = ['articul', 'brand', 'kind', 'description', 'price_one', 'price_two', 'price_three', 'created', 'updated' ]

    # prepopulated_fields = {'slug': ('category', 'model' ), }
    history_list_display = ['price_one', 'price_two', 'price_three', ]
    list_display_links = ['articul', ]
    search_fields = ['articul', 'brand__name', 'description']
    # prepopulated_fields = {'slug': ('description', 'brand',  )}


class QuickOrderNewTireAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('phone', ('status', ), ('client', ), 'complete', 'created', 'updated')
        }
        ),
        ('Коментар:', {
            # 'classes': ('wide', 'extrapretty'),
            'fields': ('comment',)
        }
        ),
        ('Шини:', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('tire', )
        }
        ),
    )

    list_display = ['id', 'phone', 'complete', 'status', 'created', 'updated', 'get_tire']
    readonly_fields = ['created', 'updated', 'tire']

    list_editable = ['complete',]
    list_display_links = ['id', 'phone']
    search_fields = ['phone',]
    

    def get_tire(self, obj):
        return obj.tire.description

    # def get_readonly_fields(self, request, obj=None):

    #     if obj.manager != None:
    #        return  self.readonly_fields + ['manager',]
    #     return self.readonly_fields


admin.site.register(Tire, TireAdmin)
admin.site.register(QuickOrderNewTire, QuickOrderNewTireAdmin)
admin.site.register(Width)
admin.site.register(Height)
admin.site.register(Radius)
admin.site.register(Brand)
admin.site.register(Kind)
admin.site.register(Season)