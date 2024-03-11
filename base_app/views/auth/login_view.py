from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages

from base_app.mixins import NoAuthRequiredMixin


class LoginView(NoAuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "base_app/auth/login.html")

    def post(self, request: HttpRequest):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            # Alert that the user is logged in
            login(request, user)
            messages.success(request, "You have logged in successfully")
            return redirect(reverse("home"))

        messages.error(request, "The user details has gone wrong!")
        return redirect(reverse("login"))
