from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .services import *
from shop import models, serializers
from rest_framework.exceptions import ValidationError
from requests.exceptions import HTTPError


class GameListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        games = models.games.objects.filter(active=True)
        serializer = serializers.GameListSerializer(games, many=True, context={'request':request})
        return Response(serializer.data)


class CartListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_games = [cart.game for cart in models.Cart.objects.filter(customer=request.user)]
        serializer = serializers.GameListSerializer(cart_games, many=True, context={'request':request})
        return Response(serializer.data)


class OrderListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = models.Order.objects.filter(customer=request.user).order_by('order_date')
        serializer = serializers.OrderListSerializer(orders, many=True, context={'request':request})
        return Response(serializer.data)