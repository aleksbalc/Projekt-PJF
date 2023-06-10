from django.contrib import admin

# Register your models here.

from .models import ZadaniaStale, ZadaniaJednorazowe

admin.site.register(ZadaniaStale)
admin.site.register(ZadaniaJednorazowe)