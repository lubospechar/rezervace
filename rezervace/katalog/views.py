# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render

import json

from katalog.models import Rezervace, Okres, Status

def home(request):
	okresy = Okres.objects.all()
	rezervace = Rezervace.objects.all()
	statusy = Status.objects.all()
	
	if request.GET.get('okres'):
		rezervace = rezervace.filter(okres = request.GET.get('okres'))
		
	if request.GET.get('status'):
		rezervace = rezervace.filter(status = request.GET.get('status'))
	
	return render(request, 'home.html', 
		{
			'rezervace': rezervace,
			'okresy': okresy,
			'statusy': statusy,
		}
	)

def profil(request, slug):
	try:
		profil = Rezervace.objects.get(slug = slug)
	except Rezervace.DoesNotExist:
		raise Http404
	
	return render(request, 'profil.html', {'profil': profil,})
	
def mapa(request):
	rezervace = Rezervace.objects.all()
	return render(request, 'mapa.html', {'rezervace': rezervace})
