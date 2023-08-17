from django.urls import path, include
from .views import PlantListCreateView
from rest_framework.routers import DefaultRouter
from Core import views
# router = DefaultRouter()
# router.register('Plants',PlantListCreateView)
urlpatterns = [
    path('api/Plants/', PlantListCreateView.as_view(), name='plant-list-create'),
    path('api-token-auth',include('rest_framework.authtoken.urls')),
]
