from django.http import HttpRequest
from django.shortcuts import redirect, reverse, render
from django.views import View

from base_app.mixins import AuthRequiredMixin, AdminRequiredMixin
from base_app.models import RenterRegisterRequests


class AdminRenterRegisterRequestsListView(AuthRequiredMixin, AdminRequiredMixin, View):
    def get(self, request: HttpRequest):
        # Filter Renter Register Requests on the basis of the condition that the
        # request is pending i.e is_reviewed = False
        register_requests = RenterRegisterRequests.objects.filter(is_reviewed=False)

        return render(
            request,  # REQUEST
            "base_app/admin/admin_renter_register_requests.html",  # TEMPLATE
            {"requests": register_requests},  # CONTEXT
        )

        return redirect(reverse("home"))
