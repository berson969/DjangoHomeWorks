from csv import DictReader

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator


with open(settings.BUS_STATION_CSV, 'r') as f:
    BUS_STATIONS = []
    for row in DictReader(f):
        BUS_STATIONS.append(row)



def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(BUS_STATIONS, 10)
    bus_stations_list = paginator.get_page(page_number)
    context = {
        'bus_stations': bus_stations_list,
        'page': bus_stations_list,
    }
    return render(request, 'stations/index.html', context)
