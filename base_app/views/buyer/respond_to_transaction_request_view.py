from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db import transaction as transaction_module

from base_app.models import (
    ApplicationUser,
    TransactionRequest,
    TransactionStatus,
    Transactions,
    Notifications,
    NotificationType,
    VehicleRent,
)
from base_app.mixins import AuthRequiredMixin


class TransactionRequestRespondView(AuthRequiredMixin, View):
    def post(self, request: HttpRequest, request_id: str) -> HttpResponse:
        with transaction_module.atomic():
            # Create a transaction
            # Create two notifications
            transaction_request = TransactionRequest.objects.get(reference_id=request_id)
            transaction = Transactions.objects.create(
                transaction_request=transaction_request,
                pidx="aausdhwuagduysadas",
                expires_in=29871283,
            )

            transaction_request.status = TransactionStatus.COMPLETED
            transaction_request.save()

            Notifications(
                notification_for=transaction_request.renting_request.buyer,
                message="Payment completed!",
                desc=f"The payment for {transaction_request.renting_request.vehicle.vehicle_name} is complete",
                related_transaction_request=transaction_request,
                notification_type=NotificationType.REQUEST_RESULT,
            ).save()

            Notifications(
                notification_for=transaction_request.renting_request.vehicle.owner.application_user,
                message="Payment completed!",
                desc=f"The user {transaction_request.renting_request.buyer.get_full_name()} has completed payment for {transaction_request.renting_request.vehicle.vehicle_name}. Please proceed with the further steps as soon as possible.",
                related_transaction_request=transaction_request,
                notification_type=NotificationType.REQUEST_RESULT,
            ).save()

            # Suppose the payment happened here
            transaction.status = TransactionStatus.COMPLETED
            transaction.save()

            VehicleRent(
                rent_request=transaction_request.renting_request,
                expires_at=timezone.now() + transaction_request.renting_request.renting_period,
            ).save()

            messages.success(request, "Payment Successful")

        return redirect(reverse("home"))
