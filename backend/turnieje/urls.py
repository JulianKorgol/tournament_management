from django.urls import path, include
from rest_framework import routers
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('example/', views.ExampleEndpointView.as_view()),
]
