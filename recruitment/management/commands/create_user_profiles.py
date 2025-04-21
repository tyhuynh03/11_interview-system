from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recruitment.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(profile__isnull=True)
        count = 0
        
        for user in users:
            user_type = 'admin' if user.is_superuser else 'candidate'
            UserProfile.objects.create(user=user, user_type=user_type)
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} user profiles'))