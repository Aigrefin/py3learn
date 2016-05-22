from django.db import models


class Dictionary(models.Model):
    language = models.CharField(max_length=200)

    def __str__(self):
        return self.language


class Translation(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    known_word = models.CharField(max_length=200)
    word_to_learn = models.CharField(max_length=200)

    def __str__(self):
        return self.known_word

    class Meta:
        ordering = ['known_word']
