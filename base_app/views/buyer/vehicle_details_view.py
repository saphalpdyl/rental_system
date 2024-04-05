from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.utils import timezone

from base_app.models import Vehicles, VehicleRentingRequests, RentingStatus, Notifications
from base_app.mixins import AuthRequiredMixin


class BuyerVehicleDetailsView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest, vehicle_id: str) -> HttpResponse:
        try:
            vehicle = Vehicles.objects.get(reference_id=vehicle_id)
            previous_request = VehicleRentingRequests.objects.filter(
                buyer=request.user,
                status=RentingStatus.PENDING,
                vehicle=vehicle
            )

            return render(request, "base_app/buyer/vehicle_details.html", {
                "vehicle": vehicle,
                "is_previous_request_exists": previous_request.exists(),
            })
        except Exception as e:
            messages.error(request, f"ERROR: {e}")
            return redirect(reverse("home"))

    # INFO: Handles renting requests creation
    def post(self, request: HttpRequest, vehicle_id: str) -> HttpResponse:
        # If renting request already exist do nothing
        # How to identify a pre existing request ?
        #   1. Filter all request where buyer is our current user(request.user)
        #   2. Filter all request which have status as PENDING
        try:
            vehicle = Vehicles.objects.get(reference_id=vehicle_id)
            previous_request = VehicleRentingRequests.objects.filter(
                buyer=request.user,
                status=RentingStatus.PENDING,
                vehicle=vehicle,
            )

            if previous_request.exists():
                raise Exception("A pending request already exists for this user")

            # If the request does not exists
            # Create a renting request
            VehicleRentingRequests.objects.create(
                buyer=request.user,
                vehicle=vehicle,
                renting_period=timezone.timedelta(minutes=5),
                status=RentingStatus.PENDING,
            )
            messages.success(request, "Your request has been sent to the renter")

            Notifications(
                notification_for=vehicle.owner.application_user,
                message=f"Somebody requested renting for your car {vehicle.vehicle_name}",
            ).save()

            return redirect(reverse("buyer_vehicle_details", args=[vehicle_id]))
        except Exception as e:
            messages.error(request, f"Error while renting: {e}")
            return redirect(reverse("buyer_vehicle_details", args=[vehicle_id]))
