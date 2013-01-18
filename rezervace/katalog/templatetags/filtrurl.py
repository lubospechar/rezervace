# coding: utf-8
from django import template
from django.utils.datastructures import MultiValueDictKeyError

register = template.Library()

@register.simple_tag
def filtrurl(req, get=None, param=None, pryc=None):
	if get:
		if not param:
			if get:
				try:
					if req.GET[get] == 'vzestupne':
						param = 'sestupne'
					else:
						param = 'vzestupne'
				except MultiValueDictKeyError:
					param = 'vzestupne'
		
		
		vrat = u'?%s=%s' % (get, param)
			
	else:
		vrat = '?'
	
	if req.GET:
		for polozka in req.GET.dict():
			if not polozka == get:
				if not polozka == pryc:
					vrat = vrat + u'&amp;%s=%s' % (polozka, req.GET[polozka])
				
	return vrat

@register.simple_tag
def mapaurl(req):
	vrat = '?'
	if req.GET:
		for polozka in req.GET.dict():
			if polozka == 'status' or polozka == 'okres':
				vrat = vrat + u'%s=%s&amp;' % (polozka, req.GET[polozka])
	
	return vrat

@register.simple_tag
def nazev_odkazu(nazev, get, pk):
	try:
		if int(get) == pk:
			return "<strong>%s</strong>" % nazev
	except:
		pass
	return nazev

@register.simple_tag
def nazev_odkazu_vse(nazev, get):
	if not get:
		return "<strong>%s</strong>" % nazev
	else:
		return nazev