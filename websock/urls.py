from chat import views as chat_views

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', chat_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('accounts/logout/',  auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='logout'),
    path('chat/admin/', chat_views.new_message, name='new_message'),
    path('chat/', include('chat.urls')),
]
