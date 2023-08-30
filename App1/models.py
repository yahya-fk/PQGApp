from django.db import models

class PQGSettings(models.Model):
    PQG=models.CharField(max_length=5,unique=True)
    Static=models.IntegerField()
    Dynamic=models.IntegerField()

def is_superuser(user):
    return user.is_superuser

class GlobalValue(models.Model):
    objectif = models.IntegerField()
