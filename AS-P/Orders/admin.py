from django.contrib import admin
from .models import Order
from .models import content
# Register your models here.
admin.site.register(Order)
admin.site.register(content)