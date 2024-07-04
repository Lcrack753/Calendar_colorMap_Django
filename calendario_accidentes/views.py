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
    context = {}
    # JSON
    json = request_json()

    # Parametros y filtro
    modo = request.GET.get('modo')
    if modo != None:
        json = [d for d in json if d['modo'] == modo]

    stamp = request.GET.get('stamp') if request.GET.get('stamp') in ['y','m','w'] else 'y'

    # Dates List
    dates = [datetime.strptime(_['fecha'],r'%Y-%m-%d').date() for _ in json]

    context['year'] = cal_defs.cal_color(stamp='y', dates=dates)
    context['month'] = cal_defs.cal_color(stamp='m', dates=dates)
    context['week'] = cal_defs.cal_color(stamp='w', dates=dates)

    return render(request,'calendario_accidentes/mapa_calor.html', context)