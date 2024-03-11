from django.shortcuts import redirect, reverse
from django.contrib.auth import logout
from django.http import HttpRequest
from django.contrib import messages
from django.views import View

from base_app.mixins import AuthRequiredMixin


class HandleLogout(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            messages.success(request, "Logged out Successfully!")
            logout(request)
        return redirect(reverse("home"))
