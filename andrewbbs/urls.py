from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.index,
        name="screen-list",
    ),
    path(
        "<slug:slug>",
        views.detail,
        name="screen-detail",
    ),
]
