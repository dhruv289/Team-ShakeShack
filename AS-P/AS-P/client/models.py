from django.db import models
from users import models as users_model
from Inventory import models as Inventory_models

# Create your models here.
class cart(models.Model):
    username = models.ForeignKey(users_model.user, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory_models.Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f'{self.username} ({self.item})'

        

