from django.shortcuts import render, redirect

#inorder to protect the expenses application home page from unauthorized acess we need this decorator
from django.contrib.auth.decorators import login_required

from . models import Source, UserIncome

from django.contrib import messages

from django.contrib.auth.models import User

#this paginator import will allow us to show 5 expenses per page in the main home page that shows all the expenses of the user
from django.core.paginator import Paginator

#to implement search in realtime we will import JSON
import json

#this will allow us to send in a json back
from django.http import JsonResponse, HttpResponse

#import the UserPreferences model from userPreferences application
from userpreferences.models import UserPreferences

#this will allow us to use date and time functions in our views.py
import datetime
#this module will help us to export our expenses in the csv format
import csv
import xlwt

#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def index(request):
    #get the category from the database
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user) #currently logged in user should only see the expenses that they created in this website

    #paginate the expenses table so it do not take to much space in the ui space in the home page
    #here we are providing the Paginator(the data that we want to paginate, number of data set per page in integers)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page') #this gonna be picking value of a page from the url and return it
    #now we need to construct a page object
    #now a page object represents the expenses we will se on those individual pages
    page_obj = Paginator.get_page(paginator,page_number)

    #query the database currency of the user
    #query the database currency of the user
    userPreferences_exists = UserPreferences.objects.filter(user=request.user).exists()
    if userPreferences_exists:
         currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = "NONE"

    stuff_for_frontend = {
          'income':income,
          'page_obj': page_obj,
          'currency':currency,
    }
    return render(request, 'income/index.html', stuff_for_frontend)

#here search income functrion will come
#this function will search expenses from the list of expenses
def search_income(request):
    if request.method == 'POST':
        #get everything that the user will be sending in the search form
        #so here we will get the JSON over the network so that we can search for expenses in realtime
        search_str = json.loads(request.body).get('searchText') #the user is sending in a json when searching for expenses in the search field
        #now whatever we are sending in the network we need to convert it into a python dictionary

        #now we will query our expenses model
        #amount__starts_with=search_str will allow us to search for expenses in the models database via amount attribute
        #here we will also restrict user from searching other's expenses
        #this will contain the query sets
        income = UserIncome.objects.filter(amount__icontains=search_str,
            owner=request.user) | UserIncome.objects.filter(date__icontains=search_str,
            owner=request.user) | UserIncome.objects.filter(description__icontains=search_str,
            owner=request.user) | UserIncome.objects.filter(source__icontains=search_str,
            owner=request.user)
        data = income.values()
        #since we are passing a list and not a dictionary this can fail to be serialize so pass safe = False
        return JsonResponse(list(data), safe=False)

#this fumction will handle the addition of new expense in our application
#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def add_income(request):
    #get the category from the database
    source = Source.objects.all()
    stuff_for_frontend = {
          'sources':source,
          'values':request.POST,
    }

    #check if the request is a get request
    if request.method == 'GET':
        return render(request, 'income/add_income.html',stuff_for_frontend)

    #check if it is a post request for amount
    if request.method == 'POST':
        #if the request is post then we can check for the amount
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html',stuff_for_frontend)

        #for description
        #if the request is post then we can check for the amount
        description = request.POST['description']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html',stuff_for_frontend)

        #category of expense
        source = request.POST['source']

        #date of expense
        income_date = request.POST['income_date']
        if not income_date:
            messages.error(request, 'date of income is required')
            return render(request, 'income/add_income.html',stuff_for_frontend)

        #if there are no errors that we've checked for then we can go ahead and save this from data to our database
        #get the owner of the expense the user who is logged in and is create an expense in the app
        user = request.user #this will return and give us the currently logged in user in our website
        UserIncome.objects.create(amount=amount, description=description, source=source, date=income_date, owner=user)
        messages.success(request, 'Income is saved successfully!')
        return redirect('income')

    return render(request, 'income/add_income.html',stuff_for_frontend)

#this function is going to handle the eiting of our exsisting expenses
#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def income_edit(request, id):
    #find the expense via id in the database so that the user can edit the expense
    income= UserIncome.objects.get(pk=id) #pk is an attribute that django sets up for every model

    #restrict other logged in users from seeing edit page of other users in this website
    if income.owner.id != request.user.id:
        messages.error(request, 'You cannot view what is not yours')
        return redirect('income')

    #get the category from the database
    source = Source.objects.all()
    stuff_for_frontend = {
         'incomes':income,
         'values':income,
         'sources':source,
    }
    if request.method=='GET':
        return render(request, 'income/edit_income.html',stuff_for_frontend)
    if request.method=='POST':
        #if the request is post then we can check for the amount
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html',stuff_for_frontend)

        #for description
        #if the request is post then we can check for the amount
        description = request.POST['description']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html',stuff_for_frontend)

        #category of expense
        source = request.POST['source']

        #date of expense
        income_date = request.POST['income_date']
        if not income_date:
            messages.error(request, 'date of income is required')
            return render(request, 'income/edit_income.html',stuff_for_frontend)

        #if there are no errors that we've checked for then we can go ahead and save this from data to our database
        #get the owner of the expense the user who is logged in and is update the expense that is already present in the app
        user = request.user #this will return and give us the currently logged in user in our website
        income.owner = user
        income.amount=amount
        income.description=description
        income.source=source
        income.date=income_date
        income.save()
        messages.success(request, 'income is updated successfully!')
        return redirect('income')
    return render(request, 'income/edit_income.html',stuff_for_frontend)

#this function is going to handle the deleting of our exsisting expenses
#login_required decorator will not allow any user that is not logged in this website
@login_required(login_url='login_required_exp')
def income_delete(request, id):
    #find the expense via id in the database so that the user can edit the expense
    income= UserIncome.objects.get(pk=id) #pk is an attribute that django sets up for every model
    data_for_front_end ={
        'income':income,
    }

    #restrict other logged in users from seeing edit page of other users in this website
    if income.owner.id != request.user.id:
        messages.error(request, 'You cannot view what is not yours')
        return redirect('income')

    if request.method == 'POST':
        income.delete() #delete the project from the database
        return redirect('income')
    return render(request, "income/delete_template.html", data_for_front_end)

#this function will prevent the user from viewing pages who is not logged in in this website
def login_required_function(request):
    return render(request, 'authentication/login_required.html')

#this function will sct as an endpoint for our javascript
#this is weponsible for feeding our charts the data which will be used to acreate an income chart for the past 6 months or past 1 month or pas week etc...
def income_source_summary(request): # this function is for income summary for past one month
    #first of all we need to know the date that it was 1 month ago
    #for us todo that import datetime
    #get the date which is today
    #for us to know what date it was 1 months ago we need to use time delta function
    #what timedelta does that it takes in the days
    todays_date = datetime.date.today()
    one_month_ago = todays_date - datetime.timedelta(days=30)
    #so here we are querying the expenses that has the date greater than or equal to one_month_ago date and date that is less thank or equal to todays_date
    #this will give us the expenses that is between the todays_date and one_month_ago dates from the database
    income = UserIncome.objects.filter(owner = request.user ,date__gte = one_month_ago, date__lte=todays_date)

    #now construct the final representation of the data that we are getting in
    finalrep = {}

    #get all the cataogries that exists in the database
    #I am going to create a helper function todo that
    #it will take in an expense and then it will return for me the catagory of that expense
    def get_source(income):
        return income.source

    #no that I have this helper function I am going to call this function for every expense that I have in the database when I am getting the data about expenses in the expense database
    #now the way map works is I am going to give irt a function here in this case it will be get_catagory and expenses
    #so map will be calling the get_catagory function for each expenses it will return a list that will contain catagories for each of the expenses
    #set will remove all the duplicates in this result returned by the map if any
    source_list = list(set(map(get_source, income)))

    def get_income_source_amount(source):
        amount=0
        filtered_by_source=income.filter(source=source)

        for item in filtered_by_source:
            amount+=item.amount
        return amount

    for x in income:
        for y in source_list:
            # [y] is the key for the finalrep dictionary
            # get_expense_catagory_amount(y) is a value
            finalrep[y]=get_income_source_amount(y)

    return JsonResponse({'income_source_data':finalrep}, safe=False)

#this function is for income summary for past 6 months
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
        income = UserIncome.objects.filter(owner = request.user ,date__gte = six_months_ago, date__lte=todays_date)

        #now construct the final representation of the data that we are getting in
        finalrep = {}

        #get all the cataogries that exists in the database
        #I am going to create a helper function todo that
        #it will take in an expense and then it will return for me the catagory of that expense
        def get_source(income):
            return income.source

        #no that I have this helper function I am going to call this function for every expense that I have in the database when I am getting the data about expenses in the expense database
        #now the way map works is I am going to give irt a function here in this case it will be get_catagory and expenses
        #so map will be calling the get_catagory function for each expenses it will return a list that will contain catagories for each of the expenses
        #set will remove all the duplicates in this result returned by the map if any
        source_list = list(set(map(get_source, income)))

        def get_income_source_amount(source):
            amount=0
            filtered_by_source=income.filter(source=source)

            for item in filtered_by_source:
                amount+=item.amount
            return amount

        for x in income:
            for y in source_list:
                # [y] is the key for the finalrep dictionary
                # get_expense_catagory_amount(y) is a value
                finalrep[y]=get_income_source_amount(y)

        return JsonResponse({'income_source_data':finalrep}, safe=False)

#this function is for income summary for past 12 months
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
        income = UserIncome.objects.filter(owner = request.user ,date__gte = twelve_months_ago, date__lte=todays_date)

        #now construct the final representation of the data that we are getting in
        finalrep = {}

        #get all the cataogries that exists in the database
        #I am going to create a helper function todo that
        #it will take in an expense and then it will return for me the catagory of that expense
        def get_source(income):
            return income.source

        #no that I have this helper function I am going to call this function for every expense that I have in the database when I am getting the data about expenses in the expense database
        #now the way map works is I am going to give irt a function here in this case it will be get_catagory and expenses
        #so map will be calling the get_catagory function for each expenses it will return a list that will contain catagories for each of the expenses
        #set will remove all the duplicates in this result returned by the map if any
        source_list = list(set(map(get_source, income)))

        def get_income_source_amount(source):
            amount=0
            filtered_by_source=income.filter(source=source)

            for item in filtered_by_source:
                amount+=item.amount
            return amount

        for x in income:
            for y in source_list:
                # [y] is the key for the finalrep dictionary
                # get_expense_catagory_amount(y) is a value
                finalrep[y]=get_income_source_amount(y)

        return JsonResponse({'income_source_data':finalrep}, safe=False)

#this function will render out the expenses summary page
@login_required(login_url='login_required_exp')
def stats_view(request):
    return render(request, 'income/stats.html')

#``````````````````````handeling expense export functionality STARTS HERE ````````````````````````````````````````````````````

#this function will handle the export of expense in csv format
def export_csv(request):
    #here we are gonna be using the python csv module
    #we need to create a response tha we will send to the user using Httpresponse class
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Income'+ str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Source','Date']) #this will set up the first row
    Income = UserIncome.objects.filter(owner=request.user)

    for income in Income:
        writer.writerow([income.amount,income.description,income.source,income.date])
    return response

#this function will handle the export of expense in xcel format
#inorder to do that we will be using xlwt
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Income'+ str(datetime.datetime.now())+'.xls'

    #import xlwt before writing the code below
    workbook_wb = xlwt.Workbook(encoding='utf-8')  #you can think of a workbook as an excel file itself
    #now we can start adding sheets to this file
    workbook_sheets = workbook_wb.add_sheet('Income') #here Expenses is the name of the sheet
    #now we can start andding rows to the sheets
    row_num=0 #make this variable bold because its gonna be the header in this excel sheet
    font_style = xlwt.XFStyle()
    #we want to make the first row bold
    font_style.font.bold=True

    #creating columns in the excel sheet
    columns = ['Amount','Description','Source','Date']
    #so now once we have the columns setup hence we can inert it in the row that we've created earlier
    for column_number in range(len(columns)):
        workbook_sheets.write(row_num,column_number, columns[column_number], font_style)#write the row number the column number, the actual content and the font configuration
    #reset the font style so that the header only keep the bold font style
    font_style=xlwt.XFStyle()

    #now create the dynamic rows for the expenses data in the excel sheet
    rows = UserIncome.objects.filter(owner=request.user).values_list('amount','description','source','date')
    #now that we have got our row we can add this row to our xcel sheet
    for row in rows:
        row_num+=1
        for column_number in range(len(row)):
            # typecast row[column_number] to string because it can cause rendering issues in the ms excel of this file if not done
            workbook_sheets.write(row_num,column_number, str(row[column_number]), font_style) #write the row number the column number, the actual content and the font configuration
    workbook_wb.save(response)
    return response

#``````````````````````handeling expense export functionality ENDS HERE ````````````````````````````````````````````````````
