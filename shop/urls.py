from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token 
from . import views

urlpatterns = [
    path('gamelist/', views.GameListAPIView.as_view()),
    path('cart/', views.CartListAPIView.as_view()),
    path('orderlist/', views.OrderListAPIView.as_view()),
    path('registration/', views.RegistrationAPIView.as_view()),
    path('genres/', views.GenresAPIView.as_view()),
    path('developers/', views.DeveloperAPIView.as_view()),
    path('reviews/<uuid:uuid>/', views.ReviewAPIView.as_view()),
    path('login/', obtain_auth_token )
]