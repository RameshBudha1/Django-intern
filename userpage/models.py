from django.db import models
from products.models import Products
from django.contrib.auth.models import User

class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    PAYMENT = (
        ('Cash On Delivery','Cash On Delivery'),
        ('Esewa','Esewa'),
    )
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField(null = True)
    status = models.CharField(max_length=200,default="Pending...", null = True )
    payment_method = models.CharField(max_length=200,choices=PAYMENT)
    payment_status = models.BooleanField(default=False, null=True)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)


