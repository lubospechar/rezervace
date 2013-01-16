# coding: utf-8
import struct


from django.contrib.gis.db import models
from django.db.models import Sum


from django.contrib.auth.models import User

class Kraj(models.Model):
	nazev = models.CharField(max_length=25, unique=True, verbose_name="Název")
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.nazev

	class Meta:
		verbose_name = "Kraj"
		verbose_name_plural = "Kraje"
		ordering = ["nazev",]
		
class Okres(models.Model):
	nazev = models.CharField(max_length=35, unique=True, verbose_name="Název")
	kraj = models.ForeignKey(Kraj)
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.nazev

	class Meta:
		verbose_name = "Okres"
		verbose_name_plural = "Okresy"
		ordering = ["nazev",]
		
class Tema(models.Model):
	tema = models.CharField(max_length=40, unique=True, verbose_name="Téma")
	poradi = models.IntegerField(verbose_name="Logické pořadí")
	limit = models.IntegerField(verbose_name="Nutný počet fotografií")

	def __unicode__(self):
		return self.tema
	    
	class Meta:
		verbose_name = "Téma"
		verbose_name_plural = "Témata"
		ordering = ["poradi"]


class Status(models.Model):
	status = models.CharField(max_length=100, verbose_name="Status")
	zkratka = models.CharField(max_length=10, verbose_name="Zkratka")
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.zkratka
	
	class Meta:
		verbose_name = "Status"
		verbose_name_plural = "Statusy"
		ordering = ["status",]

class Fotografie(models.Model):
	tema = models.ForeignKey(Tema, verbose_name="Téma")
	pocet = models.IntegerField(default=0, verbose_name="Počet fotografií tohoto tématu")
	rezervace = models.ForeignKey('Rezervace', verbose_name="Rezervace")
	vlastni_limit = models.IntegerField(null=True, blank=True, verbose_name="Vlastní limit")
	
	def __unicode__(self):
		return u'%s: %s' % (self.tema, self.pocet)
	
	def limit(self):
		if self.vlastni_limit:
			return self.vlastni_limit
		else:
			return self.tema.limit
			
	def stav(self):
		
		if self.pocet >= self.limit():
			return 100
		else:
			return int(float(self.pocet)/float(self.limit())*100)
	
	class Meta:
		verbose_name = "Fotografie"
		verbose_name_plural = "Fotografie"
		ordering = ["tema",]


class Rezervace(models.Model):
	kod = models.IntegerField(verbose_name="Kód")
	nazev = models.CharField(max_length=100, verbose_name="Název")
	slug = models.SlugField(unique=True)
	status = models.ForeignKey(Status, verbose_name="Status")
	predmet = models.TextField(null=True, blank=True, verbose_name="Předmět ochrany")
	stred = models.PointField(verbose_name="Přibližný střed")
	wikipedia = models.URLField(null=True, blank=True, verbose_name="Odkaz na wikipedii")
	commons = models.URLField(null=True, blank=True, verbose_name="Odkaz na commons")
	okres = models.ManyToManyField(Okres, verbose_name="Okres", null=False, blank=False)
	uprava = models.DateTimeField(auto_now=True, verbose_name="Poslední úprava položky")
	objects = models.GeoManager()
	
	def __unicode__(self):
		return self.nazev
	
	def celkovy_pocet_fotografii(self):
	    pocet = self.fotografie_set.all().aggregate(Sum('pocet'))
	    return pocet['pocet__sum']
	
	def stav(self):
		fotografie = self.fotografie_set.all()
		
		procento = list()
		for polozka in fotografie:
			procento.append(polozka.stav())
				
		return int(sum(procento)/len(procento))
	
	def barva(self):
		index = int(round(self.stav(),-1) / 10)
		barva = {
			0: '#ff0000',
			1: '#ff3900',
			2: '#ff7400',
			3: '#ffaf00',
			4: '#ffd300',
			5: '#ffff00',
			6: '#e7ff00',
			7: '#d0ff00',
			8: '#b3ff00',
			9: '#79ff00',
			10: '#00ff00',
		    }
		
		return barva[index]
				
	
	class Meta:
		verbose_name = "Rezervace"
		verbose_name_plural = "Rezervace"
		ordering = ["nazev",]

	
class Poznamky(models.Model):
	poznamka = models.CharField(max_length=255)
	rezervace = models.ForeignKey(Rezervace, verbose_name="Rezervace")
	uzivatel = models.ForeignKey(User, verbose_name="Uživatel")
	datum = models.DateTimeField(auto_now=True, verbose_name="Datum")
	
	class Meta:
		verbose_name = "Poznámka"
		verbose_name_plural = "Poznámky"
		ordering = ["datum",]
	
	def __unicode__(self):
	  return u'%s - %s' % (self.datum, self.uzivatel)