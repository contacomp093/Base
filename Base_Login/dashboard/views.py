from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def index(request):
    profile = request.user.userprofile

    if profile.role == "provider":
        return redirect("dashboard:provider")

    return redirect("dashboard:client")


@login_required
def dashboard_provider(request):
    profile = request.user.userprofile

    if profile.role != "provider":
        return redirect("dashboard:client")

    return render(request, "dashboard/provider_index.html")


@login_required
def dashboard_client(request):
    profile = request.user.userprofile

    if profile.role != "client":
        return redirect("dashboard:provider")

    return render(request, "dashboard/client_index.html")
