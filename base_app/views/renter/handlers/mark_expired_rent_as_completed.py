from django.shortcuts import redirect, reverse
from django.http import HttpRequest
from django.views import View

from base_app.models import VehicleRent, VehicleRentStatus, Vehicles
from base_app.mixins import AuthRequiredMixin


class HandleMarkExpiredRentCompleted(AuthRequiredMixin, View):
    def post(self, request: HttpRequest, vehicle_id: str):
        vehicle = Vehicles.objects.get(reference_id=vehicle_id)
        rent = VehicleRent.objects.get(rent_request__vehicle=vehicle, status=VehicleRentStatus.EXPIRED)

        vehicle.is_available = True
        vehicle.is_booked = False
        vehicle.save()

        rent.status = VehicleRentStatus.COMPLETED
        rent.save()

        return redirect(reverse("home"))