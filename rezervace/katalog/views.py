# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import MultiPoint, Point
from django.template.defaultfilters import slugify

import json
import xml.etree.ElementTree as ET

from katalog.models import Rezervace, Okres, Status
from katalog.forms import ChroupyForm


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
	
	
	strankovani = Paginator(rezervace, 25)
	stranka = request.GET.get('stranka')
	try:
		rezervace_strankovani = strankovani.page(stranka)
	except PageNotAnInteger:
		rezervace_strankovani = strankovani.page(1)
	except EmptyPage:
		rezervace_strankovani = strankovani.page(strankovani.num_pages)
	
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
	okresy = Okres.objects.all()
	statusy = Status.objects.all()
	
	if request.GET:
		for pole in request.GET.dict():
			kwargs = {pole: request.GET[pole]}
			rezervace = rezervace.filter(**kwargs)
	
	
	
	multipoint = list()
	
	if rezervace.count() > 0:
		for polozka in rezervace:
				multipoint.append(polozka.stred)
	else:
		multipoint.append(Point(14, 48))
		multipoint.append(Point(16.5, 51))
			
		
	multi = MultiPoint(multipoint)
	
	return render(request, 'mapa.html',
		{
			'rezervace': rezervace,
			'okresy': okresy,
			'statusy': statusy,
			'req': request.GET.dict(),
			'hranice': multi.extent
		}
	)

# zpracuje xml soubor, ktery vyplivne drusop.nature.cz
def chroupy(request):
	if request.POST:
		formular = ChroupyForm(request.POST, request.FILES)
		if formular.is_valid():
			f = request.FILES['soubor']
			text = unicode(f.read().decode('cp1250', errors='replace')).encode('cp1250')
			#text = unicode(f.read(), 'cp1250')
			#text = f.read().decode('cp1250', errors='replace')
			tree = ET.fromstring(text)
			for record in tree:
				polozka = Rezervace()
				polozka.kod = record.find('CIS').text
				polozka.nazev = record.find('NAZEV').text
				polozka.status = formular.cleaned_data['status']
				polozka.stred = Point(0, 0)
				polozka.save()
				if Rezervace.objects.filter(slug=slugify(polozka.nazev)).exists():
					polozka.slug = slugify('%s%s' % (polozka.nazev, polozka.kod))
					print polozka.slug
					
				else:
					polozka.slug = slugify(polozka.nazev)
					print polozka.slug
				polozka.okres = formular.cleaned_data['okres']
				polozka.save()
			
			return HttpResponse('ok')
		
	else:
		formular = ChroupyForm()
	
	return render(request, 'chroupy.html', {'formular': formular,})