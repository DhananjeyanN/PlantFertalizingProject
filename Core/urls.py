from django.urls import path

from Core import views

urlpatterns = [
path('', views.index, name = 'index'),
path('add_plant', views.add_plant, name = 'add_plant'),
]