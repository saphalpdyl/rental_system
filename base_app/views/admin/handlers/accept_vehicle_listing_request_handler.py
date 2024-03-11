from django.shortcuts import redirect, reverse
from django.http import HttpRequest
from django.views import View

from base_app.models import VehicleListingRequests
from base_app.mixins import AuthRequiredMixin, AdminRequiredMixin


class HandleAcceptVehicleListingRequest(AuthRequiredMixin, AdminRequiredMixin, View):
    def post(self, request: HttpRequest, request_id: str):
        if request.user.is_authenticated:
            if request.user.is_admin:
                vehicle_request = VehicleListingRequests.objects.get(reference_id=request_id)

                vehicle = vehicle_request.vehicle
                vehicle_request.is_reviewed = True
                vehicle.can_be_listed = True

                vehicle.save()
                vehicle_request.save()

                return redirect(reverse("admin_vehicle_listing_request_list"))
