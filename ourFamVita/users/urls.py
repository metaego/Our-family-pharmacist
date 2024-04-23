from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("acc-info/", views.acc_info, name="acc_info"),
]
