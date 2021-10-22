from django.urls import path
from django.conf.urls import url

'''import TaskList class from views.py into this urls.py file of the application'''
from . import views

'''
TaskList is a class in our views.py but our urls.py of our app cannot use class in here so we will have to modify
the code for the url from this 'example url =     path('add_todo/',views.add_todo, name="add_todo"),'
to this 'exaple url = path('', TaskList.as_view(), name='tasks'),'

view by default looks for pk value
path('task/<int:pk>/', TaskDetail.as_view(), name='tasks'),
'''

#here use a decorateor that will allow su to use pi calls to validate username
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
     #income page home page
     path('', views.index , name='income'),

     #CRUD links for income page
     path('add-income', views.add_income , name='add_income'),
     path('edit-income/<int:id>', views.income_edit , name='income_edit'),
     path('delete-income/<int:id>/', views.income_delete , name='income_delete'),
     #
     # #this url route is required by our searchIncome.js file in the static folder so that we can search for the income
     path('search-income', csrf_exempt(views.search_income) , name='search_income'),

     #this route will restrict un authorized users from viewing pages in the website
     path('login_required/', views.login_required_function , name='login_required_exp'),

     #this is url for the endpoint that handles the representation of expenses of last 1 month in form of a chart in expense summary page
     path('income_source_summary', views.income_source_summary, name='income_source_summary'),

     #url for expenses summary past 6 months summary_past_six_months
     path('summary_past_six_months', views.summary_past_six_months, name='summary_past_six_months'),

     #url for expenses summary past 6 months summary_past_twelve_months
     path('summary_past_twelve_months', views.summary_past_twelve_months, name='summary_past_twelve_months'),

     #this url will be rendered when we go in the expenses summary
     path('income_stats_view', views.stats_view, name='income_stats_view'),

     #urls related to expenses export functionality
     path('export_csv', views.export_csv, name='export_csv_income'),
     path('export_excel', views.export_excel, name='export_excel_income'),
]
