from django.db import models

# Create your models here.
class UserData(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    company=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    password2=models.CharField(max_length=20)

    def __str__(self):
        return self.name