from django.contrib import admin
from .models import ProfileUser
from shop.models import QuickOrder

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User 


# class ProfileUserAdmin(admin.ModelAdmin):

#     fieldsets = (
#         (None, {
#             'fields': (('user_profile', ), ('city', 'delivery', ), ('birthday'), 'discount',)
#         }),
#         ('Менеджер:', {
#             'classes': ('wide', 'extrapretty', ),
#             'fields': ('user_manager',)
#         }),
#     )

#     list_display = ['user_profile', ]
#     list_display_links = ['user_profile', ]
#     readonly_fields = ['user_profile', ]
#     search_fields = ['user_profile', ]

# admin.site.register(ProfileUser, ProfileUserAdmin)

class ProfileUserInform(admin.StackedInline):
    model = ProfileUser
    fk_name = "user_profile"
    can_delete = False
    verbose_name_plural = 'Profile'

class QuickOrderInform(admin.StackedInline):
    model = QuickOrder
    fk_name = "client"
    can_delete = False
    verbose_name_plural = 'QuickOrder'

    extra = 1

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileUserInform, QuickOrderInform)

# # Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)