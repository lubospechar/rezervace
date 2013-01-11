# coding: utf-8
from django.contrib.gis import admin

from katalog.models import Kraj, Okres, Obdobi, Fotografie, Rezervace, Poznamky, Status


class KrajAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nazev",)}

admin.site.register(Kraj, KrajAdmin)



class OkresAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nazev",)}

admin.site.register(Okres, OkresAdmin)

admin.site.register(Obdobi)

class PoznamkyInline(admin.TabularInline):
	model = Poznamky
	
class FotografieInline(admin.TabularInline):
	model = Fotografie


class RezervaceAdmin(admin.OSMGeoAdmin):
	inlines = [
		PoznamkyInline,
		FotografieInline,
	]
	
	prepopulated_fields = {"slug": ("nazev",)}

admin.site.register(Rezervace, RezervaceAdmin)

class StatusAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("zkratka",)}

admin.site.register(Status, StatusAdmin)