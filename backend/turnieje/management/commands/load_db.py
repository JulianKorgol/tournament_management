from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Loads example data to database'

    def handle(self, *args, **options):
        admin = User.objects.create_user('julian', '', '1234')
        admin.save()
        print('Data loaded successfully')
