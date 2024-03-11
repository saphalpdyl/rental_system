from django.shortcuts import redirect, reverse
from django.http import HttpRequest
from django.views import View

from base_app.models import VehicleListingRequests
from base_app.mixins import AuthRequiredMixin, AdminRequiredMixin


class HandleRejectVehicleListingRequest(AuthRequiredMixin, AdminRequiredMixin, View):
    def post(self, request: HttpRequest, request_id: str):
        vehicle_request = VehicleListingRequests.objects.get(reference_id=request_id)
        vehicle_request.vehicle.delete()

        return redirect(reverse("admin_vehicle_listing_request_list"))
