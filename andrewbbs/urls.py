from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.index,
        name="screen-list",
    ),
    path(
        "screen/<slug:slug>",
        views.detail,
        name="screen-detail",
    ),
    path(
        "access",
        views.access,
        name="access",
    ),
    path(
        "members/register",
        views.member_register,
        name="member-register"
    ),
    path(
        "members/login",
        views.member_login,
        name="member-login"
    ),
    path(
        "members/otp/<int:pk>",
        views.member_login_verify,
        name="member-login-verify"
    ),
    path(
        "members/logout",
        views.member_logout,
        name="member-logout"
    ),
]
