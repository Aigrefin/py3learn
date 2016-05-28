from django.contrib import admin

from .models import Dictionary, Translation, Configuration


class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 1


class DictionaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['language']}),
    ]
    inlines = [TranslationInline]

admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Configuration, admin.ModelAdmin)
