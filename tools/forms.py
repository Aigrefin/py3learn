from django.forms import forms


class ExerciseForm(forms.Form):
    text = forms.CharField(label='text', max_length=50000, required=True)
