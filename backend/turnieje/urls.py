from django.urls import path, include
from rest_framework import routers
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('me/', views.MeView.as_view()),
    path('me/games/', views.MyGames.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
    path('dashboard/tournament/<str:tournament_uuid>/', views.TournamentDetailsView.as_view()),
    path('dashboard/tournament/<str:tournament_uuid>/matches', views.TournamentMatches.as_view()),
    # Public
    path('public/tournaments/', views.ListTournamentsView.as_view()),
#     path('public/tournament/<str:tournament_uuid>/', views.TournamentView.as_view()),
    # Admin
    path('admin_panel/adduser/', views.AdminPanelAddUser.as_view()),
    # Coordinator
    path('coordinator_panel/addtournament/', views.AddTournament.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/manage/', views.ManageTournament.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/manage/user/add/', views.AddPeopleToTournament.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/manage/user/remove/', views.RemovePeopleFromTournament.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/manage/games/generate/', views.GenerateGames.as_view()),
    # path('coordinator_panel/tournament/<str:tournament_uuid>/games/get/', views.GetGames.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/games/getnotplayed/', views.GetNotPlayedGames.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/score/add/', views.AddScore.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/score/modify/', views.ModifyScore.as_view()),
    path('coordinator_panel/tournament/<str:tournament_uuid>/score/delete/', views.RemoveScore.as_view()),
]
