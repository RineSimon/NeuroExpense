from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expense_list, name='list'),
    path('add/', views.expense_create, name='add'),
    path('edit/<int:pk>/', views.expense_update, name='edit'),
    path('delete/<int:pk>/', views.expense_delete, name='delete'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_create, name='budget_add'),
]
