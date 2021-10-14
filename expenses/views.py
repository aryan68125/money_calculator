from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'expenses/index.html')

#this fumction will handle the addition of new expense in our application
def add_expense(request):
    return render(request, 'expenses/add_expense.html')
