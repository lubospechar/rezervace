# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from katalog.models import Rezervace, Okres, Status

def home(request):
	okresy = Okres.objects.all()
	statusy = Status.objects.all()
	rezervace = Rezervace.objects.all()
	
	if request.GET:
		for pole in request.GET.dict():
			if not pole == 'stranka':
				kwargs = {pole: request.GET[pole]}
				try:
					int(request.GET[pole])
					rezervace = rezervace.filter(**kwargs)
				except ValueError:
					if request.GET[pole] == 'vzestupne':
						rezervace = rezervace.order_by(pole)
					else:
						rezervace = rezervace.order_by("-" + pole)
	
	
	strankovani = Paginator(rezervace, 20)
	stranka = request.GET.get('stranka')
	try:
		rezervace_strankovani = strankovani.page(stranka)
	except PageNotAnInteger:
		rezervace_strankovani = strankovani.page(1)
	except EmptyPage:
		contacts = strankovani.page(strankovani.num_pages)
	
	return render(request, 'home.html', 
		{
			'rezervace': rezervace_strankovani,
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
