from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser("ebadmin", "mancerung@gmail.com", "1112")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))