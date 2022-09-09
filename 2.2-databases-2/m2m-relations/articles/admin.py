from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        its_main = 0
        for form in self.forms:
            if self.deleted_forms and self._should_delete_form(form):
                continue
            elif form.cleaned_data.get('is_main'):
                its_main += 1
        if its_main > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif its_main == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    list_filter = ['title']
    inlines = [ScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    # inlines = [ScopeInline, ]
