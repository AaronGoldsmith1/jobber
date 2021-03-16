from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/<int:event_id>', views.event_detail, name='event_detail'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('events/<int:event_id>/assoc_event/<int:user_id>/', views.assoc_event, name="assoc_event"),
    path('events/<int:event_id>/unassoc_event/<int:user_id>/', views.unassoc_event, name="unassoc_event"),
]
