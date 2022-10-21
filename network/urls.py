
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("<int:id>/comments", views.comments, name="comments"),
    path("<int:id>create_comment", views.create_comment, name="create_comment"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("<int:id>/increase_likes", views.increase_likes, name="increase_likes"),
    path("<int:id>/decrease_likes", views.decrease_likes, name="decrease_likes"),
    path("profile/<str:username>/follow_toggle", views.follow_toggle, name="follow_toggle"),
    path("following_posts", views.following_posts, name="following_posts"),
]
