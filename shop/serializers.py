
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from shop import models


class GameListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')
    genre = serializers.SerializerMethodField('get_genre')
    developer = serializers.SerializerMethodField('get_developer')

    class Meta:
        model = models.Game
        fields = ['uuid','name', 'release_date', 'developer', 'active', 'genre', 'count', 'price']

    def create(self, validated_data):
        return models.Game.objects.create(**validated_data)

    def get_count(self, obj):

        if self.context.get('order', None) is not None:
            ordgame = obj.find_in_order(self.context['order'])
            return ordgame.count

        if self.context['request'].user.is_anonymous:
            return 0

        cust = self.context['request'].user
        cart = obj.find_in_cart(cust)
        if cart is None:
            return 0
        return cart.count

    def get_genre(self, obj):
        genres = []
        for gen in obj.genre.all():
            genres.append(gen.name)
        return genres

    def get_developer(self, obj):
        return obj.developer.name

class OrderListSerializer(serializers.ModelSerializer):
    game = serializers.SerializerMethodField('get_game')

    class Meta:
        model = models.Order
        fields = ['uuid', 'order_date', 'status', 'customer_id', 'game']

    def create(self, validated_data):
        user = self.context['request'].user
        order =  models.Order.objects.create(**validated_data, customer=user)
        for cart in models.Cart.objects.filter(customer=user):
            models.OrderedGame.objects.create(order=order, game=cart.game, count=cart.count)
            cart.delete()
        return order
    
    def update(self, instance, validated_data):
        if validated_data.get('status') is not None:
            instance.status = validated_data.get('status')
        if validated_data.get('order_date') is not None:
            instance.order_date = validated_data.get('order_date')

        instance.save()
        return instance

    def get_game(self, obj):
        return GameListSerializer(obj.get_games(), many = True, context={'order':obj}).data


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already registered')

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already registered')

        return value

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')  
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        validated_data['token'] = Token.objects.create(user=user)
        return validated_data