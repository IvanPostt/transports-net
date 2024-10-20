from django.db import models

from users.models import User


# Create your models here.

class CatTransport(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Transport(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=CatTransport, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    def total_quantity(self):
        return sum(basket.quantity for basket in self)

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Transport, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Транспорт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    # def total_sum(self):
    #      baskets = Basket.objects.filter(user=self.user)
    #      return sum(basket.sum() for basket in baskets)
    #
    # def total_quantity(self):
    #      baskets = Basket.objects.filter(user=self.user)
    #      return sum(basket.quantity for basket in baskets)
    #
