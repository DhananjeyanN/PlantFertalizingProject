from django.urls import path

from Core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reg_index', views.reg_index, name='reg_index'),
    path('add_plant', views.add_plant, name='add_plant'),
    path('update_c/<int:plant_id>', views.update_plant_c, name='update_plant_c'),
    path('delete_plant/<int:plant_id>', views.delete_plant, name='delete_plant'),
    path('add_sensor/<int:plant_id>', views.add_sensor, name='add_sensor'),
]
