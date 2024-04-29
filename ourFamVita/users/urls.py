from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("acc-info/", views.acc_info, name="acc_info"),
    path("signout/", views.signout, name="signout"),
]
