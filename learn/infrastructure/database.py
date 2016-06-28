from django.db.models import Q
from django.utils import timezone

from learn.models import Translation, RythmNotation, Dictionary


class Database:
    def schedule_words(self, translations, user, now):
        for translation in translations:
            RythmNotation.objects.create(user=user, translation=translation, successes=0,
                                         next_repetition=now)

    def get_unseen_words(self, dictionary_pk, quantity_of_words_to_plan, user):
        translations = Translation.objects.filter(
                Q(dictionary_id=dictionary_pk),
                ~Q(rythmnotation__user=user))[:quantity_of_words_to_plan]
        return translations

    def get_ordered_scheduled_words_to_learn_before_date(self, choose_before, dictionary_pk, user):
        return Translation.objects \
            .filter(dictionary_id=dictionary_pk, rythmnotation__user=user,
                    rythmnotation__next_repetition__lt=choose_before) \
            .order_by('rythmnotation__next_repetition')

    def get_translation(self, translation_pk):
        return Translation.objects.get(pk=translation_pk)

    def get_matching_notation(self, user, translation):
        return translation.rythmnotation_set.filter(user=user).first()

    def save_rythm_notation(self, next_repetition, successes, rythm_notation):
        rythm_notation.next_repetition = next_repetition
        rythm_notation.successes = successes
        rythm_notation.save()

    def get_date_of_next_word_to_learn(self, user):
        return RythmNotation.objects.filter(user=user).order_by('next_repetition').first().next_repetition

    def get_dictionary_language(self, dictionary_pk):
        return Dictionary.objects.get(id=dictionary_pk).language

    def get_random_well_known_word(self, dictionary_pk, user):
        now = timezone.now()
        in_a_month = now.replace(month=now.month + 1)
        return Translation.objects \
            .filter(dictionary_id=dictionary_pk, rythmnotation__user=user,
                    rythmnotation__next_repetition__gt=in_a_month) \
            .order_by('?').first()
