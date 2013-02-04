from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'katalog.views.home', name='home'),
    url(r'^mapa/', 'katalog.views.mapa', name='mapa'),
    url(r'^rezervace/(?P<slug>[-\w]+)/$', 'katalog.views.profil', name='profil'),
    url(r'^chroupy/$', 'katalog.views.chroupy', name='chroupy'),
    url(r'^statistiky/$', 'katalog.views.statistiky', name='statistiky'),
    # url(r'^rezervace/', include('rezervace.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
