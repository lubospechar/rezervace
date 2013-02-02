# coding: utf-8
from django.contrib.gis import admin

from katalog.models import Kraj, Okres, Tema, Fotografie, Rezervace, Poznamky, Status


class KrajAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nazev",)}

admin.site.register(Kraj, KrajAdmin)



class OkresAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nazev",)}

admin.site.register(Okres, OkresAdmin)

admin.site.register(Tema)

class PoznamkyInline(admin.TabularInline):
	model = Poznamky
	
class FotografieInline(admin.TabularInline):
	model = Fotografie


#class RezervaceAdmin(admin.OSMGeoAdmin):
class RezervaceAdmin(admin.ModelAdmin):
	inlines = [
		PoznamkyInline,
		FotografieInline,
	]
	list_display = ('nazev', 'kod', 'status', 'uprava', 'kontrola_adres')
	list_filter = ['uprava','status', 'okres']
	
	prepopulated_fields = {"slug": ("nazev",)}

admin.site.register(Rezervace, RezervaceAdmin)

class StatusAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("zkratka",)}

admin.site.register(Status, StatusAdmin)