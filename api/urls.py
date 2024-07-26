from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve



urlpatterns = [
    path('create_account/', views.create_account, name='api_create_account'),
    path('login/', obtain_auth_token, name='api_obtain_token'),
    path('rating/', views.add_rating,name='api_rating'),
    path('check/', views.check,name='api_check'),
    path('logout/', views.logout, name='api_logout'),
    path('me/', views.me,name='api_me'),
    
    path('<str:filename>/', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
