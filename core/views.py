from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from expenses.models import Expense, Budget, Category
from django.db.models import Sum
from django.utils import timezone
import json
from datetime import timedelta

def landing(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/landing.html')

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    
    # Monthly Total
    monthly_expenses = Expense.objects.filter(
        user=user, 
        date__gte=first_day_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Daily Spending
    daily_expenses = Expense.objects.filter(
        user=user, 
        date=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Remaining Budget
    total_budget = Budget.objects.filter(
        user=user, 
        month=today.month, 
        year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    remaining_budget = total_budget - monthly_expenses
    
    # Recent Transactions
    recent_transactions = Expense.objects.filter(user=user).order_by('-date', '-created_at')[:5]
    
    # Chart Data (Last 7 days)
    chart_days = []
    chart_amounts = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        amount = Expense.objects.filter(user=user, date=day).aggregate(Sum('amount'))['amount__sum'] or 0
        chart_days.append(day.strftime('%a'))
        chart_amounts.append(float(amount))
        
    # Category breakdown for Pie Chart
    category_data = []
    categories = Category.objects.filter(expenses__user=user, expenses__date__gte=first_day_of_month).distinct()
    for cat in categories:
        amount = Expense.objects.filter(user=user, category=cat, date__gte=first_day_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
        category_data.append({
            'name': cat.name,
            'amount': float(amount),
            'color': cat.color
        })
    # Top spending category
    top_cat_obj = Expense.objects.filter(user=user, date__gte=first_day_of_month).values('category__name').annotate(total=Sum('amount')).order_by('-total').first()
    top_spending_category = top_cat_obj['category__name'] if top_cat_obj else "None"

    context = {
        'monthly_expenses': monthly_expenses,
        'daily_expenses': daily_expenses,
        'remaining_budget': remaining_budget,
        'total_budget': total_budget,
        'recent_transactions': recent_transactions,
        'chart_days': json.dumps(chart_days),
        'chart_amounts': json.dumps(chart_amounts),
        'category_data_json': json.dumps(category_data),
        'top_spending_category': top_spending_category,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def settings_view(request):
    if request.method == 'POST':
        # Handle settings update
        profile = request.user.profile
        profile.currency = request.POST.get('currency', profile.currency)
        profile.dark_mode = 'dark_mode' in request.POST
        profile.save()
        return redirect('core:settings')
        
    return render(request, 'core/settings.html')
