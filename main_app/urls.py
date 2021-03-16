from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('accounts/signup/', views.signup, name='signup'),
]
