from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from turnieje.models import Role, Account, Tournament, AccountToTournament, Game


class Command(BaseCommand):
    help = 'Loads example data to database'

    def handle(self, *args, **options):
        player_role = Role.objects.create(name='player')
        coordinator_role = Role.objects.create(name='coordinator')
        admin_role = Role.objects.create(name='admin')
        player_role.save()
        coordinator_role.save()
        admin_role.save()

        julian = User.objects.create_user('julian', '', '1234', first_name='Jan', last_name='Kowalski')
        julian.save()
        julian_admin = Account.objects.create(user=julian, role=admin_role)
        julian_admin.save()

        usertest = User.objects.create_user('usertest', '', '1234', first_name='Przemysław', last_name='Politański')
        usertest.save()
        usertest_player = Account.objects.create(user=usertest, role=player_role)
        usertest_player.save()

        usertest2 = User.objects.create_user('usertest2', '', '1234', first_name='Marcin', last_name='Straszewski')
        usertest2.save()
        usertest2_player = Account.objects.create(user=usertest2, role=player_role)
        usertest2_player.save()

        usertest3 = User.objects.create_user('usertest3', '', '1234', first_name='Stanisław', last_name='Niedzielski')
        usertest3.save()
        usertest3_player = Account.objects.create(user=usertest3, role=player_role)
        usertest3_player.save()

        usertest4 = User.objects.create_user('usertest4', '', '1234', first_name='Jack', last_name='Sparrow')
        usertest4.save()
        usertest4_player = Account.objects.create(user=usertest4, role=player_role)
        usertest4_player.save()

        usertest_cord = User.objects.create_user('testcoordinator', '', '1234', first_name='Jan', last_name='Swierczek')
        usertest_cord.save()
        usertest_coordinator = Account.objects.create(user=usertest_cord, role=coordinator_role)
        usertest_coordinator.save()

        tournament_public = Tournament.objects.create(name='Turniej publiczny', description='Opis turnieju publicznego', start_date='2020-01-01', end_date='2020-01-02', public=True)
        tournament_public.save()

        tournament_private = Tournament.objects.create(name='Turniej prywatny', description='Opis turnieju prywatnego', start_date='2020-01-01', end_date='2020-01-02', public=False)
        tournament_private.save()

        print('Data loaded successfully')
