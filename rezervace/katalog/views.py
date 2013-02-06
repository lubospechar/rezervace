# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import MultiPoint, Point
from django.template.defaultfilters import slugify

import json
import xml.etree.ElementTree as ET
from urllib import quote

from katalog.models import Rezervace, Okres, Status, Tema, Fotografie, Kraj
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
				if polozka.stred != Point(0, 0):
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
				kod = int(record.find('CIS').text)
				nazev = record.find('NAZEV').text
				okresy = formular.cleaned_data['okres']
				
				adepti_na_duplicitu = Rezervace.objects.filter(nazev=nazev)
				
				if adepti_na_duplicitu.exists():
					
					nalezen_kod = False
					for adept in adepti_na_duplicitu:
						if adept.kod == kod:
							nalezen_kod = True
							print "duplicita: kod: %s, rezervace: %s %s" % (adept.kod, adept.status, adept.nazev)
						
							for okres in okresy:
								pridat_okres = True
							
								for adept_okres in adept.okres.all():
									if adept_okres == okres:
										pridat_okres = False	
												
								if pridat_okres:
									print "   přídávám okres: %s" % okres
									adept.okres.add(okres)
									adept.save()
					
					if nalezen_kod:
						continue
					
					slug = slugify('%s-%s' % (nazev, kod))
					print u'duplicitni název, přidávím do slugu kód - slug: %s' % slug
				else:
					slug = slugify(nazev)
					
				polozka = Rezervace()
				polozka.kod = kod
				polozka.nazev = nazev
				polozka.status = formular.cleaned_data['status']
				polozka.stred = Point(0, 0)
				polozka.slug = slug
				polozka.kontrola_adres = False
				polozka.wikipedia = u'http://cs.wikipedia.org/wiki/%s' % (quote(nazev.encode('utf8')))
				polozka.commons = u'http://commons.wikimedia.org/wiki/Category:%s' % (quote(nazev.encode('utf8')))
				polozka.save()
				polozka.okres = formular.cleaned_data['okres']
				polozka.save()
				
				for tema in ['brzke jaro', 'jaro', 'leto', 'pozdni leto', 'podzim', 'zima']:
					fotografie = Fotografie()
					fotografie.tema = Tema.objects.get(tema=tema)
					fotografie.pocet = 0
					fotografie.rezervace = polozka
					fotografie.save()
				
				print u'přidáno  kod: %s, rezervace: %s %s' % (polozka.kod, polozka.status, polozka.nazev)
			
			return HttpResponse('ok')
		
	else:
		formular = ChroupyForm()
	
	return render(request, 'chroupy.html', {'formular': formular,})

def statistiky(request):
	okresy = Okres.objects.all()
	return render(request, 'statistiky.html', {'okresy': okresy})

def bod(request, id):
	rezervace = Rezervace.objects.get(pk = id)
	return render(request, 'bod.gpx', {'rezervace': rezervace}, content_type='application/xhtml+xml')

def body(request):
	rezervace = Rezervace.objects.all()
	
	if request.GET:
		for pole in request.GET.dict():
			kwargs = {pole: request.GET[pole]}
			rezervace = rezervace.filter(**kwargs)
			
			
	return render(request, 'body.gpx', {'rezervace': rezervace}, content_type='application/xhtml+xml')