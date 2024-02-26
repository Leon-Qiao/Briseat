from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/", views.form, name="form"),
    path("log/", views.log, name="log"),
    path("sugg/", views.sugg, name="sugg"),
]