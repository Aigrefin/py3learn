from django import forms


class ExerciseForm(forms.Form):
    answer = forms.CharField(label='Answer', max_length=100, required=True)


class SignInForm(forms.Form):
    username = forms.CharField(label='User name', min_length=6, max_length=30, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', min_length=6, max_length=40, required=True)

class LogInForm(forms.Form):
    username = forms.CharField(label='User name', min_length=6, max_length=30, required=True)
    password = forms.CharField(label='Password', min_length=6, max_length=40, required=True)