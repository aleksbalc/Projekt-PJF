from django.forms import ModelForm
from .models import Room, ZadaniaStale


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class ZadaniaStaleForm(ModelForm):
    class Meta:
        model = ZadaniaStale
        fields = ['name','description','recipients']