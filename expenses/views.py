from django.shortcuts import render, redirect

#inorder to protect the expenses application home page from unauthorized acess we need this decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='authentication/login')
def index(request):
    return render(request, 'expenses/index.html')

#this fumction will handle the addition of new expense in our application
def add_expense(request):
    return render(request, 'expenses/add_expense.html')
