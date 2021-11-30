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
]
