from django.shortcuts import redirect, reverse
from django.http import HttpRequest
from django.views import View

from base_app.models import RenterRegisterRequests
from base_app.mixins import AuthRequiredMixin


class HandleCreateRenterRegisterRequest(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        # Filter RenterRegisterRequests with the condition such that:
        # 1. The user who made the request( application_user ) is the current user ( request.user )
        # 2. The request is pending i.e is_reviewed = False
        register_requests = RenterRegisterRequests.objects.filter(
            application_user=request.user, is_reviewed=False
        )

        # OPTIMAL CASE: register_requests.exists() should be False because in optimal cases no previous requests
        # should have been made

        # SUB-OPTIMAL CASE: register_requests.exists() becomes True and there is 1 item i.e RenterRegisterRequests
        # In this case, this indicates that the requests has already been made before and is yet
        # to be reviewed by the admin

        # ERROR CASE: register_requests.exists() becomes True and there is >1 item.

        # QuerySet<[]> = False
        # QuerySet<[RenterRegisterRequests, ...]> = True
        if register_requests.exists() is False:
            # Create a new request to register as a renter
            RenterRegisterRequests(application_user=request.user).save()

        return redirect(reverse("home"))


