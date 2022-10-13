from django.contrib import admin

from .models import Advertisement, FavoriteAdvertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'creator', 'created_at', 'updated_at']


@admin.register(FavoriteAdvertisement)
class FavoriteAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['favorite', 'user']