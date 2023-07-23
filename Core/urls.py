from django.urls import path

from Core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reg_index', views.reg_index, name='reg_index'),
    path('reg_index_pop_up/<int:plant_id>', views.plant_details, name='reg_index_pop_up'),
    path('add_plant', views.add_plant, name='add_plant'),
]
