from django.shortcuts import redirect, reverse
from django.http import HttpRequest
from django.views import View

from base_app.models import RenterRegisterRequests, AdminUser, RenterRegisterResults, Notifications
from base_app.mixins import AuthRequiredMixin, AdminRequiredMixin


class HandleRejectRegisterRequest(AuthRequiredMixin, AdminRequiredMixin, View):
    def post(self, request: HttpRequest):
        """
        EXTRACT request_id from POST request ✅
        GET RenterRegisterRequests object using that request_id ✅
        CHANGE is_reviewed in RenterRegisterRequest to True ✅
        CREATE new RenterRegisterResult and set the is_approved to False ✅
        """
        request_id = request.POST["request_id"]
        register_request = RenterRegisterRequests.objects.get(reference_id=request_id)
        register_request.is_reviewed = True

        # Get ApplicationUser from request.user and get its
        # corresponding AdminUser object
        current_admin_user = AdminUser.objects.get(application_user=request.user)

        RenterRegisterResults(
            renter_request=register_request,
            reviewed_by=current_admin_user,
            is_approved=False,  # Because the request was rejected
        ).save()
        register_request.save()

        Notifications(
            notification_for=register_request.application_user,
            message="Transaction request reject",
            desc="Your request to become a renter has been rejected",
        ).save()

        return redirect(reverse("admin_renter_register_list"))
