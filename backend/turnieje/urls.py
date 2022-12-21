from django.urls import path, include
from rest_framework import routers
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
