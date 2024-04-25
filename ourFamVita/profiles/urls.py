from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("survey-1/", views.survey1, name="survey1"),
    path("survey-2/", views.survey2, name="survey2"),
    path("survey-3/", views.survey3, name="survey3"),
    path("<int:profile_id>/profile-info/", views.profile_info, name="profile_info"),
    path("<int:profile_id>/", views.profile_delete, name="profile_delete"), 
]
