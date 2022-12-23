from rest_framework import serializers
from .models import Tournament, AccountToTournament, Account, Role


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class DashboardAdminTournamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'start_date', 'end_date', 'public', 'uuid')


class DashboardTournamentsSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tournament.name')
    start_date = serializers.DateField(source='tournament.start_date')
    end_date = serializers.DateField(source='tournament.end_date')
    public = serializers.BooleanField(source='tournament.public')

    class Meta:
        model = AccountToTournament
        fields = ('tournament_name', 'start_date', 'end_date', 'public', 'role')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'description', 'start_date', 'end_date', 'public', 'uuid')


class TournamentDetailsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('uuid',)


class AccountBasicDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    role = serializers.CharField(source='role.name')
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'role')


class YourRoleToTournamentSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')
    class Meta:
        model = AccountToTournament
        fields = ('role',)


class AdminPanelRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name',)


class AdminPanelAddUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()