from django.db import models
from customer.models import Customer
from product.models import Product


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    STATUS = [
        (1, 'Completed'),
        (2, 'Canceled'),
        (3, 'Processing'),
        (4, 'Pending'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(OrderItem)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.name