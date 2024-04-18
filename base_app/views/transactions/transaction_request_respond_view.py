from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.http import HttpRequest
from django.contrib import messages

from base_app.models import (
    ApplicationUser,
    TransactionRequest,
    TransactionStatus,
    Notifications,
    NotificationType
)
from base_app.mixins import AuthRequiredMixin


class TransactionRequestRespondView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest, tr_request_id: str):
        transaction_request = get_object_or_404(TransactionRequest, reference_id=tr_request_id)
        if not (transaction_request.status == TransactionStatus.PENDING):
            messages.error(request, "This transaction request has already been processed")
            return redirect(reverse("notification_list_view"))
        
        total_price = transaction_request.days * transaction_request.price_per_day

        renter: ApplicationUser = transaction_request.renting_request.vehicle.owner.application_user
        return render(request, "base_app/transactions/transaction_request_respond.html", {
            "transaction_request": transaction_request,
            "seller": renter,
            "total_price": total_price,
        })

    # Reject Request
    def post(self, request: HttpRequest, tr_request_id: str):
        transaction_request = get_object_or_404(TransactionRequest, reference_id=tr_request_id)
        if not (transaction_request.status == TransactionStatus.PENDING):
            messages.error(request, "This transaction request has already been processed")
            return redirect(reverse("notification_list_view"))

        transaction_request.status = TransactionStatus.REJECTED
        transaction_request.save()

        vehicle = transaction_request.renting_request.vehicle
        vehicle.is_booked = False
        vehicle.is_available = True
        vehicle.save()

        Notifications(
            # notification_for=transaction_request.seller_product.data_generated_by.application_user,
            notification_for=transaction_request.renting_request.vehicle.owner.application_user,
            message="Transaction request reject",
            desc="Your transaction request for {} with {} at {} has been rejected".format(
                transaction_request.days * transaction_request.price_per_day,
                request.user.username,
                transaction_request.price_per_day
            ),
            notification_type=NotificationType.TRANSACTION,
        ).save()

        return redirect(reverse("notification_list_view"))
