from django.db import models
from Location_Data import models as Location_Data_models
# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    clinic = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email_ID = models.CharField(max_length=200) #replace with email field?
    token_code = models.ForeignKey(users.tokencode, on_delete=models.CASCADE)
    location=models.ForeignKey(Location_Data_models.Location, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
    
class tokencode(models.Model):
    token_code = models.CharField(max_length=200)
    email_ID = models.CharField(max_length=200)
    
    def __str__(self):
        return self.token_code
