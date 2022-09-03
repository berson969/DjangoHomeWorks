from django.contrib import admin

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'pub_date', 'pub_date_str', 'image']
    list_filter = ['name', 'author']

