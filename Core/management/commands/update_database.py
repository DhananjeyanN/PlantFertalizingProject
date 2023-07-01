from django.core.management.base import BaseCommand

from Core.models import Plant


class Command(BaseCommand):
    help = 'update_database'

    def handle(self, *args, **kwargs):
        print('Plant!!!')
        #logic to update database
        # Plant.update_all()