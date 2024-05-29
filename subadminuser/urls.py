from django.urls import path
from .views import *

urlpatterns = [
    path('sub/admin/add/company', subadminaddcompany, name='subadminaddcompany'),
    path('sub/admin/company/list', subadmincompanylist, name='subadmincompanylist'),
    path('sub/admin/add/employee', subadminaddemployee, name='subadminaddemployee'),
    path('sub/admin/employee/list', subadminemployeelist, name='subadminemployeelist'),
    path('sub/admin/panel', subadminpanel, name='subadminpanel'),
    path('sub/admin/delete/<username>', subadmin_del_user, name="subadmin_del_user"),
    path('sub/admin/view/details/<username>', subadmin_view_details, name="subadmin_view_details"),
    path('sub/admin/contact/details/<username>', subadmin_call_details, name="subadmin_call_details"),
]