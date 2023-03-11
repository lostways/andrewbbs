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
        name="register"
    ),
    path(
        "members/login",
        views.member_login,
        name="login"
    ),
    path(
        "members/otp/<int:pk>/<uuid>",
        views.member_otp,
        name="member_otp"
    ),
    path(
        "members/otp/check",
        views.member_check_otp,
        name="member_check_otp"
    )
]
