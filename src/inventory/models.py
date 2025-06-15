from django.db import models
from category.models import Category
from product.models import Product


class Inventory(models.Model):
    STATUS = [
        (1, 'Active'),
        (2, 'Out of stock'),
        (3, 'Draft'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.IntegerField()
    status = models.IntegerField(choices=STATUS, default=1)
    code = models.CharField(max_length=100)
    size = models.DecimalField(decimal_places=2, max_digits=10)
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.title