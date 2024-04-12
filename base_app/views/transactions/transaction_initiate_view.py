import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views import View
from django.http import HttpRequest
from django import forms
from django.contrib import messages

from base_app.models import (
    TransactionRequest,
)
from base_app.mixins import AuthRequiredMixin


class KhaltiPaymentForm(forms.Form):
    mobile = forms.IntegerField(widget=forms.TextInput())
    transaction_pin = forms.CharField(max_length=4, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class TransactionInitiateView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        payment_form = KhaltiPaymentForm()

        return render(request, "base_app/transactions/transaction_initiate.html", {
            "payment_form": payment_form,
        })

    def post(self, request: HttpRequest):
        transaction_request_id = request.GET.get("tr_request_id")
        transaction_request: TransactionRequest = get_object_or_404(TransactionRequest, reference_id=transaction_request_id)

        payment_form = KhaltiPaymentForm(request.POST)
        if not payment_form.is_valid():
            messages.error(request, "The form fields were invalid!")
            return redirect(reverse("home"))

        if len(payment_form.data["transaction_pin"]) != 4 or len(str(payment_form.data["mobile"])) != 10:
            messages.error(request, "The input fields were invalid!")
            return redirect(reverse("home"))

        url = "https://khalti.com/api/v2/payment/initiate/"
        payload = {
            "public_key": os.environ.get("KHALTI_PUBLIC_API_KEY"),
            "mobile": payment_form.data["mobile"],
            "transaction_pin": payment_form.data["transaction_pin"],
            "product_identity": f"{transaction_request.renting_request.vehicle.vehicle_name}-{transaction_request.renting_request.vehicle.reference_id}.{request.user.user_id}",
            "product_name": transaction_request.renting_request.vehicle.vehicle_name,
            "amount": 1000,
        }

        response = requests.post(url, json=payload)
        response_json = json.loads(response.text)

        if response.status_code != 200:
            messages.error(request, f"Error: {response_json.get('error_key')} - {response_json.get('detail')}")
            return redirect(f"{reverse('payment_initiate')}?tr_request_id={transaction_request_id}")

        token = response_json["token"]

        return redirect(f"{reverse('payment_initiate_confirm_code')}?token={token}&tr_request_id={transaction_request_id}")
