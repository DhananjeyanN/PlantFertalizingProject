from django.urls import path

from accounts import views

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('generate_api_key/', views.generate_api_key, name='generate_api_key'),
]
