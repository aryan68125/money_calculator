from django.shortcuts import render

#os module will allow us to find the currencies.json file in our project
import os
import json
from django.conf import settings
#----------------os related stuff ends here--------------------------------

#import database models
from . models import UserPreferences

from django.contrib import messages

#now create a view for preferences url
def preferences(request):
    user_preferences = UserPreferences.objects.get(user=request.user) #get the previously saved user preferences related to the user who is logged in
    if request.method == 'GET':
        #convert the list of curerencies which is in json object into a python dictionary then we can render it in the fronend of our website
        currency_data = []
        #for us to read the currencies.json file we need a path to that file so here we will use os module to do that
        file_path = os.path.join(settings.BASE_DIR,'currencies.json')
        #python debugger
        # import pdb;
        # pdb.set_trace()

        #now that we have found the currencies.json file in our django project we need to get the data from it
        #one of the utilities that we can use is a function called open
        #open('takes in a file', and a mode that we are pening it for example READ or WRITE etc....)
        #for this we are gonna use the context manager way
        #by default the mode is actually read in the open function
        #r = read, w = write, a = append
        #open function will open the file read from it and store the data from that file in json_file variable
        with open(file_path, 'r') as json_file: #this particular syntax of opening files you don't need to close the file manually it is automatically closed once the task is complete
            #now we have to turn this json_file into something that we can read
            #json.load(json_file) will convert the contents of json_file variable into a python dictionary and store it in the data variable
            data=json.load(json_file)
            #now all we have to do is take the contents from the data dictionary and put it in the array or a list
            #so to do that we need to loop through the dictionary using key value pairs
            for key,value in data.items():
                #now we can append each object in the data dictionary to the list currency_data
                #now we can pass this list to the frontend and use it however we see fit
                currency_data.append({'name':key,'value':value})

        #python debugger
        # import pdb;
        # pdb.set_trace()

        stuff_for_frontend = {
            'currency_data':currency_data
        }

        return render(request, 'preferences/preferences.html', stuff_for_frontend)
    else:
        #POST('currency') currency is the currency for loop variable in preferences.html page
        currency=request.POST['currency']
        #now we have got the currency chosen by the user from the lisbox no all we need to do is save it
        user_preferences.currency=currency
        user_preferences.save()
        messages.success(request,'Changes saved')
