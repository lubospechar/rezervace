# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render

import json

from katalog.models import Rezervace, Okres, Status

def home(request):
	okresy = Okres.objects.all()
	statusy = Status.objects.all()
	rezervace = Rezervace.objects.all()
	
	if request.GET:
		for pole in request.GET.dict():
			kwargs = {pole: request.GET[pole]}
			try:
				int(request.GET[pole])
				rezervace = rezervace.filter(**kwargs)
			except ValueError:
				pass
	
	
	return render(request, 'home.html', 
		{
			'rezervace': rezervace,
			'okresy': okresy,
			'statusy': statusy,
			'req': request.GET.dict()
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
