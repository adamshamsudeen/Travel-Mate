from django.contrib.auth.models import Permission, User
from django.db import models


class Trip(models.Model):
    user = models.ForeignKey(User, default=1)
    trip_source = models.CharField(max_length=250)
    trip_dest= models.CharField(max_length=250)
    vehicle = models.CharField(max_length=250)
    date = models.DateField()
    amount = models.IntegerField()

    def __str__(self):
        return self.trip_source + ' - ' + self.trip_dest
