from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    price = models.FloatField(default=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


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
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Order"
