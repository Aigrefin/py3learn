from django.shortcuts import render
from py3njection import inject

from learn.infrastructure.database import Database


@inject
def exercise_wrong_answer(request, dictionary_pk, translation_pk, database: Database):
    context = {
        'dictionary_pk': dictionary_pk,
        'translation_pk': translation_pk,
        'translation': database.get_translation(translation_pk),
    }
    return render(request, 'learn/exercise_wrong_answer.html', context=context)