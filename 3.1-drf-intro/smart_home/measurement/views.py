# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from django.conf import settings
from django.shortcuts import render

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, InfoSensorSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView


class GetUpdateDeleteSensor(RetrieveUpdateDestroyAPIView):
    """
    Изменение и удаление датчиков
    """
    queryset = Sensor.objects.all()
    serializer_class = InfoSensorSerializer

    class Meta:
        verbose_name = 'Получение, изменение и удаление сенсоров'


class AddMeasurement(CreateAPIView):
    """
    Ввод показаний датчика
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class ListSensor(ListCreateAPIView):
    """
    Список всех датчиков и создание нового датчика
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    class Meta:
        verbose_name = 'Создание сенсора и вывод списка сенсоров'


def imageForm(request, image_name):
    template = 'images.html'
    measurement = Measurement.objects.get(photo='images/' + image_name)
    context = {
        'url': measurement.photo.url,
        'name': image_name,
    }
    return render(request, template, context)
