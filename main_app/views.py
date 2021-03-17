from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, password_validation, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.views.decorators.csrf import csrf_protect

from .models import Event


def customPasswordValidator(password):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not any(char.isdigit() for char in password):
        return 'Password must contain at least 1 digit.'
    if not any(char in special_characters for char in password):
        return 'Password must contain at least 1 special character.'
    if not any(char.isupper() for char in password):
        return 'Password must contain at lest 1 uppercase letter'
    if len(password) < 8:
        return 'Password must be at least 8 characters long'
    return 'Invalid Password, Please Try Again.'


def home(request):
    upcoming = Event.objects.filter(dateTime__gte=datetime.now()).order_by('dateTime')
    passed = Event.objects.filter(dateTime__lt=datetime.now()).order_by('-dateTime')
    if (request.POST):
        search_term = request.POST.get("search_term")
        search_results = list(filter(lambda event: search_term.lower() in event.title.lower(), upcoming))
        return render(request, 'home.html', {'upcoming': search_results, 'visibility': "visible", "placeholder": search_term})
    return render(request, 'home.html', {'upcoming': upcoming, "visibility": "hidden", "placeholder": "Search"})


def about(request):
    return render(request, 'about.html')


@login_required
def user_profile(request):
    user_events = Event.objects.filter(users__id=request.user.id)
    upcoming = user_events.filter(dateTime__gte=datetime.now()).order_by('dateTime')
    passed = user_events.filter(dateTime__lt=datetime.now()).order_by('-dateTime')
    username = request.user.username

    join_date = f"{request.user.date_joined.month}/{request.user.date_joined.day}/{request.user.date_joined.year}"

    if (request.POST):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        # user enters a new user name
        if request.user.username != request.POST.get('username'):

            # username already in use, show error
            if User.objects.filter(username=request.POST.get('username')).exists() == True:
                messages.error(request, "Invalid User Name, Please Try Again.")
            else:
                updated_username = request.POST.get('username')
                user.username = updated_username

        # username stays the same
        elif request.user.username == request.POST.get('username') and len(list(User.objects.filter(username=request.user.username))) == 1:
            updated_username = request.user.username

        if request.POST.get('password') != '':
            validation_message = customPasswordValidator(request.POST.get('password'))
            try:
                # validate the password and catch the exception
                password_validation.validate_password(request.POST.get('password'))
                updated_password = request.POST.get('password')
                user.set_password(updated_password)
                # the exception raised here is different than serializers.ValidationError
            except ValidationError:
                messages.error(request, validation_message)

            update_session_auth_hash(request, request.user)
        user.save()
        return render(request, 'user/profile.html', {'username': user.username, 'join_date': join_date})
    return render(request, 'user/profile.html', {'username': username, 'join_date': join_date, 'upcoming': upcoming, 'passed': passed})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
        else:
            print(form.errors.as_json())
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    if (request.user.id == None):
        is_logged_in = False
    else:
        is_logged_in = True

    try:
        is_registered = event.users.get(id=request.user.id)

    except ObjectDoesNotExist:
        is_registered = False

    return render(request, 'event/detail.html', {'event': event, 'user_id': request.user.id, 'is_registered': is_registered, "is_logged_in": is_logged_in})


def events_by_category(request, category):
    upcoming = Event.objects.filter(dateTime__gte=datetime.now()).order_by('dateTime')
    search_results = list(filter(lambda event: category == event.get_category_display().lower(), upcoming))
    return render(request, 'event/category-search-results.html', {'category': category, 'search_results': search_results})


@login_required
def assoc_event(request, user_id, event_id):
    Event.objects.get(id=event_id).users.add(user_id)
    return HttpResponseRedirect("")


@login_required
def unassoc_event(request, user_id, event_id):
    Event.objects.get(id=event_id).users.remove(user_id)
    return HttpResponseRedirect("")
