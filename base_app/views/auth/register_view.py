from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View

from base_app.mixins import NoAuthRequiredMixin
from base_app.models import ApplicationUser


class RegisterView(NoAuthRequiredMixin, View):
    """
        GET / Show Login Done
        POST / Done
        Extraction Done
        Create Done
        redirect to Login Done
    """

    def get(self, request: HttpRequest):
        return render(request, "base_app/auth/register.html")

    def post(self, request: HttpRequest):
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
