from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_protect

from .models import Event

# Create your views here.


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

    username = request.user.username
    join_date = f"{request.user.date_joined.month}/{request.user.date_joined.day}/{request.user.date_joined.year}"
    if (request.POST):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        updated_username = request.POST.get('username')
        user.username = updated_username
        user.save()
        return render(request, 'user/profile.html', {'username': updated_username, 'join_date': join_date})
    return render(request, 'user/profile.html', {'username': username, 'join_date': join_date})


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


def event_detail(request, event_id):

    event = Event.objects.get(id=event_id)

    try:
        is_registered = event.users.get(id=request.user.id)

    except ObjectDoesNotExist:
        is_registered = False

    return render(request, 'event/detail.html', {'event': event, 'user_id': request.user.id, 'is_registered': is_registered})


def events_by_category(request, category):
    upcoming = Event.objects.filter(dateTime__gte=datetime.now()).order_by('dateTime')
    search_results = list(filter(lambda event: category == event.get_type_display(), upcoming))
    return render(request, 'event/category-search-results.html', {'category': category, 'search_results': search_results})


def assoc_event(request, user_id, event_id):
    Event.objects.get(id=event_id).users.add(user_id)
    return HttpResponseRedirect("")


def unassoc_event(request, user_id, event_id):
    Event.objects.get(id=event_id).users.remove(user_id)
    return HttpResponseRedirect("")
