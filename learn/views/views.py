from django.shortcuts import redirect
from django.views import generic

from learn.models import Dictionary


def index(request):
    return redirect('learn:dictionaries')


class DictionariesView(generic.ListView):
    model = Dictionary
    template_name = 'learn/dictionaries.html'
    context_object_name = 'dictionaries_list'

    def get_queryset(self):
        return Dictionary.objects.order_by('language')


class TranslationsView(generic.DetailView):
    model = Dictionary
    template_name = 'learn/translations.html'
