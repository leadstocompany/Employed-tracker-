from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


# Register your models here.


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'user', 'create_at', 'update_at')
    list_filter = ('create_at', 'update_at')


class ContactCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'contact', 'cats', 'mobile', 'create_at', 'update_at')
    list_filter = ('create_at', 'update_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(ContactCategory, ContactCategoryAdmin)
