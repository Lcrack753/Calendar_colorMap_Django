from calendar import Calendar
from collections import Counter
from datetime import date
from typing import List
import requests
from pprint import pprint


try:
    response = requests.get('https://so.jst.gob.ar/json/sucesos.json')
    response.raise_for_status()  # Lanza una excepción en caso de error HTTP

    # Si la respuesta es exitosa (código 200), devolvemos los datos JSON
    json = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error al hacer la solicitud HTTP: {e}")

MESES_DIAS = {
    '1': ('Enero', 31),
    '2': ('Febrero', 29),
    '3': ('Marzo', 31),
    '4': ('Abril', 30),
    '5': ('Mayo', 31),
    '6': ('Junio', 30),
    '7': ('Julio', 31),
    '8': ('Agosto', 31),
    '9': ('Septiembre', 30),
    '10': ('Octubre', 31),
    '11': ('Noviembre', 30),
    '12': ('Diciembre', 31),
}


def calcular_diferencia_color(color1, color2, n):
    try:
        delta_color = [(color2[i] - color1[i]) / (n - 1) for i in range(3)]
    except ValueError as e:
        print(e)
    return delta_color

def generar_gradiente(color1, color2, n):
    if n <= 1:
        return [color1]
    delta_color = calcular_diferencia_color(color1, color2, n)

    gradient_colors = []
    for i in range(n):
        color = tuple(int(color1[j] + delta_color[j] * i) for j in range(3))
        # color_hex = "#{:02X}{:02X}{:02X}".format(*color)
        gradient_colors.append(color)

    return gradient_colors


def contar_mes_dia(dates: List[date] = [], stamp: chr = 'y'):
    count = Counter()
    for _ in dates:
        if stamp == 'm':
            count[f'{_.day}'] += 1
        elif stamp == 'w':
            count[f'{_.weekday() + 1}'] += 1
        else:
            count[f'{_.month}-{_.day}'] +=  1

    return count


def cal_formated(year = 2024):
    cal = []
    for month in range(1,13):
        py_cal = [day for week in Calendar().monthdatescalendar(year, month) for day in week]
        cal.append({
            'month_name': MESES_DIAS[str(month)][0],
            'days': []
        })
        for day in py_cal:
            if day.month != month:
                cal[month-1]['days'].append(
                    {'date':day.day, 'class': 'no_month', 'background':None, 'large_date': day.isoformat()}
                )
            elif day == date.today():
                cal[month-1]['days'].append(
                    {'date':day.day, 'class': 'today', 'background':None, 'large_date': day.isoformat()}
                )
            elif day.weekday() == 5 or day.weekday() == 6:
                cal[month-1]['days'].append(
                    {'date':day.day, 'class': 'weekend', 'background':None, 'large_date': day.isoformat()}
                )
            else:
                cal[month-1]['days'].append(
                    {'date':day.day, 'class': 'yes_month', 'background':None, 'large_date': day.isoformat()}
                )
    return cal

def cal_generic(stamp: chr = 'y'):
    cal = []
    if stamp == 'w':
        for day in range(1,8):
            cal.append(
                        {'date':day, 'background':None}              
            )
    elif stamp == 'm':
        for day in range(1,32):
            cal.append(
                        {'date':day, 'background':None, 'large_date': f'XXXX-XX-{day}'}              
            )
    else:
        for month in range(1,13):
            cal.append({
                'month_name': MESES_DIAS[str(month)][0],
                'days': []
            })
            for day in range(1,MESES_DIAS[str(month)][1]+1):
                cal[month-1]['days'].append(
                            {'date':day, 'background':None, 'large_date': f'XXXX-{month}-{day}'}
                )
    return cal 


def cal_color(stamp: chr = 'y', color1 =  (150, 229, 242), color2 = (16, 40, 158), dates: List[date] = [], formated_year: int = None):
    assert stamp in ['y','m','w'], 'stamp invalido'
    # if formated_year:
    #     cal = cal_formated(formated_year)
    # else:
    #     cal = cal_generic(stamp=stamp)
    cal = cal_formated(formated_year) if formated_year else cal_generic(stamp=stamp)
    if len(dates) < 1:
        return cal
    count = contar_mes_dia(dates,stamp)
    count_max =count.most_common()[0][1]
    gradiente = generar_gradiente(color1,color2, count_max)
    if stamp == 'w':
        for _, day in enumerate(cal):
            cal[_]['percentage'] = f"{0:.2f}%"
            if count[str(day['date'])] == 0:
                continue
            else:
                cal[_]['background'] = gradiente[count[str(day['date'])] - 1]
                cal[_]['percentage'] = f"{100 * count[str(day['date'])] / count.total() :.2f}%"
    elif stamp == 'm':
        for _, day in enumerate(cal):
            cal[_]['percentage'] = f"{0:.2f}%"
            if count[str(day['date'])] == 0:
                continue
            else:
                cal[_]['background'] = gradiente[count[str(day['date'])] - 1]
                cal[_]['percentage'] = f"{100 * count[str(day['date'])] / count.total() :.2f}%"
    else:
        for idx, month in enumerate(cal):
            for _, day in enumerate(month['days']):
                cal[idx]['days'][_]['percentage'] = f"{0:.2f}%"
                cal[idx]['days'][_]['large_date'] = f'XXXX-{idx + 1}-{day['date']}'

                if formated_year:
                    cal[idx]['days'][_]['large_date'] = f'{formated_year}-{idx + 1}-{day['date']}'
                if count[f"{idx+1}-{day['date']}"] == 0:
                    continue
                else:
                    cal[idx]['days'][_]['background'] = gradiente[count[f"{idx+1}-{day['date']}"] - 1]
                    cal[idx]['days'][_]['percentage'] = f"{100 * count[f"{idx+1}-{day['date']}"] / count.total():.2f}%"
    return cal

if __name__ == "__main__":
    list_dates = [date(2024,5,6),date(2024,5,2),date(2024,5,3),date(2024,5,1),date(2024,7,6),date(2024,7,15),date(2024,5,3),date(2024,5,3),date(2024,5,3)]
    # pprint(cal_color(stamp='m',dates=list_dates))
    pprint(cal_color(stamp='y', dates=list_dates, formated_year=2024))
