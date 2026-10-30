from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from expenses.models import Expense, Category
from django.db.models import Sum, Avg
from django.utils import timezone
from django.contrib import messages
import json
from datetime import timedelta, datetime
import calendar

@login_required
def analytics_dashboard(request):
    if 'join_beta' in request.GET:
        messages.success(request, "Awesome! You've been added to the waitlist for Analytics 2.0.")
        return redirect('analytics:dashboard')

    user = request.user
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_elapsed = today.day
    
    # 1. Monthly Stats (Current Month)
    expenses_this_month = Expense.objects.filter(user=user, date__gte=first_day_of_month)
    total_this_month = expenses_this_month.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Average Daily (This Month)
    avg_daily = float(total_this_month) / days_elapsed if days_elapsed > 0 else 0
    
    # Predicted (This Month)
    predicted = avg_daily * days_in_month
    
    # 2. Highest Spending Category (This Month)
    top_cat = expenses_this_month.values('category__name').annotate(total=Sum('amount')).order_by('-total').first()
    
    # 3. Weekly Comparison
    # Start of this week (Monday)
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)
    
    this_week_total = Expense.objects.filter(user=user, date__gte=this_week_start, date__lte=today).aggregate(Sum('amount'))['amount__sum'] or 0
    last_week_total = Expense.objects.filter(user=user, date__gte=last_week_start, date__lte=last_week_end).aggregate(Sum('amount'))['amount__sum'] or 0
    
    week_diff_percent = 0
    if last_week_total > 0:
        week_diff_percent = ((float(this_week_total) - float(last_week_total)) / float(last_week_total)) * 100
    elif this_week_total > 0:
        week_diff_percent = 100 # If nothing spent last week, but spent this week

    context = {
        'avg_daily': avg_daily,
        'predicted': predicted,
        'top_cat': top_cat,
        'week_diff_percent': week_diff_percent,
        'this_week_total': this_week_total,
        'total_this_month': total_this_month,
    }
    
    return render(request, 'analytics/analytics.html', context)
