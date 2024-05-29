from django.contrib.auth.models import AbstractUser
from django.db import models


# @superuser_required()
# @staff_member_required

class User(AbstractUser):
    is_admin = models.BooleanField('Is Admin', default=False)
    is_subadmin = models.BooleanField('Is Subadmin', default=False)
    is_company = models.BooleanField('Is Company', default=False)
    is_employee = models.BooleanField('Is Employee', default=False)
    cats = models.IntegerField(default=0, blank=True, null=True)

# https://github.com/MamaMoh/Role_based_login_system/blob/master/account/models.py

class SubAdmin(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="SubAdmin.user_name +")
    manager = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="superusername +")
    name = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True, editable=False)
    email = models.EmailField(max_length=200, unique=True, blank=True)
    mobile = models.CharField(max_length=13, unique=True, blank=True)
    img = models.ImageField(upload_to='subadmin/', blank=True)
    user_type = models.CharField(max_length=200, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    udpate_at = models.DateTimeField(auto_now=True)


class CompanyAdmin(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="company.user_name +")
    # manager = models.ForeignKey(SubAdmin, on_delete=models.CASCADE, blank=True)
    manager = models.ForeignKey(User, blank=False, on_delete=models.CASCADE,
                                related_name="subadmin.sub_manager +")
    user_type = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True, editable=False)
    company_name = models.CharField(max_length=200, blank=True)
    person_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=13, blank=True)
    email = models.CharField(max_length=200, blank=True)
    img = models.ImageField(upload_to='company/', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    udpate_at = models.DateTimeField(auto_now=True)


class EmployeeAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="employee.user_name +")
    # manager = models.ForeignKey(CompanyAdmin, on_delete=models.CASCADE, blank=True, editable=False)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company.sub_manager +")
    user_type = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True, editable=False)
    person_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=13, blank=True)
    email = models.CharField(max_length=200, blank=True)
    img = models.ImageField(upload_to='employee/', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    udpate_at = models.DateTimeField(auto_now=True)


class AndroidData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="android_data +")
    name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.CharField(max_length=200, blank=True, null=True, default="is_employee")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Manage AndroidData "
        # ordered = ['-create_at']


class ContactDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="android_data +")
    name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=200, blank=True, null=True, default="is_employee")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Manage ContactDetails"
