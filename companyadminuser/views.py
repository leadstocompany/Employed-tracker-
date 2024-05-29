import random
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from main.models import *
from .models import *


# Create your views here.

def companyadminpanel(request):
    if not request.user.is_authenticated:
        if CompanyAdmin.objects.filter(user_type="is_company"):
            return redirect('login_attempt')
    cats = Category.objects.filter(user__id=request.user.id)
    return render(request, 'companypanel.html', {'cats': cats})


def companyaddemployee(request):
    if not request.user.is_authenticated:
        return redirect('login_attempt')

    valu = CompanyAdmin.objects.all()
    if request.method == 'POST':
        manager_id = request.POST.get('manager', None)
        person_name = request.POST.get('person_name', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        img = request.FILES['img']
        manager = CompanyAdmin.objects.get(id=manager_id)

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
            return render(request, "companyemployeeadd.html", {"msg": msg})
        if User.objects.filter(email=email).first():
            msg = "Email Address Already Exists!"
            return render(request, "companyemployeeadd.html", {"msg": msg})

        data = User.objects.create_user(first_name=person_name, email=email, last_name=mobile, username=user)
        data.set_password(password)
        data.save()

        values = EmployeeAdmin.objects.create(person_name=person_name, email=email, mobile=mobile, user=data,
                                              password=password, img=img, user_type=user_type, manager=manager)
        values.save()
        msg = "New Employee Created Successfully!"
        return render(request, 'companysuccess.html', {'msg': msg, "pass": password, 'user': user})
    return render(request, 'companyemployeeadd.html', {'valu': valu})


def companyemployeelist(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_attempt')
    # print(request.user)
    # sub_manager = CompanyAdmin.objects.get(user_name=request.user)
    # print(sub_manager)
    # sub_manager = CompanyAdmin.objects.get(id=id)
    # print(sub_manager,"Company Username")
    # emp = EmployeeAdmin.objects.filter(sub_manager=sub_manager)
    emp = EmployeeAdmin.objects.all().filter(manager__id=request.user.id)
    print(emp)
    return render(request, 'companyemployeelist.html', {'emp': emp})


# https://stackoverflow.com/questions/25345392/how-to-add-url-parameters-to-django-template-url-tag


def company_del_user(request, username):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    try:
        u = User.objects.get(username=username)
        u.delete()
        msg = "Delete Data Has Been Successfully!"
        return render(request, 'companyerror.html', {'msg': msg})

    except User.DoesNotExist:
        msg = "User Not Found !"
        return render(request, 'companyerror.html')

    except Exception as e:
        return render(request, 'companyerror.html', {'err': e.message})

    return render(request, 'companyemployeelist.html')


def company_view_details(request, username):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    user = User.objects.get(username=username)
    data = AndroidData.objects.filter(user=user)
    return render(request, "company_view_details.html", {"data": data})


def Company_call_details(request, username):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    user = User.objects.get(username=username)
    data = ContactDetails.objects.filter(user=user)
    return render(request, "company_contact_details.html", {'data': data})


# @staticmethod
def master_contact_details(request):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    # user = User.objects.get(username=username)
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        type = request.POST.get('type')
        mobile = request.POST.get('mobile')
        create_at = request.POST.get('create_at')
        duration = request.POST.get('duration')

        # if name and category is not None:
        #     data = AndroidData.objects.filter(name=name).filter(category=category)
        #     return render(request, "master_contact_details.html", {'data': data})

        # if type and mobile is not None:
        #     data = AndroidData.objects.filter(type=type).filter(mobile=mobile)
        cat = AndroidData.objects.order_by().values('category').annotate(Count('category'))
        calltype = AndroidData.objects.order_by().values('type').annotate(Count('type'))
        umobile = AndroidData.objects.order_by().values('mobile').annotate(Count('mobile'))
        dtimes = AndroidData.objects.order_by().values('create_at').annotate(Count('create_at'))
        calldur = AndroidData.objects.order_by().values('duration').annotate(Count('duration'))
        pname = AndroidData.objects.order_by().values('name').annotate(Count('name'))
        data = AndroidData.objects.filter(
            Q(category__icontains=category) | Q(type__icontains=type) | Q(mobile__icontains=mobile) | Q(
                create_at__icontains=create_at) | Q(duration__icontains=duration) | Q(name__icontains=name))
        return render(request, "master_contact_details.html", {'data': data, 'cat': cat, 'calltype':calltype, 'umobile':umobile, 'dtimes':dtimes, 'calldur':calldur, 'pname':pname})
        # multiple_q = Q(Q(name__icontains=name) | Q(category__icontains=category) | Q(type__icontains=type) | Q(mobile__icontains=mobile) | Q(create_at__icontains=create_at) | Q(duration__icontains=duration))
        # data = AndroidData.objects.filter(multiple_q)
        # return render(request, "master_contact_details.html", {'data': data})
    else:
        print("error")
        data = AndroidData.objects.all()
        # values = AndroidData.objects.distinct('category')
        cat = AndroidData.objects.order_by().values('category').annotate(Count('category'))
        calltype = AndroidData.objects.order_by().values('type').annotate(Count('type'))
        umobile = AndroidData.objects.order_by().values('mobile').annotate(Count('mobile'))
        dtimes = AndroidData.objects.order_by().values('create_at').annotate(Count('create_at'))
        calldur = AndroidData.objects.order_by().values('duration').annotate(Count('duration'))
        pname = AndroidData.objects.order_by().values('name').annotate(Count('name'))
        # var = list(set(cats))
        # data = list(set(value))
        return render(request, "master_contact_details.html", {'data': data, 'cat': cat, 'calltype':calltype, 'umobile':umobile, 'dtimes':dtimes, 'calldur':calldur, 'pname':pname})

    return render(request, "master_contact_details.html")


def create_category(request):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        var = User.objects.get(username=request.user)

        # if Category.objects.filter(name=name):
        #     msg = "Category Already Exists"
        #     return render(request, 'create_category.html', {'msg': msg})
        if var.cats == 5:
            msg = "Can't Create More Category!"
            return render(request, 'create_category.html', {'msg': msg})
        data = Category.objects.create(name=name, user=user)
        data.save()

        var.cats = var.cats + 1
        var.save()

        return redirect('companyadminpanel')
    return render(request, 'create_category.html')


def contact_category(request, slug):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    cats = Category.objects.get(slug=slug)
    data = ContactCategory.objects.filter(cats=cats)
    return render(request, 'contact_category.html', {"data": data})


def add_contact_category(request):
    if not request.user.is_authenticated:
        return redirect('login_attempt')
    cats = Category.objects.all()
    emp = EmployeeAdmin.objects.all()
    cnt = ContactDetails.objects.all()
    if request.method == 'POST':
        cats_id = request.POST.get('cats', None)
        contact_id = request.POST.get('contact', None)
        user_id = request.POST.get('user', None)
        cats = Category.objects.get(id=cats_id)
        contact = ContactDetails.objects.get(id=contact_id)
        user = User.objects.get(id=user_id)
        data = ContactCategory.objects.create(cats=cats, contact=contact, user=user)
        data.save()
        return redirect('companyadminpanel')
    return render(request, 'add_contact_category.html', {'cats': cats, 'emp': emp, 'cnt': cnt})

#
# def terms_condition(request):
#     return render(request, 'terms-condition.html')
#
# def privacy_policy(request):
#     return render(request, 'privacy-policy.html')
