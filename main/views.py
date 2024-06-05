import datetime
# Create your views here.
# and CompanyAdmin.objects.filter(user_type="is_company")
import pdb
import random

import jwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from dateutil.parser import parse

from .models import *
from .serializers import *


def login_attempt(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_obj = User.objects.filter(username=username).first()

            if user_obj is None:
                msg = "username Not Found"
                return render(request, "login_pages.html", {"msg": msg})

            user = authenticate(username=username, password=password)
            # pdb.set_trace()
            if user is None:
                msg = "Wrong Password"
                return render(request, "login_pages.html", {"msg": msg})
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect("adminpanel")

                elif user.is_staff:
                    login(request, user)
                    return redirect("subadminpanel")

                elif user.is_active:
                    login(request, user)
                    return redirect("companyadminpanel")
                else:
                    msg = "Something Went Wrong! Please Contact Administrator"
                    return render(request, "login_pages.html", {"msg": msg})
            else:
                msg = "Invalid Credential!"
                return render(request, "login_pages.html", {"msg": msg})
    except Exception as e:
        print(e)
        msg = "Something Went Wrong Please Connect With Administrator !"
        return render(request, "login_pages.html", {"msg": msg})
    return render(request, "login_pages.html")


def logout_view(request):
    logout(request)
    return redirect("login_attempt")


def change_pass(request):
    if not request.user.is_authenticated:
        return redirect("login_attempt")
    if request.method == "POST":
        oldpass = request.POST.get("oldpass")
        newpass = request.POST.get("newpass")

        if oldpass == "" or newpass == "":
            msg = "All Field is Required"
            return render(request, "error.html", {"msg": msg})

        user = authenticate(username=request.user, password=oldpass)

        if user != None:
            if len(newpass) < 8:
                msg = "Your Password at least minimum 8 character"
                return render(request, "error.html", {"msg": msg})

        user = User.objects.get(username=request.user)
        user.set_password(newpass)
        user.save()
        return redirect("logout_view")
    return render(request, "forgetpassword.html")


def adminpanel(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    sa = SubAdmin.objects.all().count()
    ca = CompanyAdmin.objects.all().count()
    ea = EmployeeAdmin.objects.all().count()
    ua = User.objects.all().count()
    return render(request, "adminpanel.html", {"sa": sa, "ca": ca, "ea": ea, "ua": ua})


def createstaff(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    try:
        valu = SubAdmin.objects.all()
        if request.method == "POST":
            manager_id = request.POST.get("manager", None)
            name = request.POST.get("name", None)
            mobile = request.POST.get("mobile", None)
            email = request.POST.get("email", None)
            img = request.FILES["img"]
            manager = User.objects.get(id=manager_id)
            digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            lower_char = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]

            upper_char = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
            ]

            symbol = ["@", "#", "$"]

            rand_digit = random.sample(digit, 3)
            rand_upper = random.sample(upper_char, 1)
            rand_lower = random.sample(lower_char, 5)
            rand_symbol = random.sample(symbol, 1)

            digit_value = "".join([str(i) for i in rand_digit])
            digit_upper = "".join([str(i) for i in rand_upper])
            digit_lower = "".join([str(i) for i in rand_lower])
            digit_symbol = "".join([str(i) for i in rand_symbol])
            password = digit_upper + digit_lower + digit_symbol + digit_value

            user_digit = random.sample(digit, 4)
            user_upper = random.sample(upper_char, 3)
            user_lower = random.sample(lower_char, 5)

            user_value = "".join([str(i) for i in user_digit])
            user_upper = "".join([str(i) for i in user_upper])
            user_lower = "".join([str(i) for i in user_lower])

            user = user_upper + user_lower + user_value

            if User.objects.filter(username=user).first():
                msg = "User Name Already Exists!"
                return render(request, "subadmin.html", {"msg": msg})

            if User.objects.filter(email=email).first():
                msg = "Email Address Already Exists!"
                return render(request, "subadmin.html", {"msg": msg})

            if SubAdmin.objects.filter(mobile=mobile).first():
                msg = "Mobile Number Already Exists!"
                return render(request, "subadmin.html", {"msg": msg})

            user_type = "SubAdmin"
            data = User.objects.create_user(
                first_name=name,
                email=email,
                last_name=mobile,
                is_staff=True,
                username=user,
            )
            data.set_password(password)
            data.save()

            values = SubAdmin.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                user=data,
                password=password,
                manager=manager,
                img=img,
                user_type=user_type,
            )
            values.save()
            msg = "New Sub Admin Created Successfully!"
            return render(
                request, "success.html", {"msg": msg, "pass": password, "user": user}
            )
    except Exception as e:
        print(e)
        msg = "Something Went Wrong Please Connect With Administrator!"
        return render(request, "error.html", {"msg": msg})
    return render(request, "subadmin.html", {"valu": valu})


def subadminlist(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    data = SubAdmin.objects.all()
    # data = SubAdmin.objects.filter(manager__id=request.user.id)
    return render(request, "subadminlist.html", {"data": data})


def addcompany(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    sub = SubAdmin.objects.all()
    try:
        if request.method == "POST":
            manager_id = request.POST.get("manager", None)
            company_name = request.POST.get("company_name", None)
            person_name = request.POST.get("person_name", None)
            mobile = request.POST.get("mobile", None)
            email = request.POST.get("email", None)
            img = request.FILES["img"]
            manager = User.objects.get(id=manager_id)

            user_type = "is_company"
            digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            lower_char = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]

            upper_char = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
            ]

            symbol = ["@", "#", "$"]

            rand_digit = random.sample(digit, 3)
            rand_upper = random.sample(upper_char, 1)
            rand_lower = random.sample(lower_char, 5)
            rand_symbol = random.sample(symbol, 1)

            digit_value = "".join([str(i) for i in rand_digit])
            digit_upper = "".join([str(i) for i in rand_upper])
            digit_lower = "".join([str(i) for i in rand_lower])
            digit_symbol = "".join([str(i) for i in rand_symbol])
            password = digit_upper + digit_lower + digit_symbol + digit_value

            user_digit = random.sample(digit, 4)
            user_upper = random.sample(upper_char, 3)
            user_lower = random.sample(lower_char, 5)

            user_value = "".join([str(i) for i in user_digit])
            user_upper = "".join([str(i) for i in user_upper])
            user_lower = "".join([str(i) for i in user_lower])

            user = user_upper + user_lower + user_value

            if User.objects.filter(username=user).first():
                msg = "User Name Already Exists!"
                return render(request, "addcompany.html", {"msg": msg})

            if User.objects.filter(email=email).first():
                msg = "Email Address Already Exists!"
                return render(request, "addcompany.html", {"msg": msg})

            if CompanyAdmin.objects.filter(mobile=mobile):
                msg = "Mobile Number Already Exists!"
                return render(request, "addcompany.html", {"msg": msg})

            data = User.objects.create_user(
                first_name=company_name,
                email=email,
                last_name=person_name,
                is_active=True,
                username=user,
            )
            data.set_password(password)
            data.save()

            values = CompanyAdmin.objects.create(
                company_name=company_name,
                person_name=person_name,
                email=email,
                mobile=mobile,
                user=data,
                password=password,
                img=img,
                user_type=user_type,
                manager=manager,
            )
            values.save()
            msg = "New Company Created Successfully!"
            return render(
                request, "success.html", {"msg": msg, "pass": password, "user": user}
            )
    except Exception as e:
        print(e)
        msg = "Something Went Wrong Please Connect With Administrator! "
        return render(request, "error.html", {"msg": msg})
    return render(request, "addcompany.html", {"sub": sub})


def companylist(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    data = CompanyAdmin.objects.all()
    return render(request, "companylist.html", {"data": data})


def addemployee(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    try:
        comp = CompanyAdmin.objects.all()
        if request.method == "POST":
            manager_id = request.POST.get("manager", None)
            person_name = request.POST.get("person_name", None)
            mobile = request.POST.get("mobile", None)
            email = request.POST.get("email", None)
            img = request.FILES["img"]

            manager = User.objects.get(id=manager_id)

            user_type = "is_employee"
            digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            lower_char = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]

            upper_char = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
            ]

            symbol = ["@", "#", "$"]

            rand_digit = random.sample(digit, 3)
            rand_upper = random.sample(upper_char, 1)
            rand_lower = random.sample(lower_char, 5)
            rand_symbol = random.sample(symbol, 1)

            digit_value = "".join([str(i) for i in rand_digit])
            digit_upper = "".join([str(i) for i in rand_upper])
            digit_lower = "".join([str(i) for i in rand_lower])
            digit_symbol = "".join([str(i) for i in rand_symbol])
            password = digit_upper + digit_lower + digit_symbol + digit_value

            user_digit = random.sample(digit, 4)
            user_upper = random.sample(upper_char, 3)
            user_lower = random.sample(lower_char, 5)

            user_value = "".join([str(i) for i in user_digit])
            user_upper = "".join([str(i) for i in user_upper])
            user_lower = "".join([str(i) for i in user_lower])

            user = user_upper + user_lower + user_value

            if User.objects.filter(username=user).first():
                msg = "User Name Already Exists!"
                return render(request, "addemployee.html", {"msg": msg})

            if User.objects.filter(email=email).first():
                msg = "Email Address Already Exists!"
                return render(request, "addemployee.html", {"msg": msg})

            if EmployeeAdmin.objects.filter(mobile=mobile).first():
                msg = "Mobile Number Already Exists!"
                return render(request, "addemployee.html", {"msg": msg})

            data = User.objects.create_user(
                first_name=person_name, email=email, last_name=mobile, username=user
            )
            data.set_password(password)
            data.save()

            values = EmployeeAdmin.objects.create(
                person_name=person_name,
                email=email,
                mobile=mobile,
                user=data,
                password=password,
                img=img,
                user_type=user_type,
                manager=manager,
            )
            values.save()
            msg = "New Employee Created Successfully!"
            return render(
                request, "success.html", {"msg": msg, "pass": password, "user": user}
            )
    except Exception as e:
        print(e)
        msg = "Something Went Wrong Please Connect with Administrator!"
        return render(request, "error.html", {"msg": msg})
    return render(request, "addemployee.html", {"comp": comp})


def employeelist(request):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    emp = EmployeeAdmin.objects.all()
    return render(request, "employeelist.html", {"emp": emp})


# def delete_user(request):
#     context = {}
#     if "pid" in request.GET:
#         pid = request.GET["pid"]
#         usr = get_object_or_404(User, id=pid)
#         context["usr"] = usr
#         if "action" in request.GET:
#             usr.delete()
#             context["status"] = str(usr.username) + "User Delete Successfully"
#
#     return render(request, 'employeelist.html', context)


class ContactDetailsView(viewsets.ModelViewSet):
    queryset = ContactDetails.objects.all()
    serializer_class = ContactDetailsSerializer


class AddMultipleContactView(APIView):
    @extend_schema(
        request=ContactDetailsSerializer(many=True), responses=ContactDetailsSerializer
    )
    def post(self, request, format=None):
        print(request.data)
        serializer = ContactDetailsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            for contact in serializer.data:
                print(contact)
                # check contact exist or not
                if not ContactDetails.objects.filter(
                    mobile=contact["mobile"], user_id=contact["user"]
                ).exists():
                    print("Error")
                    ContactDetails.objects.create(
                        name=contact["name"],
                        mobile=contact["mobile"],
                        user_id=contact["user"],
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Contact Added Successfully", status=201)


class AddMultipleCallLogs(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AndroidDataSerializerWithoutUser(many=True),
        responses=AndroidDataSerializer,
    )
    def post(self, request, format=None):
        print(request.data)
        serializer = AndroidDataSerializerWithoutUser(data=request.data, many=True)

        # fina latest call logs
        latest_call_logs = AndroidData.objects.order_by("-date").first()


        if latest_call_logs is not None:
            if serializer.is_valid():
                for logs in serializer.data:
                    if latest_call_logs.date <= parse(logs["date"]):
                        AndroidData.objects.create(**logs, user=request.user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                for logs in serializer.data:
                    AndroidData.objects.create(**logs, user=request.user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Contact Added Successfully", status=201)


class AndroidDataView(viewsets.ModelViewSet):
    queryset = AndroidData.objects.all()
    serializer_class = AndroidDataSerializer


# class AndroidDataView(APIView):
#
#     def get(self, request, format=None):
#         snippets = AndroidData.objects.all()
#         serializer = AndroidDataSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = AndroidDataSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class ContactDetailsView(APIView):
#     def get(self, request, format=None):
#         snippets = ContactDetails.objects.all()
#         serializer = ContactDetailsSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ContactDetailsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


def del_user(request, username):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    try:
        u = User.objects.get(username=username)
        u.delete()
        msg = "Delete Data Has Been Successfully!"
        return render(request, "error.html", {"msg": msg, "u": u})

    except User.DoesNotExist:
        msg = "User Not Found !"
        return render(request, "error.html")

    except Exception as e:
        return render(request, "error.html", {"err": e.message})

    return render(request, "employeelist.html")


def view_details(request, username):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    user = User.objects.get(username=username)
    data = AndroidData.objects.filter(user=user)
    return render(request, "view_details.html", {"data": data})


def call_details(request, username):
    if not request.user.is_superuser:
        return redirect("login_attempt")
    user = User.objects.get(username=username)
    data = ContactDetails.objects.filter(user=user)
    return render(request, "call_details.html", {"data": data})


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(request={"username", "password"})
    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]

        print(username, password)

        user = authenticate(username=username, password=password)

        if user is not None:

            refresh = RefreshToken.for_user(user)

            payload = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            user = {"user": username, "email": user.email, "user_id": user.id}
            return JsonResponse(
                {
                    "success": "Login Success Fully",
                    "user": user,
                    "status": True,
                    "tokens": payload,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return JsonResponse(
                {"success": "false", "msg": "The credentials provided are invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )


def disclaimer(request):
    return render(request, "disclaimer.html")
