from py3njection import inject

from learn.infrastructure.database import Database
from learn.infrastructure.strings import caseless_equal
from learn.services.repetition import compute_next_repetition


class Answer:
    @inject
    def __init__(self, database: Database):
        self.database = database

    def is_good_answer(self, answer, translation):
        return caseless_equal(translation.word_to_learn, answer)

    def update_translation_statistics(self, good_answer, user, translation):
        rythm_notation = self.database.get_matching_notation(user, translation)
        if good_answer:
            next_repetition = compute_next_repetition(rythm_notation.successes)
            successes = rythm_notation.successes + 1
        else:
            next_repetition = compute_next_repetition(rythm_notation.successes)
            successes = 0
        self.database.save_rythm_notation(next_repetition, successes, rythm_notation)


