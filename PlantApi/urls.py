from django.urls import path
from .views import PlantListCreateView
from Core import views

urlpatterns = [
    path('Plant', PlantListCreateView.as_view(), name='Plant-List-Create'),
]
