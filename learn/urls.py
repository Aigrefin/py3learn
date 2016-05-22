from django.conf.urls import url

from . import views

app_name = 'learn'

urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^dictionaries/?$',
        views.DictionariesView.as_view(), name='dictionaries'),
    url(r'^dictionaries/(?P<pk>[0-9]+)/translations?$',
        views.TranslationsView.as_view(), name='translations'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises$',
        views.randomise_exercise, name='randomise_exercise'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)$',
        views.exercise, name='exercise'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/wrong_answer$',
        views.exercise_wrong_answer, name='exercise_wrong_answer'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/(?P<bad_input>bad_input)$',
        views.exercise, name='exercise_bad_input'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/validate$',
        views.validate_exercise, name='validate_exercise'),
]
