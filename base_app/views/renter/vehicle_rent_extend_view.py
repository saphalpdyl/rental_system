from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.utils import timezone

from base_app.mixins import AuthRequiredMixin, RenterRequiredMixin
from base_app.models import (
    VehicleRent,
    VehicleRentStatus,
)


class VehicleRentExtendView(AuthRequiredMixin, RenterRequiredMixin, View):
    def get(self, request: HttpRequest, vehicle_rent_id: str):
        vehicle_rent = VehicleRent.objects.get(reference_id=vehicle_rent_id);

        if vehicle_rent.status == VehicleRentStatus.COMPLETED:
            messages.error(request, "Vehicle rent has already been marked completed.")
        
        return render(request, "base_app/renter/vehicle_rent_extend.html", {
            "rent": vehicle_rent
        })

    def post(self, request: HttpRequest, vehicle_rent_id: str):
        try:
            rent = VehicleRent.objects.get(reference_id=vehicle_rent_id)
            extension_days = int(request.POST['vehicle_extend_by'])

            # TODO: Change from minutes to days
            rent.expires_at = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=extension_days)
            rent.status = VehicleRentStatus.ACTIVE
            rent.save()
            
            messages.success(request, f"Rent extended by {extension_days} days")
            return redirect(reverse("renter_dashboard_vehicle_list"))
        except Exception as e:
            print(e)
            messages.error(request, "Invalid input data")
            return redirect(reverse("renter_dashboard_vehicle_list"))