from django.urls import path

from Core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reg_index', views.reg_index, name='reg_index'),
    path('add_plant', views.add_plant, name='add_plant'),
    path('update/<int:plant_id>', views.update_plant, name='update_plant'),
]
