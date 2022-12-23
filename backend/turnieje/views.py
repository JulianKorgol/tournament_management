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
from .models import Account, Role, Tournament, AccountToTournament, Game

# Input Serializers
from .serializers import LoginSerializer, TournamentDetailsViewSerializer, AdminPanelAddUserSerializer
# Output Serializers
from .serializers import DashboardAdminTournamentsSerializer, DashboardTournamentsSerializer, TournamentSerializer, AccountBasicDetailsSerializer, YourRoleToTournamentSerializer, AdminPanelRolesSerializer


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            account = Account.objects.get(user=request.user)
            if account.role.name == 'admin':
                return True
        return False


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


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status=HTTP_200_OK)


class MeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        acc = Account.objects.get(user=request.user)
        acc_data = AccountBasicDetailsSerializer(acc).data
        return Response({'account': acc_data}, status=HTTP_200_OK)


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        acc = Account.objects.get(user=request.user)

        if acc.role.name == "player" or acc.role.name == "coordinator":
            try:
                tournaments = AccountToTournament.objects.filter(account=acc)
            except AccountToTournament.DoesNotExist:
                return Response({"tournaments": []})

            tournaments_data = DashboardTournamentsSerializer(tournaments, many=True).data
            return Response({"tournaments": tournaments_data})
        elif acc.role.name == "admin":
            try:
                tournaments = Tournament.objects.all()
            except Tournament.DoesNotExist:
                return Response({"tournaments": []})

            tournaments_data = DashboardAdminTournamentsSerializer(tournaments, many=True).data
            return Response({"tournaments": tournaments_data})


class ListTournamentsView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            tournaments = Tournament.objects.filter(public=True)
        except Tournament.DoesNotExist:
            return Response({"tournaments": []})

        tournaments_data = TournamentSerializer(tournaments, many=True).data
        return Response({"tournaments": tournaments_data})


class TournamentView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, tournament_uuid):
        try:
            tournament = Tournament.objects.get(uuid=tournament_uuid, public=True)
        except Tournament.DoesNotExist:
            return Response({"tournament": None})

        tournament_data = TournamentSerializer(tournament).data
        return Response({"tournament": tournament_data})


class TournamentDetailsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentDetailsViewSerializer

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        try:
            tournament = Tournament.objects.get(uuid=tournament_uuid)
        except Tournament.DoesNotExist:
            return Response({"tournament": None})

        if role == "player" or role == "coordinator":
            try:
                account_to_tournament = AccountToTournament.objects.get(account=acc, tournament=tournament)
            except AccountToTournament.DoesNotExist:
                return Response({"tournament": None})

            tournament_data = TournamentSerializer(tournament).data
            my_role = YourRoleToTournamentSerializer(account_to_tournament).data
            return Response({"tournament": tournament_data, "my_role": my_role})
        elif role == "admin":
            tournament_data = TournamentSerializer(tournament).data
            return Response({"tournament": tournament_data, "my_role": 'admin'})

        return Response({"tournament": None})


class AdminPanelAddUser(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminPanelAddUserSerializer

    def get(self, request):
        roles = Role.objects.all()
        roles_data = AdminPanelRolesSerializer(roles, many=True).data
        return Response({"roles": roles_data})

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')

        if not username or not password or not role or not first_name or not last_name or not email:
            return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(name=role)
        except Role.DoesNotExist:
            return Response({"error": "Invalid role"}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        except:
            return Response({"error": "Username already exists"}, status=HTTP_400_BAD_REQUEST)
        user.save()

        account = Account.objects.create(user=user, role=role)
        account.save()

        return Response({'success': True}, status=HTTP_200_OK)


