
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
        cust = self.context['request'].user
        return obj.find_in_cart(cust).count