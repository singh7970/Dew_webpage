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



def index(request):
    return render(request,'index.html')


@permission_classes([IsAuthenticated])
@login_required()
def home(request):
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

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You are authenticated!"})




#viewotp
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import OTP

def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print(email)  # Debugging

        # Get or create user
        user, created = User.objects.get_or_create(username=email, email=email)

        # Generate and save OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(user=user, otp_code=otp_code)

        # Send OTP via email
        send_mail(
            "Your OTP Code",
            f"Your OTP code is {otp_code}. It expires in 5 minutes.",
            "raj3847kumar@gmail.com",  # Change to your actual email
            [email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your email.")
        return redirect("verify_otp")  # Redirect to verification page

    return render(request, "send-otp.html")

def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp_code = request.POST.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_instance = OTP.objects.filter(user=user, otp_code=otp_code).last()

            if otp_instance and otp_instance.is_valid():
                messages.success(request, "Email verified successfully!")
                otp_instance.delete()  # Delete OTP after successful verification
                return redirect("login_user")  # Redirect after successful login
            else:
                messages.error(request, "Invalid mail or expired OTP.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, "verify_otp.html")
