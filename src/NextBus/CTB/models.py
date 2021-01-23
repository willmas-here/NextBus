from django.db import models
from django.urls import reverse

# Create your models here.
class Route(models.Model):
    co          = models.CharField(max_length=4)
    route       = models.CharField(max_length=4)
    orig_tc     = models.CharField(max_length=50)
    orig_sc     = models.CharField(max_length=50)
    orig_en     = models.CharField(max_length=50)
    dest_tc     = models.CharField(max_length=50)
    dest_sc     = models.CharField(max_length=50)
    dest_en     = models.CharField(max_length=50)
    stops_i     = models.CharField(max_length=1000)
    stops_o     = models.CharField(max_length=1000)

    def __str__(self):
        return self.route

    def get_absolute_url(self):
        return reverse('CTB:route', kwargs={'route_num':str(self.route)})


class Stop(models.Model):
    stop    = models.IntegerField()
    name_tc = models.CharField(max_length=50)
    name_sc = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    lat     = models.FloatField()
    long    = models.FloatField()

    def __str__(self):
        return self.name_en