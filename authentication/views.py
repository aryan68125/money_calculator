from django.shortcuts import render
from django.views import View

#imports related to live username and email validation in the registration form
#to work with json we need to import json
import json
from django.http import JsonResponse

#import User auth model from django
from django.contrib.auth.models import User

#import the validate-email module in this view
from validate_email import validate_email

# Create your views here.
#this class will handle the registration of the users
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

#JSON allows us to communicate with our font end
#by default server will return a 200ok json response which is not ideal
#this class will validate username entered by the user in the register.html form in realtime
class UsernameValidationView(View):
    def post(self, request):
        #now we will get trhe username that the user has entered already in the form from the front-end
        #json.loads() the loads will take in data infor of json and convert it in to python dictionary
        data = json.loads(request.body)
        #now we can pick the username from data variable
        #the data variable will contain everything
        username = data['username']

        #checking if the username is alphanumeric or not
        if not str(username).isalnum():
            stuff_for_frontend = {
                'username_error': 'username should only contain alphanumeric characters'
            }
            return JsonResponse(stuff_for_frontend, status = 400)

        #now chencking if the username is already taken or not
        #or in other words if the username is already there in the database or not
        #User.objects.filter(username=username).exists() this will return a true or false depending on wheather the username is already there in the database or not
        if User.objects.filter(username=username).exists():
            stuff_for_frontend = {
                'username_error': 'username taken'
            }
            return JsonResponse(stuff_for_frontend, status = 409) #409 means that this resource is conflicting with the resource which is already present in the database

        #if every thing is correct then return username valid json response to the front-end
        stuff_for_frontend={
            'username_valid':True
        }

        return JsonResponse(stuff_for_frontend)

#this class will validate email entered by the user in the register.html form in realtime
class EmailValidationView(View):
    def post(self, request):
        #now we will get trhe username that the user has entered already in the form from the front-end
        #json.loads() the loads will take in data infor of json and convert it in to python dictionary
        data = json.loads(request.body)
        #now we can pick the username from data variable
        #the data variable will contain everything
        email = data['email']

        #checking if the username is alphanumeric or not
        if not validate_email(email): #here we will use a python module to validate our emails
            stuff_for_frontend = {
                'email_error': 'email is invalid'
            }
            return JsonResponse(stuff_for_frontend, status = 400)

        #now chencking if the username is already taken or not
        #or in other words if the username is already there in the database or not
        #User.objects.filter(email=email).exists() this will return a true or false depending on wheather the email is already there in the database or not
        if User.objects.filter(email=email).exists():
            stuff_for_frontend = {
                'email_error': 'email taken'
            }
            return JsonResponse(stuff_for_frontend, status = 409) #409 means that this resource is conflicting with the resource which is already present in the database

        #if every thing is correct then return email valid json response to the front-end
        stuff_for_frontend={
            'email_valid':True
        }

        return JsonResponse(stuff_for_frontend)

#this class will handle the login of all the users in our website
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
