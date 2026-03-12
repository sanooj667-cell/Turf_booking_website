from django import forms
from .models import Turf

class TurfForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = ["category", "name", "location", "price", "image", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
