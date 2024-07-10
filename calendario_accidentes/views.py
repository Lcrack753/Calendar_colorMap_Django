from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import cal_defs
import requests
from datetime import datetime
import re
from pprint import pprint

def request_json():
    try:
        response = requests.get('https://so.jst.gob.ar/json/sucesos.json')
        response.raise_for_status()  # Lanza una excepción en caso de error HTTP

        # Si la respuesta es exitosa (código 200), devolvemos los datos JSON
        json = response.json()
        return json['expedientes']
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")

def filter_expedientes_by_large_date(json_data, large_date):
    exp_list = []
    try:
        large_date_obj = datetime.strptime(large_date, r'%Y-%m-%d')
        for exp in json_data:
            fecha_obj = datetime.strptime(exp['fecha'], r'%Y-%m-%d')
            if large_date_obj.date() == fecha_obj.date():
                exp_list.append({
                    'modo': exp['modo'],
                    'id': exp['id'],
                    'hora': exp['hora'],
                    'estado': exp['estado'],
                    'nro':exp['nro_expediente'],
                    'fecha': exp['fecha']
                })
    except ValueError:
        try:
            large_date_obj = datetime.strptime(large_date, r'%m-%d')
            for exp in json_data:
                fecha_obj = datetime.strptime(exp['fecha'], r'%Y-%m-%d')
                if large_date_obj.month == fecha_obj.month and large_date_obj.day == fecha_obj.day:
                    exp_list.append({
                        'modo': exp['modo'],
                        'id': exp['id'],
                        'hora': exp['hora'],
                        'estado': exp['estado'],
                        'nro':exp['nro_expediente'],
                        'fecha': exp['fecha']
                    })
        except ValueError:
            return None  # Retorna None si no se puede parsear ninguna de las dos fechas
        
    return exp_list



# Create your views here.
def index(request):
    # FETCH JSON
    json = request_json()
    MODOS = list(set([exp['modo'] for exp in json]))

    pprint(list(set([exp['estado'] for exp in json])))
    # PARAMETROS GET
    year = request.GET.get('year') or '2024'
    modo_request = request.GET.get('modo')
    large_date = request.GET.get('large_date')
    context = {
        'year': year,
        'modos': MODOS
    }

    # Filtrado de Expedienets por MODO
    if modo_request and modo_request in MODOS:
        json = [d for d in json if d['modo'] == modo_request]


    # Filtrado Expedientes por FECHA
    exp_list = []
    exp_date = filter_expedientes_by_large_date(json,large_date)
    for modo in set([d['modo'] for d in exp_date]):
        exp_list.append({
            'modo': modo,
            'expedientes': [d for d in exp_date if d.get('modo') == modo]
        })
    context['exp_list']= exp_list

    # Filtrado por año
    dates = [datetime.strptime(_['fecha'],r'%Y-%m-%d').date() for _ in json]
    dates_filter = [day for day in dates if day.year == int(year)]

    # Calendarios por AÑO
    context.update({
        'cal_year_filtered': cal_defs.cal_color(dates=dates_filter, formated_year=int(year)),
        'cal_month_filtered': cal_defs.cal_color(stamp='m',dates=dates_filter),
        'cal_week_filtered': cal_defs.cal_color(stamp='w',dates=dates_filter),
    })

    # Calendarios TODOS los años
    context.update({
        'cal_year': cal_defs.cal_color(stamp='y', dates=dates),
        'cal_month': cal_defs.cal_color(stamp='m', dates=dates),
        'cal_week': cal_defs.cal_color(stamp='w', dates=dates)
    })

    return render(request,'calendario_accidentes/mapa_calor.html', context)