from django.urls import path, include
from .views import PlantListCreateView, DataTableListCreateView
from rest_framework.routers import DefaultRouter
from PlantApi import views
# router = DefaultRouter()
# router.register('Plants',PlantListCreateView)
urlpatterns = [
    #Plant urls
    # path('api-token-auth',include('rest_framework.authtoken.urls')),
    path('plants', PlantListCreateView.as_view(), name='plant-list-create'),
    path('datatable', DataTableListCreateView.as_view(), name='data_table-list-create'),
    path('get_plant/<int:plant_id>/', views.get_plant, name='update_plant'),  # Corrected here
    path('get_all_plants/', views.get_all_plants, name='get_plants'),  # Corrected here
    path('update_plant/<int:plant_id>/', views.update_plant, name='update_plant'),  # Corrected here
    #Datatable urls
    path('datatable/add/', views.create_data_table_entry, name='create_data_table_entry'),
    path('datatable/read/<int:entry_id>/', views.read_data_table_entry, name='read_data_table_entry'),
    path('datatable/update/<str:entry_id>/', views.update_data_table_entry, name='update_data_table_entry'),
    path('datatable/del/<int:entry_id>/', views.del_data_table_entry, name='delete_data_table_entry'),
]

