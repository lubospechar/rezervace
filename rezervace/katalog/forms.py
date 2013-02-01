# coding: utf-8
from django import forms
from django.forms import ModelForm, Form

from katalog.models import Rezervace

class ChroupyForm(ModelForm):
	soubor = forms.FileField()
	
	class Meta:
		model = Rezervace
		fields = ('status', 'okres')
	

