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

class inventory(models.Model):
    item_id=models.DecimalField(max_digit=5)
    name=models.CharField(max_length=200)
    weight=models.DecimalField(max_digit=4,decimal_places=2)
    category=models.CharField(max_length=200)
    description=models.CharField(max_length=200
    
    
    def __str__(self):
        return self.name
    
