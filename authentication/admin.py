# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from authentication.models import User

from .models import User

class CustomUserAdmin(UserAdmin):
    # list_display = ('username', 'email','phone_number', 'date_of_birth','is_staff', 'account_created','last_update','is_verified')
    list_display = ('email','phone_number', 'date_of_birth', 'username','full_name','is_staff', 'account_created','last_update','is_verified')
    readonly_fields = ('account_created','last_update')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('email','is_verified')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'account_created')}),
    )

admin.site.register(User, CustomUserAdmin)