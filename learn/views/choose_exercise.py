from django.shortcuts import redirect

from learn.services.choice import random_choice, rythm_choice


def choose_rythm_notation_exercise(request, dictionary_pk):
    if request.user.is_authenticated():
        translation = rythm_choice(dictionary_pk, request.user)
    else:
        translation = random_choice(dictionary_pk)
    if not translation:
        return redirect('learn:come_back', dictionary_pk=dictionary_pk)
    return redirect('learn:exercise', dictionary_pk=dictionary_pk, translation_pk=translation.id)