from django.contrib import admin

# Register your models here.
from account.models import Profile, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
