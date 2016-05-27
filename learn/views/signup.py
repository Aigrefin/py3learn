from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from learn.forms import SignInForm

USERNAME = 'username'
USERNAME_ALREADY_EXISTS_ = 'This username already exists.'


def signup_view(request):
    if request.method == 'POST':
        return _form_sent_case(request)
    return render(request, 'learn/signup.html')


def _form_sent_case(request):
    form = SignInForm(request.POST)
    context = _keep_assigned_fields(request)
    if form.is_valid():
        user_already_exists = User.objects.filter(username=form.cleaned_data.get(USERNAME))
        if user_already_exists:
            return _render_user_exists_error(context, request)
        _create_user(form)
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        login(request, user)
        return redirect('learn:dictionaries')
    else:
        return _render_autovalidation_errors(context, form, request)


def _create_user(form):
    User.objects.create_user(username=form.cleaned_data.get('username'),
                             email=form.cleaned_data.get('email'),
                             password=form.cleaned_data.get('password'))


def _keep_assigned_fields(request):
    return {
        'fields': {
            'username': request.POST['username'],
            'email': request.POST['email'],
        }
    }


def _render_user_exists_error(context, request):
    context['form_errors'] = [(USERNAME, [USERNAME_ALREADY_EXISTS_]), ]
    return render(request, 'learn/signup.html', context=context)


def _render_autovalidation_errors(context, form, request):
    context['form_errors'] = form.errors.items()
    return render(request, 'learn/signup.html', context=context)
