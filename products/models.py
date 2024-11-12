from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f"{self.category_name}"
    
    class Meta:
        verbose_name_plural = ('Category')

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_image = models.FileField(upload_to="static/uploads", null = True)
    product_quantity = models.IntegerField()
    product_description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name}"
    
    class Meta:
        verbose_name_plural = ('Products')
    

