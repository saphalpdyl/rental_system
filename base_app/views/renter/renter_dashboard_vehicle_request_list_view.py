from django.shortcuts import redirect, reverse, render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib import messages

from base_app.models import (
    Vehicles,
    VehicleRentingRequests,
    RentingStatus,
    Transactions,
    TransactionStatus,
    TransactionRequest,
    Notifications,
    NotificationType
)
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

    def post(self, request: HttpRequest, vehicle_id: str) -> HttpResponse:
        try:
            renting_request = VehicleRentingRequests.objects.get(reference_id=request.POST['request_id'])

            # Setting the request as approved
            renting_request.status = RentingStatus.APPROVED
            renting_request.save()

            # Setting other request are not approved
            # Error: 01
            # other_requests = VehicleRentingRequests.objects.filter(vehicle=renting_request.vehicle, status=RentingStatus.PENDING).exclude(renting_request)
            other_requests = VehicleRentingRequests.objects.filter(vehicle=renting_request.vehicle, status=RentingStatus.PENDING).exclude(reference_id=renting_request.reference_id)
            for rrequest in other_requests:
                rrequest.status = RentingStatus.REJECTED
                rrequest.save()

            # Create the transaction request and the notification
            transaction_request = TransactionRequest.objects.create(
                renting_request=renting_request,
            )

            # Setting the vehicle as booked
            renting_request.vehicle.is_booked = True
            renting_request.vehicle.is_available = False
            renting_request.save()

            Notifications(
                notification_for=renting_request.buyer,
                message="{} has accepting your request for renting {}".format(
                    request.user.username,
                    renting_request.vehicle.vehicle_name,
                ),
                desc="Accept to be redirected to payment window.",
                notification_type=NotificationType.TRANSACTION_REQUEST,
                related_transaction_request=transaction_request
            ).save()

            return redirect(reverse("renter_dashboard_vehicle_list"))

        except Exception as e:
            messages.error(request, f"ERROR: {e}")
            return redirect(reverse("renter_dashboard_vehicle_request_list", args=[vehicle_id]))
