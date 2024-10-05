from django.urls import path, include
from . import views

urlpatterns = [
    path('add-component/', views.add_component),
    path('get-service-cost/', views.get_service_cost),
    path('add-vehicle-for-service/', views.add_vehicle_for_service),
]