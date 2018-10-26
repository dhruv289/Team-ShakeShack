from django.db import models
import mpu #Install via "pip install mpu --user"

# Create your models here.

class user(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    clinic = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email_ID = models.CharField(max_length=200)
    token code = models.CharField(max_length=200)

    def __str__(self):
        return self.username

class Location(models.Model):
	name = models.CharField(max_length=200)
	latitude = models.FloatField
	longitude = models.FloatField
	altitude = models.IntegerField
	
	def _str_(self);
		return self.name

class Distance(models.Model):
	placeA = models.ForeignKey(Location, on_delete=models.CASCADE)
	placeB = models.ForeignKey(Location, on_delete=models.CASCADE)
	distance = models.FloatField(default = 0.0)
	
	def save(self, *args, **kwargs):
		self.distance = self.calculate()
		super(Distance, self).save(*args, **kwargs)
	
	def calculate(self):
		return mpu.haversine_distance((placeA.latitude, placeA.longitude), (placeB.latitude, placeB.longitude))
