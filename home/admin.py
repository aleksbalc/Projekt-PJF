from django.contrib import admin

# Register your models here.

from .models import ZadaniaStale, ZadaniaJednorazowe, H_ZadaniaJednorazowe, H_ZadaniaStale, PrzydzieloneZadanieStale

admin.site.register(ZadaniaStale)
admin.site.register(ZadaniaJednorazowe)
admin.site.register(H_ZadaniaStale)
admin.site.register(H_ZadaniaJednorazowe)
admin.site.register(PrzydzieloneZadanieStale)