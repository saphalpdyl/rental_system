from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.utils import timezone

from base_app.mixins import AuthRequiredMixin, RenterRequiredMixin
from base_app.models import (
    VehicleRent,
    VehicleRentStatus,
    Notifications,
    NotificationType,
    TransactionRequest,
    TransactionType,
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

            transaction_request = TransactionRequest.objects.create(
                renting_request=rent.rent_request,
                days=extension_days,
                price_per_day=rent.rent_request.vehicle.price,
                request_type=TransactionType.EXTENSION,
            )

            Notifications(
                notification_for=rent.rent_request.buyer,
                message=f"Your vehicle rent for {rent.rent_request.vehicle.vehicle_name} has been extended by {extension_days} days. Pay for the extension as soon as possible.",
                desc="Please return the vehicle on {rent.expires_at} as close to the expiry time as possible",
                related_transaction_request=transaction_request,
                notification_type=NotificationType.TRANSACTION_REQUEST,
            ).save()

            Notifications(
                notification_for=rent.rent_request.vehicle.owner.application_user,
                message=f"You have extended {rent.rent_request.buyer.first_name}'s rent by {extension_days} days",
                desc=""
            ).save()
            
            messages.success(request, f"Rent extended by {extension_days} days")
            return redirect(reverse("renter_dashboard_vehicle_list"))
        except Exception as e:
            print(e)
            messages.error(request, "Invalid input data")
            return redirect(reverse("renter_dashboard_vehicle_list"))