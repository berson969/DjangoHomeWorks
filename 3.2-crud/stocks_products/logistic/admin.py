from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import Product, Stock, StockProduct


class StockProductInlineFormset(BaseInlineFormSet):
    pass


class StockProductInline(admin.TabularInline):
    model = StockProduct
    formset = StockProductInlineFormset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']
    inlines = [StockProductInline, ]


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ['stock', 'product', 'quantity', 'price']


