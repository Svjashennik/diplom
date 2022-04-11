from django.urls import path, include

from shop import views

urlpatterns = [
    path('gamelist/', views.GameListAPIView.as_view()),
    
]