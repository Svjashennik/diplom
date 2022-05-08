
from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .services import *
from . import models, serializers
from rest_framework.exceptions import ValidationError
from requests.exceptions import HTTPError


class GameListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        start = int(request.query_params.get('start', 0))
        end = int(request.query_params.get('end', 20))
        genre = request.query_params.get('genre', None)
        dev = request.query_params.get('dev', None)

        if genre is not None:
            games = models.Genre.objects.filter(name=genre).first().games.all()
        else:
            games = models.Game.objects.filter(active=True)
        if dev is not None:
            games = games.filter(developer__name=dev)
    
        serializer = serializers.GameListSerializer(games[start: end], many=True, context={'request':request})
        return Response(serializer.data)

    def get_serializer_class(self):
        return serializers.GameListSerializer


class CartListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_games = [cart.game for cart in models.Cart.objects.filter(customer=request.user)]
        serializer = serializers.GameListSerializer(cart_games, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        game = models.Game.objects.filter(uuid=request.data['uuid']).first()
        return Response(game.add_to_cart(request.user))

    def get_serializer_class(self):
        return serializers.GameListSerializer

class OrderListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = models.Order.objects.filter(customer=request.user).order_by('order_date')
        serializer = serializers.OrderListSerializer(orders, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.OrderListSerializer(data={"status":"Pending"}, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request):
        order = models.Order.objects.get(uuid=request.data['uuid'])
        serializer = serializers.OrderListSerializer(order, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def get_serializer_class(self):
        return serializers.OrderListSerializer


class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def get_serializer_class(self):
        return serializers.RegistrationSerializer


class ReviewAPIView(APIView):

    def get(self, request, uuid):
        game = models.Game.objects.get(pk=uuid)
        serializer = serializers.ReviewSerializer(game.reviews.all(), many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request, uuid):
        game = models.Game.objects.get(pk=uuid)
        serializer = serializers.ReviewSerializer(data=request.data, context={'request':request, 'game':game})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def get_serializer_class(self):
        return serializers.ReviewSerializer


class GenresAPIView(APIView):
    
    def get(self, request):
        genres = models.Genre.objects.all().order_by('name')
        serializer = serializers.GenresSerializer(genres, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        return serializers.GenresSerializer


class DeveloperAPIView(APIView):
    
    def get(self, request):
        devs = models.Developer.objects.all().order_by('name')
        serializer = serializers.DeveloperSerializer(devs, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        return serializers.DeveloperSerializer