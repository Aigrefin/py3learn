from django.shortcuts import redirect, render

from learn.forms import ExerciseForm
from learn.infrastructure.strings import caseless_equal
from learn.models import Translation, Dictionary
from learn.services.choice import random_choice, rythm_choice
from learn.services.repetition import compute_next_repetition


def choose_random_exercise(request, dictionary_pk):
    translation = random_choice(dictionary_pk)
    return redirect('learn:exercise', dictionary_pk=dictionary_pk, translation_pk=translation.id)


def choose_rythm_notation_exercise(request, dictionary_pk):
    if request.user.is_authenticated():
        translation = rythm_choice(request.user, dictionary_pk)
    else:
        translation = random_choice(dictionary_pk)
    if not translation:
        return redirect('learn:come_back', dictionary_pk=dictionary_pk)
    return redirect('learn:exercise', dictionary_pk=dictionary_pk, translation_pk=translation.id)


def validate_exercise(request, dictionary_pk, translation_pk):
    form = ExerciseForm(request.POST)
    if request.method != 'POST' or not form.is_valid():
        return redirect('learn:exercise_bad_input', dictionary_pk=dictionary_pk, translation_pk=translation_pk,
                        bad_input='bad_input')
    translation = Translation.objects.get(pk=translation_pk)
    good_answer = caseless_equal(translation.word_to_learn, form.cleaned_data['answer'])
    if good_answer:
        positive_update(translation, request)
        return redirect('learn:choose_exercise', dictionary_pk=dictionary_pk)
    else:
        negative_update(translation, request)
        return redirect('learn:exercise_wrong_answer', dictionary_pk=dictionary_pk, translation_pk=translation_pk)


def positive_update(translation, request):
    if request.user.is_authenticated():
        rythm_notation = translation.rythmnotation_set.filter(user=request.user).first()
        rythm_notation.successes += 1
        rythm_notation.next_repetition = compute_next_repetition(rythm_notation.successes)
        rythm_notation.save()


def negative_update(translation, request):
    if request.user.is_authenticated():
        rythm_notation = translation.rythmnotation_set.filter(user=request.user).first()
        rythm_notation.successes = 0
        rythm_notation.next_repetition = compute_next_repetition(rythm_notation.successes)
        rythm_notation.save()


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


def come_back(request, dictionary_pk):
    if not request.user.is_authenticated:
        return redirect(request, 'learn:dictionaries')
    translation = Translation.objects.filter(dictionary__id=dictionary_pk, rythmnotation__user_id__exact=request.user.id).order_by('rythmnotation__next_repetition').first()
    next_repetition = translation.rythmnotation_set.first().next_repetition
    language = Dictionary.objects.get(id=dictionary_pk)
    return render(request, 'learn/come_back.html', context={
        'next_repetition': next_repetition,
        'dictionary_pk': dictionary_pk,
        'language': language,
    })
