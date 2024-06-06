from django.contrib import admin
from .models import *
# from import_export.admin import ExportActionMixin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import *

# Register your models here.


class SubAdminPanel(admin.ModelAdmin):
    list_display = (
        "user",
        "id",
        "manager",
        "name",
        "password",
        "create_at",
        "udpate_at",
    )
    list_filter = ("create_at", "udpate_at")
    # readonly_fields = ('user', 'manager', 'user_type')


class CompanyAdminPanel(ImportExportModelAdmin):
    list_display = (
        "user",
        "id",
        "manager",
        "company_name",
        "person_name",
        "password",
        "create_at",
        "udpate_at",
    )
    list_filter = ("create_at", "udpate_at")
    # readonly_fields = ('user', 'manager', 'user_type')


class EmployeeAdminPanel(ImportExportModelAdmin):
    list_display = (
        "user",
        "id",
        "manager",
        "person_name",
        "password",
        "create_at",
        "udpate_at",
    )
    list_filter = ("create_at", "udpate_at")
    # readonly_fields = ('user', 'manager', 'user_type')


class AndroidDataPanel(ImportExportModelAdmin):
    list_display = (
        "user",
        "id",
        "duration",
        "mobile",
        "name",
        "user_type",
        "create_at",
        "update_at",
    )
    list_filter = ("create_at", "update_at")
    actions = ["delete_model"]

    def delete_queryset(self, request, queryset):
        queryset.delete()

    def delete_model(self, request, obj):
        obj.delete()


class ContactDetailsAdmin(ImportExportModelAdmin):
    list_display = ("user", "id", "name", "category", "mobile", "create_at")
    list_filter = ("create_at", "update_at", "category")


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "password",
            "is_admin",
            "is_subadmin",
            "is_company",
            "is_employee",
            "cats",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "email",
            "password",
            "is_admin",
            "is_subadmin",
            "is_company",
            "is_employee",
            "cats",
        )


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "username",
        "email",
        "is_admin",
        "is_subadmin",
        "is_company",
        "is_employee",
        "cats",
    )

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_subadmin', 'is_company', 'is_employee')

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' in self.cleaned_data:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_subadmin', 'is_company', 'is_employee', 'groups', 'user_permissions', 'cats')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('email',)
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
# class CustomUserAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_subadmin', 'is_company', 'is_employee', 'groups', 'user_permissions', 'cats')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )

# admin.site.register(User, CustomUserAdmin)

admin.site.register(SubAdmin, SubAdminPanel)
admin.site.register(CompanyAdmin, CompanyAdminPanel)
admin.site.register(EmployeeAdmin, EmployeeAdminPanel)
admin.site.register(AndroidData, AndroidDataPanel)
admin.site.register(ContactDetails, ContactDetailsAdmin)
# admin.site.register(User)
