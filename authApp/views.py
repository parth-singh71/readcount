from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! Please login to continue.')
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'authApp/signup.html', context=context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                django_login(request, user)
                return redirect('storyhome')
            else:
                messages.info(request, 'Username or password incorrect')
        else:
            messages.error(request, "Invalid form")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'authApp/login.html', context=context)


def logout_view(request):
    django_logout(request)
    return redirect('login')
