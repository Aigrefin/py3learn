from django.contrib.auth.models import User
from django.db import models


class Dictionary(models.Model):
    language = models.CharField(max_length=200)

    def __str__(self):
        return self.language


class Translation(models.Model):
    MUST_KNOW = 'MH'
    SHOULD_KNOW = 'SH'
    NICE_TO_KNOW = 'NTH'
    KNOWLEDGE_CHOICE = (
        (MUST_KNOW, 'Must know'),
        (SHOULD_KNOW, 'Should know'),
        (NICE_TO_KNOW, 'Nice to know'),
    )
    importance = models.CharField(max_length=3, choices=KNOWLEDGE_CHOICE, default=MUST_KNOW)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    known_word = models.CharField(max_length=200)
    word_to_learn = models.CharField(max_length=200)

    class Meta:
        ordering = ['known_word']

    def __str__(self):
        return self.known_word

    def get_importance_str(self):
        results = [importance for importance in self.KNOWLEDGE_CHOICE if self.importance == importance[0]]
        first_result = results[0]
        understandable_importance = first_result[1]
        return understandable_importance


class RythmNotation(models.Model):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    successes = models.BigIntegerField()
    next_repetition = models.DateTimeField(auto_now_add=True)
