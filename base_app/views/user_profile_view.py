from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest
from django.contrib import messages

from base_app.models import (
    ApplicationUser,
)

from base_app.mixins import AuthRequiredMixin


class UserProfileView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        user: ApplicationUser = request.user
        return render(request, "base_app/user_profile.html", {
            "user": user,
        })

    def post(self, request: HttpRequest):
        user: ApplicationUser = request.user

        # Validate username
        new_username = request.POST.get("username")
        if new_username and new_username != request.user.username:
            # The username has been changed
            if ApplicationUser.objects.filter(username=new_username).exists():
                messages.error(request, f"User with username {new_username} already exists")
                return redirect(reverse("user_profile"))

        # Validate phone number
        new_phone = request.POST.get("phone")
        if new_phone and new_phone != request.user.phone:
            if len(new_phone) < 10 or not new_phone.isnumeric():
                messages.error(request, "Invalid phone number")
                return redirect(reverse("user_profile"))

        # Validate password
        new_pass = request.POST.get("new_password")
        new_pass_confirm = request.POST.get("new_password_confirm")
        if new_pass and new_pass_confirm:
            if new_pass != new_pass_confirm or len(new_pass) < 6:
                messages.error(request, "Invalid or mismatching password")
                return redirect(reverse("user_profile"))
            else:
                messages.success(request, "Successfully changed password")
                user.set_password(new_pass)

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = new_username
        user.phone = new_phone
        user.save()

        messages.success(request, "Profile updated!")
        return redirect(reverse("user_profile"))
