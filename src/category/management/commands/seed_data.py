from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from datetime import timedelta
from faker import Faker

from category.models import Category
from product.models import Product
from customer.models import Customer
from order.models import Order, OrderItem
from inventory.models import Inventory


class Command(BaseCommand):
    help = 'Seed the database with fake data for testing'

    def handle(self, *args, **kwargs):

        fake = Faker()

        # Create categories
        categories = []
        for _ in range(10):
            cat = Category.objects.create(name=fake.word().capitalize())
            categories.append(cat)

        # Create products
        products = []
        for _ in range(50):
            cat = random.choice(categories)
            p = Product.objects.create(
                title=fake.word().capitalize(),
                category=cat,
                price=round(random.uniform(10, 500), 2),
                stock=random.randint(0, 100),
                status=random.choice([1, 2, 3]),
                code=fake.unique.ean(length=8)
            )
            products.append(p)

        # Create inventories
        for product in products[:50]:  # Not all products need inventory
            Inventory.objects.create(
                product=product,
                title=product.title,
                category=product.category,
                price=product.price,
                stock=product.stock,
                status=product.status,
                code=product.code,
                size=round(random.uniform(1, 20), 2),
                color=fake.color_name()
            )

        # Create customers
        customers = []
        for _ in range(100):
            c = Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                segment=str(random.choice([1, 2, 3, 4])),
                orders=0,
                total_spent=0
            )
            customers.append(c)

        # Create orders + order items
        for _ in range(200):
            customer = random.choice(customers)
            order_date = timezone.now() - timedelta(days=random.randint(0, 730))  # within last 2 years
            order = Order.objects.create(
                customer=customer,
                date=order_date,
                total=0,
                status=random.choice([True, False])
            )

            total = 0
            for _ in range(random.randint(1, 5)):  # 1-5 items per order
                product = random.choice(products)
                quantity = round(random.uniform(1, 5), 2)
                amount = round(quantity * float(product.price), 2)

                item = OrderItem.objects.create(
                    product=product,
                    quantity=quantity,
                    amount=amount
                )

                order.items.add(item)
                total += amount

            order.total = round(total, 2)
            order.save()

            # Update customer stats
            customer.orders += 1
            customer.total_spent = round(customer.total_spent + total, 2)
            customer.save()

        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))
