from django.conf.urls import url
from django.contrib.auth.views import logout

import learn.views.choose_exercise
import learn.views.comeback
import learn.views.wrong_answer
from learn.views import signup, exercise, login
from .views import views

app_name = 'learn'

urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^signup/?$', signup.signup_view, name='signup'),
    url(r'^login/?$', login.login_view, name='login'),
    url(r'^logout/$', logout,{'next_page': '/login'}, name='logout'),
    url(r'^dictionaries/?$',
        views.DictionariesView.as_view(), name='dictionaries'),
    url(r'^dictionaries/(?P<pk>[0-9]+)/translations?$',
        views.TranslationsView.as_view(), name='translations'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises$',
        learn.views.choose_exercise.choose_rythm_notation_exercise, name='choose_exercise'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)$',
        exercise.exercise, name='exercise'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/come_back$',
        learn.views.comeback.come_back, name='come_back'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/wrong_answer$',
        learn.views.wrong_answer.exercise_wrong_answer, name='exercise_wrong_answer'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/(?P<bad_input>bad_input)$',
        exercise.exercise, name='exercise_bad_input'),
    url(r'^dictionaries/(?P<dictionary_pk>[0-9]+)/exercises/(?P<translation_pk>[0-9]+)/validate$',
        exercise.validate_exercise, name='validate_exercise'),
]
