from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Tournaments(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class AcoountToTournament(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + " " + self.tournament.name


class Matches(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='player2')
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tournament.name + " " + self.player1.user.username + " " + self.player2.user.username
