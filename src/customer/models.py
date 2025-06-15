from django.db import models

class Customer(models.Model):
    SEGMENT = [
        (1, 'New Customer'),
        (2, 'Regular Customer'),
        (3, 'VIP Customer'),
        (4, 'Inactive Customer'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    segment = models.CharField(choices=SEGMENT, max_length=1)
    orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_update = models.DateTimeField(auto_now=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
