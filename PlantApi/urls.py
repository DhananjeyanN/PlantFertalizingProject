from django.urls import path, include
from .views import PlantListCreateView, DataTableListCreateView
from rest_framework.routers import DefaultRouter
from Core import views
# router = DefaultRouter()
# router.register('Plants',PlantListCreateView)
urlpatterns = [
    # path('api-token-auth',include('rest_framework.authtoken.urls')),
    path('plants', PlantListCreateView.as_view(), name='plant-list-create'),
    path('datatable', DataTableListCreateView.as_view(), name='data_table-list-create'),
]
