from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest

from base_app.models import ApplicationUser


def home_view(request):
    return render(request, "base_app/home.html")


def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "base_app/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            print("Logged in")

        return render(request, "base_app/home.html")

    """
        GET / Show Login
        POST /
        USERNAME, PASSWORD
        authenticate ->  User or None
        User check ( if user: )
        Login
    """


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone_no = request.POST["phone_no"]
        password = request.POST["password"]

        ApplicationUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_no=phone_no,
            password=password,
        ).save()
        return redirect(reverse("login"))

    return render(request, "base_app/register.html")

    """
        GET / Show Login Done
        POST / Done
        Extraction Done
        Create Done
        redirect to Login Done
    """


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("home"))
