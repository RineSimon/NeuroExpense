import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_expense_tracker.settings')
django.setup()

from expenses.models import Category

def populate_categories():
    categories = [
        ('Food', 'utensils', '#ef4444'),
        ('Shopping', 'shopping-bag', '#ec4899'),
        ('Transport', 'car', '#3b82f6'),
        ('Bills', 'credit-card', '#f59e0b'),
        ('Entertainment', 'tv', '#8b5cf6'),
        ('Health', 'heart', '#10b981'),
        ('Education', 'graduation-cap', '#6366f1'),
        ('Investment', 'trending-up', '#059669'),
        ('Other', 'box', '#6b7280'),
    ]

    for name, icon, color in categories:
        Category.objects.get_or_create(name=name, defaults={'icon': icon, 'color': color})
    print("Categories populated successfully!")

if __name__ == '__main__':
    populate_categories()
