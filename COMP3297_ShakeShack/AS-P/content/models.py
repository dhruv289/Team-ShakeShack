from django.db import models

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
    
class cart(models.Model):
    username = models.ForeignKey(user, on_delete=modes.CASCADE)
    item = models.DecimalField(max_digits=5)
    quantity = models.DecimalField(max_digits=5)
    
    def __str__(self):
        return f'{self.username} ({self.item})'

class content(models.Model):
    username = models.ForeignKey(user, on_delete=modes.CASCADE)
    item = models.DecimalField(max_digits=5)
    quantity = models.DecimalField(max_digits=5)
    orderID = models.ForeignKey(orders, on_delete=modes.CASCADE)
    
    def __str__(self):
        return f'{self.username} ({self.item})'
