from django.urls import path

from . import views

app_name = "hn_follow_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("users", views.hn_user_index, name="users"),
    path("users/<str:username>/edit", views.hn_user_edit, name="edit_user"),
    path("users/<str:username>/delete", views.hn_user_delete, name="delete_user"),
    path("submissions", views.submissions, name="submissions"),
]
