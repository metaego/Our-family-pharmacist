from django.urls import path
from users.views import logout, signup, acc_info

urlpatterns = [
    path("logout/", logout),
    path("signup/", signup),
    path("acc_info/", acc_info),
]
