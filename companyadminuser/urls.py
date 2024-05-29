from django.urls import path
from .views import *

urlpatterns = [
    path('company/add/employee', companyaddemployee, name='companyaddemployee'),
    path('company/employee/list', companyemployeelist, name='companyemployeelist'),
    path('company/admin/panel', companyadminpanel, name='companyadminpanel'),
    path('company/user/delete/<username>', company_del_user, name="company_del_user"),
    path('company/user/details/<username>', company_view_details, name="company_view_details"),
    path('company/user/contact/<username>', Company_call_details, name="company_call_details"),
    path('master/contact/details', master_contact_details, name='master_contact_details'),
    path('create/category', create_category, name='create_category'),
    path('contact/category/<slug>', contact_category, name="contact_category"),
    path("add/contact/category", add_contact_category, name="add_contact_category")
]
