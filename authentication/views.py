from django.shortcuts import render
from django.views import View
# Create your views here.
#this class will handle the registration of the users
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

#this class will handle the login of all the users in our website
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
