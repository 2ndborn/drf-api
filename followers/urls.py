from django.urls import path
from followers import views

urlpatterns = [
    path('followers/', views.followerList.as_view()),
    path('followers/<int:pk>/', views.followerList.as_view()),
]
