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
		
class Obdobi(models.Model):
	obdobi = models.CharField(max_length=40, unique=True, verbose_name="Období")
	poradi = models.IntegerField(verbose_name="Logické pořadí")
	limit = models.IntegerField(verbose_name="Nutný počet fotografií")

	def __unicode__(self):
		return self.obdobi
	    
	class Meta:
		verbose_name = "Období"
		verbose_name_plural = "Období"
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
	obdobi = models.ForeignKey(Obdobi, verbose_name="Období")
	pocet = models.IntegerField(default=0, verbose_name="Počet fotografií za období")
	rezervace = models.ForeignKey('Rezervace', verbose_name="Rezervace")
	
	def __unicode__(self):
		return u'%s: %s' % (self.obdobi, self.pocet)
	
	def stav(self):
		if self.pocet >= self.obdobi.limit:
			return 100
		else:
			return int(float(self.pocet)/float(self.obdobi.limit)*100)
	
	class Meta:
		verbose_name = "Fotografie"
		verbose_name_plural = "Fotografie"
		ordering = ["obdobi",]


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
		r = (255*(100-self.stav()))/100; 
		g = (255*self.stav())/100
		b = 0
		
		return '#%s' % (struct.pack('BBB', r, g, b).encode('hex'))
				
	
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