from django.urls import path, include
from rest_framework import routers
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('me/', views.MeView.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
    path('dashboard/tournament/<str:tournament_uuid>/', views.TournamentDetailsView.as_view()),
    # Public
    path('public/tournaments/', views.ListTournamentsView.as_view()),
    path('public/tournament/<str:tournament_uuid>/', views.TournamentView.as_view()),
    # Admin
    path('admin_panel/adduser/', views.AdminPanelAddUser.as_view()),
]
