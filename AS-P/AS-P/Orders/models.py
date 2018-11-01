from django.db import models
from users import models as users_models
from Inventory import models as Inventory_models


# Create your models here.
class Order(models.Model):
	orderID=models.IntegerField()
	owner=models.ForeignKey(users_models.user,on_delete=models.CASCADE)
	#username=user.objects.select_related().get(owner.username)
	status=models.CharField(max_length=200)
	priority=models.CharField(max_length=200)
	#location=user.objects.select_related().get(owner.location)
	def __str__(self):
		return self.orderID

class content(models.Model):
    username = models.ForeignKey(users_models.user, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Inventory_models.Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.username} ({self.item})'