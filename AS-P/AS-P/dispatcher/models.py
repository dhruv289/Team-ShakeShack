from django.db import models
from Orders.models import Order
# Create your models here.
class Drones(models.Model):
	drone_num = models.IntegerField()
	present_weight = models.DecimalField(max_digits = 10, decimal_places = 5)

	def __str__(self):
		return str(drone_num)


class Drones_content():
	drone = models.ForeignKey(Drones, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	def __str__():
		return str(self.drone.drone_num)