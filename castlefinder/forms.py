from django import forms
from .models import DropDown
from .models import Review


class CastleFilterForm(forms.Form):
    location_search = forms.CharField(label="Enter a location", max_length=50, required=False)
    

FILTER_CHOICES= [
    ('rating', 'Rating'),
    ('distance', 'Distance'),
    ('name', 'Name'),
    ]

class DropDown(forms.Form):
    filter= forms.CharField(label='Choose a filter:', widget=forms.Select(choices=FILTER_CHOICES))

class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = ['rating', 'review']