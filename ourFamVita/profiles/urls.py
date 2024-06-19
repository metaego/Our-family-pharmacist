from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("survey-1/", views.survey1, name="survey1"),
    path("survey-2/", views.survey2, name="survey2"),
    path("survey-3/", views.survey3, name="survey3"),
    path("<int:profile_id>/profile-edit-1/", views.profile_edit1, name="profile_edit1"),
    path("<int:profile_id>/profile-edit-2/", views.profile_edit2, name="profile_edit2"),
    path("<int:profile_id>/profile-edit-3/", views.profile_edit3, name="profile_edit3"),
    path("<int:profile_id>/", views.profile_delete, name="profile_delete"), 
]
