from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("provider/", views.dashboard_provider, name="provider"),
    path("client/", views.dashboard_client, name="client"),
]
