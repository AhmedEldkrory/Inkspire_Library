from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from online_library.models import User

class Command(BaseCommand):
    help = 'Lists all users and resets their passwords to 1230'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        if not users:
            self.stdout.write(self.style.WARNING("No users found in the database."))
            return
        
        self.stdout.write(self.style.SUCCESS("\n=== All Users ==="))
        self.stdout.write(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Role':<10} {'Is Staff':<10} {'Is Superuser':<12}")
        self.stdout.write("-" * 90)
        
        for user in users:
            self.stdout.write(f"{user.id:<5} {user.username:<20} {user.email:<30} {user.role:<10} {str(user.is_staff):<10} {str(user.is_superuser):<12}")
        
        # Reset all passwords
        new_password = '1230'
        hashed_password = make_password(new_password)
        
        count = 0
        for user in users:
            user.password = hashed_password
            user.save()
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully reset passwords for {count} users to '{new_password}'"))
