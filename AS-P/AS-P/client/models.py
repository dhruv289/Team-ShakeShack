from django.db import models
from users import models as users_model
from Inventory import models as Inventory_models

# Create your models here.
class cart(models.Model):
    username = models.ForeignKey(users_model.user, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory_models.Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shipping_weight = models.DecimalField(max_digits = 10, decimal_places = 4, null = True)
    
    def __str__(self):
        return f'{self.username} ({self.item})'

        

