from django.db import models

class Castle(models.Model):
    name = models.CharField(max_length=50, blank=False)
    rating = models.DecimalField(decimal_places=1, max_digits=2, blank=False)
    distance = models.DecimalField(blank=False, decimal_places=2, max_digits=10000)
    imageReference = models.CharField(max_length=50, blank=False, default=None)



class CastleImage(models.Model):
  image = models.ImageField(upload_to='castle_images/')
  castle = models.ForeignKey(Castle, on_delete=models.CASCADE)