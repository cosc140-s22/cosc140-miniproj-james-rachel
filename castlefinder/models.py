from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import models as auth_models


FILTER_CHOICES = (
    ('name','NAME'),
    ('distance', 'DISTANCE'),
    ('rating','RATING'),
)

class Castle(models.Model):
    name = models.CharField(max_length=50, blank=False)
    rating = models.DecimalField(decimal_places=1, max_digits=2, blank=False)
    distance = models.DecimalField(blank=False, decimal_places=2, max_digits=10000)
    imageReference = models.CharField(max_length=50, blank=False, default=None)
    searchWord = models.CharField(max_length=50, blank=False)
    placeID= models.CharField(max_length=50, blank=False)



class CastleImage(models.Model):
  image = models.ImageField(upload_to='castle_images/')
  castle = models.ForeignKey(Castle, on_delete=models.CASCADE)

class DropDown(models.Model):
  color = models.CharField(max_length=8, choices=FILTER_CHOICES, default='green')


class Review(models.Model):
    Author = models.CharField(max_length=50, blank=False)
    rating = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    castle = models.ForeignKey(Castle, models.CASCADE)
    def __str__(self):
        return f"Review for {self.castle.name}"