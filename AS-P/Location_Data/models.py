
from django.db import models
import mpu #Install via "pip install mpu --user"

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=10,decimal_places=7)
	longitude = models.DecimalField(max_digits=10,decimal_places=7)
	altitude = models.DecimalField(max_digits=10,decimal_places=7)
	
	def __str__(self):
		return self.name

	
#		return self.longitude
#
class Distance(models.Model):
	placeA=models.CharField(max_length=200,null=True)
	placeB=models.CharField(max_length=200,null=True)
	distance=models.FloatField(default=0.00)

	def __str__(self):
		return self.placeA+" to "+self.placeB



	def getDistance(placeA,placeB):
		return distance
	
#	def save(self, *args, **kwargs):
#		self.distance = self.calculate()
#		super(Distance, self).save(*args, **kwargs)
	
#	def calculate(self):
#		return mpu.haversine_distance((placeA.latitude, placeA.longitude), (place.latitude, placeB.longitude))
