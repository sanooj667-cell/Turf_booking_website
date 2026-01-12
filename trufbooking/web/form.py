from django import forms
from .models import Turf

class TurfForm(forms.ModelForm):
        class Meta:
            model = Turf
            fields = ["category","name","location","price","image","description","owner"]