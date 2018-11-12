from django.db import models
from users import models as users_models
from Inventory import models as Inventory_models
from Location_Data import models as Location_Data_models

# Create your models here.
class Order(models.Model):
	order_id=models.DecimalField(max_digits=4,decimal_places=2)
	owner=models.ForeignKey(users_models.user,on_delete=models.CASCADE)
	status=models.CharField(max_length=200)
	priority=models.CharField(max_length=200)
	creation_time = models.DateTimeField(auto_now_add=True)
	dispatch_time = models.DateTimeField(null = True, blank = True)
	location=models.ForeignKey(Location_Data_models.Location, on_delete=models.CASCADE, null=True, blank=True)
	weight = models.DecimalField(max_digits=10,decimal_places=4,null=True)

	def __str__(self):
		return str(self.order_id)

class content(models.Model):
    username = models.ForeignKey(users_models.user, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Inventory_models.Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4,decimal_places=0)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.orderID} ({self.item_id})'