from django.forms import ModelForm
from .models import Room, ZadaniaStale, ZadaniaJednorazowe


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class ZadaniaStaleForm(ModelForm):
    class Meta:
        model = ZadaniaStale
        fields = ['name','description','recipients']

class ZadaniaJednorazoweForm(ModelForm):
    class Meta:
        model = ZadaniaJednorazowe
        fields = ['name','description','progress']