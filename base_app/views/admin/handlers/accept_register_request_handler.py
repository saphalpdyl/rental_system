from django.shortcuts import redirect, reverse
from django.http import HttpRequest
from django.views import View

from base_app.models import (
    RenterRegisterRequests,
    AdminUser,
    RenterRegisterResults,
    ApplicationUser,
    RenterUser,
    Notifications,
)
from base_app.mixins import AuthRequiredMixin, AdminRequiredMixin


class HandleAcceptRegisterRequest(AuthRequiredMixin, AdminRequiredMixin, View):
    def post(self, request: HttpRequest):
        """
        EXTRACT request_id from POST request ✅
        GET RenterRegisterRequests object using that request_id ✅
        CHANGE is_reviewed to TRUE ✅
        CHANGE that user's is_renter value to True ✅
        RETRIEVE the current admin user ✅
        CREATE RenterRequest result and set is_approved to True ✅
        """

        # EXTRACT values from the POST request
        # {
        # "csrfmiddlewaretoken": "~~~~~",
        # "request_id": "~~~~~"  <-- We need this
        # }
        request_id = request.POST["request_id"]

        # Because we are filtering using the PRIMARY KEY i.e request_id
        # we can be sure that only one associated request ( RenterRegisterRequests ) can exist
        # That's why we are using .get() instead of .filter()
        register_request = RenterRegisterRequests.objects.get(reference_id=request_id)

        # Setting the is_reviewed field of the request to True
        register_request.is_reviewed = True

        ################################################################################################
        # current_application_user: ApplicationUser = request.user
        # HOW WAS IT FIXED: here's request.user returns the current user i.e admin
        # However, the value is_renter field to be changed is the ApplicationUser's not admin's
        # Hence, we use the value of register_request.application_user which gives back the user making the request
        requester: ApplicationUser = (
            register_request.application_user
        )  # The one who requested i.e Client not Admin
        requester.is_renter = True
        requester.save()

        # Using the current logged in user ( request.user ) which is an ApplicationUser
        # and filtering the corresponding AdminUser using the FK application_user
        # by comparing it with current ( ApplicationUser ) user.
        current_admin_user = AdminUser.objects.get(application_user=request.user)

        # Created a new Result
        RenterRegisterResults(
            renter_request=register_request,
            reviewed_by=current_admin_user,
            is_approved=True,  # Because we have accepted
        ).save()
        register_request.save()

        # Create a RenterUser
        RenterUser(
            application_user=requester  # Create a corresponding RenterUser for the requester
        ).save()

        # Send a notification
        Notifications(
            notification_for=register_request.application_user,
            message="Transaction request reject",
            desc="Your request to become a renter has been accepted",
        ).save()

        return redirect(reverse("admin_renter_register_list"))