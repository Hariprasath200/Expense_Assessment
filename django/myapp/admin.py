from django.contrib import admin
from .models import CustomUser, Profile,Expense
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'role')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
admin.site.register(Expense)