from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

# router = DefaultRouter()
# router.register('androiddata', AndroidDataView, basename='androiddata')
# router.register('contact/details', ContactDetailsView, basename='ContactDetailsView')

urlpatterns = [
    # path('terms/condition', terms_condition, name='{% url 'terms_condition' %}'),
    # path('privacy/policy', privacy_policy, name='{% url 'privacy_policy' %}'),
    # ath('disclaimer', disclaimer, name='{% url 'disclaimer' %}'),
    path("adminpanel", adminpanel, name="adminpanel"),
    path("create/subadmin", createstaff, name="createstaff"),
    path("", login_attempt, name="login_attempt"),
    path("logout", logout_view, name="logout_view"),
    path("change/pass", change_pass, name="change_pass"),
    path("subadminlist", subadminlist, name="subadminlist"),
    path("addcompany", addcompany, name="addcompany"),
    path("companylist", companylist, name="companylist"),
    path("addemployee", addemployee, name="addemployee"),
    path("employeelist", employeelist, name="employeelist"),
    # path('delete/user', del_user, name="delete_user"),
    path("del_user/<username>", del_user, name="delete_user"),
    path("login", LoginView.as_view(), name="loginview"),
    path("view/details/<username>", view_details, name="view_details"),
    path("contact/details/<username>", call_details, name="call_details"),
    path(
        "contact/details",
        ContactDetailsView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
                "post": "create",
                "get": "list",
            }
        ),
        name="ContactDetailsView",
    ),
    path(
        "androiddata",
        AndroidDataView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
                "post": "create",
                "get": "list",
            }
        ),
        name="androiddata",
    ),
    path(
        "contact/list/add",
        AddMultipleContactView.as_view(),
        name="Add Multiple Contact",
    ),
    path(
        "callLogs/list/add",
        AddMultipleCallLogs.as_view(),
        name="Add Multiple Call Logs",
    ),
]
