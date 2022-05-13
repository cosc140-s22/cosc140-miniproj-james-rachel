from django import forms
from .models import DropDown


class CastleFilterForm(forms.Form):
    location_search = forms.CharField(label="Enter a location", max_length=50, required=False)
    filter=forms.CharField(label="Pick a filter", max_length=50, required=False)

class DropDownForm(forms.Form):
    class Meta:
        model = DropDown
        fields = ['color']
