from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPreferences(models.Model):
    #ont to one relation between this user model and this preferences model
    # on_delete=models.CASCADE will delete the preferences that belog to that user if the user deletes his/her account
    user =  models.OneToOneField(to=User, on_delete=models.CASCADE) #set up user for whome we are going to keep track of their settings
    currency = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user) + 's' + ' preferences'
