from django.db import models

# Create your models here.
class Accounts(models.Model):
    username=models.TextField()
    password=models.TextField()