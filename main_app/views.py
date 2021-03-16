from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def user_profile(request):
    print(request)
    username = request.user.username
    join_date = f"{request.user.date_joined.month}/{request.user.date_joined.day}/{request.user.date_joined.year}"

    return render(request, 'user/profile.html', {'username': username, 'join_date': join_date, })

@login_required
def edit_user(request):
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    if request.POST and user_form.is_valid():
        user_form.save()
        return redirect('user/profile.html')
    else:
        return render(request, 'user/profile.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
