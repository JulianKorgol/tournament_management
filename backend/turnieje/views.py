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
import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Account, Role, Tournament, AccountToTournament, Game

# Input Serializers
from .serializers import LoginSerializer, TournamentDetailsViewSerializer, AdminPanelAddUserSerializer, AddTournamentSerializer, ManageTournamentSerializer, AddPeopleToTournamentSerializer, RemovePeopleFromTournamentSerializer, AddScoreSerializer, RemoveScoreSerializer
# Output Serializers
from .serializers import DashboardAdminTournamentsSerializer, DashboardTournamentsSerializer, TournamentSerializer, AccountBasicDetailsSerializer, YourRoleToTournamentSerializer, AdminPanelRolesSerializer, GameSerializer, AccountToTournamentSerializer


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
        return Response(None, status=HTTP_400_BAD_REQUEST)


class ListTournamentsView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            tournaments = Tournament.objects.filter(public=True)
        except Tournament.DoesNotExist:
            return Response({"tournaments": []}, status=HTTP_200_OK)

        tournaments_data = TournamentSerializer(tournaments, many=True).data
        return Response({"tournaments": tournaments_data})


class TournamentView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, tournament_uuid):
        try:
            tournament = Tournament.objects.get(uuid=tournament_uuid, public=True)
        except Tournament.DoesNotExist:
            return Response({"tournament": None}, status=HTTP_404_NOT_FOUND)

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

        return Response({"tournament": None}, status=HTTP_400_BAD_REQUEST)


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


class AddTournament(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddTournamentSerializer

    def post(self, request):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            name = request.data.get('name')
            description = request.data.get('description')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if not name or not description or not start_date or not end_date:
                return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)

            tournament = Tournament.objects.create(name=name, description=description, start_date=start_date, end_date=end_date)
            tournament.save()

            return Response({'success': True, 'uuid': tournament.uuid}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class ManageTournament(generics.GenericAPIView):
    persmission_classes = [IsAuthenticated]
    serializer_class = ManageTournamentSerializer

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"tournament": None})

            tournament_data = TournamentSerializer(tournament).data
            return Response({"tournament": tournament_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)

    def post(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            name = request.data.get('name')
            description = request.data.get('description')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            public = request.data.get('public')
            uuid = tournament_uuid

            if not uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=uuid)
            except Tournament.DoesNotExist:
                return Response({"tournament": None})

            try:
                if name:
                    tournament.name = name
                if description:
                    tournament.description = description
                if start_date:
                    tournament.start_date = start_date
                if end_date:
                    tournament.end_date = end_date
                if public:
                    tournament.public = public
            except:
                return Response({"error": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

            tournament.save()

            return Response({"success": True}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class AddPeopleToTournament(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddPeopleToTournamentSerializer

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            accounts = Account.objects.all()
            accounts_data = AccountToTournamentSerializer(accounts, many=True).data
            return Response({"accounts": accounts_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)

    def post(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            username = request.data.get('username')
            role = request.data.get('role')

            if not tournament_uuid or not username or not role:
                return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                role = Role.objects.get(name=role)
            except Role.DoesNotExist:
                return Response({"error": "Invalid role"}, status=HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "Invalid user"}, status=HTTP_400_BAD_REQUEST)

            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                return Response({"error": "Invalid user"}, status=HTTP_400_BAD_REQUEST)

            try:
                account_to_tournament = AccountToTournament.objects.get(account=account, tournament=tournament)
            except AccountToTournament.DoesNotExist:
                account_to_tournament = AccountToTournament.objects.create(account=account, tournament=tournament, role=role)
                account_to_tournament.save()
                return Response({"success": True}, status=HTTP_200_OK)
            return Response({"error": "User already in tournament"}, status=HTTP_400_BAD_REQUEST)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class RemovePeopleFromTournament(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemovePeopleFromTournamentSerializer

    def post(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            username = request.data.get('username')

            if not tournament_uuid or not username:
                return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "Invalid user"}, status=HTTP_400_BAD_REQUEST)

            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                return Response({"error": "Invalid user"}, status=HTTP_400_BAD_REQUEST)

            try:
                account_to_tournament = AccountToTournament.objects.get(account=account, tournament=tournament)
            except AccountToTournament.DoesNotExist:
                return Response({"error": "User not in tournament"}, status=HTTP_400_BAD_REQUEST)

            account_to_tournament.delete()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class GenerateGames(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            accounts = AccountToTournament.objects.filter(tournament=tournament)
            if len(accounts) < 2:
                return Response({"error": "Not enough players"}, status=HTTP_400_BAD_REQUEST)

            games = []
            for i in range(len(accounts)):
                for j in range(len(accounts)):
                    if i != j:
                        try:
                            game = Game.objects.get(player1=accounts[i].account, player2=accounts[j].account, tournament=tournament)
                        except Game.DoesNotExist:
                            try:
                                game = Game.objects.get(player1=accounts[j].account, player2=accounts[i].account, tournament=tournament)
                            except Game.DoesNotExist:
                                games.append(Game.objects.create(player1=accounts[i].account, player2=accounts[j].account, tournament=tournament))

            for game in games:
                game.save()

            return Response({"success": True}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class GetGames(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(tournament=tournament)
            data = GameSerializer(games, many=True).data

            return Response({"games": data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class GetNotPlayedGames(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(tournament=tournament, player1_score=None, player2_score=None)
            data = GameSerializer(games, many=True).data

            return Response({"games": data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class AddScore(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddScoreSerializer

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            accounts = AccountToTournament.objects.filter(tournament=tournament, role='player')
            if len(accounts) < 2:
                return Response({"error": "Not enough players"}, status=HTTP_400_BAD_REQUEST)

            accounts_data = AccountToTournamentSerializer(accounts, many=True).data
            return Response({"players": accounts_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)

    def post(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            player1_username = request.data.get('player1')
            player2_username = request.data.get('player2')
            player1_score = request.data.get('player1_score')
            player2_score = request.data.get('player2_score')

            if not player1_username or not player2_username or not player1_score or not player2_score:
                return Response({"error": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

            try:
                player1 = Account.objects.get(username=player1_username)
            except Account.DoesNotExist:
                return Response({"error": "Invalid player1"}, status=HTTP_400_BAD_REQUEST)

            try:
                player2 = Account.objects.get(username=player2_username)
            except Account.DoesNotExist:
                return Response({"error": "Invalid player2"}, status=HTTP_400_BAD_REQUEST)

            try:
                game = Game.objects.get(player1=player1, player2=player2, tournament=tournament)
            except Game.DoesNotExist:
                return Response({"error": "Game does not exist"}, status=HTTP_400_BAD_REQUEST)

            game.player1_score = player1_score
            game.player2_score = player2_score
            game.date = datetime.now()
            game.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class ModifyScore(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddScoreSerializer

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(tournament=tournament)
            if len(games) == 0:
                return Response({"error": "No games to modify"}, status=HTTP_400_BAD_REQUEST)

            games_data = GameSerializer(games, many=True).data
            return Response({"games": games_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)

    def post(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            player1_username = request.data.get('player1')
            player2_username = request.data.get('player2')
            player1_score = request.data.get('player1_score')
            player2_score = request.data.get('player2_score')

            if not player1_username or not player2_username or not player1_score or not player2_score:
                return Response({"error": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

            try:
                player1 = Account.objects.get(username=player1_username)
            except Account.DoesNotExist:
                return Response({"error": "Invalid player1"}, status=HTTP_400_BAD_REQUEST)

            try:
                player2 = Account.objects.get(username=player2_username)
            except Account.DoesNotExist:
                return Response({"error": "Invalid player2"}, status=HTTP_400_BAD_REQUEST)

            try:
                game = Game.objects.get(player1=player1, player2=player2, tournament=tournament)
            except Game.DoesNotExist:
                return Response({"error": "Game does not exist"}, status=HTTP_400_BAD_REQUEST)

            if player1_score:
                game.player1_score = player1_score
            if player2_score:
                game.player2_score = player2_score
            game.date = datetime.now()
            game.save()
            return Response({"success": True}, status=HTTP_200_OK)


class RemoveScore(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveScoreSerializer

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(tournament=tournament)
            if len(games) == 0:
                return Response({"error": "No games to remove"}, status=HTTP_400_BAD_REQUEST)

            games_data = GameSerializer(games, many=True).data
            return Response({"games": games_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)

    def post(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            player1_username = request.data.get('player1')
            player2_username = request.data.get('player2')

            if not player1_username or not player2_username:
                return Response({"error": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

            try:
                player1 = Account.objects.get(username=player1_username)
            except Account.DoesNotExist:
                return Response({"error": "Invalid player1"}, status=HTTP_400_BAD_REQUEST)

            try:
                player2 = Account.objects.get(username=player2_username)
            except Account.DoesNotExist:
                return Response({"error": "Invalid player2"}, status=HTTP_400_BAD_REQUEST)

            try:
                game = Game.objects.get(player1=player1, player2=player2, tournament=tournament)
            except Game.DoesNotExist:
                return Response({"error": "Game does not exist"}, status=HTTP_400_BAD_REQUEST)

            game.player1_score = None
            game.player2_score = None
            game.date = datetime.now()
            game.save()
            return Response({"success": True}, status=HTTP_200_OK)


class MyGames(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'player':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(Q(player1=acc) | Q(player2=acc), tournament=tournament)
            if len(games) == 0:
                return Response({"error": "You have no games"}, status=HTTP_400_BAD_REQUEST)

            games_data = GameSerializer(games, many=True).data
            return Response({"games": games_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)


class TournamentMatches(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_uuid):
        acc = Account.objects.get(user=request.user)
        role = acc.role.name

        if role == 'player':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(Q(player1=acc) | Q(player2=acc), tournament=tournament)
            if len(games) == 0:
                return Response({"error": "You have no games"}, status=HTTP_200_OK)

            games_data = GameSerializer(games, many=True).data
            return Response({"games": games_data}, status=HTTP_200_OK)
        elif role == 'admin' or role == 'coordinator':
            if not tournament_uuid:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            try:
                tournament = Tournament.objects.get(uuid=tournament_uuid)
            except Tournament.DoesNotExist:
                return Response({"error": "Invalid tournament"}, status=HTTP_400_BAD_REQUEST)

            games = Game.objects.filter(tournament=tournament)
            if len(games) == 0:
                return Response({"error": "No games to show"}, status=HTTP_200_OK)

            games_data = GameSerializer(games, many=True).data
            return Response({"games": games_data}, status=HTTP_200_OK)
        return Response(None, status=HTTP_400_BAD_REQUEST)
