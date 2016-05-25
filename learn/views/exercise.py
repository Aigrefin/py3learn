from django.shortcuts import redirect, render

from learn.forms import ExerciseForm
from learn.infrastructure.strings import caseless_equal

from learn.models import Translation


def randomise_exercise(request, dictionary_pk):
    translation = Translation.objects.filter(dictionary__id=dictionary_pk).order_by('?').first()
    return redirect('learn:exercise', dictionary_pk=dictionary_pk, translation_pk=translation.id)


def validate_exercise(request, dictionary_pk, translation_pk):
    form = ExerciseForm(request.POST)
    if request.method != 'POST' or not form.is_valid():
        return redirect('learn:exercise_bad_input', dictionary_pk=dictionary_pk, translation_pk=translation_pk,
                        bad_input='bad_input')
    translation = Translation.objects.get(pk=translation_pk)
    good_answer = caseless_equal(translation.word_to_learn, form.cleaned_data['answer'])
    if good_answer:
        return redirect('learn:randomise_exercise', dictionary_pk=dictionary_pk)
    else:
        return redirect('learn:exercise_wrong_answer', dictionary_pk=dictionary_pk, translation_pk=translation_pk)


def exercise(request, dictionary_pk, translation_pk, wrong_answer=False, bad_input=False):
    context = {
        'dictionary_pk': dictionary_pk,
        'translation_pk': translation_pk,
        'translation': Translation.objects.get(pk=translation_pk),
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