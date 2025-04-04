from django.shortcuts import render,redirect
from.models import Register
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny,IsAuthenticated ,IsAdminUser
from .serializers import RegisterSerializer
from rest_framework import status
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

# app/views.py
import logging

logger = logging.getLogger('app')  

def index(request):
    return render(request,'index.html')


@permission_classes([IsAuthenticated])
@login_required()
def home(request):
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
    
    return render(request, "home.html")


# @login_required()
# def home(request):
#     return render(request,"home.html")




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
            next_url = request.GET.get("next") or "home"  # Ensure it redirects properly
            return redirect(next_url)
             
        
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


@api_view(['GET', 'POST','PUT','PATCH','DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def drf_view(request):  
    if request.method == 'GET':
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication






#viewotp
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import OTP
from django.http import JsonResponse
import json

def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"success": False, "message": "Invalid email address."})

        # Remove any existing OTPs for this email
        OTP.objects.filter(email=email).delete()

        # Generate and save a new OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(email=email, otp_code=otp_code)

        # Send OTP via email
        send_mail(
            "Your OTP Code",
            f"Your OTP code is {otp_code}. It expires in 5 minutes.",
            "raj3847kumar@gmail.com",  # Replace with your actual email
            [email],
            fail_silently=False,
        )

        return JsonResponse({"success": True, "message": "OTP sent to your email."})

    return JsonResponse({"success": False, "message": "Invalid request."})
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        otp_code = data.get("otp")

        try:
            
            otp_instance = OTP.objects.filter(email=email, otp_code=otp_code).order_by("-created_at").first()

            print(otp_instance)

            if otp_instance and otp_instance.is_valid():
                otp_instance.delete()  # OTP is used, so delete it
                return JsonResponse({"verified": True, "message": "Email verified successfully!"})

            return JsonResponse({"verified": False, "message": "Invalid or expired OTP."})

        except User.DoesNotExist:
            return JsonResponse({"verified": False, "message": "User not found."})

    return JsonResponse({"verified": False, "message": "Invalid request."})



# def verify_otp(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             email = data.get("email")
#             otp_code = data.get("otp")

#             print(f"Received Email: {email}")
#             print(f"Received OTP: {otp_code}")

#             if not email or not otp_code:
#                 return JsonResponse({"error": "Email and OTP are required"}, status=400)

#             otp_entry = OTP.objects.filter(email=email).order_by("-created_at").first()
#             print(otp_entry)
#             print(f"Stored OTP: {otp_entry.otp_code if otp_entry else 'No OTP found'}")

#             if not otp_entry or otp_entry.otp_code != otp_code:
#                 return JsonResponse({"error": "Invalid OTP"}, status=400)

#             otp_entry.delete()
#             return JsonResponse({"message": "OTP verified successfully!"}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": f"Failed to verify OTP: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You have access to this view!"})


