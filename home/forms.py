from django.forms import ModelForm
from .models import ZadaniaStale, ZadaniaJednorazowe, PrzydzieloneZadanieStale
from django import forms
from django.contrib.auth.models import User, Group

class ZadaniaStaleForm(ModelForm):
    class Meta:
        model = ZadaniaStale
        fields = ['name','description']

class PrzydzieloneZadanieStaleForm(ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='programista'))
    class Meta:
        model = PrzydzieloneZadanieStale
        fields = ['id_zs','recipient']

class ZadaniaJednorazoweForm(ModelForm):
    class Meta:
        model = ZadaniaJednorazowe
        fields = ['name','description']

class EditJednorazoweForm(ModelForm):
    class Meta:
        model = ZadaniaJednorazowe
        fields = ['started','finished']

