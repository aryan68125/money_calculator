from django.shortcuts import render, redirect

#inorder to protect the expenses application home page from unauthorized acess we need this decorator
from django.contrib.auth.decorators import login_required

from . models import Category, Expense

from django.contrib import messages

from django.contrib.auth.models import User

#this paginator import will allow us to show 5 expenses per page in the main home page that shows all the expenses of the user
from django.core.paginator import Paginator

#to implement search in realtime we will import JSON
import json

#this will allow us to send in a json back
from django.http import JsonResponse

#import the UserPreferences model from userPreferences application
from userpreferences.models import UserPreferences

#this will allow us to use date and time functions in our views.py
import datetime

#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def index(request):
    #get the category from the database
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user) #currently logged in user should only see the expenses that they created in this website

    #paginate the expenses table so it do not take to much space in the ui space in the home page
    #here we are providing the Paginator(the data that we want to paginate, number of data set per page in integers)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page') #this gonna be picking value of a page from the url and return it
    #now we need to construct a page object
    #now a page object represents the expenses we will se on those individual pages
    page_obj = Paginator.get_page(paginator,page_number)

    #query the database currency of the user
    currency = UserPreferences.objects.get(user=request.user).currency

    stuff_for_frontend = {
          'expenses':expenses,
          'page_obj': page_obj,
          'currency':currency,
    }
    return render(request, 'expenses/index.html', stuff_for_frontend)

#this function will search expenses from the list of expenses
def search_expenses(request):
    if request.method == 'POST':
        #get everything that the user will be sending in the search form
        #so here we will get the JSON over the network so that we can search for expenses in realtime
        search_str = json.loads(request.body).get('searchText') #the user is sending in a json when searching for expenses in the search field
        #now whatever we are sending in the network we need to convert it into a python dictionary

        #now we will query our expenses model
        #amount__starts_with=search_str will allow us to search for expenses in the models database via amount attribute
        #here we will also restrict user from searching other's expenses
        #this will contain the query sets
        expenses = Expense.objects.filter(amount__icontains=search_str,
            owner=request.user) | Expense.objects.filter(date__icontains=search_str,
            owner=request.user) | Expense.objects.filter(description__icontains=search_str,
            owner=request.user) | Expense.objects.filter(category__icontains=search_str,
            owner=request.user)
        data = expenses.values()
        #since we are passing a list and not a dictionary this can fail to be serialize so pass safe = False
        return JsonResponse(list(data), safe=False)

#this fumction will handle the addition of new expense in our application
#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def add_expense(request):
    #get the category from the database
    categories = Category.objects.all()
    stuff_for_frontend = {
          'categories':categories,
          'values':request.POST,
    }

    #check if the request is a get request
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html',stuff_for_frontend)

    #check if it is a post request for amount
    if request.method == 'POST':
        #if the request is post then we can check for the amount
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html',stuff_for_frontend)

        #for description
        #if the request is post then we can check for the amount
        description = request.POST['description']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html',stuff_for_frontend)

        #category of expense
        category = request.POST['category']

        #date of expense
        expense_date = request.POST['expense_date']
        if not expense_date:
            messages.error(request, 'date of expense is required')
            return render(request, 'expenses/add_expense.html',stuff_for_frontend)

        #if there are no errors that we've checked for then we can go ahead and save this from data to our database
        #get the owner of the expense the user who is logged in and is create an expense in the app
        user = request.user #this will return and give us the currently logged in user in our website
        Expense.objects.create(amount=amount, description=description, category=category, date=expense_date, owner=user)
        messages.success(request, 'Expense is saved successfully!')
        return redirect('expenses')

    return render(request, 'expenses/add_expense.html',stuff_for_frontend)

#this function is going to handle the eiting of our exsisting expenses
#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def expense_edit(request, id):
    #find the expense via id in the database so that the user can edit the expense
    expense= Expense.objects.get(pk=id) #pk is an attribute that django sets up for every model

    #restrict other logged in users from seeing edit page of other users in this website
    if expense.owner.id != request.user.id:
        messages.error(request, 'You cannot view what is not yours')
        return redirect('expenses')

    #get the category from the database
    categories = Category.objects.all()
    stuff_for_frontend = {
         'expense':expense,
         'values':expense,
         'categories':categories,
    }
    if request.method=='GET':
        return render(request, 'expenses/edit-expense.html',stuff_for_frontend)
    if request.method=='POST':
        #if the request is post then we can check for the amount
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html',stuff_for_frontend)

        #for description
        #if the request is post then we can check for the amount
        description = request.POST['description']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html',stuff_for_frontend)

        #category of expense
        category = request.POST['category']

        #date of expense
        expense_date = request.POST['expense_date']
        if not expense_date:
            messages.error(request, 'date of expense is required')
            return render(request, 'expenses/edit-expense.html',stuff_for_frontend)

        #if there are no errors that we've checked for then we can go ahead and save this from data to our database
        #get the owner of the expense the user who is logged in and is update the expense that is already present in the app
        user = request.user #this will return and give us the currently logged in user in our website
        expense.owner = user
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=expense_date
        expense.save()
        messages.success(request, 'Expense is updated successfully!')
        return redirect('expenses')
    return render(request, 'expenses/edit-expense.html',stuff_for_frontend)

#this function is going to handle the deleting of our exsisting expenses
#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def expense_delete(request, id):
    #find the expense via id in the database so that the user can edit the expense
    expense= Expense.objects.get(pk=id) #pk is an attribute that django sets up for every model
    data_for_front_end ={
        'expense':expense,
    }

    #restrict other logged in users from seeing edit page of other users in this website
    if expense.owner.id != request.user.id:
        messages.error(request, 'You cannot view what is not yours')
        return redirect('expenses')

    if request.method == 'POST':
        expense.delete() #delete the project from the database
        return redirect('expenses')
    return render(request, "expenses/delete_template.html", data_for_front_end)

def login_required_function(request):
    return render(request, 'authentication/login_required.html')

#this function will sct as an endpoint for our javascript
#this is weponsible for feeding our charts the data which will be used to acreate an expense chart for the past 6 months or past 1 month or pas week etc...
def expense_catagory_summary(request): # this function is for expenses summary for past one month
    #first of all we need to know the date that it was 1 month ago
    #for us todo that import datetime
    #get the date which is today
    #for us to know what date it was 1 months ago we need to use time delta function
    #what timedelta does that it takes in the days
    todays_date = datetime.date.today()
    one_month_ago = todays_date - datetime.timedelta(days=30)
    #so here we are querying the expenses that has the date greater than or equal to one_month_ago date and date that is less thank or equal to todays_date
    #this will give us the expenses that is between the todays_date and one_month_ago dates from the database
    expenses = Expense.objects.filter(owner = request.user ,date__gte = one_month_ago, date__lte=todays_date)

    #now construct the final representation of the data that we are getting in
    finalrep = {}

    #get all the cataogries that exists in the database
    #I am going to create a helper function todo that
    #it will take in an expense and then it will return for me the catagory of that expense
    def get_catagory(expense):
        return expense.category

    #no that I have this helper function I am going to call this function for every expense that I have in the database when I am getting the data about expenses in the expense database
    #now the way map works is I am going to give irt a function here in this case it will be get_catagory and expenses
    #so map will be calling the get_catagory function for each expenses it will return a list that will contain catagories for each of the expenses
    #set will remove all the duplicates in this result returned by the map if any
    catagory_list = list(set(map(get_catagory, expenses)))

    def get_expense_catagory_amount(category):
        amount=0
        filtered_by_catagory=expenses.filter(category=category)

        for item in filtered_by_catagory:
            amount+=item.amount
        return amount

    for x in expenses:
        for y in catagory_list:
            # [y] is the key for the finalrep dictionary
            # get_expense_catagory_amount(y) is a value
            finalrep[y]=get_expense_catagory_amount(y)

    return JsonResponse({'expense_catagory_data':finalrep}, safe=False)

#this function is for expenses summary for past 6 months
def summary_past_six_months(request):
        #first of all we need to know the date that it was 1 month ago
        #for us todo that import datetime
        #get the date which is today
        #for us to know what date it was 1 months ago we need to use time delta function
        #what timedelta does that it takes in the days
        todays_date = datetime.date.today()
        six_months_ago = todays_date - datetime.timedelta(days=180)
        #so here we are querying the expenses that has the date greater than or equal to one_month_ago date and date that is less thank or equal to todays_date
        #this will give us the expenses that is between the todays_date and one_month_ago dates from the database
        expenses = Expense.objects.filter(owner = request.user ,date__gte = six_months_ago, date__lte=todays_date)

        #now construct the final representation of the data that we are getting in
        finalrep = {}

        #get all the cataogries that exists in the database
        #I am going to create a helper function todo that
        #it will take in an expense and then it will return for me the catagory of that expense
        def get_catagory(expense):
            return expense.category

        #no that I have this helper function I am going to call this function for every expense that I have in the database when I am getting the data about expenses in the expense database
        #now the way map works is I am going to give irt a function here in this case it will be get_catagory and expenses
        #so map will be calling the get_catagory function for each expenses it will return a list that will contain catagories for each of the expenses
        #set will remove all the duplicates in this result returned by the map if any
        catagory_list = list(set(map(get_catagory, expenses)))
        def get_expense_catagory_amount(category):
            amount=0
            filtered_by_catagory=expenses.filter(category=category)

            for item in filtered_by_catagory:
                amount+=item.amount
            return amount

        for x in expenses:
            for y in catagory_list:
                # [y] is the key for the finalrep dictionary
                # get_expense_catagory_amount(y) is a value
                finalrep[y]=get_expense_catagory_amount(y)

        return JsonResponse({'expense_catagory_data':finalrep}, safe=False)

#this function is for expenses summary for past 12 months
def summary_past_twelve_months(request):
        #first of all we need to know the date that it was 1 month ago
        #for us todo that import datetime
        #get the date which is today
        #for us to know what date it was 1 months ago we need to use time delta function
        #what timedelta does that it takes in the days
        todays_date = datetime.date.today()
        twelve_months_ago = todays_date - datetime.timedelta(days=360)
        #so here we are querying the expenses that has the date greater than or equal to one_month_ago date and date that is less thank or equal to todays_date
        #this will give us the expenses that is between the todays_date and one_month_ago dates from the database
        expenses = Expense.objects.filter(owner = request.user ,date__gte = twelve_months_ago, date__lte=todays_date)

        #now construct the final representation of the data that we are getting in
        finalrep = {}

        #get all the cataogries that exists in the database
        #I am going to create a helper function todo that
        #it will take in an expense and then it will return for me the catagory of that expense
        def get_catagory(expense):
            return expense.category

        #no that I have this helper function I am going to call this function for every expense that I have in the database when I am getting the data about expenses in the expense database
        #now the way map works is I am going to give irt a function here in this case it will be get_catagory and expenses
        #so map will be calling the get_catagory function for each expenses it will return a list that will contain catagories for each of the expenses
        #set will remove all the duplicates in this result returned by the map if any
        catagory_list = list(set(map(get_catagory, expenses)))

        def get_expense_catagory_amount(category):
            amount=0
            filtered_by_catagory=expenses.filter(category=category)

            for item in filtered_by_catagory:
                amount+=item.amount
            return amount

        for x in expenses:
            for y in catagory_list:
                # [y] is the key for the finalrep dictionary
                # get_expense_catagory_amount(y) is a value
                finalrep[y]=get_expense_catagory_amount(y)

        return JsonResponse({'expense_catagory_data':finalrep}, safe=False)

#this function will render out the expenses summary page
def stats_view(request):
    return render(request, 'expenses/stats.html')
