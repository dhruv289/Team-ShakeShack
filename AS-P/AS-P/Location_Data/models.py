
from django.db import models
import mpu #Install via "pip install mpu --user"

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=4,decimal_places=2)
	longitude = models.DecimalField(max_digits=5,decimal_places=2)
	altitude = models.DecimalField(max_digits=5,decimal_places=2)
	
	def _str_(self):
		return self.name

	
#		return self.longitude
#
#class Distance(models.Model):
#	placeA = models.ForeignKey(Location, on_delete=models.CASCADE)
#	placeB = models.ForeignKey(Location, on_delete=models.CASCADE)
	
#	distance = models.FloatField(default = 0.0)
	
#	def save(self, *args, **kwargs):
#		self.distance = self.calculate()
#		super(Distance, self).save(*args, **kwargs)
	
#	def calculate(self):
#		return mpu.haversine_distance((placeA.latitude, placeA.longitude), (place.latitude, placeB.longitude))
