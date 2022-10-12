
from django.contrib.auth import login,logout,authenticate
from django.views import View 
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import random

class LoginView(View):
    return_url=""
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("pages:home")
        LoginView.return_url=request.GET.get("return_url")
        return render(request,'accounts/login.html')
    
    def check_email(self,email):
        return CustomUser.objects.filter(email=email)

        
    def post(self,request):
        email=request.POST.get("email")
        password=request.POST.get("password")
        if not self.check_email(email):
            messages.warning(request,"You are not a Customer!!")
            return redirect("login")

        url_check=False 
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You're logged in successfully!!")
            if LoginView.return_url:
                return redirect(f"{LoginView.return_url}")
               
            else:
                return redirect("pages:home")    
        else:
            messages.warning(request,"Email or password is incorrect!!")
            if LoginView.return_url:
                url_check=LoginView.return_url
            return render(request,'accounts/login.html',{"email":email,"url_check":url_check})

class RegisterView(View):
    def get(self,request): 
        if request.user.is_authenticated:
            return redirect("pages:home")
        return render(request,"accounts/register.html")
    def post(self,request):
        email=request.POST.get("email")
        password=request.POST.get("password")
        username=request.POST.get("username")
        password=request.POST.get("password")
        email_check=CustomUser.objects.filter(email=email)
        username_check=CustomUser.objects.filter(username=username)
        if username_check.exists():
            username=str("@")+username+str(random.randint(1000,9999))
        else:
            username=str("@")+username

        if not email_check:
            user=CustomUser(
                username=str(username).replace(" ",""),
                email=email,
                password=make_password(password),
                user_type="3"
                )
            user.save()
            if user:
                messages.success(request,"Your account created successfully!!")
                return redirect("login")
        else:
            messages.success(request,"Email address already exists!!!")
            return redirect("register")

class LogoutView(View):
    def get(self,request): 
        logout(request)
        messages.success(request,"You're logged out successfully!!")
        return redirect("pages:product-list")

