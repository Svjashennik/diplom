
from rest_framework import serializers
from django.contrib.auth.models import User
from shop import models


class GameListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Game
        fields = ['name', 'release_date', 'developer_id', 'active', 'genre']

    def create(self, validated_data):
        return models.Game.objects.create(**validated_data)
