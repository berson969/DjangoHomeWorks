from django.urls import path
from .views import ListSensor, GetUpdateDeleteSensor, AddMeasurement, imageForm

urlpatterns = [
    path('sensors/', ListSensor.as_view()),
    path('sensors/<int:pk>', GetUpdateDeleteSensor.as_view()),
    path('measurements/', AddMeasurement.as_view()),
]
