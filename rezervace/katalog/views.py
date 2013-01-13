# coding: utf-8
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from katalog.models import Rezervace


def home(request):
    rezervace = Rezervace.objects.all()
    return render(request, 'home.html', {'rezervace': rezervace,})