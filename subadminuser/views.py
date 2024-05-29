import random

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.models import *


# Create your views here.

def subadminpanel(request):
    if not request.user.is_staff:
        return redirect('login_attempt')
    cam = CompanyAdmin.objects.filter(manager__id=request.user.id).count()
    emp = EmployeeAdmin.objects.all().count()
    return render(request, 'subadminpanel.html', {'cam': cam, 'emp': emp})


def subadminaddcompany(request):
    if not request.user.is_staff:
        return redirect('login_attempt')
    valu = SubAdmin.objects.all()
    if request.method == 'POST':
        manager_id = request.POST.get('manager', None)
        company_name = request.POST.get('company_name', None)
        person_name = request.POST.get('person_name', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        img = request.FILES['img']
        manager = User.objects.get(id=manager_id)

        user_type = "is_company"
        digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        lower_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                      'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                      'z']

        upper_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                      'Z']

        symbol = ['@', '#', '$']

        rand_digit = random.sample(digit, 3)
        rand_upper = random.sample(upper_char, 1)
        rand_lower = random.sample(lower_char, 5)
        rand_symbol = random.sample(symbol, 1)

        digit_value = ''.join([str(i) for i in rand_digit])
        digit_upper = ''.join([str(i) for i in rand_upper])
        digit_lower = ''.join([str(i) for i in rand_lower])
        digit_symbol = ''.join([str(i) for i in rand_symbol])
        password = digit_upper + digit_lower + digit_symbol + digit_value

        user_digit = random.sample(digit, 4)
        user_upper = random.sample(upper_char, 3)
        user_lower = random.sample(lower_char, 5)

        user_value = ''.join([str(i) for i in user_digit])
        user_upper = ''.join([str(i) for i in user_upper])
        user_lower = ''.join([str(i) for i in user_lower])

        user = user_upper + user_lower + user_value

        if User.objects.filter(username=user).first():
            msg = "User Name Already Exists!"
            return render(request, "companyadd.html", {"msg": msg})
        if User.objects.filter(email=email).first():
            msg = "Email Address Already Exists!"
            return render(request, "companyadd.html", {"msg": msg})

        data = User.objects.create_user(first_name=company_name, email=email, last_name=person_name, is_active=True,
                                        username=user)
        data.set_password(password)
        data.save()

        values = CompanyAdmin.objects.create(company_name=company_name, person_name=person_name, email=email,
                                             mobile=mobile, user=data, password=password,
                                             img=img, user_type=user_type, manager=manager)
        values.save()
        msg = "New Company Created Successfully!"
        return render(request, 'subsuccess.html', {'msg': msg, "pass": password, 'user': user})
    return render(request, 'companyadd.html', {'valu': valu})


def subadmincompanylist(request):
    if not request.user.is_staff:
        return redirect('login_attempt')
    data = CompanyAdmin.objects.filter(manager__id=request.user.id)
    return render(request, 'listcompany.html', {'data': data})


def subadminaddemployee(request):
    if not request.user.is_staff:
        return redirect('login_attempt')
    valu = CompanyAdmin.objects.all()
    if request.method == 'POST':
        manager_id = request.POST.get('manager', None)
        person_name = request.POST.get('person_name', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        img = request.FILES['img']
        manager = User.objects.get(id=manager_id)
        # sub_manager = request.user
        user_type = "is_employee"
        digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        lower_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                      'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                      'z']

        upper_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                      'Z']

        symbol = ['@', '#', '$']

        rand_digit = random.sample(digit, 3)
        rand_upper = random.sample(upper_char, 1)
        rand_lower = random.sample(lower_char, 5)
        rand_symbol = random.sample(symbol, 1)

        digit_value = ''.join([str(i) for i in rand_digit])
        digit_upper = ''.join([str(i) for i in rand_upper])
        digit_lower = ''.join([str(i) for i in rand_lower])
        digit_symbol = ''.join([str(i) for i in rand_symbol])
        password = digit_upper + digit_lower + digit_symbol + digit_value

        user_digit = random.sample(digit, 4)
        user_upper = random.sample(upper_char, 3)
        user_lower = random.sample(lower_char, 5)

        user_value = ''.join([str(i) for i in user_digit])
        user_upper = ''.join([str(i) for i in user_upper])
        user_lower = ''.join([str(i) for i in user_lower])

        user = user_upper + user_lower + user_value

        if User.objects.filter(username=user).first():
            msg = "User Name Already Exists!"
            return render(request, "employeeadd.html", {"msg": msg})
        if User.objects.filter(email=email).first():
            msg = "Email Address Already Exists!"
            return render(request, "employeeadd.html", {"msg": msg})

        data = User.objects.create_user(first_name=person_name, email=email, last_name=mobile, username=user)
        data.set_password(password)
        data.save()

        values = EmployeeAdmin.objects.create(person_name=person_name, email=email, mobile=mobile, user=data,
                                              password=password, img=img, user_type=user_type, manager=manager)
        values.save()
        msg = "New Employee Created Successfully!"
        return render(request, 'subsuccess.html', {'msg': msg, "pass": password, 'user': user})
    return render(request, 'employeeadd.html', {'valu': valu})


def subadminemployeelist(request):
    if not request.user.is_staff:
        return redirect('login_attempt')
    emp = EmployeeAdmin.objects.all()
    return render(request, 'listemployee.html', {'emp': emp})


def subadmin_del_user(request, username):
    if not request.user.is_staff:
        return redirect('login_attempt')
    try:
        u = User.objects.get(username=username)
        u.delete()
        msg = "Delete Data Has Been Successfully!"
        return render(request, 'error.html', {'msg': msg})

    except User.DoesNotExist:
        msg = "User Not Found !"
        return render(request, 'error.html', {"msg": msg})

    except Exception as e:
        return render(request, 'error.html', {'msg': e.message})

    return render(request, 'listcompany.html')


def subadmin_view_details(request, username):
    if not request.user.is_staff:
        return redirect('login_attempt')
    user = User.objects.get(username=username)
    data = AndroidData.objects.filter(user=user)
    return render(request, "sub_admin_view.html", {"data": data})


def subadmin_call_details(request, username):
    if not request.user.is_staff:
        return redirect('login_attempt')
    user = User.objects.get(username=username)
    data = ContactDetails.objects.filter(user=user)
    return render(request, "subadmin_contact_details.html", {'data': data})
