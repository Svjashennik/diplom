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



class Genre(models.Models):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    decs = models.TextField(blank=True)



class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField()
    developer_id = models.ForeignKey(Developer, on_delete=models.SET_NULL)
    genre =  models.ForeignKey(Genre, on_delete=models.SET_NULL)


    def __str__(self):
        return f'{self.name}'


class Order(models.Model):

    class Status(models.TextChoices):
        pending='Pending'
        success = 'Success'
        canceled = 'Cancel'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.TextField(choices=Status.choices)


class OrderedGame(models.Model):
    order = models.ForeignKey(Order, primary_key=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, primory_key=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)


class Cart(models.Model):
    customer = models.ForeignKey(User,primary_key=True, on_delete=models.CASCADE)
    game = models.ForeignKey(User,primary_key=True, on_delete=models.SET_NULL)
    count =  models.IntegerField(default=1)


class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(User, on_delete=models.SET_NULL)
    text = models.TextField()
    grade = models.IntegerField()