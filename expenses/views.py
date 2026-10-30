from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, Budget, Category
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone

@login_required
def expense_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    expenses = Expense.objects.filter(user=request.user)
    
    if query:
        expenses = expenses.filter(Q(title__icontains=query) | Q(notes__icontains=query))
    if category_id:
        expenses = expenses.filter(category_id=category_id)
        
    categories = Category.objects.all()
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'categories': categories
    })

@login_required
def expense_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes')
        receipt = request.FILES.get('receipt')
        
        category = get_object_or_404(Category, id=category_id)
        
        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            date=date,
            payment_method=payment_method,
            notes=notes,
            receipt=receipt
        )
        messages.success(request, "Expense added successfully!")
        return redirect('expenses:list')
        
    categories = Category.objects.all()
    return render(request, 'expenses/expense_form.html', {
        'categories': categories,
        'today': timezone.now().date()
    })

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.category = get_object_or_404(Category, id=request.POST.get('category'))
        expense.date = request.POST.get('date')
        expense.payment_method = request.POST.get('payment_method')
        expense.notes = request.POST.get('notes')
        if request.FILES.get('receipt'):
            expense.receipt = request.FILES.get('receipt')
        
        expense.save()
        messages.success(request, "Expense updated successfully!")
        return redirect('expenses:list')
        
    categories = Category.objects.all()
    return render(request, 'expenses/expense_form.html', {
        'expense': expense, 
        'categories': categories,
        'today': timezone.now().date()
    })

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect('expenses:list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    
    # Enrich budgets with spending data
    for budget in budgets:
        spent = Expense.objects.filter(
            user=request.user,
            category=budget.category,
            date__month=budget.month,
            date__year=budget.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        budget.spent = float(spent)
        if budget.amount > 0:
            budget.percentage = min(100, (budget.spent / float(budget.amount)) * 100)
        else:
            budget.percentage = 0
            
    return render(request, 'expenses/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date') # Use this to extract month/year
        
        # Simple parsing or use current month if date is not provided correctly
        from datetime import datetime
        dt = datetime.strptime(date, '%Y-%m-%d')
        
        Budget.objects.update_or_create(
            user=request.user,
            category_id=category_id,
            month=dt.month,
            year=dt.year,
            defaults={'amount': amount}
        )
        messages.success(request, "Budget set successfully!")
        return redirect('expenses:budget_list')
        
    categories = Category.objects.all()
    return render(request, 'expenses/budget_form.html', {
        'categories': categories,
        'today': timezone.now().date()
    })
