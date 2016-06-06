from django.shortcuts import redirect, render
from py3njection import inject

from learn.infrastructure.database import Database


@inject
def come_back(request, dictionary_pk, database: Database):
    if not request.user.is_authenticated():
        return redirect(request, 'learn:dictionaries')

    next_repetition = database.get_date_of_next_word_to_learn(user=request.user)
    language = database.get_dictionary_language(dictionary_pk)

    return render(request, 'learn/come_back.html', context={
        'next_repetition': next_repetition,
        'dictionary_pk': dictionary_pk,
        'language': language,
    })
