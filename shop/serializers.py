
from rest_framework import serializers
from django.contrib.auth.models import User
from shop import models


class GameListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    class Meta:
        model = models.Game
        fields = ['name', 'release_date', 'developer_id', 'active', 'genre', 'count']

    def create(self, validated_data):
        return models.Game.objects.create(**validated_data)

    def get_count(self, obj):

        if self.context.get('order', None) is not None:
            ordgame = obj.find_in_order(self.context['order'])
            return ordgame.count

        if self.context['request'].user.is_anonymous():
            return 0
            
        cust = self.context['request'].user
        cart = obj.find_in_cart(cust)
        if cart is None:
            return 0
        return cart.count


class OrderListSerializer(serializers.ModelSerializer):
    game = serializers.SerializerMethodField('get_game')

    class Meta:
        model = models.Order
        fields = ['uuid', 'order_date', 'status', 'customer_id', 'game', 'count']

    def create(self, validated_data):
        return models.Order.objects.create(**validated_data)

    def get_game(self, obj):
        return GameListSerializer(obj.get_game(), many = True, context={'order':obj})
