from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .services import *
from . import models, serializers
from rest_framework.exceptions import ValidationError
from requests.exceptions import HTTPError
from rest_framework import permissions, status
from .permissions import OwnerOrReadOnly
from django.contrib.auth.models import User

class BugReportListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        report = models.BugReport.objects.filter(owner=request.user).order_by('index')
        serializer = serializers.BugReportListSerializer(report, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.BugReportSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def get_serializer_class(self):
        return serializers.BugReportSerializer



class BugReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnerOrReadOnly]

    def get(self, request, uuid):
        report = models.BugReport.objects.get(uuid=uuid)
        serializer = serializers.BugReportSerializer(report, context={'request': request})
        return Response(serializer.data)

    def put(self, request, uuid):
        report = models.BugReport.objects.get(uuid=uuid)
        self.check_object_permissions(request, report)
        serializer = serializers.BugReportSerializer(report, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, uuid):
        report = models.BugReport.objects.get(uuid=uuid)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

    def get_serializer_class(self):
        return serializers.BugReportSerializer


class UserBugListAPIView(APIView):

    def get(self, request, username):
        user = User.objects.get(username=username)
        report = models.BugReport.objects.filter(owner=user).order_by('index')
        serializer = serializers.BugReportListSerializer(report, many=True, context={'request':request})
        return Response(serializer.data)
    
    def get_serializer_class(self):
        return serializers.BugReportListSerializer



class AccountInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'username':request.user.username})