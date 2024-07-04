from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import cal_defs

# Create your views here.
def index(request):
    context = {
        'cal': cal_defs.cal_generic()
    }
    return render(request,'calendario_accidentes/index.html', context)