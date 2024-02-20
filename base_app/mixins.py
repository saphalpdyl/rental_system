from django.shortcuts import reverse, redirect
from django.http import HttpRequest
from django.contrib import messages


# Check if the user is authed before rendering the view
class AuthRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please Log in first")
            return redirect(reverse("login"))
        return super().dispatch(request, *args, **kwargs)


# Check if the user is not authenticated before rendering the view
class NoAuthRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "User is already logged in!")
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "The current user is not admin")
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)
