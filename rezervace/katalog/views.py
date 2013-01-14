# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render

import json

from katalog.models import Rezervace

def _json(data):
    return HttpResponse(json.dumps(data))

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
	return render(request, 'mapa.html')

def data(request):
	rezervace = Rezervace.objects.all()
	data = list()
	for polozka in rezervace:
		data.append({'nazev': polozka.nazev, 'status': polozka.status.status, 'x': polozka.stred.x, 'y': polozka.stred.y, 'kvalita': polozka.kvalita()})
	return _json(data)