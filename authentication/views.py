from django.shortcuts import render, redirect
from django.views import View

#imports related to live username and email validation in the registration form
#to work with json we need to import json
import json
from django.http import JsonResponse

#import User auth model from django
from django.contrib.auth.models import User

#import the validate-email module in this view
from validate_email import validate_email

#imports related to displaying messages
from django.contrib import messages


#--------------------------USER REGISTRATION, LOGIN, AUTHENTICATION,LOGOUT RELATED IMPORTS STARTS HERE----------------------------------
#for our login page to have proper login and user authaentication process we have to make these imports below
from django.contrib.auth import login, authenticate, logout
from django.contrib import auth

#import the built in django user model
from django.contrib.auth.models import User

'''this is a inbuilt django Views class that handles the remdering of views that are built in to the django web framework'''
from django.views.generic import View

'''install validate-email module before importing it type pip3 install validate-email in your terminal to install the module'''
from validate_email import validate_email

'''
construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
'''
from django.contrib.sites.shortcuts import get_current_site

#now redirect user to the login page
# so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from . utils import generated_token
from django.core.mail import EmailMessage
from django.conf import settings

#import UserCreationForm built in django register form for register page
from django.contrib.auth.forms import UserCreationForm

#----------------------reset password----------------------
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#----------------------reset password----------------------

#restrict unauthenticated user from seeing add project page
#we won't be using mixins here because we are using function based views mixins are used when using class based views when foloowing standard procedures for django web development
#instead we will be using login_required decorator to ristrict unauthenticated users from acessing certain pages in our website
from django.contrib.auth.decorators import login_required

#--------------------------USER REGISTRATION, LOGIN, AUTHENTICATION,LOGOUT RELATED IMPORTS ENDS HERE----------------------------------


# Create your views here.
#this class will handle the registration of the users
class RegistrationView(View):
    #this dispatch function prevents logged in user from seeing registration page
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('expenses')
        return super().dispatch(*args, **kwargs)
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        #handle the user registration process
        #get user data from User djangoinbuilt model
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        stuff_for_frontend = {
            'fieldvalues': request.POST
        }

        #validate the user data
        #disable the submit-btn when the user information is invalid in register.js
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) <6:
                    messages.error(request, "Your password should be atleast 6 charaters long")
                    return render(request, 'authentication/register.html', stuff_for_frontend)
                elif password != password2:
                    messages.error(request, "Password is not matching")
                    return render(request, 'authentication/register.html', stuff_for_frontend)

                #save the user in the database
                user = User.objects.create_user(username=username, email=email) #set username and email
                user.set_password(password) #set the password

                #now before we save the user we need to make sure that the newly created user cannot login into the website
                user.is_active = False

                #now finally save the changes and commit thoes changed data in the database
                user.save()

                #now after the user is saved in the database we can send them account activation link to their respective email address
                #send the verification link to the user's email address

                #step1. construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
                #       and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
                current_site = get_current_site(request) #get_current_site(request) will give us the current domain of our website dinamically
                #step2. create an email subject
                email_subject= 'Email verification'

                #step3. construct a message
                # so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
                #convert the user.pk into bytes so we need to import:- from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
                #import a module that generated a unique token for our application when we need to verify the user's email address :- from django.contrib.auth.tokens import PasswordResetTokenGenerator it can be used to activate accounts and to reset password
                create_a_context_for_front_end={
                    'user':user,
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generated_token.make_token(user),
                }
                message = render_to_string('authentication/activate.html',create_a_context_for_front_end)
                #step4. send an email for authentation of the account import :- from django.core.mail import EmailMessage and import settings :- from django.conf import settings
                '''
                email_message = EmailMessage(
                   email_subject,            #subject of the email
                   message,                  #message that you want to send via email
                   settings.EMAIL_HOST_USER, #EMAIL_HOST = 'smtp.gmail.com' that is being imported from the settings.py of the django project
                   [email],                  #email adderess entered by the user in the regitration form in the front end of the application of the django project
                )
                '''
                email_message = EmailMessage(
                   email_subject,
                   message,
                   settings.EMAIL_HOST_USER,
                   [email],
                )
                email_message.send()
                #now redirect user to the login page
                return redirect('success')

                #create the user account

                #display the messages
                #types of messages
                # messages.warning(request, 'Account created Activation link sent to your email')
                #in order to sytle error messages you need to add this in settings.py file
                #make error messages into danger so that bootstrap can understand it and style it properly
                #import messages by typing from django.contrib import messages in settings.py file
                # MESSAGE_TAGS = {
                #     messages.ERROR : 'danger'
                # }
                # messages.error(request, 'Account created Activation link sent to your email')
                messages.success(request, 'Account created Succesfully!')
                messages.info(request, 'Activation link sent check your email')
                return render(request, 'authentication/register.html', stuff_for_frontend)

            else:
                return render(request, 'authentication/register.html', stuff_for_frontend)

        else:
            return render(request, 'authentication/register.html', stuff_for_frontend)

#this class is responsible for activating the user account when the user clicks the link in their email address
class ActivateAccountView(View):
    def get(self, request,uidb64,token):
        print(f"request = {request}")
        #in here we will check if the token is valid or not
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(f"uid = {uid}")
            #do not use User.objects.filter(pk=uid).exists(): instead use User.objects.get(pk=uid) otherwise when you
            #deploy your application on heroku it will throuw an exception
            user = User.objects.get(pk=uid)
            print(f"user = {user}")
        except User.DoesNotExist:
            user = None

        #now check the user before activating them
        if user is not None and generated_token.check_token(user,token):
            print(f"token = {token}")
            #now activate the user in the database for operational ready i.e user now have the permission to use the web Application
            user.is_active = True
            print(f"user active stauts = {user.is_active}")
            user.save()
            messages.success(request,'account activated successfully')
            return redirect('login')
        messages.error(request,'account activation Failed!')
        return render(request,'authentication/error.html', status=401)

class SuccessView(View):
    def get(self, request):
        return render(request,'authentication/success.html')

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
    #this dispatch function prevents logged in user from seeing login page
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('expenses')
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        #pick out the data from the login.html form
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password :
            #if username and password is not none then we will try to login this user in our website
            user = auth.authenticate(username=username, password=password)

            #user is successfully authenticated then we get the user back
            if user:
                if user.is_active:
                    #if the user account is activated via email verification link then allow user to login to their account
                    auth.login(request, user)
                    #now we can redirect user to the home page after login
                    # messages.success(request,'account activated you can now login')
                    return redirect('expenses')
                else:
                    messages.error(request,'It looks like your account is not activated')
                    message.warning(request,'Please check you email for activation link')
                    return render(request, 'authentication/login.html')
            else:
                messages.error(request,'invalid username or password')
                return render(request, 'authentication/login.html')

        else:
            messages.error(request,'username and password cannot be empty')
            return render(request, 'authentication/login.html')

class LogoutView(View):
    def post (self, request):
        auth.logout(request)#this will logout the user
        return redirect('login')

#--------------reset password related views starts here-----------------
class RequestResetEmailView(View):
    #this dispatch function prevents logged in user from seeing reset-password page
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('expenses')
        return super().dispatch(*args, **kwargs)

    #here we are gonna have a from where user can supply their email address
    def get(self, request):
        return render(request, 'authentication/request-reset-email.html')

    #here we will handle the post request from request-reset-email.html page
    def post(self,request):
        email = request.POST['email']

        #before we send the mail to this email address we need to check if this user even exist in our database
        if not validate_email(email): #step1. check the email is valid or not
            messages.add_message(request,messages.ERROR,'email address not valid!')
            return render(request, 'users/request-reset-email.html')

        user = User.objects.filter(email=email) #this will find the user having the email address entered in the provide email section of the reset passsword html page
        if user.exists():
            # this will return true if the user is already in our website's database
            #send the verification link to the user's email address
            #step1. construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
            #       and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(request) #get_current_site(request) will give us the current domain of our website dinamically
            #step2. create an email subject
            email_subject= 'Reset password'

            #step3. construct a message
            # so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
            #convert the user.pk into bytes so we need to import:- from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
            #import a module that generated a unique token for our application when we need to verify the user's email address :- from django.contrib.auth.tokens import PasswordResetTokenGenerator it can be used to activate accounts and to reset password
            create_a_context_for_front_end={
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]), #here we won't use the utils.py file to generate a token here we will use an inbuilt class to generate a token to set a new password
            }
            message = render_to_string('users/reset-user-password.html',create_a_context_for_front_end)
            #step4. send an email for authentation of the account import :- from django.core.mail import EmailMessage and import settings :- from django.conf import settings
            '''
            email_message = EmailMessage(
               email_subject,            #subject of the email
               message,                  #message that you want to send via email
               settings.EMAIL_HOST_USER, #EMAIL_HOST = 'smtp.gmail.com' that is being imported from the settings.py of the django project
               [email],                  #email adderess entered by the user in the regitration form in the front end of the application of the django project
            )
            '''
            email_message = EmailMessage(
               email_subject,
               message,
               settings.EMAIL_HOST_USER,
               [email],
            )
            email_message.send()


        messages.add_message(request,messages.SUCCESS,'email reset link has been sent to your email address')
        return render(request, 'users/request-reset-email.html')

class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        #send uidb64 and token  to the set-new-password.html via context dictionary
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        #prevent user from using the same token that was sent in the email of the user to reset the password
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token): #if this returns false then the link is already used to reset the password
                messages.add_message(request,messages.ERROR,'Password reset link expired')
                return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(request,messages.INFO,'Oops something went wrong!')
            return render(request, 'authentication/set-new-password.html',context)

        return render(request, 'authentication/set-new-password.html', context)

    #handeling the post requests
    def post(self, request, uidb64, token):
        #send uidb64 and token  to the set-new-password.html via context dictionary
        context = {
            'uidb64':uidb64,
            'token':token,
            'has_error': False,
        }

        #check the password
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')
        if len(password1) < 6:
            messages.add_message(request,messages.ERROR,'password must be atleast 6 characters long')
            context['has_error'] = True
        if password1 != password2:
            messages.add_message(request,messages.ERROR,'password do not match')
            context['has_error'] = True
        if context['has_error'] == True:
            return render(request, 'authentication/set-new-password.html',context)

        #if the user entered the correct password then we are going to proceed with setting the new password for the user account
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.add_message(request,messages.SUCCESS,'password changed successfully')
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(request,messages.INFO,'Oops something went wrong!')
            return render(request, 'authentication/set-new-password.html',context)

        return render(request, 'authentication/set-new-password.html',context)



#-------------------------USER Registration, EMAIL VERIFICATION , LOGIN AND LOGOUT FUNCTIONALITY ENDS HERE--------------------------------
