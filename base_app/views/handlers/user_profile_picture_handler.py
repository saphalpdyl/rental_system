from django.shortcuts import redirect, reverse
from django.views import View
from django.http import HttpRequest
from django.contrib import messages

from base_app.models import ApplicationUser
from base_app.mixins import AuthRequiredMixin


class HandleProfilePictureChange(AuthRequiredMixin, View):
    def post(self, request: HttpRequest):
        new_profile_img = request.FILES.get("new_profile_picture")
        if new_profile_img:
            user: ApplicationUser = request.user
            user.profile_picture = new_profile_img
            user.save()
            messages.success(request, "Profile picture updated!")
        else:
            messages.error(request, "ERROR: Couldn't extract file")
        return redirect(reverse("user_profile"))


class HandleProfilePictureRemove(AuthRequiredMixin, View):
    def post(self, request: HttpRequest):
        user: ApplicationUser = request.user
        user.profile_picture = "uploads/images/default_user_pp.jpg"
        user.save()
        return redirect(reverse("user_profile"))
