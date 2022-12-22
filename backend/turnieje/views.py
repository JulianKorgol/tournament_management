from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework import generics
from django.core.exceptions import ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Account, Role, Tournaments, AcoountToTournament, Matches

# Input Serializers
from .serializers import LoginSerializer
# Output Serializers
from .serializers import DashboardAdminTournamentsSerializer, DashboardTournamentsSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return Response(status=HTTP_200_OK)
        return Response(None, status=HTTP_401_UNAUTHORIZED)


class ExampleEndpointView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': "You are logged in!", 'user': request.user.username})


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status=HTTP_200_OK)


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        acc = Account.objects.get(user=request.user)

        if acc.role.name == "player" or acc.role.name == "coordinator":
            try:
                tournaments = AcoountToTournament.objects.filter(account=acc)
            except AcoountToTournament.DoesNotExist:
                return Response({"tournaments": []})

            tournaments_data = DashboardTournamentsSerializer(tournaments, many=True).data
            return Response({"tournaments": tournaments_data})
        elif acc.role.name == "admin":
            try:
                tournaments = Tournaments.objects.all()
            except Tournaments.DoesNotExist:
                return Response({"tournaments": []})

            tournaments_data = DashboardAdminTournamentsSerializer(tournaments, many=True).data
            return Response({"tournaments": tournaments_data})
