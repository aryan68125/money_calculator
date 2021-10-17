from django.urls import path
from django.conf.urls import url

'''import TaskList class from views.py into this urls.py file of the application'''
from . import views

'''we can actually use the views directly
    path('logout/', LogoutView.as_view(next_page = 'login' ), name='logout'), will use the LogoutView directly
    next_page = 'login' means once we press login button in pur front end it should send the user back to the login page
'''
from django.contrib.auth.views import LogoutView

'''
TaskList is a class in our views.py but our urls.py of our app cannot use class in here so we will have to modify
the code for the url from this 'example url =     path('add_todo/',views.add_todo, name="add_todo"),'
to this 'exaple url = path('', TaskList.as_view(), name='tasks'),'

view by default looks for pk value
path('task/<int:pk>/', TaskDetail.as_view(), name='tasks'),
'''
urlpatterns = [

    path('', views.index , name='expenses'),
    path('add-expense/', views.add_expense , name='add-expense'),
    path('edit-expense/<int:id>', views.expense_edit , name='expense_edit'),
    path('delete-expense/<int:id>/', views.expense_delete , name='expense_delete'),

    #this route will restrict un authorized users from viewing pages in the website
    path('login_required/', views.login_required_function , name='login_required_exp'),
]
