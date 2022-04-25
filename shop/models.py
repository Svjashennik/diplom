from platform import release
from django.db import models
import uuid
from django.contrib.auth.models import User

from datetime import datetime, timezone, timedelta

class Developer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    country = models.TextField(blank=True)
    city = models.TextField(blank=True)
    desc = models.TextField(blank=True)


class Genre(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    decs = models.TextField(blank=True)


class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField()
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, related_name='games', null=True)
    genre =  models.ManyToManyField(Genre, related_name='games')
    active = models.BooleanField(default=True)
    price = models.FloatField(default=3)


    def __str__(self):
        return f'{self.name}'
    
    def find_in_cart(self,user):
        return Cart.objects.filter(customer=user, game=self).first()
    
    def find_in_order(self, order):
        return OrderedGame.objects.filter(order=order).first()

    def add_to_cart(self, user, count = 1):
        cart = self.find_in_cart()
        if cart is not None:
            cart.count+=1
            cart.save()
            return True
        Cart.objects.create(customer=user, game=self ,count=1)
        return True
    

class Key(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    game = models.ForeignKey(Game,  on_delete=models.CASCADE, related_name='keys')
    text = models.TextField()
    active = models.BooleanField(default=True)

class Order(models.Model):

    class Status(models.TextChoices):
        pending='Pending'
        success = 'Success'
        canceled = 'Cancel'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.TextField(choices=Status.choices)

    def get_games(self):
        return [ordgame.game for ordgame in models.OrderedGame.objects.filter(order=self)]


class OrderedGame(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='games')
    game = models.ForeignKey(Game,  on_delete=models.CASCADE, related_name='orders')
    count = models.IntegerField(default=1)


class Cart(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='carts')
    count =  models.IntegerField(default=1)


class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    game = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    grade = models.IntegerField()