
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.post, name="post"),
    path("<int:user_id>", views.user_page, name="user_page"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following")
]
