from django.shortcuts import redirect, reverse, render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib import messages

from base_app.models import Vehicles, VehicleRentingRequests, RentingStatus
from base_app.mixins import AuthRequiredMixin, RenterRequiredMixin


class RenterDashboardVehicleRequestListView(AuthRequiredMixin, RenterRequiredMixin, View):
    def get(self, request: HttpRequest, vehicle_id: str) -> HttpResponse:
        try:
            vehicle = Vehicles.objects.get(reference_id=vehicle_id)
            renting_requests = VehicleRentingRequests.objects.filter(
                status=RentingStatus.PENDING,
                vehicle=vehicle,
            )

            return render(request, "base_app/renter/renter_dashboard_vehicle_request_list.html", {
                "renting_requests": renting_requests,
                "vehicle": vehicle,
            })
        except Exception as e:
            messages.error(request, f"ERROR: {e}")
            return redirect(reverse("renter_dashboard_vehicle_request_list", args=[vehicle_id]))