# coding: utf-8
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def filtrurl(req):
	for pole in req:
		pass
	return pole