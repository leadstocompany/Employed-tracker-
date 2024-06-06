from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from import_export.admin import ExportActionMixin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from import_export.admin import ImportExportModelAdmin

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


admin.site.register(SubAdmin, SubAdminPanel)
admin.site.register(CompanyAdmin, CompanyAdminPanel)
admin.site.register(EmployeeAdmin, EmployeeAdminPanel)
admin.site.register(AndroidData, AndroidDataPanel)
admin.site.register(ContactDetails, ContactDetailsAdmin)
admin.site.register(User)
