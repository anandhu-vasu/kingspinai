from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,company_name,phone,username,password=None):
        if not email:
            raise ValueError("email is required")
        if not company_name:
            raise ValueError("company name  Id is required")
        if not phone:
            raise ValueError("Please provide active phone number")
        if not username:
            raise ValueError("User name is required")

        user=self.model(
           email=self.normalize_email(email),
           company_name=company_name,
           username=username,
           phone=phone,


        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,company_name,phone,password=None):
        user=self.create_user(
            email=email,
            username=username,
            company_name=company_name,
            
            phone=phone,
            password=password
        )    
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    username=models.CharField(verbose_name='user name',max_length=60)
    email=models.EmailField(verbose_name="email address", max_length=60,unique=True)
    company_name=models.CharField(verbose_name="company name",max_length=200)
    phone=models.CharField(verbose_name="Mobile number",max_length=20)
    date_joined=models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=True)
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["company_name","username","phone"]
    objects=UserManager()
    

    def __str__(self):
        return self.username


    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True        