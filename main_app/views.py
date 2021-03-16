from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

from .models import Event

# Create your views here.


def home(request):
    # events = Event.objects.filter('dateTime'> 'dateTime.datetime.now()')
    events = Event.objects.order_by('dateTime')
    # future_events = [event for event in events if datetime(event.dateTime) > datetime.now()]
    # future_events = sorted(events, key=lambda x: x.dateTime, reverse=True)
    upcoming = Event.objects.filter(dateTime__gte=datetime.now()).order_by('dateTime')
    passed = Event.objects.filter(dateTime__lt=datetime.now()).order_by('-dateTime')
    return render(request, 'home.html', {'upcoming': upcoming})


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
    # context = {'event': event }
    # if request.user:
    #     user = request.user
    #     context["user"] = user
    return render(request, 'event/detail.html', {'event':event})

def assoc_event(request, user_id, event_id):
    User.objects.get(id=user_id).events.add(event_id)
    return redirect('event/detail.html', event_id=event_id)

def unassoc_event(request, user_id, event_id):
    User.objects.get(id=user_id).events.remove(event_id)
    return redirect('event/detail.html', event_id=event_id)
