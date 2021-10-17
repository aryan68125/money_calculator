from django.db import models

from django.utils.timezone import now

from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    amount=models.FloatField()
    date=models.DateField(default=now)
    description = models.TextField()
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self):
        return self.description

    #this will allow us to sort our expenses via date they were created
    class Meta:
        ordering = ['-date']

class Category(models.Model):
    name = models.CharField(max_length=266)

    #modyfying the categorys to catagories
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
