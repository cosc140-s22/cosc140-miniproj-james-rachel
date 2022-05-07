from django.db import models

class Castle(models.Model):
    name = models.CharField(max_length=50, blank=False)
    rating = models.DecimalField(decimal_places=1, max_digits=1, blank=False)
    distance = models.IntegerField(blank=False)

class CastleImage(models.Model):
  image = models.ImageField(upload_to='castle_images/')
  caption = models.CharField(max_length=30)
  product = models.ForeignKey(Castle, on_delete=models.CASCADE)