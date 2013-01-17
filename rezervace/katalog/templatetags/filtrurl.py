# coding: utf-8
from django import template

register = template.Library()

@register.simple_tag
def filtrurl(req, get=None, param=None):
	if get:
		vrat = u'?%s=%s' % (get, param)
	else:
		vrat = '?'
	
	if req.GET:
		for polozka in req.GET.dict():
			if not polozka == get:
				vrat = vrat + u'&amp;%s=%s' % (polozka, req.GET[polozka])
				
	return vrat