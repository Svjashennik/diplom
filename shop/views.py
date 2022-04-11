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
