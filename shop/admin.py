from django.contrib import admin
from shop import models


@admin.register(models.Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'country')
    list_filter = ['country']
    search_fields = ['name']


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
    search_fields = ['name']


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
    list_filter = ['genre']
    search_fields = ['name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'status', 'order_date')
    list_filter = ['customer', 'status']


@admin.register(models.OrderedGame)
class OrderedGameAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'order', 'game', 'count')
    list_filter = ['order']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'game')
    list_filter = ['customer']


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'game','grade')
    list_filter = ['customer', 'game']    

