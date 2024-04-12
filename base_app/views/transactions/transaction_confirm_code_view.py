import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.http import HttpRequest
from django.contrib import messages
from django.utils import timezone
from django.db import transaction as transaction_module
from django import forms

from base_app.models import (
    TransactionRequest,
    Transactions,
    TransactionStatus,
    Notifications,
    NotificationType,
    VehicleRent,
    VehicleRentStatus
)
from base_app.mixins import AuthRequiredMixin


class TransactionConfirmCodeForm(forms.Form):
    otp_code = forms.CharField(max_length=6)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class TransactionConfirmCodeView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        confirmation_form = TransactionConfirmCodeForm()
        return render(request, "base_app/transactions/transaction_confirm_code.html", {
            "confirmation_form": confirmation_form,
        })

    def post(self, request: HttpRequest):
        try:
            token = request.GET["token"]
            tr_request_id = request.GET["tr_request_id"]

            confirmation_form = TransactionConfirmCodeForm(request.POST)

            if not confirmation_form.is_valid():
                messages.error(request, "Form fields were invalid!")
                return redirect(reverse("notification_list_view"))

            if len(confirmation_form.data["otp_code"]) != 6 or len(confirmation_form.data["pin"]) != 4:
                messages.error(request, "The fields couldn't be validated")
                return redirect(reverse("notification_list_view"))

            url = "https://khalti.com/api/v2/payment/confirm/"
            payload = {
                "public_key": os.environ.get("KHALTI_PUBLIC_API_KEY"),
                "token": token,
                "confirmation_code": confirmation_form.data["otp_code"],
                "transaction_pin": confirmation_form.data["pin"]
            }

            response = requests.post(url, json=payload)
            response_json = json.loads(response.text)

            if response.status_code != 200:
                messages.error(request, f"Error Key: {response_json.get('error_key')} - {response_json.get('detail')}")
                return redirect(reverse("notification_list_view"))
            

            # If the transaction is a success
            with transaction_module.atomic():
                transaction_request: TransactionRequest = get_object_or_404(TransactionRequest, reference_id=tr_request_id)
                transaction_request.status = TransactionStatus.COMPLETED
                transaction_request.save()
                
                transaction = Transactions(
                    status=TransactionStatus.COMPLETED,
                    transaction_request=transaction_request,
                    expires_in=10000,
                    pidx=token,
                )
                transaction.save()

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

                VehicleRent(
                    rent_request=transaction_request.renting_request,
                    expires_at=timezone.localtime(timezone.now()) + transaction_request.renting_request.renting_period,
                    status=VehicleRentStatus.ACTIVE,
                ).save()
                
            return redirect(reverse("notification_list_view"))
            
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Invalid token.")
            return redirect(reverse("notification_list_view"))
