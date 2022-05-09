from django import forms

class CastleFilterForm(forms.Form):
    location_search = forms.CharField(label="Enter a location", max_length=50, required=False)
    
