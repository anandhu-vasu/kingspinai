from django.db import models

# Create your models here.
class UserData(models.Model):
    COUNTRIES=(
    ('IND','India'),
    ('UAE','Uae'),
    ('CA','Canada'),
    
    )
    name=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()
    company=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    password2=models.CharField(max_length=20)
    country=models.CharField(max_length=3,choices=COUNTRIES)
    city=models.CharField(max_length=20)
    postalcode=models.CharField(max_length=20)

    def __str__(self):
        return self.name