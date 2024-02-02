from django.shortcuts import reverse, redirect
from django.http import HttpRequest
from django.contrib import messages


class AuthRequiredMixin:
    redirect_if_not_authed = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please Log in first")
            if self.redirect_if_not_authed is not None:
                return redirect(self.redirect_if_not_authed)
            return redirect(reverse("login"))
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    redirect_if_not_admin = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "The current user is not admin")
            if self.redirect_if_not_admin is not None:
                return redirect(self.redirect_if_not_authed)
            return redirect(reverse("login"))
        return super().dispatch(request, *args, **kwargs)
