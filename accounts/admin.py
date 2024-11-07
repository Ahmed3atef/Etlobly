# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount
from .forms import UserRegistrationForm

class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    model = UserAccount
    list_display = ('email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'DOB', 'image', 'instapay_account')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_data_entry')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'DOB','phone_number','is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(UserAccount, CustomUserAdmin)
