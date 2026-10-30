import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_expense_tracker.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    username = 'admin'
    password = 'password123'
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, 'admin@example.com', password)
        print(f"Superuser '{username}' created with password '{password}'")
    else:
        print(f"User '{username}' already exists.")

if __name__ == '__main__':
    create_test_user()
