from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from base_app.models import Vehicles
from base_app.mixins import AuthRequiredMixin


class BuyerVehicleListView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        vehicles = Vehicles.objects.filter(is_available=True, is_booked=False, can_be_listed=True)

        return render(request, "base_app/buyer/rent_a_vehicle.html", {
            "vehicles": vehicles,
        })
