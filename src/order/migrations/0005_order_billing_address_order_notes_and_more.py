# Generated by Django 5.2.3 on 2025-06-16 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='unpaid', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
