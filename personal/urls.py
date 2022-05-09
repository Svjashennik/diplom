from django.urls import path, include
from . import views

urlpatterns = [
    path('bugreports/', views.BugReportListAPIView.as_view()),
    path('bugreport/<uuid:uuid>/', views.BugReportAPIView.as_view()),
    path('userlist/<str:username>/', views.UserBugListAPIView.as_view()),
    path('account_info/', views.AccountInfoAPIView.as_view()),
]