from django import forms
from .models import *

class locationModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('location','destination',)

class placeModelForm(forms.ModelForm):
    class Meta:
        model = place
        fields = ('name',)