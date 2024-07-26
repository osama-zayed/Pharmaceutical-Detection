from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns =[
    path('login',LoginView.as_view(),name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('registr', views.RegistrViews, name='registr'),
    path('signup', views.signup, name='signup'),
]