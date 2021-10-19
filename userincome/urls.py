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
]
