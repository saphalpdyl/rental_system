from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest
from django.contrib import messages

from base_app.models import Vehicles, VehicleRentingRequests, RentingStatus, VehicleRent, VehicleRentStatus, Review
from base_app.mixins import AuthRequiredMixin


class BuyerRentingHistoryView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest ):

        vehicle_rents = VehicleRent.objects.filter(status=VehicleRentStatus.COMPLETED)

        # Create a (is_already_reviewed, vehicle_rent) tuple list
        vehicle_rents_with_is_already_reviewed = []
        for rent in vehicle_rents:
            is_already_reviewed = Review.objects.filter(vehicle=rent.rent_request.vehicle, reviewer=request.user).exists()
            vehicle_rents_with_is_already_reviewed.append((is_already_reviewed, rent))
        
        return render(request, "base_app/buyer/vehicle_renting_history.html", {
            "vehicle_rents": vehicle_rents_with_is_already_reviewed,
        })