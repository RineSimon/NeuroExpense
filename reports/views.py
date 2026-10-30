import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

@login_required
def reports_home(request):
    return render(request, 'reports/reports.html')

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Category', 'Date', 'Payment Method', 'Notes'])
    
    expenses = Expense.objects.filter(user=request.user)
    for expense in expenses:
        writer.writerow([
            expense.title, 
            expense.amount, 
            expense.category.name if expense.category else 'N/A', 
            expense.date, 
            expense.get_payment_method_display(), 
            expense.notes
        ])
        
    return response

@login_required
def export_pdf(request):
    expenses = Expense.objects.filter(user=request.user)
    template_path = 'reports/pdf_template.html'
    context = {'expenses': expenses, 'user': request.user}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expense_report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
