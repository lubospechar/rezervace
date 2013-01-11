# coding: utf-8
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Kraj(models.Model):
	nazev = models.CharField(max_length=25, unique=True)
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.nazev

	class Meta:
		verbose_name = "Kraj"
		verbose_name_plural = "Kraje"
		ordering = ["nazev",]
		
class Okres(models.Model):
	nazev = models.CharField(max_length=35, unique=True)
	kraj = models.ForeignKey(Kraj)
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.nazev

	class Meta:
		verbose_name = "Okres"
		verbose_name_plural = "Okresy"
		ordering = ["nazev",]
		
class Obdobi(models.Model):
	obdobi = models.CharField(max_length=40, unique=True)

	def __unicode__(self):
		return self.obdobi

	class Meta:
		verbose_name = "Období"
		verbose_name_plural = "Období"
		ordering = ["obdobi",]


class Status(models.Model):
	status = models.CharField(max_length=100)
	zkratka = models.CharField(max_length=10)
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.status
	
	class Meta:
		verbose_name = "Status"
		verbose_name_plural = "Statuty"
		ordering = ["status",]

class Rezervace(models.Model):
	nazev = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	status = models.ForeignKey(Status)
	predmet = models.TextField(null=True, blank=True)
	stred = models.PointField()
	wikipedia = models.URLField(null=True, blank=True)
	commons = models.URLField(null=True, blank=True)
	okres = models.ForeignKey(Okres)
	uprava = models.DateTimeField()
	objects = models.GeoManager()
	
	def __unicode__(self):
		return self.nazev
	
	class Meta:
		verbose_name = "Rezervace"
		verbose_name_plural = "Rezervace"
		ordering = ["nazev",]

class Fotografie(models.Model):
	obdobi = models.ForeignKey(Obdobi)
	pocet = models.IntegerField(default=0)
	rezervace = models.ForeignKey(Rezervace)
	
	def __unicode__(self):
		return '%s: %s' % (self.obdobi, self.pocet)
	
	class Meta:
		verbose_name = "Fotografie"
		verbose_name_plural = "Fotografie"
	
class Poznamky(models.Model):
	poznamka = models.CharField(max_length=255)
	rezervace = models.ForeignKey(Rezervace)
	uzivatel = models.ForeignKey(User)
	datum = models.DateTimeField()
	
	class Meta:
		verbose_name = "Poznámka"
		verbose_name_plural = "Poznámky"
		ordering = ["datum",]
	