from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    price = models.FloatField(default=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_recipe")


# class Sellrecipe(models.Model):
#     image = models.ImageField(upload_to='media')
#     price = models.FloatField()
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=1000)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Recipe, through='CartItem')


class CartItem(models.Model):
    product = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    order_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, choices=[(
        'Pending', 'Pending'), ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')], default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return str(self.order_id)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    payment_status = models.CharField(
        max_length=50, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.transaction_id


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} in order {self.order}"
