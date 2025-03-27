from django.shortcuts import render,redirect
from.models import Register
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer
from rest_framework import status
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password



def index(request):
    return render(request,'index.html')

@login_required()
def home(request):
    return render(request,"home.html")




def login_user(request):
    if request.method == "POST": 
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:  
            login(request, user)
            # request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["email"] = user.email
            request.session.modified = True
            request.session.set_expiry(10)
            print("DEBUG: Session Created -", dict(request.session.items()))  # Debugging

            messages.success(request, "Login successful!") 
            return redirect("home")  
        
        else: 
            messages.error(request, "Invalid username or password!") 
            return redirect("login_user")  

    return render(request, "login.html") 


def Register_user(request):
    if request.method=="POST":
        first_name=request.POST.get('first-name')
        last_name=request.POST.get('last-name')
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        conf_password=request.POST.get("conf_password")
        print(f"user{username},emial {email},pass={password},fname {first_name},l name {last_name},comf {conf_password}")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('Register_user')
        if password != conf_password:
            messages.error(request, "Passwords do not match!")
            return redirect('Register_user')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('Register_user')
        user = User(first_name=first_name,last_name=last_name,username=username,email=email,
            password=password )
        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login_user') 


    return render(request,"register.html")


def view_data(request):
    data=User.objects.all()
    return render(request,"view_data.html",{'data':data})

def final_page(request):
    return render(request,'final.html')

def logout_v(request):
    logout(request)  # Logs out the user
    request.session.flush()
    return redirect('login_user')

def contact(request):
    return render(request,'contact.html')




from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You are authenticated!"})

