from django.shortcuts import redirect, render
from py3njection import inject

from learn.forms import ExerciseForm
from learn.infrastructure.database import Database
from learn.models import Translation, Dictionary
from learn.services.answer import Answer
from learn.services.choice import random_choice, rythm_choice
from learn.services.repetition import compute_next_repetition


def choose_random_exercise(request, dictionary_pk):
    translation = random_choice(dictionary_pk)
    return redirect('learn:exercise', dictionary_pk=dictionary_pk, translation_pk=translation.id)


def choose_rythm_notation_exercise(request, dictionary_pk):
    if request.user.is_authenticated():
        translation = rythm_choice(dictionary_pk, request.user)
    else:
        translation = random_choice(dictionary_pk)
    if not translation:
        return redirect('learn:come_back', dictionary_pk=dictionary_pk)
    return redirect('learn:exercise', dictionary_pk=dictionary_pk, translation_pk=translation.id)


@inject
def validate_exercise(request, dictionary_pk, translation_pk, database: Database, answer: Answer):
    form = ExerciseForm(request.POST)
    if request.method != 'POST' or not form.is_valid():
        return redirect('learn:exercise_bad_input', dictionary_pk=dictionary_pk, translation_pk=translation_pk,
                        bad_input='bad_input')
    translation = database.get_translation(translation_pk)
    good_answer = answer.is_good_answer(form.cleaned_data['answer'], translation)
    if request.user.is_authenticated():
        answer.update_translation_statistics(good_answer, request.user, translation)
    if good_answer:
        return redirect('learn:choose_exercise', dictionary_pk=dictionary_pk)
    else:
        return redirect('learn:exercise_wrong_answer', dictionary_pk=dictionary_pk, translation_pk=translation_pk)


def exercise(request, dictionary_pk, translation_pk, wrong_answer=False, bad_input=False):
    translation = Translation.objects.get(pk=translation_pk)
    notation = None
    date = None
    if request.user.is_authenticated():
        notation = translation.rythmnotation_set.filter(user=request.user).first()
        date = compute_next_repetition(notation.successes + 1)
    context = {
        'dictionary_pk': dictionary_pk,
        'translation_pk': translation_pk,
        'translation': translation,
        'notation': notation,
        'estimated_next_repetition': date,
        'wrong_answer': wrong_answer != False,
        'bad_input': bad_input != False,
    }
    return render(request, 'learn/exercise.html', context=context)


def exercise_wrong_answer(request, dictionary_pk, translation_pk):
    context = {
        'dictionary_pk': dictionary_pk,
        'translation_pk': translation_pk,
        'translation': Translation.objects.get(pk=translation_pk),
    }
    return render(request, 'learn/exercise_wrong_answer.html', context=context)


@inject
def come_back(request, dictionary_pk, database: Database):
    if not request.user.is_authenticated:
        return redirect(request, 'learn:dictionaries')
    next_repetition = database.get_date_of_next_word_to_learn(user=request.user)
    language = Dictionary.objects.get(id=dictionary_pk)
    return render(request, 'learn/come_back.html', context={
        'next_repetition': next_repetition,
        'dictionary_pk': dictionary_pk,
        'language': language,
    })
