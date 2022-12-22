from rest_framework import serializers
from .models import Tournaments, AcoountToTournament


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class DashboardAdminTournamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournaments
        fields = ('name', 'start_date', 'end_date', 'public')


class DashboardTournamentsSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tournament.name')
    start_date = serializers.DateField(source='tournament.start_date')
    end_date = serializers.DateField(source='tournament.end_date')
    public = serializers.BooleanField(source='tournament.public')

    class Meta:
        model = AcoountToTournament
        fields = ('tournament_name', 'start_date', 'end_date', 'public', 'role')