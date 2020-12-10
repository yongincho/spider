
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import hashlib
from lib.s3wrapper import S3Wrapper
import os, time
from wrapper.redis_wrapper import RedisWrapper
from django.conf import settings
from .models import SpiderUser, SpiderUserLog, SpiderUserFace, SpiderIdentifyRequest


# Class-based View (CBV)

# Admin Login API
class Login(APIView):

    permission_classes = (AllowAny,)  # Allow any to access

    def get(self, request):
        return render(request, "login.html")  # If method is GET, render login page

    def post(self, request):  # If method is POST:
        
        user_nickname = request.POST["nickname"]  # Get nickname from user input
        user_pw = request.POST["pw"]  # Get password from user input

        user = authenticate(nickname = user_nickname, password = user_pw)  # Authenticate by matching nickname and password

        user_info = SpiderUser.objects.get(nickname = user_nickname)  # Get user info from database

        MSG = {"info": ""}

        if user == None:  # If authentication fails:
            MSG["info"] = "Incorrect UserName or Password"  # Output message that it is incorrect
            SpiderUserLog.objects.create(log_body = "Admin Login", log_type = 2, log_success = 2, user_info_id = user_info.id)  # Insert login data into User Log table
            return render(request, "login.html", MSG)  # Render login page with message

        token, flag = Token.objects.get_or_create(user=user)  # Get token

        SpiderUserLog.objects.create(log_body = "Admin Login", log_type = 2, log_success = 1, user_info_id = user_info.id)  # Insert login data into User Log table

        return render(request, "dashboard.html")  # Render dashboard page


# Admin Register API
class Register(APIView):

    permission_classes = (AllowAny,)  # Allow any to access

    def get(self, request):
        return render(request, "register.html")  # If method is GET, render register page

    def post(self, request):
        
        user_email = request.POST["email"]  # Get email from user input
        user_nickname = request.POST["nickname"]  # Get nickname from user input
        user_place = request.POST["place"]  # Get place from user input
        user_pw = request.POST["pw"]  # Get password from user input

        MSG = {"info": ""}
        
        if SpiderUser.objects.get(nickname = user_nickname) != None:  # If nickname exists:
            MSG["info"] = "UserName exists. Please choose a different UserName."  # Output message 
            SpiderUserLog.objects.create(log_body = "Admin Register", log_type = 3, log_success = 2, user_info_id = 1)  # Insert register data into User Log table
            return render(request, "register.html", MSG)  # Render register page with message
        
        if SpiderUser.objects.get(email = user_email) != None:  # If email exists:
            MSG["info"] = "Email exists. Please use a different email."  # Output message
            SpiderUserLog.objects.create(log_body = "Admin Register", log_type = 3, log_success = 2, user_info_id = 1)  # Insert register data into User Log table
            return render(request, "register.html", MSG)  # Render register page with message

        hashed_pw = make_password(user_pw)  # Hash the password

        SpiderUser.objects.create(email = user_email, nickname = user_nickname, place = user_place, password = hashed_pw)  # Insert register data into User table

        user_info = SpiderUser.objects.get(nickname = user_nickname)  # Get user info from database

        SpiderUserLog.objects.create(log_body = "Admin Register", log_type = 3, log_success = 1, user_info_id = user_info.id)  # Insert register data into User Log table

        return render(request, "dashboard.html")  # Render dashboard page


# Face Register API for Admin
class RegisterFace(APIView):
    
    permission_classes = (IsAuthenticated,)  # Allow only authenticated admin to access

    def get(self, request):
        return render(request, "face_register.html")  # If method is GET, render face_register page

    def post(self, request):

        print(request.data)

        user_nickname = request.POST["nickname"]
        upload_file = request.FILES["file"]  # Get facial image png file from user input

        if ".png" not in upload_file.name:
            MSG = {"info": "Please upload png file"}
            return render(request, "face_register.html", MSG)

        user_info = SpiderUser.objects.get(nickname = user_nickname) # How do I get id or token of this log in person

        m = hashlib.md5()  
        m.update(upload_file.read())
        hash_filename = m.hexdigest()  # Hash the filename

        converted_filename = hash_filename+"_"+user_info.nickname+".png"  # Convert filename to hashed name + username + .png

        fs = FileSystemStorage(
            location = settings.STORAGE_DIRECTORY
        )
        filename = fs.save(converted_filename, upload_file)

        s3 = S3Wrapper(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)  # Access S3
        s3.upload("spider-face-bucket", settings.STORAGE_DIRECTORY+converted_filename, converted_filename)  # Upload file to S3

        os.remove(settings.STORAGE_DIRECTORY+converted_filename)  # Remove file from the server

        SpiderUserFace.objects.create(user_face = converted_filename, user_info_id = user_info.id)  # Insert face data into UserFace table

        SpiderUserLog.objects.create(log_body = "Face Register", log_type = 4, log_success = 1, user_info_id = user_info.id)  # Insert face data into User Log table

        MSG = {"info": "Face Successfully Registered"}  # Output message

        return render(request, "face_register.html", MSG)  # Render face_register page with message


# User API
class Identify(APIView):

    permission_classes = (AllowAny,)  # Allow any to access

    def get(self, request):
        response = {
            "success": False,
            "message": "Wrong method"
        }
        return Response(response, status=status.HTTP_200_OK)  # Output "wrong method" response for GET

    def post(self, request):

        upload_file = request.FILES["file"]  # Get file from user input (or from camera device/hardware)
        username = request.POST['username']

        m = hashlib.md5()
        m.update(upload_file.read())
        file_hash = m.hexdigest()

        s3_filename = file_hash + '_' + username
        fs = FileSystemStorage(
            location = settings.STORAGE_DIRECTORY
        )
        filename = fs.save(s3_filename, upload_file)

        s3 = S3Wrapper(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)  # Access S3

        #user_info = SpiderUser.objects.get(id = id) # How do I get id or token of this not log in person

        #user_face = SpiderUserFace.objects.get(user_info_id = user_info.id)  # Get user face info
        s3.upload("spider-face-bucket", settings.STORAGE_DIRECTORY + s3_filename, s3_filename)  # Upload file to S3
        ticket = hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()

        SpiderIdentifyRequest.objects.create(user_info=request.user, identify_username=username,
                s3_path=s3_filename, ticket=ticket)
        response = {
            "success": True,
            "message": "Request Success",
            "ticket": ticket
        }
        return Response(response, status=status.HTTP_200_OK)  # Output "success" response (usually followed by login access)


class Result(APIView):

    permission_classes = (AllowAny,)  # Allow any to access

    def get(self, request):
        
        ticket = request.GET["ticket"]

        user_info = SpiderIdentifyRequest.objects.get(ticket = ticket)

        if user_info == None:  # If ticket does not exist:
            response = {
                "success": False,
                "message": "Ticket does not exist"
            }
            return Response(response, status=status.HTTP_200_OK)  # Output "fail" response 

        if user_info.status == 0:
            response = {
                "success": False,
                "message": "Preparing for Detection"
            }  
            return Response(response, status=status.HTTP_200_OK)  # Output "fail" response

        if user_info.status == 1:
            response = {
                "success": False,
                "message": "Detecting"
            }
            return Response(response, status=status.HTTP_200_OK)  # Output "fail" response

        user_log = SpiderUserLog.objects.filter(log_ticket = ticket).all()
        user_log = user_log[len(user_log)-1].log_body

        response = {
            "success": user_log,
            "message": "Detection Result",
            "ticket": ticket
        }

        return Response(response, status=status.HTTP_200_OK)


class Dashboard(APIView):

    permission_classes = (IsAuthenticated,)  # Allow only authenticated admin to access

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard.html'

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)  # If method is GET, render dashboard page


class User(APIView):

    permission_classes = (IsAuthenticated,)  # Allow only authenticated admin to access

    def get(self, request):
        return render(request, "user.html")  # If method is GET, render user page


class About(APIView):

    permission_classes = (IsAuthenticated,)  # Allow only authenticated admin to access

    def get(self, request):
        return render(request, "about.html")  # If method is GET, render about page


