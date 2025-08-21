from django.urls import path

from users.views import login, register, profile, logout, password_reset

app_name = 'shop'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('password-reset/', password_reset, name='password_reset')
]
