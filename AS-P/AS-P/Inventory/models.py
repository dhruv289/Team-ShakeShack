from django.db import models

# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=200)
    weight=models.DecimalField(max_digits=4,decimal_places=2)
    category=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    item_id=models.IntegerField()
    
    def __str__(self):
        return self.item_id