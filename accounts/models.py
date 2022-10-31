
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserModel




class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,blank=True,null=True) 
    email=models.EmailField(unique=True)
    USER_TYPE=(
        ("1","Administrator"),
        ("2","Vendor"),
        ("3","Customer"),
    )
    user_type=models.CharField(max_length=1,choices=USER_TYPE) 
    profile_picture=models.ImageField(upload_to="media",
           default="media/no_avatar.png")
    otp=models.CharField(max_length=6,blank=True,null=True)
   
    objects=UserModel()
    
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=[]


  