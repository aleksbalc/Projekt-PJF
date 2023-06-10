from django.forms import ModelForm
from .models import ZadaniaStale, ZadaniaJednorazowe

class ZadaniaStaleForm(ModelForm):
    class Meta:
        model = ZadaniaStale
        fields = ['name','description']

class ZadaniaJednorazoweForm(ModelForm):
    class Meta:
        model = ZadaniaJednorazowe
        fields = ['name','description']