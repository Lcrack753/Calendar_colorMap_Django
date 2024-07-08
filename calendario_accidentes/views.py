from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import cal_defs
import requests
from datetime import datetime

def request_json():
    try:
        response = requests.get('https://so.jst.gob.ar/json/sucesos.json')
        response.raise_for_status()  # Lanza una excepción en caso de error HTTP

        # Si la respuesta es exitosa (código 200), devolvemos los datos JSON
        json = response.json()
        return json['expedientes']
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")


# Create your views here.
def index(request):
    json = request_json()
    MODOS = list(set([exp['modo'] for exp in json]))

    context = {}
    year = request.GET.get('year') or '2024'
    context['year'] = year
    context['modos'] = MODOS
    modo = request.GET.get('modo')
    print(modo)
    # JSON



    # Dates List
    
    if modo and modo in MODOS:
        json = [d for d in json if d['modo'] == modo]
    dates = [datetime.strptime(_['fecha'],r'%Y-%m-%d').date() for _ in json]
    dates_filter = [day for day in dates if day.year == int(year)]


    context['cal_year_filtered'] = cal_defs.cal_color(dates=dates_filter, formated_year=int(year))
    context['cal_month_filtered'] = cal_defs.cal_color(stamp='m',dates=dates_filter)
    context['cal_week_filtered'] = cal_defs.cal_color(stamp='w',dates=dates_filter)
    context['cal_year'] = cal_defs.cal_color(stamp='y', dates=dates)
    context['cal_month'] = cal_defs.cal_color(stamp='m', dates=dates)
    context['cal_week'] = cal_defs.cal_color(stamp='w', dates=dates)


    return render(request,'calendario_accidentes/mapa_calor.html', context)