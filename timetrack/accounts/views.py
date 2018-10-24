from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from timetrack import theme


def login_view(request):

    if User.objects.count() == 0:
        return redirect("accounts:register")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("projects:list")

    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", theme.apply({"form": form}))


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("projects:list")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", theme.apply({"form": form}))
