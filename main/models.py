from operator import contains

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# @superuser_required()
# @staff_member_required
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    is_admin = models.BooleanField("Is Admin", default=False)
    is_subadmin = models.BooleanField("Is Subadmin", default=False)
    is_company = models.BooleanField("Is Company", default=False)
    is_employee = models.BooleanField("Is Employee", default=False)
    cats = models.IntegerField(default=0, blank=True, null=True)
    objects = UserManager()  
    def __str__(self):
        return self.username
    # def save(self, *args, **kwargs):
       
    #     # Ensure password is hashed if it has been set/changed
    #     if self.pk is None and self.password:
    #         self.set_password(self.password)
    #     else:
    #         existing_user = User.objects.filter(pk=self.pk).first()
    #         if existing_user and existing_user.password != self.password:
    #             self.set_password(self.password)
    #     super().save(*args, **kwargs)
    #
   

# https://github.com/MamaMoh/Role_based_login_system/blob/master/account/models.py


class SubAdmin(models.Model):
    user = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE, related_name="SubAdmin.user_name +"
    )
    manager = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE, related_name="superusername +"
    )
    name = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True, editable=False)
    email = models.EmailField(max_length=200, unique=True, blank=True)
    mobile = models.CharField(max_length=13, unique=True, blank=True)
    img = models.ImageField(upload_to="subadmin/", blank=True)
    user_type = models.CharField(max_length=200, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    udpate_at = models.DateTimeField(auto_now=True)


class CompanyAdmin(models.Model):
    user = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE, related_name="company.user_name +"
    )
    # manager = models.ForeignKey(SubAdmin, on_delete=models.CASCADE, blank=True)
    manager = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name="subadmin.sub_manager +",
    )
    user_type = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True, editable=False)
    company_name = models.CharField(max_length=200, blank=True)
    person_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=13, blank=True)
    email = models.CharField(max_length=200, blank=True)
    img = models.ImageField(upload_to="company/", blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    udpate_at = models.DateTimeField(auto_now=True)


class EmployeeAdmin(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name="employee.user_name +"
    )
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company.sub_manager +"
    )
    user_type = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True, editable=False)
    person_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=13, blank=True)
    email = models.CharField(max_length=200, blank=True)
    img = models.ImageField(upload_to="employee/", blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    udpate_at = models.DateTimeField(auto_now=True)


class AndroidData(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="android_data +",
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)

    date = models.DateTimeField(null=True)
    user_type = models.CharField(
        max_length=200, blank=True, null=True, default="is_employee"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Manage AndroidData "
        # ordered = ['-create_at']


class ContactDetails(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="android_data +",
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=200, blank=True, null=True, default="is_employee"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Manage ContactDetails"
        # make user and mobile number unique
        constraints = [
            models.UniqueConstraint(fields=["user", "mobile"], name="unique_contact")
        ]
