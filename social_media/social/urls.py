from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_post, name="create_post"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("like/<int:id>/", views.like_post, name="like_post"),
    path("comment/<int:id>/", views.add_comment, name="add_comment"),
]
