from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View

from base_app.mixins import AuthRequiredMixin, RenterRequiredMixin
from base_app.models import (
    Vehicles,
    RenterUser,
    VehicleListingRequests
)


class VehicleAddForListingView(AuthRequiredMixin, RenterRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "base_app/renter/vehicle_add_for_listing.html")

    def post(self, request: HttpRequest):
        name = request.POST["vehicle_name"]
        desc = request.POST["vehicle_desc"]
        price = request.POST["vehicle_price"]
        company = request.POST["vehicle_company"]
        vtype = request.POST["vehicle_type"]
        seater = request.POST["vehicle_seater"]
        number_plate = request.POST["vehicle_number_plate"]

        docs = request.FILES.get("vehicle_documents")
        desc_img = request.FILES.get("vehicle_description_image")

        current_renter_user = RenterUser.objects.get(application_user=request.user)

        this_vehicle = Vehicles(
            owner=current_renter_user,
            vehicle_name=name,
            vehicle_desc=desc,
            price=price,
            vehicle_company=company,
            vehicle_type=vtype,
            vehicle_seater=seater,
            vehicle_number_plate=number_plate,
            vehicle_documents=docs,
            vehicle_description_image=desc_img,
        )
        this_vehicle.save()

        VehicleListingRequests(
            vehicle=this_vehicle,
        ).save()

        return redirect(reverse("vehicle_add"))
