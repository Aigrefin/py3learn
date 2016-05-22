from django import forms


class ExerciseForm(forms.Form):
    answer = forms.CharField(label='Answer', max_length=100, required=True)
