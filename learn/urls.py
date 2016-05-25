from django.conf.urls import url
from django.contrib.auth.views import logout

from learn.views import signin, exercise, login
from .views import views

app_name = 'learn'

urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^signin/?$', signin.signin_view, name='signin'),
    url(r'^login/?$', login.login_view, name='login'),
    url(r'^logout/$', logout,{'next_page': '/login'}, name='logout'),
    url(r'^dictionaries/?$',
        views.DictionariesView.as_view(), name='dictionaries'),
    url(r'^dictionaries/(?P<pk>[0-9]+)/translations?$',
        views.TranslationsView.as_view(), name='translations'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises$',
        exercise.randomise_exercise, name='randomise_exercise'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)$',
        exercise.exercise, name='exercise'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/wrong_answer$',
        exercise.exercise_wrong_answer, name='exercise_wrong_answer'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/(?P<bad_input>bad_input)$',
        exercise.exercise, name='exercise_bad_input'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/validate$',
        exercise.validate_exercise, name='validate_exercise'),
]
