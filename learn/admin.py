from django.contrib import admin
from py3njection import inject

from learn.services.normalizer import TranslationNormalizer
from .models import Dictionary, Translation, Configuration


class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 1


class DictionaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['language']}),
    ]
    inlines = [TranslationInline]

    @inject
    def save_formset(self, request, form, formset, change, normalizer: TranslationNormalizer):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            normalized_instance = normalizer.normalize_translation(instance)
            normalized_instance.save()
        formset.save_m2m()


admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Configuration, admin.ModelAdmin)
