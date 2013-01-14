# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render

import json

from katalog.models import Rezervace

def home(request):
    rezervace = Rezervace.objects.all()
    return render(request, 'home.html', {'rezervace': rezervace,})

def profil(request, slug):
	try:
		profil = Rezervace.objects.get(slug = slug)
	except Rezervace.DoesNotExist:
		raise Http404
	
	return render(request, 'profil.html', {'profil': profil,})
	
def mapa(request):
	rezervace = Rezervace.objects.all()
	return render(request, 'mapa.html', {'rezervace': rezervace})
