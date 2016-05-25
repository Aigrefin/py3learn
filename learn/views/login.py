from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from learn.forms import LogInForm


def login_view(request):
    if request.method == 'POST':
        return _form_sent_case(request)
    return render(request, 'learn/login.html')


def _form_sent_case(request):
    form = LogInForm(request.POST)
    context = _keep_assigned_fields(request)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is None:
            return _render_user_or_password_error(context, request)
        login(request, user)
        return redirect('learn:dictionaries')
    else:
        return _render_autovalidation_errors(context, form, request)


def _keep_assigned_fields(request):
    return {
        'fields': {
            'username': request.POST['username'],
        }
    }


def _render_autovalidation_errors(context, form, request):
    context['form_errors'] = form.errors.items()
    return render(request, 'learn/login.html', context=context)


def _render_user_or_password_error(context, request):
    context['form_errors'] = [('Login failed', ['User name and/or password are incorrect.']), ]
    return render(request, 'learn/login.html', context=context)
